import pygame, object, sound

window_W = 1200
window_H = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((window_W, window_H))

main_building = pygame.image.load("C:\Users\user\Desktop\OOP_FinalProject\image\Main_Building.png")
main_building = pygame.transform.scale(main_building, (1200, 600))