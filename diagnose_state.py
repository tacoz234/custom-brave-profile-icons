import json
import os

base_path = os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser/")
local_state_path = os.path.join(base_path, "Local State")

print(f"Checking Base Path: {base_path}")

if not os.path.exists(local_state_path):
    print("Local State file not found!")
    exit()

try:
    with open(local_state_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    info_cache = data.get("profile", {}).get("info_cache", {})
    
    print(f"\nFound {len(info_cache)} profiles in Local State:")
    
    for profile_dir, info in info_cache.items():
        print(f"\n--- {info.get('name')} ({profile_dir}) ---")
        print(f"  gaid_id: {info.get('gaia_id')}")
        print(f"  use_gaia_picture: {info.get('use_gaia_picture')}")
        print(f"  is_using_default_avatar: {info.get('is_using_default_avatar')}")
        print(f"  avatar_icon: {info.get('avatar_icon')}")
        
        # Check Preferences for this profile
        pref_path = os.path.join(base_path, profile_dir, "Preferences")
        if os.path.exists(pref_path):
            try:
                with open(pref_path, 'r', encoding='utf-8') as pf:
                    p_data = json.load(pf)
                    p_profile = p_data.get("profile", {})
                    print(f"  [Preferences] using_gaia_avatar: {p_profile.get('using_gaia_avatar')}")
                    print(f"  [Preferences] using_default_avatar: {p_profile.get('using_default_avatar')}")
            except Exception as e:
                print(f"  [Preferences] Error reading: {e}")
        else:
            print(f"  [Preferences] File not found at {pref_path}")
            
        # Check Image Files
        img_png = os.path.join(base_path, profile_dir, "Google Profile Picture.png")
        img_noext = os.path.join(base_path, profile_dir, "Google Profile Picture")
        
        print(f"  [File] .png exists: {os.path.exists(img_png)} ({os.path.getsize(img_png) if os.path.exists(img_png) else 0} bytes)")
        print(f"  [File] no-ext exists: {os.path.exists(img_noext)} ({os.path.getsize(img_noext) if os.path.exists(img_noext) else 0} bytes)")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
