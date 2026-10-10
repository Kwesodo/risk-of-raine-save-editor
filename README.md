# Risk of Rain 2 Save Editor

Edit Risk of Rain 2 XML profiles locally in your browser. Built with Python 3.15 and Brython 3.15. Your saves stay on your device.

## Features

- Edit Lunar Coins and unlock survivors, skills, skins, artifacts and items.
- Browse content by expansion and search achievements.
- Unlock individual entries or the entire catalog.
- Open an XML save or try a sample profile, then download your changes.

Includes content from the base game, Survivors of the Void, Seekers of the Storm, Alloyed Collective and Hallowed Concepts.

## Quick start

With `uv` installed, run these commands from the project folder:

```sh
uv python install 3.15.0
uv sync --locked
uv run risk-of-raine-save-editor --open
```

The editor opens at `http://127.0.0.1:8000`. Use `--port 8001` if the default port is busy. Stop the server with `Ctrl+C`.

## Editing a save

1. Close the game and back up your profile XML.
2. Open the file in the editor and make your changes.
3. Click **Download XML** and replace the original profile with the downloaded file.

Steam profiles are stored in:

```text
<Steam folder>\userdata\<Steam ID>\632360\remote\UserProfiles
```

The editor does not overwrite the original file. DLC content requires the corresponding expansion in the game.

## Development

```sh
uv run ruff check src typings
uv run ruff format --check src typings
uv build
```

Restart the server after changing source files or styles.

## License

[MIT](LICENSE) — Copyright (c) 2026 Kwesodo.
