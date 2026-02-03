# Brave Custom Profile Icons

A Python tool to set custom profile pictures for Brave Browser profiles on macOS.

Brave (and Chromium-based browsers) typically restricts custom profile avatars to users signed in with a Google Account ("GAIA"). This tool bypasses that limitation by injecting a local "GAIA" configuration, allowing you to use any image you want for any profile.

## Features
- **Profile Selection:** Automatically detects your Brave profiles.
- **Image Processing:** Auto-crops and resizes your image to the standard 256x256 format.
- **Dual Interface:** Choose between a simple Command Line Interface (CLI) or a Graphical User Interface (GUI).
- **Safe:** Backs up your configuration files (`Local State.bak`, `Preferences.bak`) before making changes.
- **macOS Native:** Uses system tools to handle file permissions correctly.

## Prerequisites
- macOS
- Python 3.x
- Brave Browser installed

## Installation

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
1. Ensure Brave was **fully quit** (Cmd+Q) before running the script.
2. Run the script again. We use a "Fake GAIA ID" injection method to trick the browser into loading the local file.

### "Operation not permitted" Error
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
