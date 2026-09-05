# Headset battery: HID protocol notes

Volume+ reads a wireless headset's battery over raw USB HID. This page collects
the protocol **facts** for the headsets it targets: USB IDs, the request bytes,
and where the battery value sits in the reply.

These facts (device IDs, report bytes, byte offsets, scaling) are transcribed as
reference from the [HeadsetControl](https://github.com/Sapd/HeadsetControl)
project (GPLv3). **No code is copied.** HeadsetControl's implementation is
consulted only as documentation of the reverse-engineered protocols, which are
facts and not copyrightable. Volume+'s reader is written independently. Anything
we newly work out, we aim to contribute back to HeadsetControl.

If you own one of the **Beta** headsets below, the
[headset-probe.py](../tools/headset-probe.py) tool sends exactly these requests
and prints the raw replies, which is what we need to confirm or fix a profile.

Cross-check every value against a real device (known charge level, or a USB
capture) before trusting it.

---

## SteelSeries Arctis 7 / Arctis Pro (legacy) — Verified

| Field | Value |
| --- | --- |
| Vendor ID | `0x1038` |
| Product IDs | `0x1260` Arctis 7 · `0x12AD` Arctis 7 (2019) · `0x1252` Arctis Pro (2019) · `0x1280` Arctis Pro GameDAC |
| HID collection | Windows: the `0xFF43` usage-page collection (usage `0x202`) on interface 5. The other collections on that interface reject the write. |
| Battery request | output report `06 18`, zero-padded to 31 bytes. Byte 0 `0x06` is the report ID. |
| Reply | the first read after the write returns `06 18 <bat> ...`; later reads are empty. |
| Battery value | `reply[2]`, direct percentage 0–100, no scaling. |
| Charging | Not exposed by this model. `reply[3]` stays `0x00` on battery and on the charger, and SteelSeries GG itself shows no charging state for the Arctis 7. A live `reply[2] == 0` is treated as "headset off" (it powers down well above 0%). |
| Poll cadence | slow, 30–60 s. |

Newer SteelSeries models (Nova 7, 7+, Nova Pro Wireless) use a different request
and do expose a real charging byte. They get their own entries as they are added.

---

## HyperX family — Beta (no HyperX hardware has confirmed these yet)

All four are implemented from public documentation and ship **disabled**. A
HyperX owner running `headset-probe.py` and opening an issue is what flips one to
verified. HyperX Cloud 3 (wired) has no battery capability and is out of scope.

### Cloud Flight Wireless

| Field | Value |
| --- | --- |
| Vendor ID | `0x0951` (Kingston / HyperX) |
| Product IDs | `0x16C4` (older) · `0x1723` (newer) |
| Battery request | `21 FF 05`, zero-padded to 20 bytes. |
| Reply | identified by length (15 or 20 bytes), not by a report-ID byte. |
| Battery value | voltage in mV, big-endian at `reply[3..4]`; a polynomial curve estimates 0–100% (valid roughly 3300–4200 mV). |
| Charging | voltage above ~4107 mV means charging; no percentage is reported in that state. |

### Cloud II Wireless (HP-branded)

| Field | Value |
| --- | --- |
| Vendor ID | `0x03F0` (HP Inc) |
| Product ID | `0x0696` |
| HID collection | usage page `0xFF90`, usage `0x0303`, interface 0 |
| Commands | write `06 FF BB <cmd> 00`, zero-padded to 52 bytes; 20-byte reply, valid when `reply[0..3] == 06 FF BB <cmd>` |
| Battery level | command `0x02`, level at `reply[7]`, direct 0–100 |
| Charging | command `0x03`, `reply[4] == 1` means charging |

### Cloud II Wireless (Kingston-branded)

A different wire format from the HP-branded model. HeadsetControl credits
[HyperHeadset](https://github.com/LennardKittner/HyperHeadset) for
reverse-engineering this variant.

| Field | Value |
| --- | --- |
| Vendor ID | `0x0951` |
| Product ID | `0x1718` |
| Commands | 17-byte preamble `06 00 02 00 9A 00 00 68 4A 8E 0A 00 00 00 BB <cmd> <payload>`, zero-padded to 62 bytes; 64-byte reply, valid when `reply[0] == 0x0B` and `reply[2] == 0xBB` |
| Battery level | command `0x02`, level at `reply[7]` |
| Charging | command `0x03`, `reply[4] == 1` means charging |

### Cloud Alpha Wireless

| Field | Value |
| --- | --- |
| Vendor ID | `0x03F0` (HP Inc) |
| Product ID | `0x098D` |
| Commands | three separate 31-byte round trips, each `21 BB <cmd>` zero-padded to 31 bytes, replying 31 bytes: connection check `0x03` (`reply[3] == 1` means not connected), charging check `0x0C` (`reply[3] == 1` means charging), battery level `0x0B` (`reply[3]` = direct 0–100, only meaningful when not charging) |

---

## Not yet implemented

- **SteelSeries Arctis Nova 7** — request `06 18` padded to 64 bytes; battery
  bars 0–4 at `reply[2]`, `reply[3] == 1` means charging.
- **Corsair** VOID / Virtuoso.
- **Logitech** G-series / ASTRO A50 — voltage-based with a curve, and a
  structured HID++ handshake. Bigger job; on the roadmap.

If your headset is already supported by
[HeadsetControl](https://github.com/Sapd/HeadsetControl), linking that in an
issue is the fastest path, the protocol is already documented there.
