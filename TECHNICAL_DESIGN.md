# Technical Design Document: Brave Browser Custom Profile Icons

## Overview
This solution provides a method to apply custom profile pictures to Brave Browser profiles. Brave, being Chromium-based, does not natively support setting local custom images for profiles easily through its UI without syncing to a Google account (which is often disabled or stripped in Brave). This tool manipulates the local configuration files to achieve this.

## Architecture

### Brave Data Structure
Brave stores user data in:
- **macOS:** `~/Library/Application Support/BraveSoftware/Brave-Browser/`
- **Windows:** `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\` (Analogous structure)
- **Linux:** `~/.config/BraveSoftware/Brave-Browser/`

### Key Components
1.  **Local State File:** A JSON file located at the root of the User Data directory. It contains a `profile.info_cache` object listing all profiles and their metadata (name, avatar icon, etc.).
    - Key attributes to modify:
        - `use_gaia_picture`: Set to `true` to tell Brave to look for a local custom image.
        - `is_using_default_avatar`: Set to `false`.
2.  **Profile Directories:** Each profile has a directory (e.g., `Default`, `Profile 1`).
    - The custom image must be placed here with the specific name `Google Profile Picture.png`.

## Implementation Logic

### 1. Profile Discovery
The script parses `Local State` to list available profiles. It extracts the profile name (e.g., "Personal") and its directory name (e.g., "Profile 1").

### 2. Image Processing
The tool uses `Pillow` (PIL) to:
- Load the user-provided image.
- Crop the image to a square aspect ratio (center crop).
- Resize it to 256x256 pixels (standard size for high-DPI displays).
- Convert and save it as PNG.

### 3. File Operations & Permissions
On macOS, accessing `~/Library/Application Support` can be restricted by TCC (Transparency, Consent, and Control).
- **Challenge:** Python's native `open()` or `shutil.copy()` might fail with `Operation not permitted` even if the user has permissions, depending on how the script is invoked (e.g., via a terminal with limited permissions).
- **Solution:** The script uses `subprocess` to call system binaries (`cp`) which often inherit the terminal's permissions more reliably or trigger the necessary OS prompts.

### 4. Configuration Update
The script:
1.  Reads `Local State`.
2.  Modifies the selected profile's entry.
3.  Writes the new JSON to a temporary file.
4.  Uses `cp` to overwrite the original `Local State` (creating a backup first).

## Security Considerations
- **Backups:** The script creates a `.bak` copy of `Local State` before modification.
- **Image Safety:** Images are processed via PIL, which strips non-image data, reducing the risk of malicious file injection, though the browser itself treats it as a static asset.
- **Permissions:** The script runs locally with the user's privileges.

## Limitations
- **Browser State:** Brave should be closed during the operation to prevent it from overwriting the changes on exit.
- **Sync:** If Brave Sync is enabled, profile settings might be synced, but `use_gaia_picture` is typically a local override.
- **Updates:** Browser updates rarely change this structure, but if `Local State` schema changes, the script might need updates.
