# KlipperScreen for FLSUN S1

![Banner](https://github.com/user-attachments/assets/a2ebd6cd-e430-4d7b-a240-a8cac461b0c7)

KlipperScreen is a touchscreen GUI that interfaces with [Klipper](https://github.com/kevinOConnor/klipper) via [Moonraker](https://github.com/arksine/moonraker). It can switch between multiple printers to access them from a single location, and it doesn't even need to run on the same host, you can install it on another device and configure the IP address to access the printer.

### Documentation [![Documentation Status](https://readthedocs.org/projects/klipperscreen/badge/?version=latest)](https://klipperscreen.readthedocs.io/en/latest/?badge=latest)

[Click here to access the documentation.](https://klipperscreen.readthedocs.io/en/latest/)

<br />

## About

This version of KlipperScreen is compatible with FLSUN S1, it's optimized for Delta printers.

- Latest build of KlipperScreen
- Inner/Outer Bed integration
- Drying Box integration
- Automated with prompt macros
- Some fixes and adjustments

Repository for FLSUN S1 & T1 is available here: [Flsun-S1-T1](https://github.com/Guilouz/Flsun-S1-T1)

<br />

If you like my work, don't hesitate to support me by paying me a 🍺 or a ☕. Thank you 🙂

<a href="https://ko-fi.com/guilouz" target="_blank"><img width="350" src="https://github.com/Guilouz/Creality-Helper-Script-Wiki/blob/main/docs/assets/img/home/Ko-fi.png?raw=true"></a>

<br />

## Installation

This version is already installed by default on the Open Source Edition operating system, but if you need to reinstall it, follow these steps:

- Make sure previous installation of KlipperScreen is removed (with Kiauh).
- In SSH, enter the following commands (one at a time) to install KlipperScreen:
  ```
  cd ~ && git clone https://github.com/Guilouz/KlipperScreen-Flsun-S1.git ~/KlipperScreen
  ```
  ```
  ./KlipperScreen/scripts/KlipperScreen-install.sh
  ```

- Go to your Mainsail Web interface then select the `Machine` tab.
- Open the `moonraker.conf` file and modify the `[update_manager KlipperScreen]` section  as follows:

  ```
  [update_manager KlipperScreen]
  type: git_repo
  path: ~/KlipperScreen
  origin: https://github.com/Guilouz/KlipperScreen-Flsun-S1.git
  virtualenv: ~/.KlipperScreen-env
  requirements: scripts/KlipperScreen-requirements.txt
  system_dependencies: scripts/system-dependencies.json
  managed_services: KlipperScreen
  ```
- Once done, click on `SAVE & RESTART` at the top right to save the file.
- You can now click the refresh button (still in the Machine tab) on the `Update Manager` tile.
- Once installed you will have the new version of KlipperScreen and future updates will point directly to my repo.
