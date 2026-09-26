# Translation notes: where each piece of text appears

Read this next to `en.json`. Keys are grouped the same way as in the file.

## Top of the file (Stream Deck's action list)

- `Name`: the plugin's name. Keep **Volume+**.
- `Description`: shown in Stream Deck's plugin details. Full sentences are fine.
- `com.megacity.volumeplus.dial` / `.mic` / `.clock` / `.timer`: the four
  widgets. `Name` is shown in the action list (keep it short: one or two
  words). `Tooltip` is the hover text. `TriggerDescription` entries are the
  short hints Stream Deck shows next to a dial: what turning (`Rotate`),
  pressing (`Push`), tapping (`Touch`) and holding a tap (`LongTouch`) do.
  Keep those very short.

## `Localization.common`: shared settings text

- `muted`: shown on the touch display when the volume is muted. Short.
- `mutedCaps`: the same, in capitals, on a plain key. 10 characters or fewer
  fits best (longer text is shrunk to fit).
- `defaultDevice`: the "use whatever Windows' default device is" choice.
- `stepSize`: how much the volume changes per click of the dial.
- `refreshRate` and `refresh*`: how often the widget re-reads the volume.
- `background`, `transparent`, `solidDark`: the widget's background choice.
  "Transparent" lets the key's own background image show through.
- `none`: used for "no date" and "no sound".
- `volume`: the Timer's alarm-sound loudness slider.

## `Localization.volume` / `Localization.mic`

- `defaultTitle`: the title a new widget starts with.
- `action`: a fixed line describing what the widget does.
- `mic.defaultDevice`: "use the default microphone".

## `Localization.timer`

- `caption`, `paused`, `timesUp`: shown on the touch display above the
  countdown. **16 characters at most**; shorter is better.
- `duration`, `dialStep`, `controls`, `sound`, `file`, `playback`, `preview`:
  settings labels. The label column is narrow; one or two words.
- `step5s` … `step5m`: how much one click of the dial changes the time.
- `alarm1` … `alarm10`, `ring1` … `ring10`: the alarm and ringtone sounds that
  come with Windows. Use the words Windows uses for them in your language.
- `groupAlarms`, `groupRingtones`: headings in the sound list.
- `repeat`: the sound keeps repeating until the user presses the dial.
- `durationHelp`: keep `M:SS` and `H:MM:SS` as they are.

## `Localization.badges`

Badges are small status icons on every widget.

- `capsLock`: use what Windows calls Caps Lock in your language.
- `headsetBattery`: a wireless headset's battery level.
- `gameMode`: shows whether Corsair's "Game Mode" is on.
- `auto`, `always`, `off`: when the Game Mode badge is shown.
- `headsetDetected`: keep `{name}` exactly; it becomes the headset's name,
  e.g. "SteelSeries Arctis 7 detected."
- `gameModeHelp`: keep "Game Mode" in quotes and in English (it's the name of
  Corsair's action).

## `Localization.clock`

- `face`: the clock's design. `groupDigital` / `groupAnalog` are headings in
  that list, and `face*` are the design names.
- `faceSeg7`, `faceSeg14`, `faceDotMatrix`: styles of LED display.
- `faceFlip`: a mechanical flip clock (split-flap display).
- `format`, `hour24`, `seconds`: 24-hour clock and show-seconds options.
- `dateDow` … `dateDmy`: **examples of the date formats, not words to
  translate literally.** In your language the clock shows the date the way
  Windows formats it, so write examples of what it actually shows for Monday,
  January 5, 2026. The last one (`dateDmy`) is the all-numeric date in most
  languages (for example `05/01/2026` in Spanish).
- `timeZone`, `timeZoneHelp`: keep the example zone names (`America/New_York`
  and so on) exactly as they are; those are technical identifiers. "Title"
  refers to Stream Deck's own Title field, so use the word Stream Deck uses.
- `secondHand`: the thin hand on analog faces.
- `cardColor`: the background of the flip clock's cards.
