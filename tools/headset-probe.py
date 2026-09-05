#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# headset-probe.py  --  read-only USB HID inspector for Volume+ headset support
# MIT licensed (see tools/LICENSE). Copyright (c) 2026 Mega-City Merchandise LLC.
#
# ---------------------------------------------------------------------------
# WHAT THIS IS
# ---------------------------------------------------------------------------
# Volume+ reads a wireless headset's battery % over raw USB HID. To add or fix
# support for a headset we need to see the exact bytes it exchanges. This little
# script collects that, and nothing else.
#
# It is deliberately short and dependency-light so you can read the whole thing,
# or paste it into any AI assistant and ask "is this safe to run?", before you
# trust it.
#
# ---------------------------------------------------------------------------
# WHAT IT DOES  /  DOES NOT DO
# ---------------------------------------------------------------------------
#   * Default mode: LISTS your HID devices (vendor/product IDs, USB strings,
#     usage page). This only reads the OS device registry. Nothing is opened.
#
#   * --probe VID:PID : opens that ONE device and sends the *documented battery
#     request* for its vendor, then prints the raw reply bytes. These requests
#     are the same public, reverse-engineered requests used by HeadsetControl
#     (https://github.com/Sapd/HeadsetControl). They ask "what's your battery?".
#     They do not change any setting on the headset.
#
#   * It NEVER writes to disk (unless you pass --out FILE, which just saves the
#     console text), makes NO network connection, installs nothing, and starts
#     no background service. It exits when done.
#
#   * It REFUSES to open a Corsair device (vendor 0x1B1C). The Corsair Galleon
#     keyboard's own HID interface must not be touched -- writing to it blanks
#     the built-in Stream Deck display. Your headset dongle is a separate USB
#     device with a different vendor id and is safe.
#
# ---------------------------------------------------------------------------
# SETUP  (one line, uninstall afterwards if you like)
# ---------------------------------------------------------------------------
#   pip install hidapi
#   python headset-probe.py                 # list devices
#   python headset-probe.py --probe 1038:12AD
#   python headset-probe.py --probe 1038:12AD --out probe.txt
#
# Then open a "Headset battery badge issue" on the Volume+ repo and paste the
# output. Include your headset's real charge % if you can read it from the
# vendor app or a voice prompt.
# ---------------------------------------------------------------------------

import argparse
import sys
import time

# Corsair -- see the note above. Opening these can blank the Galleon's display.
BLOCKED_VENDORS = {0x1B1C}

# Vendor id -> friendly name, for the listing.
VENDOR_NAMES = {
    0x1038: "SteelSeries",
    0x0951: "HyperX / Kingston",
    0x03F0: "HP (HyperX)",
    0x1B1C: "Corsair",
    0x046D: "Logitech",
}

# Documented battery requests, keyed by vendor id. Each entry:
#   label     - what it is
#   report    - the request bytes (first byte is the HID report id)
#   write_len - pad the request with 0x00 up to this many bytes before writing
#   read_len  - how many bytes to try to read back
#   note      - where in the reply the battery value usually sits (for the reader)
#
# Source: HeadsetControl device tables (GPLv3 project; these byte values are
# facts about the hardware, not code). Cross-checked in docs/headset-protocols.md.
KNOWN_REQUESTS = {
    0x1038: [
        {
            "label": "SteelSeries Arctis 7 / Pro (legacy)  06 18",
            "report": [0x06, 0x18],
            "write_len": 31,
            "read_len": 32,
            "note": "battery % = reply[2], direct 0-100; reply[3] unused on this model",
        },
        {
            "label": "SteelSeries Arctis Nova 7  06 18",
            "report": [0x06, 0x18],
            "write_len": 64,
            "read_len": 64,
            "note": "battery bars = reply[2] (0-4); reply[3]==1 => charging",
        },
    ],
    0x0951: [
        {
            "label": "HyperX Cloud Flight Wireless  21 ff 05",
            "report": [0x21, 0xFF, 0x05],
            "write_len": 20,
            "read_len": 20,
            "note": "battery voltage mV, big-endian reply[3..4]; >~4107mV => charging",
        },
        {
            "label": "HyperX Cloud II Wireless (Kingston)  battery cmd 02",
            "report": [
                0x06, 0x00, 0x02, 0x00, 0x9A, 0x00, 0x00, 0x68, 0x4A, 0x8E,
                0x0A, 0x00, 0x00, 0x00, 0xBB, 0x02, 0x00,
            ],
            "write_len": 62,
            "read_len": 64,
            "note": "valid if reply[0]==0x0B and reply[2]==0xBB; level at reply[7]",
        },
    ],
    0x03F0: [
        {
            "label": "HyperX Cloud II Wireless (HP)  06 ff bb 02 00",
            "report": [0x06, 0xFF, 0xBB, 0x02, 0x00],
            "write_len": 52,
            "read_len": 20,
            "note": "valid if reply[0..2]==06 ff bb; level at reply[7]",
        },
        {
            "label": "HyperX Cloud Alpha Wireless  21 bb 0b",
            "report": [0x21, 0xBB, 0x0B],
            "write_len": 31,
            "read_len": 31,
            "note": "level at reply[3], direct 0-100 (only meaningful if not charging)",
        },
    ],
}


def _import_hid():
    try:
        import hid  # from the 'hidapi' package
        return hid
    except ImportError:
        print("The 'hidapi' package is not installed. Run:\n\n    pip install hidapi\n")
        sys.exit(1)


def hx(n, width=2):
    return f"0x{n:0{width}X}" if isinstance(n, int) else "?"


def bytes_hex(data):
    return " ".join(f"{b:02x}" for b in bytes(data))


def parse_vidpid(text):
    """Accept '1038:12ad', '0x1038:0x12AD', '1038/12ad'."""
    sep = ":" if ":" in text else "/" if "/" in text else None
    if not sep:
        raise argparse.ArgumentTypeError("use the form VID:PID, e.g. 1038:12AD")
    a, b = text.split(sep, 1)
    return int(a, 16), int(b, 16)


def list_devices(hid):
    devs = hid.enumerate()
    print(f"{len(devs)} HID device(s):\n")
    # Group by vendor:product so multi-collection devices read clearly.
    seen = {}
    for d in devs:
        key = (d["vendor_id"], d["product_id"])
        seen.setdefault(key, []).append(d)

    for (vid, pid), entries in sorted(seen.items()):
        vname = VENDOR_NAMES.get(vid, "")
        blocked = " [BLOCKED: Corsair -- probe refuses this]" if vid in BLOCKED_VENDORS else ""
        known = "  <-- Volume+ has a documented request for this vendor" if vid in KNOWN_REQUESTS else ""
        e0 = entries[0]
        print(f"{hx(vid, 4)}:{hx(pid, 4)}  {vname}{blocked}{known}")
        print(f"    product      : {e0.get('product_string') or '?'}")
        print(f"    manufacturer : {e0.get('manufacturer_string') or '?'}")
        for d in entries:
            print(
                f"    collection   : usage_page={hx(d['usage_page'])} "
                f"usage={hx(d['usage'])} interface={d.get('interface_number')}"
            )
        print(f"    --probe {vid:04x}:{pid:04x}")
        print()

    print("Next: run  python headset-probe.py --probe VID:PID  for your headset,")
    print("with the headset powered on and connected via its USB dongle.")


def probe(hid, vid, pid, out_lines):
    def emit(line=""):
        print(line)
        out_lines.append(line)

    if vid in BLOCKED_VENDORS:
        emit(f"Refusing to open vendor {hx(vid, 4)} (Corsair). See the note at the top of this file.")
        sys.exit(2)

    matches = [d for d in hid.enumerate() if d["vendor_id"] == vid and d["product_id"] == pid]
    if not matches:
        emit(f"No HID device found for {hx(vid, 4)}:{hx(pid, 4)}. Is the headset on and on its dongle?")
        emit("Run with no arguments to list what's connected.")
        sys.exit(1)

    requests = KNOWN_REQUESTS.get(vid)
    emit(f"Probing {hx(vid, 4)}:{hx(pid, 4)}  ({VENDOR_NAMES.get(vid, 'unknown vendor')})")
    emit(f"{len(matches)} HID collection(s) to try.")
    if not requests:
        emit("")
        emit("No documented battery request for this vendor yet. The device listing")
        emit("above (vendor/product id, usage page, USB strings) is still useful --")
        emit("paste it into an issue. If HeadsetControl supports this model, link it.")
        return

    for idx, d in enumerate(matches):
        emit("")
        emit(f"--- collection {idx}: usage_page={hx(d['usage_page'])} "
             f"usage={hx(d['usage'])} interface={d.get('interface_number')} ---")
        try:
            h = hid.device()
            h.open_path(d["path"])
        except Exception as e:  # noqa: BLE001
            emit(f"    open failed: {e}")
            continue
        try:
            h.set_nonblocking(0)
            for req in requests:
                payload = list(req["report"]) + [0x00] * (req["write_len"] - len(req["report"]))
                emit(f"  request : {req['label']}")
                emit(f"            {bytes_hex(payload)}")
                try:
                    written = h.write(payload)
                except Exception as e:  # noqa: BLE001
                    emit(f"    write failed: {e}")
                    continue
                if written is None or written < 0:
                    emit("    this collection rejected the write (normal, only one collection accepts it)")
                    continue
                emit(f"    wrote {written} bytes; reading replies (2s)...")
                deadline = time.time() + 2.0
                got_any = False
                while time.time() < deadline:
                    data = h.read(req["read_len"], timeout_ms=300)
                    if not data:
                        continue
                    got_any = True
                    b = list(data)
                    if b[0] == req["report"][0]:
                        emit(f"    reply : {bytes_hex(b)}  <- report id matches request")
                        window = "  ".join(f"reply[{i}]={b[i]} (0x{b[i]:02x})" for i in range(2, min(6, len(b))))
                        emit(f"            {window}")
                    else:
                        emit(f"    reply : {bytes_hex(b)}")
                if not got_any:
                    emit("    (no reply on this collection)")
                else:
                    emit(f"    hint  : {req['note']}")
        finally:
            try:
                h.close()
            except Exception:  # noqa: BLE001
                pass

    emit("")
    emit("Done. Paste everything above into a Volume+ headset issue, plus your")
    emit("headset's real charge % right now if you can read it another way.")


def main():
    ap = argparse.ArgumentParser(
        description="Read-only USB HID inspector for Volume+ headset support.",
        epilog="With no arguments it lists HID devices. Nothing is opened until you pass --probe.",
    )
    ap.add_argument("--probe", type=parse_vidpid, metavar="VID:PID",
                    help="open this device and send its documented battery request (hex ids, e.g. 1038:12AD)")
    ap.add_argument("--out", metavar="FILE", help="also write the console output to FILE (text only)")
    args = ap.parse_args()

    hid = _import_hid()
    out_lines: list[str] = []

    if args.probe:
        probe(hid, args.probe[0], args.probe[1], out_lines)
    else:
        list_devices(hid)

    if args.out and out_lines:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines) + "\n")
        print(f"\nSaved to {args.out}")


if __name__ == "__main__":
    main()
