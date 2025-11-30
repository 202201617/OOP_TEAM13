import pygame
from player import *
from object import create_random_items

class Map:
    def __init__(self, window_W, window_H, font_path="DNFBitBitTTF.ttf", map_duration_ms=20000):
        self.window_W = window_W
        self.window_H = window_H
        self.duration = map_duration_ms

        self.font = pygame.font.Font(font_path, 40)
        self.font_big = pygame.font.Font(font_path, 80)

        self.images = {
            "main_building": self._load("image/main_building.png"),
            "library": self._load("image/library.png"),
            "student_hall": self._load("image/student_hall.png"),
            "bonus": self._load("image/bonus.png"),
            "liberal_arts_building": self._load("image/liberal_arts_building.png"),
            "classroom": self._load("image/classroom.png"),
            "retry": self._load("image/retry.png"),
            "dormitory": self._load("image/dormitory.png")
        }

        self.current_stage = "main_building"
        self.stage_start_ticks = None
        self.state = "playing"  # 실제 표시 상태
        self.pending_ending_state = None  # 페이드 후 적용될 엔딩 상태

        self.bonus_duration = 10000
        self.student_elapsed_before_bonus = 0
        self.entered_bonus = False

        from ending import Ending
        self.ending_ui = Ending(window_W, window_H)

        self.items = []
        self.item_speed = 7

        # 🔥 페이드아웃 변수
        self.fade_alpha = 0
        self.is_fading = False

    def spawn_stage_items(self, stage_name, player):
        self.items = create_random_items(30, self.item_speed, self.window_W, self.window_H, stage_name, player)

    def _load(self, img_path):
        return pygame.image.load(img_path).convert_alpha()

    def reset(self):
        self.current_stage = "main_building"
        self.stage_start_ticks = None
        self.state = "playing"
        self.pending_ending_state = None
        self.entered_bonus = False
        self.fade_alpha = 0
        self.is_fading = False

    # ===================== UPDATE =====================
    def update(self, player):
        if self.state != "playing":
            return

        # HP 0 → 도미토리 엔딩
        if player.hp <= 0:
            self.ending_ui.update_best_grade(player.grade)
            self.pending_ending_state = "ending_dorm"   # 실제 엔딩은 페이드 후 적용
            self.is_fading = True
            self.fade_alpha = 0
            return

        now = pygame.time.get_ticks()
        if self.stage_start_ticks is None:
            self.stage_start_ticks = now

        elapsed = now - self.stage_start_ticks

        # ---------------- 백년관 ----------------
        if self.current_stage == "main_building":
            if elapsed >= self.duration:
                self.current_stage = "library"
                self.stage_start_ticks = now
                self.spawn_stage_items("library", player)

        # ---------------- 도서관 ----------------
        elif self.current_stage == "library":
            if elapsed >= self.duration:
                self.current_stage = "student_hall"
                self.stage_start_ticks = now
                self.spawn_stage_items("student_hall", player)

        # ---------------- 학생회관 ----------------
        elif self.current_stage == "student_hall":
            if player.have_B and player.have_O_lib and player.have_O_stu and not self.entered_bonus:

                self.student_elapsed_before_bonus = elapsed
                self.current_stage = "bonus"
                self.stage_start_ticks = now
                self.entered_bonus = True

                player.set_fly_mode()
                self.spawn_stage_items("bonus", player)

            elif elapsed >= self.duration:

                self.ending_ui.update_best_grade(player.grade)

                if player.grade <= 2.50:
                    self.pending_ending_state = "ending_retry"
                    self.is_fading = True
                    self.fade_alpha = 0
                else:
                    self.current_stage = "liberal_arts_building"
                    self.stage_start_ticks = now
                    player.set_boo_mode()
                    self.spawn_stage_items("liberal_arts_building", player)

        # ---------------- 명수당 ----------------
        elif self.current_stage == "bonus":
            if elapsed >= self.bonus_duration:
                player.set_boo_mode()
                self.current_stage = "student_hall"
                self.stage_start_ticks = pygame.time.get_ticks() - self.student_elapsed_before_bonus
                self.spawn_stage_items("student_hall", player)

        # ---------------- 교양관 ----------------
        elif self.current_stage == "liberal_arts_building":
            if elapsed >= self.duration:
                self.ending_ui.update_best_grade(player.grade)
                self.pending_ending_state = "ending_classroom"
                self.is_fading = True
                self.fade_alpha = 0

    # ===================== DRAW =====================
    def draw(self, screen, player):

        # 페이드 중에는 무조건 '현재 게임 화면' 유지
        if self.is_fading:
            # 게임 화면 그리기
            screen.blit(self.images[self.current_stage], (0, 0))

            # 페이드 레이어
            fade_surface = pygame.Surface((self.window_W, self.window_H))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0))

            # 알파 증가
            if self.fade_alpha < 255:
                self.fade_alpha += 8
            else:
                self.is_fading = False
                # 이제 실제 엔딩 상태 적용
                if self.pending_ending_state:
                    self.state = self.pending_ending_state
                    self.pending_ending_state = None

            return  # 엔딩 화면 출력 금지

        # ====== 페이드가 끝난 후 엔딩 화면 출력 ======

        if self.state == "playing":
            screen.blit(self.images[self.current_stage], (0, 0))

        elif self.state == "ending_retry":
            self.ending_ui.ending_retry(screen, player.grade)

        elif self.state == "ending_dorm":
            self.ending_ui.ending_dorm(screen, player.grade)

        elif self.state == "ending_classroom":
            self.ending_ui.ending_classroom(screen, player.grade)

    @property
    def is_playing(self):
        return self.state == "playing"

    @property
    def is_finished(self):
        return self.state != "playing"
