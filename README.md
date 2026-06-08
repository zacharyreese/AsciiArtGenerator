# ASCII Art Generator

A Python tool that converts images into ASCII art text.

## Features

- Convert any image to ASCII art
- Multiple character sets (simple, standard, blocks, binary, retro)
- Adjustable width and aspect ratio correction
- Contrast and brightness controls
- Color inversion support
- Save output to text files
- Interactive and command-line modes
- Web UI with drag-and-drop upload

## Installation

```bash
# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

pip install -r requirements.txt
```

## Usage

### Web UI

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

Features:
- Drag & drop image upload
- Live preview of uploaded image
- Adjustable width, contrast, brightness
- Character set selector
- Copy to clipboard or download as `.txt`

### Command Line

```bash
# Basic usage
python ascii_art.py image.jpg

# Specify width and character set
python ascii_art.py image.png -w 80 -c blocks

# Enhance contrast and save to file
python ascii_art.py photo.jpg --contrast 1.5 -o output.txt

# Invert colors (for dark backgrounds)
python ascii_art.py image.png --invert -w 120

# Preview only first 30 lines
python ascii_art.py image.jpg --preview 30
```

### Interactive Mode

```bash
python ascii_art.py -i
```

### Character Sets

| Set      | Characters                          | Best For            |
|----------|-------------------------------------|---------------------|
| simple   | ` .:-=+*#%@`                       | Quick previews      |
| standard | 70+ characters                      | Detailed art        |
| blocks   | ` ░▒▓█`                            | Smooth gradients      |
| binary   | ` █`                               | High contrast         |
| retro    | ` .oO`                             | Retro style           |

## Options

| Flag | Description |
|------|-------------|
| `-w, --width` | Output width in characters (default: 100) |
| `-c, --charset` | Character set: simple, standard, blocks, binary, retro |
| `--contrast` | Contrast enhancement factor (default: 1.0) |
| `--brightness` | Brightness enhancement factor (default: 1.0) |
| `--invert` | Invert light/dark |
| `--no-scale` | Disable aspect ratio correction |
| `-o, --output` | Save to file |
| `-i, --interactive` | Interactive mode |
| `--preview N` | Show only first N lines |

## Example Output

```
................................................................................
..............................::--==++++++=-:...................................
..........................:-=*#%%@@@@@@@@@@@%%#+=:..............................
.......................:=*%@@@@@@%#########@@@@@@%*=:...........................
.....................:+#@@@@%#*+===========++*#%@@@@#+:.........................
...................:+%@@@%#+===================+#%@@@%+:........................
..................=#@@@%*=========================*%@@@#=.......................
.................+%@@@*=============================+%@@@+......................
...............:*@@@#==================================#@@@*:.....................
..............:#@@@+====================================+@@@#:....................
.............-%@@@+======================================+@@@%-...................
............:%@@%==========================================%@@%:..................
...........:@@@%+==========================================+@@@:..................
...........*@@@============================================@@@*...................
..........=@@@*============================================*@@@=..................
..........%@@%==============================================%@@%..................
.........-@@@+==============================================+@@@-.................
.........+@@@================================================@@@+.................
.........#@@#================================================#@@#.................
........:@@@*================================================*@@@:................
```

## License

MIT
