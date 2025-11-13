import pygame
import sys
from pygame.locals import *

window_W = 1200
window_H = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((window_W, window_H))

main_building = pygame.image.load("C:\\Users\\user\\Desktop\\OOP_FinalProject\\image\\Main_Building.png")
main_building = pygame.transform.scale(main_building, (1200, 600))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(main_building, (0, 0)) #배경 그리기
    pygame.display.update() #게임 화면을 계속 그리기
    clock.tick(FPS)

pygame.quit()
    