from math import cos, sin, tan
import pygame as pg
import numpy as np
from sys import exit

WIDTH = 640
HEIGHT = 480


screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

triangles = []
rotation_y = 0
rotation_x = 0

# Front
triangles.append(np.array([[0,0,0], [0,1,0], [1,1,0]]))
triangles.append(np.array([[0,0,0], [1,1,0], [1,0,0]]))
# #Back
triangles.append(np.array([[0,0,1], [1,0,1], [1,1,1]]))
triangles.append(np.array([[0,0,1], [0,1,1], [1,1,1]]))
# # Up
triangles.append(np.array([[0,0,0], [1,0,0], [1,0,1]]))
triangles.append(np.array([[0,0,0], [0,0,1], [1,0,1]]))
# # Down
triangles.append(np.array([[0,1,0], [0,1,1], [1,1,0]]))
triangles.append(np.array([[1,1,0], [0,1,1], [1,1,1]]))
# # Right
triangles.append(np.array([[1,0,0], [1,0,1], [1,1,0]]))
triangles.append(np.array([[1,1,0], [1,1,1], [1,0,1]]))
# # Left
triangles.append(np.array([[0,0,0], [0,0,1], [0,1,0]]))
triangles.append(np.array([[0,1,0], [0,1,1], [0,0,1]]))

for t in triangles:
  t[:,2] += 5

def rotation_matrix_y(angle):
    return np.array([[cos(angle), 0, sin(angle), 0], 
                    [0,1,0, 0],
                    [-sin(angle), 0, cos(angle), 0],
                    [0,0,0,1]])

def rotation_matrix_x(angle):
  return np.array([
      [1,0,0,0],
      [0, cos(angle), -sin(angle), 0],
      [0, sin(angle), cos(angle), 0],
      [0,0,0,1]
    ])

def translation_matrix(cx, cy, cz):
  return np.array([
    [1,0,0,cx],
    [0,1,0,cy],
    [0,0,1,cz],
    [0,0,0,1]
  ])

def perspective_projection_matrix(h, w, angle, zfar, znear):
  a = h/w
  f = 1/tan(angle/2)
  q = -(zfar+znear) / (zfar - znear)
  q2 = 2*zfar * znear / (zfar - znear)
  return np.array([[a*f,0,0,0],
                    [0,f,0,0],
                    [0,0,q,q2],
                    [0,0,1,0]])

def draw_line(screen, start_pos, end_pos):
  pg.draw.line(screen, (0,0,0), start_pos, end_pos)

while True:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()

  screen.fill((255,255,255))

  for triangle in triangles:
    projected_vertices = []
    for vertice in triangle:
      new_vert = np.append(vertice, 1)
      print(new_vert)
      new_vert = translation_matrix(-0.5,-0.5,-5.5) @ new_vert
      new_vert = rotation_matrix_y(rotation_y) @ new_vert
      new_vert = rotation_matrix_x(rotation_x) @ new_vert
      new_vert = translation_matrix(0.5,0.5,5.5) @ new_vert
      projected_vert = perspective_projection_matrix(HEIGHT, WIDTH, np.pi/4, 1000, 0.01) @ new_vert
      projected_vert = np.squeeze(projected_vert)
      #print(projected_vert)
      if projected_vert[3] != 0:
        projected_vert = projected_vert / projected_vert[3]
      #print(projected_vert)
      
      projected_vert[0] += 1
      projected_vert[1] += 1
      projected_vert[0] *= 0.65 * WIDTH
      projected_vert[1] *= 0.65 * HEIGHT

      """projected_vert[0] += WIDTH / 2 / 2
      projected_vert[1] += HEIGHT / 2 / 2"""
      projected_vertices.append(projected_vert)
    pg.draw.circle(screen, (255,0,0), (projected_vertices[0][0], projected_vertices[0][1]), 3)
    pg.draw.circle(screen, (255,0,0), (projected_vertices[1][0], projected_vertices[1][1]), 3)
    pg.draw.circle(screen, (255,0,0), (projected_vertices[2][0], projected_vertices[2][1]), 3)
    draw_line(screen, (projected_vertices[0][0], projected_vertices[0][1]), (projected_vertices[1][0], projected_vertices[1][1]))
    draw_line(screen, (projected_vertices[1][0], projected_vertices[1][1]), (projected_vertices[2][0], projected_vertices[2][1]))
    draw_line(screen, (projected_vertices[2][0], projected_vertices[2][1]), (projected_vertices[0][0], projected_vertices[0][1]))
    projected_vertices = []


  clock.tick(60)
  pg.display.set_caption(str(clock.get_fps()))
  
  rotation_x += 0.02
  rotation_x %= 2*np.pi
  rotation_y += 0.01
  rotation_y %= 2*np.pi
  pg.display.flip()

  