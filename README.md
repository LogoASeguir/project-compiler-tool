# Project Compiler Tool (PyInstaller GUI)
![Status](https://img.shields.io/badge/status-local-lightgrey)
![License](https://img.shields.io/github/license/LogoASeguir/tool-project-compiler)
![Issues](https://img.shields.io/github/issues/LogoASeguir/tool-project-compiler)
---

GUI wrapper around **PyInstaller** for building Windows executables with:
version metadata injection, icon support, and portable packaging.

---

## Demo

<p align="center">
  <img src="demo_gui.png" width="60%" alt="Project Compiler GUI demo">
</p>

---
> Status: Windows-focused (works great for Windows builds).  
> Goal: “one screen to ship a .exe + zip” without remembering PyInstaller flags.

## Features

- Auto-detect main scripts
- Version metadata injection
- `.ico` support
- One-file or one-folder build
- Optional launcher creation
- Portable ZIP generation
- Automatic PyInstaller installation (if missing)

---

## Quick Start

### 1) Install requirements
```bash
1) pip install -r requirements.txt
2) Run the app
3) python app_compiler.py
```

---

# Usage Flow
```bash
1) Select your project folder (or main script)
2) Pick build mode: one-file or one-folder
3) Set app metadata (Optional) 
4) Build
(Export a portable ZIP (Optional))
```
---

Notes: If Windows SmartScreen complains: that’s normal for unsigned executables. Make a special exception for the build created.
Some antivirus tools may flag one-file executables because of bundling behavior. Same treatment.

---

# If your build fails, try:
```bash
1) ensure your script runs cleanly before packaging
1) updating PyInstaller
2) running the tool from a fresh venv

```

Hopefully everything will work accordingly! Don't hesitate to reach out in any case! :)
---

### Author

Built by [Renato Pedrosa]  
Part of a growing ecosystem of Python-based developer tools.
