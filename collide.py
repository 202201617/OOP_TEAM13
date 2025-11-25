from ending import *

def check_collision(player, items):
    for item in items:
        if item.active and player.rect.colliderect(item.rect):
            apply_effect(player, item)
            item.active = False

def apply_effect(player, item):
    if item.__class__.__name__ == "Book":
        player.grade += 0.10

    elif item.__class__.__name__ == "Energy":
        if player.hp < 3:
            player.hp += 1 
        
    elif item.__class__.__name__ == "Soju":
        if player.grade > 0.00:
            player.grade -= 0.05

    elif item.__class__.__name__ == "Nut":
        if player.hp > 0:
            player.hp -= 1

    elif item.__class__.__name__ == "CoffeeCup":
        if player.hp > 0:
            player.hp -= 1

    elif item.name == "B":
        player.have_B = False

    elif item.name == "O_lib":
        player.have_O_lib = False

    elif item.name == "O_stu":
        player.have_O_stu = False
