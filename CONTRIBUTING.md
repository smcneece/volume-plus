# Helping with headset support

Volume+ reads a wireless headset's battery over raw USB HID. Every headset speaks
a slightly different dialect, and the only way to support one is to know the
exact bytes it exchanges. That's where you come in.

The plugin itself is closed-source, so you don't need to build anything. Two
kinds of help:

## 1. Confirm a Beta headset

If your headset shows as **🧪 Beta** in the README table, the protocol is
implemented but unverified. To confirm it:

1. Make sure the headset is on and connected via its **USB dongle** (not
   Bluetooth).
2. In a Volume+ widget's settings, tick **Headset battery badge → Show**.
3. Note what the settings panel says it detected, and what the badge shows.
4. Compare the badge % against your headset's real charge (check the vendor
   app once, or your headset's own voice prompt).
5. [Open a headset issue](../../issues/new/choose) with: exact model, what the
   badge showed, and the real %.

If it's accurate, we flip it from Beta to verified. If it's wrong, the raw
bytes (below) let us fix it.

## 2. Add a headset that isn't listed at all

Open a headset issue with:

- **Exact model** and how it connects (USB dongle / base station).
- **USB vendor & product ID.** Windows: Device Manager → your headset or its
  dongle → Properties → Details → "Hardware Ids" → the `VID_xxxx&PID_xxxx`
  value.
- Whether the vendor's own software reports a battery %, and roughly what it
  shows right now.

If your model is already supported by
[HeadsetControl](https://github.com/Sapd/HeadsetControl), link that, it means
the protocol is already documented and adding it is quick.

## 3. Capture the raw HID bytes

For a Beta headset that shows a wrong value, or a new one we can't work out from
the IDs alone, we need the actual bytes it sends back. There's a small tool for
that: [`tools/headset-probe.py`](tools/headset-probe.py).

- It's one short Python file with one dependency (`pip install hidapi`). Read it
  first, or paste it into any AI assistant and ask whether it's safe.
- Run with no arguments it just lists your HID devices. With `--probe VID:PID` it
  opens that one device and sends the documented battery request, printing the
  raw reply.
- It writes nothing, connects to nothing, installs no service, and refuses to
  open Corsair devices. See [`tools/README.md`](tools/README.md).

Paste its output into a headset issue, along with your headset's real charge %
if you can read it another way.

The request bytes and reply offsets it uses are written up in
[`docs/headset-protocols.md`](docs/headset-protocols.md).

## Ground rules

- Protocol **facts** (IDs, report bytes, offsets, scaling) are not
  copyrightable and are fair to share. Please **don't paste GPL-licensed source
  code** into issues, a link is fine.
- Anything newly worked out here that isn't already in HeadsetControl, we aim to
  contribute upstream to them.
