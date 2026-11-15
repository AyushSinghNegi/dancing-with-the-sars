"""Voice-over: clean the team's recordings, cut the false starts and long pauses, and time every word, so the videos can
be laid out around the voice and the captions can light up each word as it is spoken.

  python video/vo.py short <recording>   # -> video/out/vo/short_vo.wav and short_vo.json (sentences, words, timings)
  python video/vo.py long <recording>

Word timings come from faster-whisper (small.en, run locally) on the cleaned recording; the caption text is the script
as spoken (written out below), aligned word by word to the recognised words. Cuts and sentence windows were chosen by
reading the recognised words and a second, slower pass (medium.en) over every place that sounded like a restart.
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "video" / "out" / "vo"
SR = 48000

# (scene, caption text as spoken, source window in seconds)
SCRIPT = {
    "short": {
        "cuts": [],
        "sentences": [
            ("cloud", "July 2026. Floods and landslides hit Pune. Every satellite photo that week showed only cloud.", (1.1, 7.98)),
            ("radar", "But NASA and ISRO's new NISAR radar sees through cloud: new water, and 50 likely landslide zones.", (8.5, 15.3)),
            ("app", "MonsoonLens turns it into answers anyone can use,", (15.85, 19.0)),
            ("map", "in 3D and on the map,", (19.25, 20.9)),
            ("checks", "with every result checked, and the weak ones shown too.", (21.25, 24.3)),
            ("field", "District teams get a ranked field check list, in four languages.", (25.0, 28.52)),
            ("end", "MonsoonLens. See the ground where the sky is closed.", (29.05, 32.95)),
        ],
    },
    "long": {
        "cuts": [(76.5, 81.46), (105.6, 108.82)],   # "Fly over it..." restart; "District teams get a be..." restart
        "sentences": [
            ("cloud", "In July 2026, floods and landslides hit Pune district in India.", (0.05, 5.9)),
            ("cloud", "All 22 daily satellite photos from 3 to 8 July showed only cloud.", (6.6, 11.2)),
            ("radar", "NASA and ISRO's NISAR radar sees through cloud, day or night.", (11.85, 16.05)),
            ("radar", "Comparing passes from 28 June and 10 July shows 8.5 km² of new water as reservoirs and rivers rose,", (16.35, 25.4)),
            ("radar", "and 50 likely landslide zones on steep ground, 8 of them high confidence.", (27.6, 32.9)),
            ("app", "MonsoonLens puts these results in a plain-language web app.", (33.55, 37.6)),
            ("app", "A guided tour explains every page in about a minute.", (37.9, 41.45)),
            ("story", "The Story walks through the event in six steps:", (41.5, 45.25)),
            ("story", "the rain from NASA's GPM satellites, the cloud, and what the radar saw.", (45.3, 50.65)),
            ("map", "Fly over every finding in 3D on Copernicus elevation, then explore every layer on the map: water, "
                    "slide zones, flooding and reported events.", (51.2, 62.1)),
            ("place", "Anyone can check a place: pick one of 431 villages and towns,", (62.7, 67.45)),
            ("place", "see what was found within 2, 5 or 10 kilometres, and share the link.", (67.5, 72.1)),
            ("place", "Here, Lonavala in Marathi.", (72.35, 74.7)),
            ("checks", "Every result is checked. An independent NISAR orbit re-found zones 8 times better than chance, and 35 "
                       "of 50 zones held with NASA's NASADEM elevation map.", (81.46, 95.75)),
            ("checks", "Reported floods matched no better than chance. The misses were in or near towns, where buildings can "
                       "hide flooded streets.", (96.4, 105.0)),
            ("field", "District teams get a ranked field check list with radar evidence for each zone,", (108.82, 113.7)),
            ("field", "nearby roads, railways and villages, a printable list and KML for phones,", (113.95, 119.4)),
            ("field", "in English, Hindi, Marathi and German.", (120.2, 123.25)),
            ("method", "The Method page lists every step, check, limit and NISAR file.", (124.05, 128.55)),
            ("method", "Everything is in four languages.", (129.1, 130.85)),
            ("method", "The whole pipeline runs in about two minutes.", (130.95, 135.15)),
        ],
    },
}

NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "eight": "8", "ten": "10",
       "fifty": "50", "kilometres": "kilometers", "km²": "km2", "re-found": "refound", "monsoonlens": "monsoonlens",
       "check": "check", "nisar": "nisar"}


def norm(w):
    w = w.lower().strip(" .,:;!?\"'()")
    w = w.replace("’", "'")
    return NUM.get(w, w)


def load(path, sr=SR):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def clean(src, dst):
    """Rumble and hiss off, gentle de-essing and levelling; loudness is set after editing."""
    chain = ("highpass=f=75,lowpass=f=15000,afftdn=nr=10:nf=-45:tn=1,deesser=i=0.35:m=0.5:f=0.5,"
             "acompressor=threshold=0.1:ratio=2.5:attack=8:release=160:makeup=1.6")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(SR), "-af", chain,
                    str(dst)], check=True)


def regions(x):
    """Speech regions from frame energy, with a high threshold to find speech and a low one to keep soft edges."""
    hop = SR // 100
    fr = np.lib.stride_tricks.sliding_window_view(x, hop * 2)[::hop]
    db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    noise, peak = np.percentile(db, 10), np.percentile(db, 98)
    hi, lo = noise + 0.35 * (peak - noise), noise + 0.16 * (peak - noise)
    on = db > hi
    regs, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        if not v and s is not None:
            regs.append([s, i])
            s = None
    if s is not None:
        regs.append([s, len(on)])
    out = []
    for a, b in regs:   # widen to the low threshold
        while a > 0 and db[a - 1] > lo:
            a -= 1
        while b < len(db) and db[b] > lo:
            b += 1
        if out and a - out[-1][1] <= 8:   # gaps under 80 ms are part of the word
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a / 100, b / 100) for a, b in out if b - a >= 6], db


def asr(x16):
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(x16, word_timestamps=True, beam_size=5, condition_on_previous_text=False,
                           initial_prompt="MonsoonLens, NISAR, ISRO, NASADEM, Lonavala, Pune.")
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


def build(which, rec):
    cfg = SCRIPT[which]
    OUT.mkdir(parents=True, exist_ok=True)
    cl = OUT / f"{which}_clean.wav"
    clean(rec, cl)
    x = load(cl)
    regs, _ = regions(x)
    words = asr(load(cl, 16000))
    cuts = cfg["cuts"]
    pad, gmax, xf = 0.04, 0.2, int(0.008 * SR)
    sentences = []
    for scene, text, (w0, w1) in cfg["sentences"]:
        keep = []
        for a, b in regs:
            a, b = max(a - pad, w0), min(b + pad, w1)
            if b <= a:
                continue
            pieces = [(a, b)]
            for c0, c1 in cuts:
                nxt = []
                for p0, p1 in pieces:
                    if p1 <= c0 or p0 >= c1:
                        nxt.append((p0, p1))
                    else:
                        if p0 < c0:
                            nxt.append((p0, c0))
                        if p1 > c1:
                            nxt.append((c1, p1))
                pieces = nxt
            keep += [p for p in pieces if p[1] - p[0] >= 0.06]
        # clips: each region plus up to half of the (shortened) pause on either side
        clips = []
        for i, (a, b) in enumerate(keep):
            g_prev = a - keep[i - 1][1] if i else 0.0
            g_next = keep[i + 1][0] - b if i + 1 < len(keep) else 0.0
            ca = a - min(g_prev, gmax) / 2
            cb = b + min(g_next, gmax) / 2
            clips.append((ca, cb))
        audio, tmap, t_out = [], [], 0.0
        for a, b in clips:
            seg = x[int(a * SR):int(b * SR)].copy()
            start = t_out
            if audio and len(seg) > xf and len(audio[-1]) > xf:   # 8 ms crossfade at every join
                f = np.linspace(0, 1, xf)
                audio[-1][-xf:] = audio[-1][-xf:] * (1 - f) + seg[:xf] * f
                seg = seg[xf:]
                start = t_out - xf / SR
            tmap.append((a, b, start))
            t_out += len(seg) / SR
            audio.append(seg)
        y = np.concatenate(audio)

        def to_out(t):
            for a, b, o in tmap:
                if t < a:
                    return o
                if t <= b:
                    return o + (t - a)
            return len(y) / SR

        # caption words aligned to recognised words inside the window
        ws = [w for w in words if w[2] > w0 and w[1] < w1]
        disp = text.split()
        A = [norm(d) for d in disp]
        B = [norm(w[0]) for w in ws]
        tim = [None] * len(disp)
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
            if op == "equal":
                for k in range(i2 - i1):
                    tim[i1 + k] = (ws[j1 + k][1], ws[j1 + k][2])
            elif op == "replace":
                t0, t1 = ws[j1][1], ws[j2 - 1][2]
                n = i2 - i1
                for k in range(n):
                    tim[i1 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
        for i in range(len(disp)):   # words not heard: squeeze them in next to their neighbours
            if tim[i] is None:
                prev = next((tim[j][1] for j in range(i - 1, -1, -1) if tim[j]), w0)
                nxt = next((tim[j][0] for j in range(i + 1, len(disp)) if tim[j]), prev + 0.2)
                tim[i] = (prev, max(prev + 0.05, min(nxt, prev + 0.25)))
        out_words = []
        for d, (s, e) in zip(disp, tim):
            so, eo = to_out(max(s, w0)), to_out(min(e, w1))
            out_words.append([d, round(so, 3), round(max(eo, so + 0.06), 3)])
        for i in range(1, len(out_words)):   # monotonic
            out_words[i][1] = max(out_words[i][1], out_words[i - 1][1] + 0.02)
        name = f"{which}_s{len(sentences):02d}.wav"
        write(OUT / name, y)
        sentences.append({"scene": scene, "text": text, "file": name, "dur": round(len(y) / SR, 3), "words": out_words,
                          "src": [w0, w1]})
        print(f"{scene:7s} {len(y) / SR:5.2f}s (from {w1 - w0:5.2f}s)  {text[:70]}")
    json.dump({"which": which, "sentences": sentences}, open(OUT / f"{which}_vo.json", "w"), indent=1, ensure_ascii=False)
    total = sum(s["dur"] for s in sentences)
    print(f"speech {total:.2f}s in {len(sentences)} sentences")


def write(path, y):
    import wave
    y = np.clip(y, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
