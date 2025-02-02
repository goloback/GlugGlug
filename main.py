import random
import sys
import pygame
from resource import main_player, monsters, prize, rope, bullet_system, game_state

def destroy_bullets():
    for bullet in bullet_system_object.bullets_list.copy():
        if bullet.destroy:
            if bullet in object_list:
                object_list.remove(bullet)
            bullet_system_object.bullets_list.remove(bullet)

def bullet_action():
    bullet_system_object.create_bullets()
    for bullet in bullet_system_object.bullets_list:
        if bullet in object_list:
            if bullet.destroy:
                object_list.remove(bullet)
        else:
            if not bullet.destroy:
                object_list.append(bullet)

def all_actions(object_list):
    bullet_action()
    destroy_bullets()
    for object in object_list:
        object.draw()
        object.move()
        if str(type(object)) =="<class 'resource.bullet'>":
            for f in fish_list.copy():
                if pygame.sprite.collide_rect(f, object):
                    object.destroy = True
                    if f in object_list:
                        object_list.remove(f)
                        if f in fish_list:
                            fish_list.remove(f)
                    glug_glug_state.point += 35
                    glug_glug_state.create_text_points()
    for i in prize_list:
        if objects_touch(glug, i) == True and glug.hand == True and i.show == True:
            i.free = False
            glug.hand = False
            glug_glug_state.point += 25
            glug_glug_state.create_text_points()
        if i.prize_at_boat == True and i.get_points == False:
            glug_glug_state.point += 40
            glug_glug_state.create_text_points()
            i.get_points = True

def objects_touch(object1, object2):
    try:
        if pygame.sprite.collide_mask(object1, object2):
            return True
        else:
            return False
    except:
        return False

pygame.init()
window = pygame.display.set_mode((1200, 750))
glug_glug_state = game_state(window)
glug = main_player(window, 'left.png', 'right.png')
rope = rope(window, 'rope.png', 'rope.png', glug)
bullet_system_object = bullet_system(window, glug)
amount_fish_1 = 30
fish_list = []


for i in range(amount_fish_1):
    fish = monsters(window, 'fishlv2.png', 'right_fish.png')
    if i % 2 == 0:
        fish.rect.centerx -= random.randint(0, 10000)
    else:
        fish.rect.centerx = random.randint(1200, 11200)

    fish.x = fish.rect.centerx
    fish_list.append(fish)

prize_list = []
crest = prize(window, 'crest.png', glug)
gold = prize(window, 'gold.png', glug)
cup = prize(window, 'cup.png', glug)
prize_list.append(crest)
prize_list.append(gold)
prize_list.append(cup)
object_list = [glug]
object_list += prize_list
object_list += fish_list
object_list.append(rope)

while True:
    print(f'fish {len(fish_list)}')
    print(f'bullet{len(bullet_system_object.bullets_list)}')
    window.fill((0, 0, 0))
    all_actions(object_list)
    glug_glug_state.show_state()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_s or i.key == pygame.K_DOWN:
                glug.move_down = True
            if i.key == pygame.K_w or i.key == pygame.K_UP:
                glug.move_up = True
            if i.key == pygame.K_a or i.key == pygame.K_LEFT:
                glug.move_left = True
            if i.key == pygame.K_d or i.key == pygame.K_RIGHT:
                glug.move_right = True
            if i.key == pygame.K_SPACE:
                bullet_system_object.press_space = True

        if i.type == pygame.KEYUP:
            if i.key == pygame.K_s or i.key == pygame.K_DOWN:
                glug.move_down = False
            if i.key == pygame.K_w or i.key == pygame.K_UP:
                glug.move_up = False
            if i.key == pygame.K_a or i.key == pygame.K_LEFT:
                glug.move_left = False
            if i.key == pygame.K_d or i.key == pygame.K_RIGHT:
                glug.move_right = False
            if i.key == pygame.K_SPACE:
                bullet_system_object.press_space = False

    pygame.display.flip()
