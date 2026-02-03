import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from brave_custom_icon import BraveProfileManager

class BraveIconApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brave Custom Icon Changer")
        self.root.geometry("400x350")
        
        self.manager = BraveProfileManager()
        self.profiles = {}
        self.selected_image_path = None

        self.create_widgets()
        self.load_profiles()

    def create_widgets(self):
        # Header
        header = ttk.Label(self.root, text="Brave Profile Icon Customizer", font=("Helvetica", 14, "bold"))
        header.pack(pady=10)

        # Profile Selection
        ttk.Label(self.root, text="Select Profile:").pack(pady=5)
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(self.root, textvariable=self.profile_var, state="readonly", width=40)
        self.profile_combo.pack(pady=5)

        # Image Selection
        ttk.Label(self.root, text="Select Image:").pack(pady=5)
        self.image_label = ttk.Label(self.root, text="No image selected", foreground="gray", wraplength=350)
        self.image_label.pack(pady=5)
        
        btn_browse = ttk.Button(self.root, text="Browse...", command=self.browse_image)
        btn_browse.pack(pady=5)

        # Apply Button
        self.btn_apply = ttk.Button(self.root, text="Apply Custom Icon", command=self.apply_icon, state="disabled")
        self.btn_apply.pack(pady=20)

        # Status
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, foreground="blue")
        self.status_label.pack(pady=10)

        # Warning
        warning_label = ttk.Label(self.root, text="Note: Close Brave Browser before applying.", foreground="red", font=("Helvetica", 10))
        warning_label.pack(side="bottom", pady=10)

    def load_profiles(self):
        try:
            self.profiles = self.manager.load_profiles()
            # Format: "Name (Profile X)"
            profile_list = [f"{info['name']} ({key})" for key, info in self.profiles.items()]
            self.profile_combo['values'] = profile_list
            if profile_list:
                self.profile_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profiles: {e}")

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.ico")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.image_label.config(text=os.path.basename(file_path), foreground="black")
            self.btn_apply.config(state="normal")

    def apply_icon(self):
        selection = self.profile_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile.")
            return
        
        # Extract profile key from selection string "Name (Profile X)"
        profile_key = selection.split("(")[-1].strip(")")
        
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "Please select an image.")
            return

        try:
            self.status_var.set("Processing...")
            self.root.update_idletasks()
            
            self.manager.set_custom_icon(profile_key, self.selected_image_path)
            
            self.status_var.set("Success! Restart Brave to see changes.")
            messagebox.showinfo("Success", "Custom icon applied successfully!\nPlease restart Brave Browser.")
        except Exception as e:
            self.status_var.set("Error occurred.")
            messagebox.showerror("Error", f"Failed to apply icon: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BraveIconApp(root)
    root.mainloop()
