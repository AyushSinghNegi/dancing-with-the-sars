"""R2/R7: resumable, local-only downloads of the six required NISAR files.

python -m pipeline.download_raw
Progress and completion records stay in ignored data/raw/. Credentials and
signed redirect URLs are never written to the log. Processing uses small crops.
"""
from __future__ import annotations
import json
import re
import time
import earthaccess
from . import config as C


def selected():
    primary = C.find(C.PRIMARY["before"])
    extra = [g for g in C.load_candidates() if g.product == "GCOV"
             and g.date in C.TIMELINE_DATES and C.same_mode(g, primary)
             and (g.direction, g.frame) == (primary.direction, primary.frame)]
    ids = list(C.PRIMARY.values()) + [g.granule_id for g in extra]
    return [C.find(gid) for gid in dict.fromkeys(ids)]


def transfer(session, granule, root):
    destination = root / f"{granule.granule_id}.h5"
    partial = destination.with_suffix(".h5.part")
    receipt = destination.with_suffix(".receipt.json")
    if destination.exists() and receipt.exists():
        saved = json.loads(receipt.read_text())
        if destination.stat().st_size == saved["bytes"]:
            return saved
    offset = partial.stat().st_size if partial.exists() else 0
    headers = {"Range": f"bytes={offset}-"} if offset else {}
    with session.get(granule.url, headers=headers, stream=True, timeout=(30, 120)) as response:
        if response.status_code not in (200, 206):
            raise RuntimeError(f"Download returned HTTP {response.status_code}")
        if response.status_code == 206:
            match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
            if not match or int(match[1]) != offset:
                raise RuntimeError("Unexpected resume byte range")
            total = int(match[3])
        else:
            offset = 0  # server ignored Range: safely restart this partial
            total = int(response.headers.get("Content-Length", 0))
        if total <= 0:
            raise RuntimeError("Server did not declare a complete file size")
        last = time.monotonic()
        with partial.open("ab" if offset else "wb") as output:
            for chunk in response.iter_content(chunk_size=8 * 1024 * 1024):
                output.write(chunk)
                offset += len(chunk)
                if time.monotonic() - last >= 30:
                    print(f"{granule.product} {granule.date}: {offset / total:.1%} ({offset / 1e9:.2f} GB)", flush=True)
                    last = time.monotonic()
        if offset != total:
            raise RuntimeError("Downloaded byte count differs from server total")
    # Signature only; never load a multi-GB original into memory.
    with partial.open("rb") as source:
        if source.read(8) != b"\x89HDF\r\n\x1a\n":
            raise RuntimeError("Downloaded content is not an HDF5 file")
    partial.replace(destination)
    saved = {"granule_id": granule.granule_id, "bytes": total,
             "verification": "HTTP total byte count and HDF5 signature; no independent checksum"}
    receipt.write_text(json.dumps(saved, indent=2) + "\n")
    return saved


def main():
    if C.IS_DEMO:
        raise SystemExit("Raw downloads require real mode")
    auth = earthaccess.login(strategy="netrc", persist=False)
    if not auth.authenticated:
        raise SystemExit("Earthdata authentication failed")
    C.RAW.mkdir(parents=True, exist_ok=True)
    session = earthaccess.get_requests_https_session()
    for granule in selected():
        print(f"Starting {granule.product} {granule.date}", flush=True)
        for attempt in range(3):
            try:
                result = transfer(session, granule, C.RAW)
                print(f"Complete {granule.product} {granule.date}: {result['bytes']} bytes", flush=True)
                break
            except Exception as exc:
                # HTTP exceptions can contain signed URLs: log only the class.
                print(f"Attempt {attempt + 1} failed ({type(exc).__name__}); partial retained", flush=True)
                if attempt == 2:
                    raise SystemExit("Download incomplete; rerun to resume") from None
                time.sleep(5)


if __name__ == "__main__":
    main()
