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

        # 진행 상태
        self.current_stage = "main_building"
        self.stage_start_ticks = None
        self.state = "playing" #playing, ending_classroom, ending_retry, ending_dorm

        # 명수당 지속 시간
        self.bonus_duration = 10000

        # 학생회관에서 보너스로 진입했을 때,
        # 그 시점까지 흐른 시간을 저장하기 위한 변수
        self.student_elapsed_before_bonus = 0
        self.entered_bonus = False

        # 엔딩 처리
        from ending import Ending
        self.ending_ui = Ending(window_W, window_H)

        #아이템
        self.items = []
        self.item_speed = 7

    def spawn_stage_items(self, stage_name, player):
        self.items = create_random_items(30, self.item_speed, self.window_W, self.window_H, stage_name, player)


    def _load(self, img_path):
        self.img = pygame.image.load(img_path).convert_alpha()
        return self.img
    
    def reset(self):
        self.current_stage = "main_building"
        self.stage_start_ticks = None
        self.state = "playing"

        self.entered_bonus = False
        
        self.ending_start_ticks = None

    # 맵 진행 로직
    def update(self, player):
        if self.state != "playing":
            return
        
        # HP 0 → 도미토리 엔딩
        if player.hp <= 0:
            # 엔딩 들어가기 전에 BEST 갱신
            self.ending_ui.update_best_grade(player.grade)
            self.state = "ending_dorm"
            return

        now = pygame.time.get_ticks()

        if self.stage_start_ticks is None:
            self.stage_start_ticks = now

        elapsed = now - self.stage_start_ticks

        # 백년관 
        if self.current_stage == "main_building":
            if elapsed >= self.duration:
                self.current_stage = "library"
                self.stage_start_ticks = now

                self.spawn_stage_items("library", player)

        # ------ 도서관 ------
        elif self.current_stage == "library":
            if elapsed >= self.duration:
                self.current_stage = "student_hall"
                self.stage_start_ticks = now

                self.spawn_stage_items("student_hall", player)

        # ------ 학생회관 ------
        elif self.current_stage == "student_hall":

            # 명수당 진입 조건 (B/O/O 모두 모으면)
            if (player.have_B and player.have_O_lib and player.have_O_stu and not self.entered_bonus):

                self.student_elapsed_before_bonus = elapsed

                self.current_stage = "bonus"
                self.stage_start_ticks = now
                self.entered_bonus = True

                player.set_fly_mode()

                self.spawn_stage_items("bonus", player)

            # 학생회관 20초가 끝난 경우 → 바로 교양관 이동
            elif elapsed >= self.duration:

                self.current_stage = "liberal_arts_building"
                self.stage_start_ticks = now

                player.set_boo_mode()

                self.spawn_stage_items("liberal_arts_building", player)

        # -------------------------------------------------
        # 명수당 (보너스 맵, 10초)
        #   - 학생회관 시간은 멈춘 상태
        #   - 10초 후 다시 학생회관으로 돌아가서
        #     멈춰 있었던 시간부터 다시 진행
        # -------------------------------------------------
        elif self.current_stage == "bonus":

            if elapsed >= self.bonus_duration:
                # 부 다시 달리기 모드
                player.set_boo_mode()

                # 학생회관으로 복귀
                self.current_stage = "student_hall"

                # 학생회관 타이머를 "멈췄던 시점"으로 복구
                #   elapsed_student = now - stage_start_ticks = 저장된 값
                self.stage_start_ticks = now - self.student_elapsed_before_bonus

                # 학생회관 아이템 다시 생성 (원하면 생략 가능)
                self.spawn_stage_items("student_hall", player)

        # -------------------------------------------------
        # 교양관 → 20초 버티면 강의실 클리어 엔딩
        # -------------------------------------------------
        elif self.current_stage == "liberal_arts_building":

            if elapsed >= self.duration:

                self.ending_ui.update_best_grade(player.grade)

                if player.grade <= 2.5:
                    self.state = "ending_retry"
                else:
                    self.state = "ending_classroom"

                self.ending_start_ticks = pygame.time.get_ticks()


    def draw(self, screen, player):
        # 플레이 중이면 현재 맵만 출력
        if self.state == "playing":
            screen.blit(self.images[self.current_stage], (0, 0))
            return

        # 엔딩
        if self.state == "ending_retry":
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