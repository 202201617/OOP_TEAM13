import pygame
import sys
from pygame.locals import *
from collide import *
from player import *
from object import *
from map import *
from ending import *
from sound import SoundManager

'''
추가해야 하는 것
1. 부 체력 이미지
2. B, 0, 0 오른쪽 위에 등록
1. 사운드
2. 부 달리는 이미지
3. 부 날고 있는 이미지
4. 일시정지
5. 최고 학점
6. bgm on&off
'''

# 기본 설정
window_W = 1200
window_H = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((window_W, window_H))
pygame.display.set_caption("학교 가BOO자고!")
clock = pygame.time.Clock()

# 사운드 초기화 및 로드
sound = SoundManager()
sound.play_bgm()

FONT = pygame.font.Font("DNFBitBitTTF.ttf", 30)
FONT_TITLE = pygame.font.Font("DNFBitBitTTF.ttf", 100)

# 바닥 높이
ground = window_H - 140 -50

#player 객체 생성
player = Player(100, ground, window_W, ground)

# 배경 이미지 로드
map = Map(window_W, window_H)
menu = pygame.image.load("image/menu.png").convert_alpha()
explain = pygame.image.load("image/explain.png").convert_alpha()

map.spawn_stage_items("main_building", player)

# 시작 버튼
btn_explain = pygame.Rect(280, 460, 150, 60)
btn_start = pygame.Rect(770, 460, 150, 60)
btn_explain_to_start = pygame.Rect(900, 500, 180, 50)

def draw_button(rect, text):
    pygame.draw.rect(screen, (255, 255, 255), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 3)
    txt = FONT.render(text, True, (0, 0, 0))
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

# 현재 화면 상태
game_state = "menu"

# 메인 루프
running = True
while running:
    # ================= 이벤트 처리 =================
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # 키보드 입력
        elif event.type == KEYDOWN:
            if game_state == "playing" and map.is_playing:
                if event.key == pygame.K_SPACE:
                    player.jump()
                    sound.play_jump()

         # 마우스 클릭 입력 (버튼 클릭)
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos

            # 메인 화면
            if game_state == "menu":

                if btn_explain.collidepoint(mx, my):
                    game_state = "explain"

                elif btn_start.collidepoint(mx, my):
                    game_state = "playing"
                    map.reset()

            # 게임설명 화면
            elif game_state == "explain":
                if btn_explain_to_start.collidepoint(mx, my):
                    game_state = "playing"
                    map.reset()

             # 엔딩 화면
            elif game_state == "playing" and not map.is_playing:
                action = map.ending_ui.check_click(event.pos)

                if action == "quit":
                    running = False
                
                elif action == "restart":
                    player.reset()
                    player.set_boo_mode()
                    map.reset()
                    
                    # 아이템 새로 생성
                    map.spawn_stage_items("main_building", player)

                    # 플레이 상태로 전환
                    game_state = "playing"

      # 화면 그리기 
    if game_state == "menu":
        screen.blit(menu, (0, 0))
        draw_button(btn_explain, "게임설명")
        draw_button(btn_start, "게임시작")

    elif game_state == "explain":
        screen.blit(explain, (0, 0))
        draw_button(btn_explain_to_start, "게임시작")

    elif game_state == "playing":

        # 1) 맵 업데이트 (GPA/HP 조건 판단 포함)
        map.update(player)

        if not map.is_playing:
            sound.stop_bgm()

        # 2) 맵 그리고 엔딩 상태면 알아서 그려줌
        map.draw(screen, player)

        # 3) 진행 중인 경우에만 플레이어 동작 가능
        if map.is_playing:
            keys = pygame.key.get_pressed()
            player.handle_input(keys)
            player.update()
            player.draw(screen)

            # 4) (참고) 학점 & HP를 화면에 띄우려면 아래 추가 가능
            hp_text = FONT.render(f"HP: {player.hp}", True, (0,0,0))
            grade_text = FONT.render(f"학점: {player.grade:.2f}", True, (0,0,0))
            screen.blit(hp_text, (20, 20))
            screen.blit(grade_text, (20, 60))

            # 5) 아이템 그리기
            for item in map.items:
                item.update(map.item_speed)
                item.draw(screen)

            # 6) 아이템/장애물 충돌 확인
            check_collision(player, map.items, sound)


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()  
