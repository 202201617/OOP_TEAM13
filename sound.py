import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # BGM 상태
        self.bgm_on = True
        
        # ===== 사운드 파일 로드 =====
        try:
            pygame.mixer.music.load("sound/bgm.mp3")
            pygame.mixer.music.set_volume(0.5)
        except:
            print("⚠ BGM 파일(bgm.mp3)을 찾을 수 없습니다.")

        # 효과음 로드
        try:
            self.jump_sound = pygame.mixer.Sound("sound/jump.wav")
            self.jump_sound.set_volume(0.7)
        except:
            print("⚠ jump.wav 파일을 찾을 수 없습니다.")

        try:
            self.hit_sound = pygame.mixer.Sound("sound/hit.wav")
            self.hit_sound.set_volume(0.7)
        except:
            print("⚠ hit.wav 파일을 찾을 수 없습니다.")

    # ===== BGM 재생 =====
    def play_bgm(self):
        if self.bgm_on:
            pygame.mixer.music.play(-1)  # 무한 반복

    # ===== BGM 정지 =====
    def stop_bgm(self):
        pygame.mixer.music.stop()

    # ===== 점프 사운드 =====
    def play_jump(self):
        try:
            self.jump_sound.play()
        except:
            pass

    # ===== 충돌 사운드 =====
    def play_hit(self):
        try:
            self.hit_sound.play()
        except:
            pass

    # ===== BGM ON/OFF 토글 =====
    def toggle_bgm(self):
        if self.bgm_on:
            pygame.mixer.music.pause()
            self.bgm_on = False
        else:
            pygame.mixer.music.unpause()
            self.bgm_on = True

    # ===== 모든 사운드 정리 =====
    def quit(self):
        pygame.mixer.stop()
        pygame.mixer.quit()
