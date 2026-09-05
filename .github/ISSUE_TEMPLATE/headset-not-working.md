---
name: Headset battery badge issue
about: Your headset isn't detected, or the battery badge shows a wrong / missing value
title: "[Headset] "
labels: headset
---

**Headset model:** (e.g. SteelSeries Arctis 7)
**Connection:** USB dongle / base station / Bluetooth / wired
**What the settings panel says it detected:** (open the widget settings; the text
under "Headset battery badge" reports this)
**What happened:** no badge appears / wrong percentage / stuck value / other

**Real charge % right now (if you can check):**
**USB vendor/product ID:** Windows Device Manager → your headset or its dongle →
Properties → Details → "Hardware Ids" → paste the `VID_xxxx&PID_xxxx` value.

**Does the vendor's own app report a battery %?** yes / no

**Raw HID bytes (optional but very helpful):** run
[`tools/headset-probe.py`](../../blob/main/tools/headset-probe.py) and paste its
output. It's read-only and safe, see `tools/README.md`.

---

See [CONTRIBUTING.md](../../blob/main/CONTRIBUTING.md) for how confirmation
works. Only wireless headsets on their own USB dongle are in scope, Bluetooth
and wired don't expose battery this way.
