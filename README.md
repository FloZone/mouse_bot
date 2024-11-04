# MouseBot
![Logo](color.ico)

A simple script that simulate mouse and keyboard activity to prevent your computer from sleeping and softwares to appear away.

Click the icon in the tray bar to start the script, press `esc` key to pause.

## Installing dependencies
All mandatory libraries and dependancies are listed in `requirements.txt`.
```bash
pip install -r ./requirements.txt
```

## Generating a new binary
Do not forget to change the script version in `setup.py` file: `SCRIPT_VERSION=X.X`.

Run the following command to build the .exe binary:
```bash
python setup.py build
```
The generated binary is located to `./dist/mouse_bot.exe`

## Other commands
* `python setup.py clean` : for cleaning temp and generated files
* `python setup.py lint` : for linting the script file
* `python setup.py fmt` : for formatting the script file
