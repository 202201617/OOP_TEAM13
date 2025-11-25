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

# 장애물
class Soju(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/soju.png")

class Nut(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/nut.png")

class CoffeeCup(Object):
    def __init__(self, x, y):
        super().__init__(x, y, "image/coffee_test.png")

COMMON_ITEMS = [Book, Energy, Soju, Nut, CoffeeCup]
COMMON_WEIGHTS = [45, 10, 25, 10, 10]

'''
추가로 명수당에서는 장애물 없이 아이템만 등장하고 점수가 변동되는 데
그 부분은 아직 구현하지 못하였음
'''

def create_random_items(seconds, speed, screen_width, screen_height, stage_name, player):
    items = []

    #30초동안 나오게 되어있음
    total_distance = (seconds + 2) * 30 * speed
    current_x = screen_width + 100

    current_pool = COMMON_ITEMS[:]
    curernt_weights = COMMON_WEIGHTS[:]
    
    bonus_item_class = None

    if stage_name == "main_building":
        bonus_item_class = B
        current_pool.append(bonus_item_class)
        curernt_weights.append(5)

    elif stage_name == "library":
        bonus_item_class = O_lib
        current_pool.append(bonus_item_class)
        curernt_weights.append(5)

    elif stage_name == "student_hall":
        bonus_item_class = O_stu
        current_pool.append(bonus_item_class)
        curernt_weights.append(5)

    is_spawned = False

    while current_x < total_distance:
        item = random.choices(current_pool, weights=curernt_weights, k=1)[0]

        if item == bonus_item_class:
            if stage_name == "main_building":
                if player.have_B or is_spawned:
                    item = Book
                else:
                    is_spawned = True

            elif stage_name == "library":
                if player.have_O_lib or is_spawned:
                    item = Book
                else:
                    is_spawned = True

            elif stage_name == "student_hall":
                if player.have_O_stu or is_spawned:
                    item = Book
                else:
                    is_spawned = True

        y = random.randint(200, 450)
        items.append(item(current_x, y))

        next_step = random.randint(50, 150)
        current_x += next_step

    return items