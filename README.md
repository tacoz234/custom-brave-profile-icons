# Brave Custom Profile Icons

**A powerful, cross-platform tool to force custom profile pictures on Brave Browser without a Google Account.**

## Overview

Brave Browser (and other Chromium-based browsers) restricts users from setting custom local images as profile avatars unless they are signed in to a Google Account. This limitation forces users to choose from a generic set of stock icons.

**Brave Custom Profile Icons** bypasses this restriction by processing your image and injecting a "Fake GAIA" configuration directly into Brave's local data. This tricks the browser into accepting your local image as a legitimate synced account picture.

## Features

- **Cross-Platform:** Native support for **macOS** and **Windows**.
- **Standalone App:** Available as a standalone `.app` for macOS (no Python required).
- **Smart Detection:** Automatically finds all your Brave profiles (Default, Profile 1, etc.).
- **Image Engine:** Auto-crops, centers, and resizes any image to the required 256x256 PNG format.
- **Safety First:** Automatically backs up configuration files (`Local State.bak`, `Preferences.bak`) before applying patches.
- **Dual Mode:** Includes both a graphical user interface (GUI) and a command-line tool (CLI).

## Quick Start (macOS App)

If you downloaded the release version:

1.  **Close Brave Browser completely** (Cmd+Q).
2.  Double-click **"Brave Icon Changer.app"**.
3.  Select your profile and image, then click **Apply**.

## Developer / Script Usage

If you are running from source:

1.  Clone or download this repository.
2.  Install the required dependency (`Pillow` for image processing):

    ```bash
    pip install -r requirements.txt
    ```

## Usage

**IMPORTANT:** Close Brave Browser completely before running the tool. If Brave is open, it will overwrite your changes immediately.

### Option 1: GUI (Recommended)
Run the graphical interface:

```bash
python3 brave_custom_icon_gui.py
```
1. Select your profile from the dropdown.
2. Click "Select Image" to choose your file.
3. Click "Apply Custom Icon".

### Option 2: Command Line
Run the terminal script:

```bash
python3 brave_custom_icon.py
```
Follow the on-screen prompts to select a profile and provide the path to your image.

## Troubleshooting

### Icon reverts to default on restart
Chromium browsers have strict validation for profile settings. If your icon disappears:
1. Ensure Brave was **fully quit** (Cmd+Q on Mac, Exit on Windows) before running the script.
2. Run the script again. We use a "Fake GAIA ID" injection method to trick the browser into loading the local file.

### "Operation not permitted" Error (macOS)
If you see permission errors on macOS:
- Ensure your Terminal app (or IDE) has **Full Disk Access** or access to the `~/Library/Application Support` directory.
- The script attempts to use `cp` via subprocess to mitigate this, but strict system settings may still block it.

## Technical Details
This tool works by:
1.  Placing a `Google Profile Picture.png` file in the specific profile directory.
2.  Modifying the `Local State` JSON file to inject a 21-digit dummy `gaia_id` and setting `use_gaia_picture` to `true`.
3.  Modifying the profile's `Preferences` file to set `using_gaia_avatar` to `true`.

## License
MIT
