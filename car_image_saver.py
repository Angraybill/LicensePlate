from PIL import Image
import numpy as np
from ultralytics import YOLO
import os, sys, stat

model =  YOLO("./best.pt")
def blur(image_array, x1, y1, radius):
    bounds = (len(image_array), len(image_array[0]))
    color_tots = [0,0,0]
    div = 0
    for v in range(-radius, radius + 1):
        if y1 + v > bounds[0] or y1 + v < 0:
            continue
        for h in range(-radius, radius + 1):
            if x1 + h < 0 or x1 + h > bounds[1]:
                continue
            for index in range(3):
                color_tots[index] += image_array[y1 + v][x1 + h][index]
            div += 1
    ret = (min(color_tots[0] // div, 255), min(color_tots[1] // div, 255), min(color_tots[2] // div, 255))
    return ret

def censor(src, dest, color):
    img_path = src
    image = Image.open(img_path).convert("RGB")
    image_array = np.array(image).tolist()

    x, y = len(image_array[0]), len(image_array)     
    results = model.predict(img_path)

    out = []
    found = True
    for r in results:
        if len(r.boxes) == 0:
            found = False
            break
        for j in r.boxes[0].xywhn:
            for p in j:
                out.append(float(str(p).split("(")[1][:-1]))

    if found:
        out = [int(out[0] * x), int(out[1] * y), int(out[2] * x), int(out[3] * y)]            
        out[0] -= out[2] // 2
        out[1] -= out[3] // 2
        lrtb = [out[0], out[0] + out[2], out[1], out[1] + out[3]]

        for x1 in range(lrtb[0], lrtb[1]):
            for y1 in range(lrtb[2], lrtb[3]):
                image_array[y1][x1] = blur(image_array, x1, y1, color) if isinstance(color, int) else color

    image_array = np.array(image_array, dtype=np.uint8)
    img_new = Image.fromarray(image_array)
    img_new.save(dest + (".png" if not dest.endswith(".png") else ""))

if __name__ == "__main__":
    # Determine if a directory has been passed as a parameter
    num_args = len(sys.argv)
    info = os.stat(sys.argv[1])
    is_dir = stat.S_ISDIR(info.st_mode)

    # Prepare color parameter for both an RGB color and a blur
    color = sys.argv[-1]
    if "," in color:
        color = color.split(",")
        color = (int(color[0].strip()), int(color[1].strip()), int(color[2].strip()))
    else:
        color = int(color)
    print(color)

    if not is_dir:
        # Single image
        if sys.argv[1].endswith(".png"):
            censor(sys.argv[1], sys.argv[2], color)
    else:
        # Directory
        images = os.listdir(sys.argv[1])
        images.sort()
        dest_path = sys.argv[2]
        dest_name = sys.argv[3]

        # fix names
        src_name = sys.argv[1]
        if src_name[-1] != "/":
            src_name += "/"
        if dest_name.endswith(".png"):
            dest_name = dest_name[:-4]
        if dest_path[-1] == "/":
            if dest_name[0] == "/":
                dest_name = dest_name[1:]
        else:
            if dest_name[0] != "/":
                dest_path += "/"

        # censor all images in the directory
        for i in range(len(images)):
            if images[i][0] == "." or not images[i].endswith(".png"):
                continue
            censor(src_name + images[i], dest_path + dest_name + ("0" * (4 - len(str(i)))) + str(i) + ".png", color)
