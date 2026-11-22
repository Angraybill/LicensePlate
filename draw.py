from ultralytics import YOLO
import pygame
import time
import sys

pygame.init()

# cd finalProject
# python3 -m idlelib draw.py

xy = 760

screen = pygame.display.set_mode((xy, xy))
model = YOLO("./best.pt")

car = False
out = []

def update():
    screen.blit(car, (0,0))
    pygame.display.update()
    #time.sleep(2)
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(out))
    pygame.display.update()



def do_the_thing(car_path):
    results = model.predict(car_path)

    #global out
    for r in results:
        for j in r.boxes[0].xywhn:
            for p in j:
                out.append(int(xy * float(str(p).split("(")[1][:-1])))
                
    out[0] -= out[2] // 2
    out[1] -= out[3] // 2

  #  global car
    car = pygame.image.load(car_path).convert()
    car = pygame.transform.scale(car, (xy,xy))

    keep = True
    update()
    while keep:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep = False

    pygame.quit()    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].endswith(".png"):
        do_the_thing(sys.argv[1])
    else:
        print("No image passed")


