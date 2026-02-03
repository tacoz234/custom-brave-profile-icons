import json
import os
import shutil
import sys
import subprocess
import tempfile
from PIL import Image

class BraveProfileManager:
    def __init__(self):
        self.base_path = os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser/")
        self.local_state_path = os.path.join(self.base_path, "Local State")
        self.profiles = {}

    def load_profiles(self):
        if not os.path.exists(self.local_state_path):
            raise FileNotFoundError(f"Local State file not found at {self.local_state_path}")
        
        try:
            with open(self.local_state_path, 'r', encoding='utf-8') as f:
                self.local_state_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Failed to decode Local State JSON.")

        profile_info_cache = self.local_state_data.get("profile", {}).get("info_cache", {})
        
        for profile_dir, info in profile_info_cache.items():
            self.profiles[profile_dir] = {
                "name": info.get("name", profile_dir),
                "dir": profile_dir,
                "path": os.path.join(self.base_path, profile_dir)
            }
        
        return self.profiles

    def _safe_copy(self, src, dst):
        """Use subprocess to copy file to bypass potential Python permission issues in some environments."""
        try:
            subprocess.check_call(['cp', src, dst])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to copy {src} to {dst}: {e}")

    def set_custom_icon(self, profile_dir, image_path):
        if profile_dir not in self.profiles:
            raise ValueError(f"Profile {profile_dir} not found.")

        profile_path = self.profiles[profile_dir]["path"]
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)

        # 1. Process Image
        # Chromium often checks for "Google Profile Picture.png"
        target_image_name = "Google Profile Picture.png"
        
        # Create a temp file for the processed image
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
            tmp_img_path = tmp_img.name
        
        try:
            img = Image.open(image_path)
            # Resize/Crop to square
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            
            img = img.crop((left, top, right, bottom))
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            img.save(tmp_img_path, "PNG")
            
            # Copy to destination (Standard name)
            target_path = os.path.join(profile_path, target_image_name)
            self._safe_copy(tmp_img_path, target_path)
            
            # Copy to destination (No extension - sometimes used by Chromium)
            target_path_no_ext = os.path.join(profile_path, "Google Profile Picture")
            self._safe_copy(tmp_img_path, target_path_no_ext)
            
            print(f"Image processed and saved to {target_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to process image: {e}")
        finally:
            if os.path.exists(tmp_img_path):
                os.remove(tmp_img_path)

        # 2. Update Local State
        # We need to re-read Local State to ensure we have the latest version
        with open(self.local_state_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "profile" in data and "info_cache" in data["profile"] and profile_dir in data["profile"]["info_cache"]:
            profile_data = data["profile"]["info_cache"][profile_dir]
            profile_data["use_gaia_picture"] = True
            profile_data["is_using_default_avatar"] = False
            # Inject dummy GAIA ID (21 digits) to trick Chromium into loading the local file
            if not profile_data.get("gaia_id"):
                profile_data["gaia_id"] = "999999999999999999999"
            
            # Explicitly set the file name
            profile_data["gaia_picture_file_name"] = "Google Profile Picture.png"

            # Reset avatar icon to a generic one
            profile_data["avatar_icon"] = "chrome://theme/IDR_PROFILE_AVATAR_56"
        else:
             raise ValueError("Profile entry missing in Local State.")

        # Write to temp file first
        with tempfile.NamedTemporaryFile(mode='w', suffix=".json", delete=False, encoding='utf-8') as tmp_json:
            json.dump(data, tmp_json, indent=2)
            tmp_json_path = tmp_json.name

        try:
            # Backup Local State
            try:
                self._safe_copy(self.local_state_path, self.local_state_path + ".bak")
            except Exception as e:
                print(f"Warning: Could not create backup: {e}")

            # Overwrite Local State
            self._safe_copy(tmp_json_path, self.local_state_path)
            print("Local State updated successfully.")
        finally:
            if os.path.exists(tmp_json_path):
                os.remove(tmp_json_path)

        # 3. Update Profile Preferences
        preferences_path = os.path.join(profile_path, "Preferences")
        if os.path.exists(preferences_path):
            try:
                with open(preferences_path, 'r', encoding='utf-8') as f:
                    pref_data = json.load(f)
                
                # Update Preferences
                if "profile" not in pref_data:
                    pref_data["profile"] = {}
                
                pref_data["profile"]["using_gaia_avatar"] = True
                pref_data["profile"]["using_default_avatar"] = False
                
                # Write back Preferences
                with tempfile.NamedTemporaryFile(mode='w', suffix=".json", delete=False, encoding='utf-8') as tmp_pref:
                    json.dump(pref_data, tmp_pref, indent=2)
                    tmp_pref_path = tmp_pref.name
                
                try:
                    self._safe_copy(preferences_path, preferences_path + ".bak")
                    self._safe_copy(tmp_pref_path, preferences_path)
                    print("Profile Preferences updated successfully.")
                finally:
                    if os.path.exists(tmp_pref_path):
                        os.remove(tmp_pref_path)
            except Exception as e:
                print(f"Warning: Failed to update Profile Preferences: {e}")
        else:
            print("Warning: Preferences file not found. Skipping.")


def list_profiles(manager):
    profiles = manager.load_profiles()
    print("\nAvailable Profiles:")
    for i, (key, val) in enumerate(profiles.items()):
        print(f"{i+1}. {val['name']} ({key})")
    return list(profiles.keys())

def main():
    manager = BraveProfileManager()
    
    print("--- Brave Custom Profile Icon Tool ---")
    print("WARNING: Please close Brave Browser completely before proceeding to avoid overwriting changes.")
    
    try:
        profile_keys = list_profiles(manager)
    except Exception as e:
        print(f"Error loading profiles: {e}")
        return

    if not profile_keys:
        print("No profiles found.")
        return

    try:
        choice = int(input("\nSelect a profile (number): "))
        if 1 <= choice <= len(profile_keys):
            selected_profile_key = profile_keys[choice-1]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input.")
        return

    image_path = input("\nEnter path to custom image file: ").strip().strip("'").strip('"')
    if not os.path.exists(image_path):
        print("Image file not found.")
        return

    try:
        manager.set_custom_icon(selected_profile_key, image_path)
        print("\nSuccess! Custom icon applied.")
        print("Please restart Brave Browser to see the changes.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
