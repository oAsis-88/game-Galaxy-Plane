import pygame
import sys
from win32api import GetSystemMetrics

pygame.init()
# 33 x 26
# 33 * (width + margin)
# 26 * (width + margin)
width = height = 40  # размер клетки
margin = 10  # отступы между клеток
W = 33
H = 26
W_lenght = W * (width * margin)
H_lenght = H * (height * margin)
Screen_Width = (GetSystemMetrics(0) - 200) // W - W * margin
Screen_Height = (GetSystemMetrics(1) - 100) // H - H * margin
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIME = (0, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
GRAY = (112, 128, 144)
BROWN = (139, 69, 19)
SIZE = (510, 510)
screen = pygame.display.set_mode(SIZE)  # окно программы
screen.fill(WHITE)
pygame.display.set_caption("Game")
color = WHITE
mas = [[0] * 10 for i in range(10)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            print(f'x={x_mouse} y={y_mouse}')
            column = x_mouse // (margin + width)
            row = y_mouse // (margin + height)
            mas[row][column] ^= 1

    for col in range(10):
        for row in range(10):
            if mas[row][col] == 1:
                color = RED
            else:
                color = WHITE
            x = col * width + (col + 1) * margin
            y = row * height + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, width, height))
    # pygame.display.flip()
    pygame.display.update()
