# License Plate Detector
Trained YOLO model to detect and censor license plates

## Setup
```bash
$ pip install -r requirements.txt
```
Or make a virtual environment
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install -r requirements.txt
```

## Usage

### View a censored plate, requires pygame
```Bash
$ python3 draw.py <image>
```
- `image` must be a .png file


### Save a new image with the license plate censored 
```bash
$ python3 car_image_saver.py <source> <dest> {<color> | <blur distance>} [secret]
```  

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `source` | `string` | Path to the image you want censored |
| `dest` | `string` | Name of new, censored image. If `dest` doesn't end with '.png' it will be added|
| `<r,g,b> \| <blur_distance>` | `int`,`int`,`int` &nbsp;\|&nbsp;  `int` | Either comma-separated RGB values or the inradius of the square used to blur |
| `secret` | `literal` | Will not save any image that doesn't detect a plate |

### Save many images at once
```bash
$ python3 car_image_saver.py <dir> <dest_path> <dest_name> {<color> | <blur distance>} [secret]
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `source` | `string` | Path to the directory containing the images you want censored. Every visible file in the directory ending in '.png' will be processed|
| `dest_path` | `string` | Path to the directory where you want all the new images to end up|
| `dest_name` | `string` | Name for new images. Each one will be named dest_nameXXXX.png |
| `<r,g,b> \| <blur_distance>` | `int`,`int`,`int` \| `int` | Either comma-separated RGB values or the inradius of the square used to blur |
| `secret` | `literal` | Will not save any image that doesn't detect a plate |

## Tips
- For a good blur, the inradius should be at least 30, which takes about 80 seconds to process per image
- At least a third of the license plate needs to be visible
- Works best on white license plates like the default Washington or California plate

## Censoring a video

### Install ffmpeg
```bash
# Windows:
$ winget install ffmpeg
# Mac:
$ brew install ffmpeg
# Linux:
$ sudo apt update && sudo apt install ffmpeg
```

### Put the video into a new directory and create a separate directory for outputs
```bash
$ mkdir src
$ mkdir dest
$ mv <movie> src
```

### Break video into frames
```bash
$ ffmpeg -i src/<movie> src/frame-%04d.png
```
### Censor all the images
```bash
$ python3 car_image_saver.py src dest frame- [<color> | <blur distance>]
```

### Recombine frames into a video
```bash
$ ffmpeg -framerate 30 -pattern_type glob -i 'dest/frame-*.png' -c:v libx264 -pix_fmt yuv420p output.mp4
```
