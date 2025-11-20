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
screen = pygame.display.set_mode((window_W, window_H)
pygame.display.set_caption("학교 가BOO자고!")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 50)
FONT_BIG = pygame.font.Font(None, 80)

# ------------------------
# 이미지 로드
# ------------------------
MAIN_BG = pygame.image.load(
    "C:\\Users\\user\\Desktop\\OOP_FinalProject\\image\\Main_Building.png"
).convert()
MAIN_BG = pygame.transform.scale(MAIN_BG, (window_W, window_H))

bonus_bg = pygame.image.load(
    "C:\Users\BCHC\OneDrive\바탕 화면\OOP_FinalProject\OOP_TEAM13\image\Bonus_Stage.pngg"
).convert()
bonus_bg = pygame.transform.scale(bonus_bg, (window_W, window_H))

# 부 캐릭터 달리기 애니메이션 3장
boo_images = [
    pygame.image.load(",,,").convert_alpha(),
    pygame.image.load(",,,").convert_alpha(),
    pygame.image.load(",,,").convert_alpha()
]
boo_images = [pygame.transform.scale(img, (90, 90)) for img in boo_images]

# ------------------------
# 버튼 클래스
# ------------------------
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        text_surf = FONT.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def clicked(self, event):
        return event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ------------------------
# 부(플레이어) 클래스
# ------------------------
class Player:
    def __init__(self):
        # 크기 조절 (필요하면 수정)
        self.images = boo_images  # 위에서 로드한 이미지 리스트 사용
        self.index = 0
        self.image = self.images[0]

        self.x = 150
        self.y = 400
        self.vy = 0
        self.is_jumping = False
        self.ground = 400 # 땅높이

    def jump(self):
        if not self.is_jumping:
            self.vy = -18
            self.is_jumping = True

    def update(self):
        # 중력 적용
        self.vy += 1
        self.y += self.vy

        if self.y >= self.ground:
            self.y = self.ground
            self.vy = 0
            self.is_jumping = False

        # 달리기 애니메이션
        if not self.is_jumping:
            self.index += 0.15 #수정가능
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[int(self.index)]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    @property
    def rect(self):
        r = self.image.get_rect()
        r.topleft = (self.x, self.y)
        return r
    
# =======================================
# 시작 화면
# =======================================
def start_screen():
    start_btn = Button("게임 시작", window_W // 2 - 130, 440, 260, 80,
                       (0, 120, 255), (0, 170, 255))

    info_btn = Button("게임 설명", window_W // 2 - 130, 350, 260, 70,
                      (120, 120, 120), (160, 160, 160))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "QUIT"

            # 게임 시작 버튼
            if start_btn.clicked(event):
                return "START"

            # 게임 설명 버튼
            if info_btn.clicked(event):
                return "INFO"

        # 배경 표시
        screen.blit(MAIN_BG, (0, 0))
        #overlay = pygame.Surface((window_W, window_H), pygame.SRCALPHA)
        #overlay.fill((0, 0, 0, 120))
        #screen.blit(overlay, (0, 0))

        # 제목
        title = FONT_BIG.render("학교 가BOO자고!", True, (255, 255, 255))
        screen.blit(title, (window_W // 2 - 250, 120))

        start_btn.draw(screen)
        info_btn.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


# =======================================
# 엔딩 화면 (다시 시작)
# =======================================
def end_screen(score):
    restart_btn = Button("다시 시작", window_W// 2 - 130, 430, 260, 80,
                         (200, 50, 50), (255, 80, 80))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "QUIT"
            if restart_btn.clicked(event):
                return "RESTART"

        screen.fill((0, 0, 0))
        msg = FONT.render(f"Score : {score}", True, (255, 255, 255))
        msg2 = FONT.render("게임 종료!", True, (255, 255, 255))

        screen.blit(msg2, (window_W // 2 - 100, 220))
        screen.blit(msg, (window_W// 2 - 90, 270))

        restart_btn.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


# ======================================
# 보너스 스테이지
#  - 책 아이템만 등장
#  - 2~5개 랜덤
#  - 책 1개당 점수 +0.5
#  - 노란색이 아니라 보너스 전용 이미지(bonus_bg) 사용
# ======================================
def bonus_stage(player, score):
    target_books = random.randint(2, 5)   # 2~5개 책 등장
    books_collected = 0
    books = []
    frame = 0
    max_time = FPS * 12  # 최대 12초 동안 진행 @@@수정 필요

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                player.jump()

        # 배경: 보너스 스테이지 전용 이미지
        screen.blit(bonus_bg, (0, 0))

        # 플레이어 업데이트/그리기
        player.update()
        player.draw(screen)

#여기부터 이해하며 수정필요

        # 책 생성 – 아직 목표 개수보다 적고, 랜덤 확률로 생성
        if len(books) < target_books and random.random() < 0.04:
            books.append(Item("book"))

        # 책 이동/충돌
        for b in books[:]:
            b.update(8)
            b.draw(screen)

            if b.rect.colliderect(player.rect):
                books_collected += 1
                score += 0.5     # 책 하나당 점수 +0.5
                books.remove(b)
            elif b.rect.right < 0:
                books.remove(b)

        info = FONT.render(
            f"BONUS! 책 {books_collected}/{target_books}개  |  Score: {score:.1f}",
            True, (255, 255, 255)
        )
        screen.blit(info, (window_W // 2 - 300, 40))

        pygame.display.update()
        clock.tick(FPS)
        frame += 1

        # 책 다 먹었거나 시간 초과 시 보너스 스테이지 종료
        if books_collected >= target_books or frame > max_time:
            return score


# =======================================
# 실제 게임 플레이 (장애물 없음) @@@ 수정해야함
# =======================================
def play_game():
    player = Player()
    score = 0
    bonus_used = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "QUIT", score
            if event.type == KEYDOWN and event.key == K_SPACE:
                player.jump()

        # 배경
        screen.blit(MAIN_BG, (0, 0))

        # 플레이어 업데이트
        player.update()
        player.draw(screen)

        # 점수 표시
        score += 1
        text = FONT.render(f"Score : {score}", True, (0, 0, 0))
        screen.blit(text, (20, 20))

        # 일정 점수 이후 보너스 진입
        if score >= 200 and not bonus_used:
            bonus_used = True
            score += bonus_stage(player)

        pygame.display.update()
        clock.tick(FPS)

        # 게임 종료 조건(지금은 임시: 점수 600)
        if score > 600:
            running = False

    return "END", score


# =======================================
# 게임 루프
# =======================================
def main():
    while True:
        action = start_screen()
        if action == "QUIT":
            break

        result, score = play_game()
        if result == "QUIT":
            break

        end_action = end_screen(score)
        if end_action == "QUIT":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()