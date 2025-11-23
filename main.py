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

FONT = pygame.font.Font("DNFBitBitTTF.ttf", 50)
FONT_TITLE = pygame.font.Font("DNFBitBitTTF.ttf", 80)

# ------------------------
# 배경 이미지 로드
# ------------------------
Main_BUildging = pygame.image.load("OOP_TEAM13/image/Main_Building.png").convert()
Main_BUildging = pygame.transform.scale(Main_BUildging, (window_W, window_H))  # 창 크기에 맞게 늘리기/줄이기


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

    # 배경 이미지 그리기
    screen.blit(Main_BUildging, (0, 0))

    # 텍스트 표시
    txt = FONT_TITLE.render("학교 가BOO자고!", True, BLACK)
    screen.blit(txt, (50, 50))


    # 화면 업데이트
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
