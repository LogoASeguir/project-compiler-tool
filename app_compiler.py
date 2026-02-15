import subprocess
import sys
import shutil
import os
import zipfile
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class CompilerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Project Compiler Tool")
        self.root.geometry("560x750")
        self.root.resizable(False, False)
        
        # Output folder
        self.builds_dir = Path.home() / "Desktop" / "App_Builds"
        
        # Variables
        self.project_path = tk.StringVar()
        self.main_script = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.output_name = tk.StringVar(value="MyApp")
        self.version = tk.StringVar(value="1.0.0")
        self.company = tk.StringVar(value="")
        self.product_name = tk.StringVar(value="My Application")
        self.description = tk.StringVar(value="")
        self.copyright = tk.StringVar(value=f"Copyright {datetime.now().year}")
        self.build_mode = tk.StringVar(value="onefile")
        self.console_mode = tk.StringVar(value="windowed")
        self.create_zip = tk.BooleanVar(value=True)
        self.create_launcher = tk.BooleanVar(value=True)
        self.output_to_desktop = tk.BooleanVar(value=True)
        self.use_spec = tk.BooleanVar(value=False)  # Simple mode by default
        
        self.build_ui()
    
    def build_ui(self):
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill=tk.BOTH, expand=True)
        
        row = 0
        
        # === PROJECT ===
        tk.Label(main, text="PROJECT", font=("Segoe UI", 11, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1
        
        tk.Label(main, text="Project Folder:").grid(row=row, column=0, sticky="w")
        row += 1
        
        proj_frame = tk.Frame(main)
        proj_frame.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        proj_frame.columnconfigure(0, weight=1)
        tk.Entry(proj_frame, textvariable=self.project_path, font=("Consolas", 9)).grid(row=0, column=0, sticky="ew")
        tk.Button(proj_frame, text="Browse", command=self.browse_project, width=8).grid(row=0, column=1, padx=(5, 0))
        row += 1
        
        tk.Label(main, text="Main Script:").grid(row=row, column=0, sticky="w")
        row += 1
        
        script_frame = tk.Frame(main)
        script_frame.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        script_frame.columnconfigure(0, weight=1)
        self.script_combo = ttk.Combobox(script_frame, textvariable=self.main_script, font=("Consolas", 9))
        self.script_combo.grid(row=0, column=0, sticky="ew")
        tk.Button(script_frame, text="Refresh", command=self.refresh_scripts, width=8).grid(row=0, column=1, padx=(5, 0))
        row += 1
        
        self.detect_label = tk.Label(main, text="", fg="gray", font=("Segoe UI", 8))
        self.detect_label.grid(row=row, column=0, sticky="w")
        row += 1
        
        ttk.Separator(main, orient="horizontal").grid(row=row, column=0, sticky="ew", pady=8)
        row += 1
        
        # === METADATA ===
        tk.Label(main, text="METADATA", font=("Segoe UI", 11, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1
        
        meta_frame = tk.Frame(main)
        meta_frame.grid(row=row, column=0, sticky="ew")
        meta_frame.columnconfigure(1, weight=1)
        
        fields = [
            ("Exe Name:", self.output_name),
            ("Version:", self.version),
            ("Product Name:", self.product_name),
            ("Company:", self.company),
            ("Description:", self.description),
            ("Copyright:", self.copyright),
        ]
        
        for i, (label, var) in enumerate(fields):
            tk.Label(meta_frame, text=label, width=12, anchor="w").grid(row=i, column=0, sticky="w", pady=1)
            tk.Entry(meta_frame, textvariable=var, font=("Segoe UI", 9)).grid(row=i, column=1, sticky="ew", pady=1)
        row += 1
        
        ttk.Separator(main, orient="horizontal").grid(row=row, column=0, sticky="ew", pady=8)
        row += 1
        
        # === ICON ===
        tk.Label(main, text="ICON", font=("Segoe UI", 11, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1
        
        icon_frame = tk.Frame(main)
        icon_frame.grid(row=row, column=0, sticky="ew", pady=(0, 3))
        icon_frame.columnconfigure(0, weight=1)
        tk.Entry(icon_frame, textvariable=self.icon_path, font=("Consolas", 9)).grid(row=0, column=0, sticky="ew")
        tk.Button(icon_frame, text="Browse", command=self.browse_icon, width=8).grid(row=0, column=1, padx=(5, 0))
        row += 1
        
        self.icon_preview = tk.Label(main, text="No icon selected", fg="gray", font=("Segoe UI", 8))
        self.icon_preview.grid(row=row, column=0, sticky="w")
        row += 1
        
        ttk.Separator(main, orient="horizontal").grid(row=row, column=0, sticky="ew", pady=8)
        row += 1
        
        # === BUILD OPTIONS ===
        tk.Label(main, text="BUILD OPTIONS", font=("Segoe UI", 11, "bold")).grid(row=row, column=0, sticky="w", pady=(0, 5))
        row += 1
        
        opt_frame = tk.Frame(main)
        opt_frame.grid(row=row, column=0, sticky="w", pady=(0, 5))
        
        tk.Label(opt_frame, text="Output:", width=10, anchor="w").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(opt_frame, text="Single .exe", variable=self.build_mode, value="onefile").grid(row=0, column=1, sticky="w")
        tk.Radiobutton(opt_frame, text="Folder", variable=self.build_mode, value="folder").grid(row=0, column=2, sticky="w", padx=(10, 0))
        
        tk.Label(opt_frame, text="Console:", width=10, anchor="w").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(opt_frame, text="Hidden (GUI)", variable=self.console_mode, value="windowed").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(opt_frame, text="Show", variable=self.console_mode, value="console").grid(row=1, column=2, sticky="w", padx=(10, 0))
        row += 1
        
        extra_frame = tk.Frame(main)
        extra_frame.grid(row=row, column=0, sticky="w", pady=5)
        tk.Checkbutton(extra_frame, text="Create ZIP", variable=self.create_zip).pack(side=tk.LEFT)
        tk.Checkbutton(extra_frame, text="Create launcher", variable=self.create_launcher).pack(side=tk.LEFT, padx=(10, 0))
        tk.Checkbutton(extra_frame, text="Advanced (spec)", variable=self.use_spec).pack(side=tk.LEFT, padx=(10, 0))
        row += 1
        
        tk.Checkbutton(main, text="Output to Desktop/App_Builds", variable=self.output_to_desktop).grid(row=row, column=0, sticky="w")
        row += 1
        
        ttk.Separator(main, orient="horizontal").grid(row=row, column=0, sticky="ew", pady=8)
        row += 1
        
        # === BUILD BUTTON ===
        self.mount_btn = tk.Button(
            main, text="MOUNT EXE", command=self.build,
            bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white",
            font=("Segoe UI", 14, "bold"), height=2, cursor="hand2"
        )
        self.mount_btn.grid(row=row, column=0, sticky="ew", pady=8)
        row += 1
        
        self.progress = ttk.Progressbar(main, mode='indeterminate', length=400)
        self.progress.grid(row=row, column=0, sticky="ew", pady=5)
        row += 1
        
        btn_frame = tk.Frame(main)
        btn_frame.grid(row=row, column=0, sticky="ew", pady=5)
        tk.Button(btn_frame, text="Clean", command=self.clean, width=10).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="Output", command=self.open_output, width=10).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="Builds", command=self.open_builds, width=10).pack(side=tk.LEFT)
        row += 1
        
        status_frame = tk.Frame(main, relief=tk.SUNKEN, bd=1)
        status_frame.grid(row=row, column=0, sticky="ew", pady=(10, 0))
        self.status_label = tk.Label(status_frame, text="Ready. Select a project folder.", anchor="w", padx=5, pady=5, font=("Segoe UI", 9))
        self.status_label.pack(fill=tk.X)
    
    def set_status(self, text, color="black"):
        self.status_label.config(text=text, fg=color)
        self.root.update()
    
    def browse_project(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.project_path.set(path)
            self.refresh_scripts()
    
    def refresh_scripts(self):
        project = self.project_path.get()
        if not project:
            return
        
        project_path = Path(project)
        if not project_path.exists():
            return
        
        py_files = [f.name for f in project_path.glob("*.py") if f.is_file()]
        self.script_combo["values"] = py_files
        
        # Auto-select main
        for p in ["main.py", "app.py", "ControlPanel.py", "gui.py", "run.py", "__main__.py"]:
            if p in py_files:
                self.main_script.set(p)
                break
        else:
            if py_files:
                self.main_script.set(py_files[0])
        
        # Auto-detect icon
        for ico in project_path.glob("*.ico"):
            self.icon_path.set(str(ico))
            self.icon_preview.config(text=f"✓ {ico.name}", fg="green")
            break
        
        # Auto-fill names
        name = project_path.name.replace(" ", "_").replace("-", "_")
        if self.output_name.get() == "MyApp":
            self.output_name.set(name)
        if self.product_name.get() == "My Application":
            self.product_name.set(project_path.name)
        
        self.detect_label.config(text=f"Found {len(py_files)} Python files", fg="green")
        self.set_status(f"Loaded: {project_path.name}", "green")
    
    def browse_icon(self):
        path = filedialog.askopenfilename(title="Select Icon", filetypes=[("Icon files", "*.ico"), ("All", "*.*")])
        if path:
            self.icon_path.set(path)
            self.icon_preview.config(text=f"✓ {Path(path).name}", fg="green")
    
    def ensure_pyinstaller(self):
        try:
            import PyInstaller
            return True
        except ImportError:
            self.set_status("Installing PyInstaller...", "blue")
            self.root.update()
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to install PyInstaller:\n{e}")
                return False
    
    def create_version_file(self, output_path: Path):
        version = self.version.get()
        parts = version.split(".")
        while len(parts) < 4:
            parts.append("0")
        v = [int(p) if p.isdigit() else 0 for p in parts[:4]]
        
        content = f'''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({v[0]}, {v[1]}, {v[2]}, {v[3]}),
    prodvers=({v[0]}, {v[1]}, {v[2]}, {v[3]}),
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)
  ),
  kids=[
    StringFileInfo([StringTable(u'040904B0', [
      StringStruct(u'CompanyName', u'{self.company.get()}'),
      StringStruct(u'FileDescription', u'{self.description.get() or self.product_name.get()}'),
      StringStruct(u'FileVersion', u'{version}'),
      StringStruct(u'InternalName', u'{self.output_name.get()}'),
      StringStruct(u'LegalCopyright', u'{self.copyright.get()}'),
      StringStruct(u'OriginalFilename', u'{self.output_name.get()}.exe'),
      StringStruct(u'ProductName', u'{self.product_name.get()}'),
      StringStruct(u'ProductVersion', u'{version}'),
    ])]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        output_path.write_text(content, encoding="utf-8")
    
    def build(self):
        # === VALIDATION ===
        project = self.project_path.get()
        if not project:
            messagebox.showerror("Error", "Select a project folder!")
            return
        
        project_path = Path(project)
        if not project_path.exists():
            messagebox.showerror("Error", "Project folder doesn't exist!")
            return
        
        script = self.main_script.get()
        if not script:
            messagebox.showerror("Error", "Select a main script!")
            return
        
        script_path = project_path / script
        if not script_path.exists():
            messagebox.showerror("Error", f"Script not found: {script}")
            return
        
        output_name = self.output_name.get().strip().replace(" ", "_").replace(".exe", "")
        if not output_name:
            messagebox.showerror("Error", "Enter an output name!")
            return
        self.output_name.set(output_name)
        
        if not self.ensure_pyinstaller():
            return
        
        # === START BUILD ===
        self.mount_btn.config(state=tk.DISABLED, text="⏳ Building...")
        self.progress.start(10)
        self.set_status("Building... please wait.", "blue")
        self.root.update()
        
        try:
            # Determine output location
            if self.output_to_desktop.get():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = self.builds_dir / f"{output_name}_{timestamp}"
                output_dir.mkdir(parents=True, exist_ok=True)
            else:
                output_dir = project_path
            
            dist_path = output_dir / "dist"
            build_path = output_dir / "build"
            
            # Create version file in project (PyInstaller needs it there)
            version_file = project_path / "_version_info.txt"
            self.create_version_file(version_file)
            
            # === BUILD COMMAND ===
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm",
                f"--name={output_name}",
                f"--distpath={dist_path}",
                f"--workpath={build_path}",
            ]
            
            # Add version file
            if version_file.exists():
                cmd.append(f"--version-file={version_file}")
            
            # Build mode
            if self.build_mode.get() == "onefile":
                cmd.append("--onefile")
            else:
                cmd.append("--onedir")
            
            # Console mode
            if self.console_mode.get() == "windowed":
                cmd.append("--windowed")
            else:
                cmd.append("--console")
            
            # Icon
            icon = self.icon_path.get()
            if icon and Path(icon).exists():
                cmd.append(f"--icon={icon}")
            
            # Add data files if advanced mode
            if self.use_spec.get():
                for ext in ["*.json", "*.txt", "*.csv", "*.png", "*.jpg", "*.ico"]:
                    for f in project_path.glob(ext):
                        if not f.name.startswith("_"):
                            cmd.append(f"--add-data={f};.")
            
            # Main script (must be last)
            cmd.append(str(script_path))
            
            # Debug: show command
            print("Running:", " ".join(cmd))
            
            # === RUN PYINSTALLER ===
            result = subprocess.run(
                cmd,
                cwd=str(project_path),
                capture_output=True,
                text=True
            )
            
            self.progress.stop()
            
            # Cleanup version file
            if version_file.exists():
                version_file.unlink()
            
            # Cleanup spec file from project
            spec_in_project = project_path / f"{output_name}.spec"
            if spec_in_project.exists():
                if self.output_to_desktop.get():
                    # Move spec to output dir
                    shutil.move(str(spec_in_project), str(output_dir / f"{output_name}.spec"))
                else:
                    spec_in_project.unlink()
            
            # === CHECK RESULT ===
            if result.returncode == 0:
                # Find exe
                if self.build_mode.get() == "onefile":
                    exe_path = dist_path / f"{output_name}.exe"
                else:
                    exe_path = dist_path / output_name / f"{output_name}.exe"
                
                if not exe_path.exists():
                    raise FileNotFoundError(f"EXE not created: {exe_path}")
                
                # Create launcher
                if self.create_launcher.get():
                    launcher = output_dir / f"RUN_{output_name}.bat"
                    if self.build_mode.get() == "onefile":
                        launcher.write_text(f'@echo off\ncd /d "%~dp0"\nstart "" "dist\\{output_name}.exe" %*\n', encoding="utf-8")
                    else:
                        launcher.write_text(f'@echo off\ncd /d "%~dp0"\nstart "" "dist\\{output_name}\\{output_name}.exe" %*\n', encoding="utf-8")
                
                # Create ZIP
                zip_path = None
                if self.create_zip.get():
                    self.set_status("Creating ZIP...", "blue")
                    self.root.update()
                    zip_path = output_dir / f"{output_name}_portable.zip"
                    
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for f in dist_path.rglob("*"):
                            if f.is_file():
                                zf.write(f, f.relative_to(output_dir))
                        
                        launcher = output_dir / f"RUN_{output_name}.bat"
                        if launcher.exists():
                            zf.write(launcher, launcher.name)
                
                # Cleanup build folder
                if build_path.exists():
                    shutil.rmtree(build_path)
                
                # === SUCCESS ===
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                self.set_status(f"✓ Success! {output_name}.exe ({size_mb:.1f} MB)", "green")
                
                msg = f"Build complete!\n\n"
                msg += f"{output_name}.exe ({size_mb:.1f} MB)\n"
                msg += f"{output_dir}\n"
                if zip_path and zip_path.exists():
                    msg += f"{zip_path.name}\n"
                msg += f"\nOpen folder?"
                
                if messagebox.askyesno("Success", msg):
                    os.startfile(str(output_dir))
            
            else:
                # === FAILED ===
                self.set_status("✗ Build failed!", "red")
                
                error = result.stderr or result.stdout or "Unknown error"
                
                # Show error popup
                popup = tk.Toplevel(self.root)
                popup.title("Build Error")
                popup.geometry("600x400")
                
                text = tk.Text(popup, wrap=tk.WORD, font=("Consolas", 9))
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                text.insert("1.0", f"Command:\n{' '.join(cmd)}\n\n{'='*50}\n\nError:\n{error[-3000:]}")
                
                scrollbar = ttk.Scrollbar(text, command=text.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                text.config(yscrollcommand=scrollbar.set)
                
                tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
        
        except Exception as e:
            self.progress.stop()
            self.set_status(f"✗ Error: {e}", "red")
            messagebox.showerror("Error", f"Build failed:\n\n{e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.mount_btn.config(state=tk.NORMAL, text="🔨 MOUNT EXE")
    
    def clean(self):
        project = self.project_path.get()
        if not project:
            messagebox.showerror("Error", "No project selected.")
            return
        
        project_path = Path(project)
        cleaned = []
        
        for folder in ["build", "dist", "__pycache__"]:
            p = project_path / folder
            if p.exists():
                shutil.rmtree(p)
                cleaned.append(folder)
        
        for pattern in ["*.spec", "_version_info.txt"]:
            for f in project_path.glob(pattern):
                f.unlink()
                cleaned.append(f.name)
        
        for cache in project_path.rglob("__pycache__"):
            if cache.is_dir():
                shutil.rmtree(cache)
        
        if cleaned:
            messagebox.showinfo("Cleaned", f"Removed:\n• " + "\n• ".join(cleaned))
            self.set_status(f"Cleaned {len(cleaned)} items", "green")
        else:
            messagebox.showinfo("Clean", "Nothing to clean")
    
    def open_output(self):
        project = self.project_path.get()
        if project:
            dist = Path(project) / "dist"
            if dist.exists():
                os.startfile(str(dist))
                return
        
        if self.builds_dir.exists():
            os.startfile(str(self.builds_dir))
        else:
            messagebox.showinfo("Info", "No output found. Build first!")
    
    def open_builds(self):
        self.builds_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(str(self.builds_dir))
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CompilerApp()
    app.run()