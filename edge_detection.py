import pygame
from pygame.locals import *
from PIL import Image
import pygame.camera
import sys

pygame.camera.init()
webcam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
webcam.start()


pygame.init()
screen = pygame.display.set_mode((640,480))
#tgt = pygame.image.load("target2 copy.png")

THRESHOLD = 10

while 1:
  for event in pygame.event.get():
    if event.type == QUIT:
      running = sys.exit()   #Exiting the while loop
  placestoblit = []
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
 
  edge_locations = [] # Locations of edges
  numedgepixels = 0 # Number of edge pixels
  # ^^ To find middle of dot
  img = webcam.get_image()
  pil_img_str = pygame.image.tostring(img, "RGBA",False)
  img = Image.fromstring("RGBA",(640,480),pil_img_str)
  pixels = img.load()
  size = img.size
 # print size[0]
 # print size[1]
  edited = Image.new("RGB", (640, 480))
  edited_pix = edited.load()

  for i in range(1, img.size[0]-1):    # for every pixel:
    for j in range(1, img.size[1]-1):
      color = pixels[i, j]
      av = (color[0] + color[1] + color[2]) / 3
      pixels[i, j] = (av,av,av)
      lowest = 255
      highest = 0
      edited_pix[i, j] = pixels[i, j]

      if pixels[i, j][1] > 0:
        for x in range(-1,1):
          for y in range(-1,1):
            color = pixels[i + x, j + y][0]
            if color > highest:
              highest = color
            if color < lowest:
              lowest = color
        if abs(highest-lowest) > THRESHOLD and pixels[i, j][1] > 0:
          edge_locations.append((i, j))
          numedgepixels += 1
          edited_pix[i, j] = (120,255,255)
          placestoblit.append((i,j))
          #pixels[i, j] = (255,255,255)

      

  imblit = pygame.image.frombuffer(edited.tostring(), (640,480), "RGB")
  screen.blit(imblit, (0,0))
  sum_x = sum_y = 0

#  screen.blit(tgt, (av_x, av_y))

    
  pygame.display.flip()
 
