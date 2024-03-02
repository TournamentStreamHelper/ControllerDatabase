# Controller Database

This repository’s purpose is to catalog various controllers, including name, photos and functionality, used primarily for fighting games and other console-first experiences.

## Directory structure

Here’s the general arborescence for this repository:

```
- {category}                     Folder for a category of controller (Example: Mouse, Keyboard, Pad, Arcade Stick, Leverless, etc.)
| - config.json                  File containing the name of the category alongside a short description of what it entails
| - {manufacturer}               Folder for a manufacturer of controllers (Example: Microsoft, Sony, Nintendo, HORI, Victrix, etc.)
| | - config.json                File containing the name of the manufacturer and, if relevant, a description
| | - {model}                    Folder for a given device (Example: Sony Dualsense, Victrix Pro BFG, B0XX, etc.)
| | | - config.json              File containing the name of the controller, specs of said controller, picture credits and variant description
| | | - image.png                Picture of the controller
```

## Console IDs

| ID | Console |
| :---- | :---- |
| `ps1` | PlayStation 1 |
| `ps2` | PlayStation 2 |
| `ps3` | PlayStation 3 |
| `ps4` | PlayStation 4 |
| `ps5` | PlayStation 5 |
| `xbox` | Xbox |
| `xb360` | Xbox 360 |
| `xb1` | Xbox One |
| `xbs` | Xbox Series X\|S |
| `nes` | Nintendo Entertainment System / Famicom |
| `snes` | Super Nintendo Entertainment System / Super Famicom |
| `n64` | Nintendo 64 |
| `ngc` | Nintendo GameCube |
| `wii` | Nintendo Wii |
| `wiiu` | Nintendo Wii U |
| `nsw` | Nintendo Switch |
| `smd` | Sega Mega Drive / Sega Genesis |
| `saturn` | Sega Saturn |
| `dc` | Sega Dreamcast |
