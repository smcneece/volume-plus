# Help translate Volume+

Volume+ can show its widget names, settings, and on-screen text in any language
Stream Deck supports. Each language is one JSON file. If you speak one of these
languages, you can help, and you don't need to own Volume+ or know how to code.

## Language status

| Language | File | Status |
| --- | --- | --- |
| English | `en.json` | Source text (the template) |
| Spanish | `es.json` | 🧪 Draft, needs a native speaker's review |
| Chinese (Simplified) | `zh_CN.json` | 🧪 Draft, needs a native speaker's review |
| Chinese (Traditional) | `zh_TW.json` | 🧪 Draft, needs a native speaker's review |
| German | `de.json` | Wanted |
| French | `fr.json` | Wanted |
| Japanese | `ja.json` | Wanted |
| Korean | `ko.json` | Wanted |

The drafts were machine-assisted. They are probably understandable, but a
native speaker will spot wording that sounds unnatural or doesn't match what
Windows and Stream Deck call things in that language. Reviews are as valuable
as new translations.

## Reviewing a draft

1. Open the draft file for your language and read it next to `en.json`.
2. Open an issue with the **Translation** template and list what you'd change
   (the key name and your suggested text), or attach a corrected file.

## Starting a new language

1. Copy `en.json` and name the copy after your language: `de.json`, `fr.json`,
   `ja.json`, `ko.json` (Stream Deck only supports these names).
2. Translate the **text on the right side** of each line. Leave the keys (left
   side) exactly as they are.
3. Read [context.md](context.md) first: it explains where each piece of text
   appears and which ones need to stay short.
4. Open an issue with the **Translation** template and attach your file.

## Rules that matter

- Keep `{name}` exactly as it is. The plugin replaces it with a headset's name.
- Keep product names in English: **Volume+**, **Stream Deck**, **Volume
  Controller**, **Corsair**, **Galleon**, and the Corsair action name
  **"Game Mode"** when it's in quotes (that's the action's name in Stream Deck).
- Short is better. Most labels sit in a narrow column, and some text appears
  on a 200×100 pixel touch display.
- Examples of formats (`M:SS`, `America/New_York`) stay as they are.
- Please don't paste machine translation without reading it; the goal is text
  that sounds natural to a native speaker.

Your name (or GitHub handle) goes in the changelog for the release that
includes your work, unless you'd rather it didn't.

## Checking a file (optional)

If you're comfortable with Node.js: the plugin's build has a checker that
confirms a file has every key, no extra keys, and the `{name}` placeholder
intact. You don't need to run it; we'll run it when your file comes in.
