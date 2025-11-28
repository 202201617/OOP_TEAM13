import pygame
from map import *
from player import *

'''
엔딩 멘트 변경
엔딩 페이드 추가
'''

class Ending:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font_title = pygame.font.Font("DNFBitBitTTF.ttf", 80)
        self.font_text = pygame.font.Font("DNFBitBitTTF.ttf", 40)
        self.font_btn = pygame.font.Font("DNFBitBitTTF.ttf", 20)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.image_dorm = pygame.image.load("image/dormitory.png")
        self.image_classroom = pygame.image.load("image/classroom.png")
        self.image_retry = pygame.image.load("image/retry.png")

        btn_w, btn_h = 200, 60
        center_x = width // 2

        self.rect_restart = pygame.Rect(center_x-btn_w-20, height-150, btn_w, btn_h)
        self.rect_quit = pygame.Rect(center_x+20, height-150, btn_w, btn_h)

        # 최고 학점(Best Score)
        self.best_grade = 0.0

    # ---------------------------------------
    # 엔딩 진입할 때 최고 학점 갱신
    # ---------------------------------------
    def update_best_grade(self, grade):
        if grade > self.best_grade:
            self.best_grade = grade

    # ---------------------------------------
    # 최종 학점 + 최고 학점 표시
    # ---------------------------------------
    def draw_final_grade(self, screen, grade):
        # 최종 학점
        txt = self.font_text.render(f"최종 학점: {grade:.2f}", True, self.WHITE)
        bg_rect = txt.get_rect(center=(self.width//2, self.height//2 + 50))
        pygame.draw.rect(screen, (0, 0, 0), bg_rect.inflate(20, 10))
        screen.blit(txt, bg_rect)

        # 🔹 BEST 학점
        best = self.font_text.render(f"최고 학점: {self.best_grade:.2f}", True, self.WHITE)
        best_rect = best.get_rect(center=(self.width//2, self.height//2 + 110))
        pygame.draw.rect(screen, (0, 0, 0), best_rect.inflate(20, 10))
        screen.blit(best, best_rect)

    # ---------------------------------------
    # 버튼
    # ---------------------------------------
    def draw_buttons(self, screen):
        pygame.draw.rect(screen, self.WHITE, self.rect_restart)
        txt_restart = self.font_btn.render("다시 시작하기", True, self.BLACK)
        screen.blit(txt_restart, (self.rect_restart.centerx - txt_restart.get_width()//2, 
                                  self.rect_restart.centery - txt_restart.get_height()//2))
        
        pygame.draw.rect(screen, self.WHITE, self.rect_quit)
        txt_quit = self.font_btn.render("종료 하기", True, self.BLACK)
        screen.blit(txt_quit, (self.rect_quit.centerx - txt_quit.get_width()//2, 
                               self.rect_quit.centery - txt_quit.get_height()//2))

    def check_click(self, pos):
        if self.rect_restart.collidepoint(pos):
            return "restart"
        elif self.rect_quit.collidepoint(pos):
            return "quit"
        return None

    def ending_dorm(self, screen, grade):
        screen.blit(self.image_dorm, (0, 0))
        
        title = self.font_title.render("Zzz...", True, self.WHITE)
        sub = self.font_title.render("체력이 다해 잠들었습니다.", True, self.WHITE)
        
        screen.blit(title, (self.width//2 - title.get_width()//2, 150))
        screen.blit(sub, (self.width//2 - sub.get_width()//2, 220))

        self.draw_final_grade(screen, grade)
        self.draw_buttons(screen)

    def ending_retry(self, screen, grade):
        screen.blit(self.image_retry, (0, 0))
        
        title = self.font_title.render("재수강 확정...", True, self.WHITE)
        sub = self.font_title.render("BOO는 재수강을 해야합니다.", True, self.WHITE)

        screen.blit(title, (self.width//2 - title.get_width()//2, 150))
        screen.blit(sub, (self.width//2 - sub.get_width()//2, 220))

        self.draw_final_grade(screen, grade)
        self.draw_buttons(screen)

    def ending_classroom(self, screen, grade):
        screen.blit(self.image_classroom, (0, 0))
        
        msg = f"축하합니다. {grade:.2f}학점을 받았습니다."
        title = self.font_title.render(msg, True, self.BLACK)

        screen.blit(title, (self.width//2 - title.get_width()//2, 200))
        self.draw_final_grade(screen, grade)
        self.draw_buttons(screen)