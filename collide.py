from ending import *

def check_collision(player, items, sound):
    for item in items:
        if item.active and player.rect.colliderect(item.rect):
            apply_effect(player, item)

            #아이템 획득 사운드 재생
            sound.play_item()

            item.active = False

def apply_effect(player, item):
    if item.__class__.__name__ == "Book":
        compare = player.grade + 0.10
        if compare >= 4.50:
            player.grade = 4.50
        else:
            player.grade = compare

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

    elif item.__class__.__name__ == "BonusBook":
        compare = player.grade + 0.20
        if compare >= 4.50:
            player.grade = 4.50
        else:
            player.grade = compare

    elif getattr(item, "name", "") == "B":
        player.have_B = True

    elif getattr(item, "name", "") == "O_lib":
        player.have_O_lib = True

    elif getattr(item, "name", "") == "O_stu":
        player.have_O_stu = True
