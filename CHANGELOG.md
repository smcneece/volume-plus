# Volume+ Changelog

What has shipped, and what is being worked on right now. The **Unreleased**
section is work in progress that is not on the Marketplace yet.

Product page: https://marketplace.elgato.com/product/volume-eb2f8e95-7378-4b9f-9842-d8eefd78cc17

## Unreleased

## 1.2.0

- Performance: less background work while the plugin sits idle. The Game Mode badge no longer re-reads every Stream Deck profile file once a second (it reads one only when it actually changes), the clock stopped rebuilding its date formatter on every redraw, and the Volume and Microphone widgets stop repainting once their picture has settled instead of every half second. Opening a widget's settings no longer briefly stutters either. Lighter on CPU and disk, no change to what you see.
- Performance: the headset battery read no longer has any chance of briefly freezing the dial or clock, even in the rare case where a headset stops responding. It always worked, this just removes the last bit of theoretical stutter.
- Groundwork for Corsair wireless headset battery support, the next headset brand after HyperX. Still waiting on volunteers to confirm it on real hardware.
- The settings panel is more compact: Caps Lock and Headset Battery are one checkbox row now instead of two, and the Clock's 24-hour and Seconds toggles share a row too.
- The Clock's Face list is grouped into Digital and Analog now, and the names are shorter since the group already says which kind it is.
- Fixed the big digital clock face clipping a hair on the edge in plain 24-hour mode (no seconds).
- New widgets now start on whatever accent color you last picked on any Volume+ widget, instead of always defaulting to blue. Pick purple for Volume, add a Clock, it starts purple too.

## 1.1.0

- New: **Microphone** widget. The same control as Volume, for your input device. Rotate to set your mic level, press or tap to mute, target any capture device or the system default.
- New: **wireless headset battery badge**. A third status badge showing your headset's charge percent, read straight from the headset's own USB dongle with no vendor software, and nothing is written to your keyboard. Your headset is detected automatically. Confirmed on the SteelSeries Arctis 7 and Arctis Pro. SteelSeries Nova 7 and several HyperX models are built in and waiting on owner confirmation before they turn on.
- New: **flip clock** face, a mechanical split-flap display with its own card and digit colors. Seven clock faces total now.
- New: give the analog **second hand its own color**, separate from the widget accent. Set it to your accent for a one-color look.
- The big digital clock face is larger and no longer clips the time when seconds are on.
- The "digital + date" face now honors the Seconds toggle.
- The clock settings panel hides options that do not apply to the face you picked.
- Status badges are now the same size on every widget.
- The headset badge shows up within about five seconds of powering the headset on, instead of up to forty-five.

## 1.0.0

- First release. Two widgets for a Stream Deck: **Volume** (a full Volume Controller replacement) and **Clock**.
- **Volume**: rotate to adjust any output device by a step size you set, press or tap to mute, target a specific device or the system default. Speaker icon, percentage readout, and a colored bar. Works on a plain key too.
- **Clock**: six faces (big digital, digital with the date, classic analog, minimal analog, analog and digital combined, a day-progress ring). 12 or 24-hour, seconds, date formats, any time zone with the city shown as a caption.
- **Caps Lock** and **Game Mode** badges on both widgets, color-matched to your theme. Game Mode auto-detects a Corsair "Game Mode" action on your profile. Neither badge touches the keyboard.
- One accent color per widget. Transparent or solid clock background.
- Windows 10 or later.
