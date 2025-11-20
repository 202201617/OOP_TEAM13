import pygame
import sys
from pygame.locals import *

# ----------------------------------
# 기본 설정
# ----------------------------------

window_W = 1200
window_H = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((window_W, window_H))
pygame.display.set_caption("학교 가BOO자고!")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 50)
FONT_BIG = pygame.font.Font(None, 80)

#----------------------------------------
# 색상 정의
# ---------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)


# -------------------------------------------------
# 메인 루프
# -------------------------------------------------

running = True
while running:

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # 화면 채우기
    screen.fill(WHITE)

    # 텍스트 표시 예시
    txt = FONT.render("Let’s BOO to School!", True, BLACK)
    screen.blit(txt, (50, 50))

    # 화면 업데이트
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()