# headset-probe.py

A small, read-only USB HID inspector. It helps us add or fix wireless-headset
battery support in Volume+ by collecting the raw bytes a headset exchanges over
its USB dongle.

It is one short file with one dependency. Read it, or paste it into any AI
assistant and ask whether it's safe, before running it.

## What it does

- **No arguments:** lists your HID devices (vendor/product IDs, USB names, usage
  pages). This only reads the operating system's device list. Nothing is opened.
- **`--probe VID:PID`:** opens that one device and sends the documented *battery
  request* for its vendor, then prints the raw reply. These are the same public,
  reverse-engineered requests used by
  [HeadsetControl](https://github.com/Sapd/HeadsetControl). They ask the headset
  for its charge level. They do not change any setting on it.

## What it will not do

- No writing to disk (unless you pass `--out FILE`, which just saves the console
  text).
- No network connection, no install, no background service. It runs once and
  exits.
- It refuses to open any Corsair device (vendor `0x1B1C`). The Corsair Galleon
  keyboard's own HID interface must never be written to; doing so blanks its
  built-in Stream Deck display. Your headset dongle is a separate USB device and
  is safe.

## Running it

```
pip install hidapi

python headset-probe.py                     # list devices
python headset-probe.py --probe 1038:12AD   # probe one device (hex VID:PID)
python headset-probe.py --probe 1038:12AD --out probe.txt
```

Have the headset powered on and connected through its USB dongle (not
Bluetooth). Then open a **Headset battery badge issue** on the main repo and
paste the output. If you can read the headset's real charge % another way (the
vendor app, a voice prompt), include that too.

To undo the one dependency afterwards: `pip uninstall hidapi`.

## License

MIT, see [LICENSE](LICENSE). The rest of this repository is not MIT; this folder
is separately licensed so you're free to read, modify, and reuse the tool.
