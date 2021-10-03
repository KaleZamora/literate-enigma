# InstallerScript
Side project for work that streamlines our new machine / user setup.

Requirements to build:

1. \>= Python 3.x
2. pip
3. pyinstaller
4. requests

How to build the online version:

1. Clone the repo, cd into it.
2. `pip3 install pyinstaller` if you don't already have it.
3. `pip3 install requests`
4. `pyinstaller installscript.py --onefile --uac-admin`

The EXE you can then place wherever and run it as admin.

You can also check the releases for the latest stable release with a pre-compiled exe.

By Zachary Knight and Gabriel Hererra with GUI done by Jimson Whiskeyman
