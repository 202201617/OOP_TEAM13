import pygame
import random

class Object:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path).convert_alpha()
        self.active = True

    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self, speed):
        if self.active:
            self.x -= speed
    
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

# 아이템
class Book(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/book.png")

class Energy(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/energy.png")

class B(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/b.png")
        self.name = "B"

class O_lib(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/o_library.png")
        self.name = "O_lib"

class O_stu(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/o_student_hall.png")
        self.name = "O_stu"

class BonusBook(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/book.png")

# 장애물
class Soju(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/soju.png")

class Nut(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/nut.png")

class CoffeeCup(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/coffee.png")

COMMON_ITEMS = [Book, Energy, Soju, Nut, CoffeeCup]
COMMON_WEIGHTS = [45, 10, 25, 10, 10]


def create_random_items(seconds, speed, screen_width, screen_height, stage_name, player):
    items = []

    total_distance = (seconds + 2) * 20 * speed
    current_x = screen_width + 100

    current_pool = COMMON_ITEMS[:]
    current_weights = COMMON_WEIGHTS[:] # 오타 수정: curernt -> current
    
    bonus_item_class = None
    
    # 1. 스테이지별 보너스 아이템 설정
    if stage_name == "main_building":
        bonus_item_class = B
        current_pool.append(bonus_item_class)
        current_weights.append(5) 
        
    elif stage_name == "library":
        bonus_item_class = O_lib
        current_pool.append(bonus_item_class)
        current_weights.append(5)

    elif stage_name == "student_hall":
        bonus_item_class = O_stu
        current_pool.append(bonus_item_class)
        current_weights.append(5)

    elif stage_name == "bonus":
        current_pool = [BonusBook, Energy]
        current_weights = [80, 20]

    # 이번 생성 루프에서 보너스 아이템이 나왔는지 체크
    is_spawned = False

    while current_x < total_distance:
        item_class = random.choices(current_pool, weights=current_weights, k=1)[0]

        # 이미 플레이어가 가지고 있거나, 이번 루프에서 이미 생성됐다면 -> 일반 책으로 변경
        if item_class == bonus_item_class:
            if stage_name == "main_building" and (player.have_B or is_spawned):
                item_class = Book
            elif stage_name == "library" and (player.have_O_lib or is_spawned):
                item_class = Book
            elif stage_name == "student_hall" and (player.have_O_stu or is_spawned):
                item_class = Book
            else:
                is_spawned = True

        y = random.randint(200, 450)
        
        # 인스턴스 생성하여 리스트에 추가
        items.append(item_class(current_x, y))

        next_step = random.randint(50, 150)
        current_x += next_step
    
    should_force_spawn = False

    # 조건 체크: 보너스 아이템이 지정되어 있고, 아직 안 나왔고, 리스트가 비어있지 않을 때
    if bonus_item_class and not is_spawned and items:
        if stage_name == "main_building" and not player.have_B:
            should_force_spawn = True
        elif stage_name == "library" and not player.have_O_lib:
            should_force_spawn = True
        elif stage_name == "student_hall" and not player.have_O_stu:
            should_force_spawn = True
            
    if should_force_spawn:
        target_idx = random.randint(0, len(items) - 1)
        
        target_item = items[target_idx]
        
        items[target_idx] = bonus_item_class(target_item.rect.x, target_item.rect.y)

    return items