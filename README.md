# Controller Database

This repository’s purpose is to catalog various controllers, including name, photos and functionality, used primarily for fighting games and other console-first experiences.

## Directory structure

Here’s the general arborescence for this repository:

```
{category}/                      Folder for a category of controller (Example: Mouse, Keyboard, Pad, Arcade Stick, Leverless, etc.)
├─ config.json                   File containing the name of the category alongside a short description of what it entails
├─ {manufacturer}/               Folder for a manufacturer of controllers (Example: Microsoft, Sony, Nintendo, HORI, Victrix, etc.)
│  ├─ config.json                File containing the name of the manufacturer and, if relevant, a description
│  ├─ {model}/                   Folder for a given device (Example: Sony Dualsense, Victrix Pro BFG, B0XX, etc.)
│  │  ├─ config.json             File containing the name of the controller, specs of said controller, picture credits and variant description
│  │  ├─ image.png               Picture of the controller
│  │  ├─ {variant}.png           Any image related to an alternative way to use the controller, either connected with an accessory or in a different configuration (See Joy-Con for examples)
```
