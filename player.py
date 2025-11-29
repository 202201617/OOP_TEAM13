import pygame

class Player:
    def __init__(self, x, y, screen_width, ground_level):
        # 이미지 크기
        self.width = 100
        self.height = 144

        self.start_x = x
        self.start_y = y
        
        self.reset()

        # 기본 이미지 로드
        self.image_boo = pygame.image.load("image/boo.png").convert_alpha()
        self.image_boo = pygame.transform.scale(self.image_boo, (self.width, self.height))

        # 명수당(보너스) 전용 — 날고 있는 이미지
        self.image_fly = pygame.image.load("image/fly_boo.png").convert_alpha()

        # 처음에는 달리기 이미지 적용
        self.image = self.image_boo

        # 물리 요소
        self.gravity = 1
        self.jump_power = -22
        self.on_ground = True

        # 이동 가능한 범위 (화면 절반까지만)
        self.left_limit = 20
        self.right_limit = screen_width // 2 - self.width - 20

        # 바닥 Y좌표
        self.ground_y = ground_level

    def reset(self):
        self.hp = 3
        self.grade = 0.00

        self.have_B = False
        self.have_O_lib = False
        self.have_O_stu = False

        self.x = self.start_x
        self.y = self.start_y

        self.vx = 0
        self.vy = 0
        self.on_ground = True

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # 키 입력 처리
    def handle_input(self, keys):
        self.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 8

    # 점프 처리
    def jump(self):
        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

    # 물리 업데이트
    def update(self):
        # 좌우 이동
        self.rect.x += self.vx

        # 화면 절반까지만 이동 제한
        if self.rect.x < self.left_limit:
            self.rect.x = self.left_limit

        if self.rect.x > self.right_limit:
            self.rect.x = self.right_limit

        # 중력 적용
        self.vy += self.gravity
        self.rect.y += self.vy

        # 바닥 충돌 처리
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vy = 0
            self.on_ground = True

        self.x = self.rect.x
        self.y = self.rect.y

    # 명수당 입장 → 날기 이미지 적용
    def set_fly_mode(self):
        self.image = self.image_fly

    # 명수당 종료 → 다시 기본 이미지
    def set_boo_mode(self):
        self.image = self.image_boo

    # 부 그리기
    def draw(self, screen):
        screen.blit(self.image, self.rect)
