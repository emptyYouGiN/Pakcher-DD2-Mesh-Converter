import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import threading
import sys

# --- CONFIGURATION ---
SCRIPT_NAME = "converter_script.py"
APP_TITLE = "Pakcher: DD2 Mesh Converter"

class PakcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("600x520")
        self.root.resizable(False, False)
        
        # Variables
        self.blender_path = tk.StringVar()
        self.files_to_process = []
        
        # Auto-detect Blender
        found_path = self.find_blender_auto()
        if found_path:
            self.blender_path.set(found_path)
        else:
            self.blender_path.set("Blender not found! Please browse manually.")

        # --- UI LAYOUT ---
        
        # 1. Blender Settings
        frame_top = tk.LabelFrame(root, text="Blender Settings", padx=10, pady=5)
        frame_top.pack(fill="x", padx=10, pady=5)
        
        tk.Entry(frame_top, textvariable=self.blender_path, width=58).pack(side="left", padx=5)
        tk.Button(frame_top, text="Browse...", command=self.browse_blender).pack(side="left")

        # 2. File Selection
        frame_mid = tk.LabelFrame(root, text="Files to Convert (.mesh.231011879)", padx=10, pady=5)
        frame_mid.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.file_listbox = tk.Listbox(frame_mid, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill="both", expand=True, side="left")
        
        btn_frame = tk.Frame(frame_mid)
        btn_frame.pack(side="right", fill="y")
        tk.Button(btn_frame, text="Add Files", command=self.add_files, bg="#dddddd", width=12).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Clear List", command=self.clear_list, bg="#dddddd", width=12).pack(fill="x", pady=2)

        # 3. Action Button
        self.btn_run = tk.Button(root, text="CONVERT (PAKCHER)", command=self.start_conversion, 
                                 bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), height=2)
        self.btn_run.pack(fill="x", padx=10, pady=10)

        # 4. Log Area
        self.log_area = scrolledtext.ScrolledText(root, height=8, state='disabled', font=("Consolas", 8))
        self.log_area.pack(fill="x", padx=10, pady=(0, 5))

        # 5. CREDITS
        credits_frame = tk.Frame(root)
        credits_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        lbl_credits = tk.Label(credits_frame, 
            text="Special thanks to DPAvg and Feuleur\nThe heroes of Vernworth and Bakbattahl", 
            font=("Segoe UI", 8, "italic"), fg="#666666", justify="right")
        lbl_credits.pack(side="right")

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def find_blender_auto(self):
        steam_path = r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"
        if os.path.exists(steam_path):
            return steam_path
        
        foundation_path = r"C:\Program Files\Blender Foundation"
        if os.path.exists(foundation_path):
            dirs = sorted(os.listdir(foundation_path), reverse=True)
            for item in dirs:
                check = os.path.join(foundation_path, item, "blender.exe")
                if os.path.exists(check):
                    return check
        return None

    def browse_blender(self):
        filename = filedialog.askopenfilename(title="Select blender.exe", filetypes=[("Executable", "*.exe")])
        if filename:
            self.blender_path.set(filename)

    def add_files(self):
        filetypes = [
            ("Legacy Mesh Files", "*.mesh.231011879"),
            ("All Files", "*.*")
        ]
        filenames = filedialog.askopenfilenames(title="Select Mesh Files", filetypes=filetypes)
        
        for f in filenames:
            if f.lower().endswith(".pak"):
                messagebox.showwarning("Format Error", 
                    f"The file '{os.path.basename(f)}' is an Archive (.pak)!\n\n"
                    "Please unpack it first using RETool, then select the internal file ending in .mesh.231011879")
                continue 
            
            if "231011879" not in f and not f.endswith(".mesh"):
                 res = messagebox.askyesno("Warning", 
                    f"The file '{os.path.basename(f)}' does not look like a Legacy Mesh (ID 231011879 is missing).\n"
                    "Are you sure you want to try converting it?")
                 if not res:
                     continue

            if f not in self.files_to_process:
                self.files_to_process.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def clear_list(self):
        self.files_to_process = []
        self.file_listbox.delete(0, tk.END)

    def start_conversion(self):
        blender = self.blender_path.get()
        if not os.path.exists(blender):
            messagebox.showerror("Error", "Blender path is invalid!")
            return
        
        if not self.files_to_process:
            messagebox.showwarning("Warning", "No files selected.")
            return

        # --- ИСПРАВЛЕНИЕ ПУТИ ---
        # Определяем, где мы находимся (в EXE или в обычном скрипте)
        if hasattr(sys, '_MEIPASS'):
            # Если запущено как EXE
            base_path = sys._MEIPASS
        else:
            # Если запущено как скрипт Python (берем папку, где лежит этот файл)
            base_path = os.path.dirname(os.path.abspath(__file__))

        script_path = os.path.join(base_path, SCRIPT_NAME)
        # ------------------------

        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Script '{SCRIPT_NAME}' not found in:\n{base_path}")
            return

        self.btn_run.config(state="disabled", text="PROCESSING...")
        self.log(">>> Starting conversion process...")
        
        threading.Thread(target=self.run_blender_process, args=(blender, script_path, self.files_to_process)).start()

    def run_blender_process(self, blender, script, files):
        cmd = [blender, "-b", "-P", script, "--"] + files
        
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                       universal_newlines=True, startupinfo=startupinfo)
            
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            self.log(">>> Done! Check your file folder.")
            messagebox.showinfo("Success", "Conversion finished!")
            
        except Exception as e:
            self.log(f"!!! CRITICAL ERROR: {e}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.root.after(0, lambda: self.btn_run.config(state="normal", text="CONVERT (PAKCHER)"))

if __name__ == "__main__":
    root = tk.Tk()
    app = PakcherApp(root)
    root.mainloop()