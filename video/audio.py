"""Music and sound effects for the MonsoonLens demo videos, synthesised from scratch (no samples, no licences needed):
a soft, slow space pad with a few bell notes, and sound effects timed to what happens on screen.

  python video/audio.py short    # -> video/out/audio/short_{music,sfx,mix}.wav and monsoonlens_demo_30s.mp4 with sound
  python video/audio.py long     # -> the same for the walkthrough

The 30-second cut is mixed quieter so a voice-over sits on top; the music and effects are also written as separate
stems so they can be balanced against the voice in any editor.
"""
from __future__ import annotations

import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_demo as V  # noqa: E402  (scene timeline and timings)

SR = 48000
OUT = ROOT / "video" / "out"
AUD = OUT / "audio"
RNG = np.random.default_rng(7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x, axis=-1)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x, axis=-1)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x, axis=-1)


def env(n, a, r, sustain=True):
    """Attack/release envelope over n samples (seconds a and r)."""
    e = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na) ** 2
    if nr < n:
        e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e


def pan(mono, p):
    """p in -1 (left) .. 1 (right), constant power; p may be an array."""
    a = (np.asarray(p) + 1) * np.pi / 4
    return np.stack([mono * np.cos(a), mono * np.sin(a)])


def place(buf, sig, t):
    i = int(round(t * SR))
    if i >= buf.shape[1] or i + sig.shape[1] <= 0:
        return
    j0 = max(0, -i)
    i = max(i, 0)
    n = min(sig.shape[1] - j0, buf.shape[1] - i)
    buf[:, i:i + n] += sig[:, j0:j0 + n]


_IR = {}


def reverb(x, seconds=3.2, wet=0.35, tone=5000):
    """Convolution with a synthetic stereo hall (decaying, darkening noise)."""
    key = (seconds, tone)
    if key not in _IR:
        n = int(seconds * SR)
        t = np.arange(n) / SR
        ir = RNG.standard_normal((2, n)) * np.exp(-t * 6.9 / seconds)
        ir = lp(ir, tone)
        ir[:, :int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
        _IR[key] = ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    ir = _IR[key]
    w = np.stack([fftconvolve(x[c], ir[c])[:x.shape[1]] for c in range(2)])
    return x * (1 - wet) + w * wet * 1.4


# ------------------------------------------------------------------ music
CHORDS = {   # soft, open voicings (MIDI): D minor 9, B-flat major 9, F major 9, C add 9
    "Dm9": [38, 45, 53, 60, 64, 69],
    "Bbmaj9": [34, 41, 50, 57, 60, 65],
    "Fmaj9": [41, 48, 57, 64, 67, 72],
    "Cadd9": [36, 43, 52, 62, 67, 71],
}
CYCLE = ["Dm9", "Bbmaj9", "Fmaj9", "Cadd9"]


def bl_saw(ph, f, top=3000):
    """Band-limited sawtooth from its harmonics (no aliasing), for a phase array in cycles."""
    out = np.zeros_like(ph)
    for k in range(1, max(2, int(top // f)) + 1):
        out += np.sin(2 * np.pi * k * ph) / k
    return out * (2 / np.pi)


def pad_chord(notes, dur, bright):
    n = int(dur * SR)
    out = np.zeros((2, n))
    t = np.arange(n) / SR
    for k, m in enumerate(notes):
        f = hz(m)
        lfo = 1 + 0.0015 * np.sin(2 * np.pi * (0.13 + 0.03 * k) * t)
        for c, det in enumerate((-6, 6)):   # cents, left and right
            ff = f * 2 ** (det / 1200)
            ph = np.cumsum(ff * lfo) / SR
            v = bl_saw(ph, ff, bright * 1.8) + 0.6 * bl_saw(ph * 1.0019 + 0.3, ff, bright * 1.8)
            out[c] += v * (0.11 if m < 48 else 0.075)
    out = lp(out, bright, order=2)
    out += np.sin(2 * np.pi * hz(notes[0] - 12) * t) * 0.09   # sub, an octave under the lowest note
    return out * env(n, 1.4, 2.2)


def bells(start, dur, notes, density, buf, level=0.05):
    """A few soft bell notes from the chord, high, sparse."""
    t = start + RNG.uniform(0.3, 0.9)
    while t < start + dur - 0.5:
        m = RNG.choice(notes[2:]) + 12
        place(buf, pan(bell(hz(m), 2.6, ((1, 1.0), (2.01, 0.3), (2.76, 0.1))) * level * RNG.uniform(0.6, 1.0),
                       RNG.uniform(-0.7, 0.7)), t)
        t += RNG.uniform(0.8, 1.6) / density


def bell(f, dur, partials=((1, 1.0), (2.01, 0.35), (2.76, 0.18), (5.4, 0.06))):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * (2.2 + 1.6 * r)) for r, a in partials)
    s[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return s


def music(sections, total):
    """sections: [(start, dur, chord, brightness Hz, bell density)]."""
    buf = np.zeros((2, int(total * SR) + SR))
    bel = np.zeros_like(buf)
    for st, dur, ch, bright, dens in sections:
        seg = pad_chord(CHORDS[ch], dur + 2.4, bright)   # overlaps the next chord while it fades
        place(buf, seg, max(0, st - 0.6))
        if dens > 0:
            bells(st, dur, CHORDS[ch], dens, bel)
    buf = reverb(buf, 3.6, 0.45, 4500) + reverb(bel, 4.5, 0.6, 7000)
    buf = buf[:, :int(total * SR)]
    fade_in, fade_out = int(1.2 * SR), int(2.4 * SR)
    buf[:, :fade_in] *= np.linspace(0, 1, fade_in)
    buf[:, -fade_out:] *= np.linspace(1, 0, fade_out) ** 1.3
    return buf


# ------------------------------------------------------------------ sound effects
def noise(n):
    return RNG.standard_normal(n)


def whoosh(dur=0.7, lo=250, hi=3200, direction=1, level=0.22, rise=0.6):
    """Band-limited noise sweeping in pitch and across the stereo field."""
    n = int(dur * SR)
    x = noise(n)
    bands = np.geomspace(lo, hi, 6)
    out = np.zeros(n)
    pos = np.linspace(0, 1, n)
    for i in range(len(bands) - 1):
        b = bp(x, bands[i], bands[i + 1])
        centre = (i + 0.5) / (len(bands) - 1)
        w = np.exp(-((pos - centre) / 0.22) ** 2)
        out += b * w
    shape = np.where(pos < rise, (pos / rise) ** 2, ((1 - pos) / (1 - rise)) ** 1.5)
    out *= shape / (np.abs(out).max() + 1e-9)
    return pan(out * level, np.linspace(-0.6 * direction, 0.6 * direction, n))


def riser(dur=0.9, level=0.12):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 200 * (12 ** (t / dur))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    x = bp(noise(n), 1200, 6000) * 0.35
    s = (tone + x) * (t / dur) ** 2.2
    return pan(s / (np.abs(s).max() + 1e-9) * level, 0)


def boom(level=0.22):
    n = int(1.8 * SR)
    t = np.arange(n) / SR
    f = 70 * np.exp(-t * 1.2) + 38
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    s += lp(noise(n), 900) * np.exp(-t * 9) * 0.25
    s[:int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))
    return pan(s / np.abs(s).max() * level, 0)


def tick(f=1800, level=0.08, p=0.0, dur=0.09):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t * (1 + 0.6 * t / dur)) * np.exp(-t * 55)
    s += bp(noise(n), 2500, 8000) * np.exp(-t * 160) * 0.2
    return pan(s / np.abs(s).max() * level, p)


def click(level=0.16, p=0.25):
    out = np.zeros((2, int(0.12 * SR)))
    for k, (t0, f, a) in enumerate(((0.0, 2600, 1.0), (0.075, 3400, 0.6))):
        n = int(0.02 * SR)
        tt = np.arange(n) / SR
        s = (bp(noise(n), 1500, 7000) * 0.6 + np.sin(2 * np.pi * f * tt)) * np.exp(-tt * 380) * a
        place(out, pan(s * level, p), t0)
    return out


def ding(f=880, level=0.09, p=0.0, dur=1.4):
    return pan(bell(f, dur) * level, p)


def sparkle(level=0.035):
    m = RNG.choice([76, 79, 81, 84, 86, 88])
    return pan(bell(hz(m), 0.6, ((1, 1.0), (3.0, 0.2))) * level, RNG.uniform(-0.8, 0.8))


def chime(level=0.12):
    out = np.zeros((2, int(4.0 * SR)))
    for k, m in enumerate([65, 72, 77, 81, 84]):   # F major, rising
        place(out, pan(bell(hz(m), 3.6) * level * (0.9 - k * 0.08), -0.5 + k * 0.25), k * 0.09)
    return out


# ------------------------------------------------------------------ cues from the video timeline
def cues(scenes):
    """(time, sound) pairs that follow the animation timings in make_demo.py."""
    tl, total = V.timeline(scenes)
    c = []
    for i, (name, fn, t0, dur) in enumerate(tl):
        if i > 0 and name != "radar":
            c.append((t0 - V.XF - 0.15, whoosh(0.75, direction=1 if i % 2 else -1, level=0.12)))
        if name == "cloud":
            c.append((t0 + 0.05, whoosh(0.5, 600, 4000, level=0.06)))
            order = sorted([(r, cc) for r in range(4) for cc in range(6)], key=lambda rc: rc[0] + rc[1] * 0.9)
            for k, (r, cc) in enumerate(order):
                c.append((t0 + 0.25 + k * 0.07, tick(1500 + 90 * ((k * 5) % 9), 0.05, -0.6 + cc * 0.24)))
            c.append((t0 + dur - 0.9, riser(0.9)))
        elif name == "radar":
            c.append((t0 - 0.02, boom()))
            c.append((t0 + 0.9, whoosh(1.3, 300, 2600, direction=1, level=0.16, rise=0.5)))
            c.append((t0 + 2.1, ding(hz(81), 0.06, -0.3, 2.4)))
            c.append((t0 + 2.3, ding(hz(76), 0.07, -0.2)))
            c.append((t0 + 2.75, ding(hz(79), 0.07, -0.2)))
            for k in range(50):
                if k % 2 == 0:
                    c.append((t0 + 2.6 + k * 0.022, sparkle(0.028)))
        elif name == "app":
            c.append((t0 + 0.05, whoosh(0.7, 200, 2200, direction=-1, level=0.14, rise=0.4)))
            c.append((t0 + 1.4, tick(2200, 0.04, 0.2)))
            c.append((t0 + 2.0, click()))
            c.append((t0 + 2.15, whoosh(0.5, 900, 5000, level=0.05)))
        elif name == "map":
            c.append((t0 + dur * 0.52, whoosh(0.8, 250, 3000, direction=1, level=0.13)))
        elif name == "checks":
            for k in range(4):
                c.append((t0 + 0.6 + k * 0.28, tick(900 + 180 * k, 0.07, -0.6 + 0.4 * k, 0.14)))
        elif name == "field":
            c.append((t0 + 0.05, whoosh(0.7, 200, 2200, direction=-1, level=0.13, rise=0.4)))
            c.append((t0 + 0.45, tick(2400, 0.035, -0.2)))
            c.append((t0 + 1.4, click(p=-0.1)))
            c.append((t0 + 1.55, whoosh(0.5, 900, 5000, level=0.05)))
            for k in range(2):
                c.append((t0 + 2.3 + k * 0.25, whoosh(0.55, 400, 3500, direction=-1, level=0.09, rise=0.35)))
            for k in range(4):
                c.append((t0 + 2.9 + k * 0.12, tick(1700 + 140 * k, 0.04, -0.6 + 0.3 * k)))
        elif name == "end":
            c.append((t0 + 0.0, chime()))
            c.append((t0 + 0.6, ding(hz(84), 0.05, 0.1, 1.8)))
        elif name in ("story", "place", "method"):
            c.append((t0 + 0.05, whoosh(0.7, 200, 2200, direction=-1, level=0.13, rise=0.4)))
            if name == "place":
                c.append((t0 + dur * 0.45, whoosh(0.55, 400, 3500, direction=-1, level=0.09, rise=0.35)))
            if name == "method":
                c.append((t0 + dur * 0.55, whoosh(0.6, 900, 5000, level=0.06)))
    return c, total


def sections_for(scenes):
    tl, total = V.timeline(scenes)
    secs = []
    k = 0
    for name, fn, t0, dur in tl:
        # long scenes get two chords; the cloud scene stays dark, the reveal brightens, the end resolves on F
        parts = 2 if dur > 6 else 1
        for j in range(parts):
            st = t0 + j * dur / parts
            if name == "cloud":
                ch, br, dens = "Dm9", 700, 0.2
            elif name == "end":
                ch, br, dens = "Fmaj9", 2200, 0.8
            else:   # B-flat lifts out of the dark D minor at the reveal; the end resolves B-flat -> F
                ch = ["Bbmaj9", "Fmaj9", "Cadd9", "Dm9"][k % 4]
                br, dens = (2400 if name == "radar" else 1800), 0.6
                k += 1
            secs.append((st, dur / parts, ch, br, dens))
    return secs, total


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x.T * 32767).astype("<i2").tobytes())


def render(which):
    scenes = V.SHORT if which == "short" else V.LONG
    video = OUT / ("monsoonlens_demo_30s.mp4" if which == "short" else "monsoonlens_walkthrough.mp4")
    secs, total = sections_for(scenes)
    mus = music(secs, total)
    sfx = np.zeros_like(mus)
    c, _ = cues(scenes)
    for t, s in c:
        place(sfx, s, t)
    sfx = reverb(sfx, 1.6, 0.18, 7000)
    AUD.mkdir(parents=True, exist_ok=True)
    # stems peak-normalised to -6 dBFS; the mix leaves room for a voice in the short cut
    mus *= 0.5 / np.abs(mus).max()
    sfx *= 0.5 / np.abs(sfx).max()
    m_gain, s_gain = (0.55, 0.85) if which == "short" else (0.8, 0.9)
    mix = mus * m_gain + sfx * s_gain
    write_wav(AUD / f"{which}_music.wav", mus)
    write_wav(AUD / f"{which}_sfx.wav", sfx)
    write_wav(AUD / f"{which}_mix_raw.wav", mix * 0.9 / np.abs(mix).max())
    target = -23 if which == "short" else -16   # LUFS: the short cut sits under a voice-over
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(AUD / f"{which}_mix_raw.wav"), "-af",
                    f"loudnorm=I={target}:TP=-1.5:LRA=11", "-ar", str(SR), str(AUD / f"{which}_mix.wav")], check=True)
    silent = OUT / f"{video.stem}_silent.mp4"
    tmp = video.with_suffix(".part.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(AUD / f"{which}_mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", str(tmp)], check=True)
    tmp.rename(video)
    print(video, round(total, 2), "s")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["short", "long"]:
        render(w)
