import random
import time

import pygame

class game_object:
    def __init__(self, window, imgleft, imgright):
        self.screen = window
        try:
            self.imgleft = pygame.image.load(imgleft)
            self.imgright = pygame.image.load(imgright)
            self.image = self.imgleft
            self.rect = self.image.get_rect()
        except:
            self.imgleft = None
            self.imgright = None
            self.image = None
            self.rect = None
        self.show = True

    def draw(self):
        if self.show:
            self.screen.blit(self.image, self.rect)

    def move(self):
        pass

class bullet(game_object):
    def __init__(self, window, player):
        super().__init__(window, None, None)
        self.player = player
        self.rect = pygame.Rect(self.player.rect.x - 1, self.player.rect.centery, 10, 2)
        self.default_x = player.rect.x
        self.destroy = False
        if self.player.image == self.player.imgleft or self.player.image == self.player.image_move_left:
            self.direction = 'L'
        else:
            self.direction = 'R'
            self.rect.x += 30
        self.speed = 0.6
        self.x = self.rect.x

    def draw(self):
        if self.show:
            pygame.draw.rect(self.screen, (248, 248, 0), self.rect)

    def move(self):
        if self.destroy:
            return
        if self.direction == 'L':
            self.x -= self.speed
            self.rect.x = self.x
            if self.x < self.default_x - 450:
                self.destroy = True
        else:
            self.x += self.speed
            self.rect.x = self.x
            if self.x > self.default_x + 450:
                self.destroy = True

class bullet_system:
    def __init__(self, window, player):
        self.press_space = False
        self.last_bullet = None
        self.bullets_list = []
        self.screen = window
        self.player = player

    def create_bullets(self):
        if self.press_space:
            if self.last_bullet is None or time.time() - self.last_bullet > 0.5:
                bullet_ = bullet(self.screen, self.player)
                self.bullets_list.append(bullet_)
                self.last_bullet = time.time()

class rope(game_object):
    def __init__(self, window, imgleft, imgright, player):
        super().__init__(window, imgleft, imgright)
        self.player = player
        self.img_boat = pygame.image.load('boat.png')
        self.img_boat_rect = self.img_boat.get_rect()
        self.img_boat_rect.top = 50
        self.img_blue = pygame.image.load('blue.png')
        self.img_blue_rect = self.img_blue.get_rect()
        self.img_blue_rect2 = self.img_blue.get_rect()
        self.img_blue_rect.top = 30
        self.img_blue_rect2.top = 30
        self.img_blue_rect.left = 0
        self.img_blue_rect2.right = 1200
        self.img_grass = pygame.image.load('grass.png')
        self.img_grass_rect = self.img_grass.get_rect()
        self.img_grass_rect2 = self.img_grass.get_rect()
        self.img_grass_rect.bottom = 750
        self.img_grass_rect2.bottom = 750
        self.img_grass_rect.left = 0
        self.img_grass_rect2.right = 1200



    def draw(self):
        if self.show:
            if self.player.image == self.player.imgleft or self.player.image == self.player.image_move_left:
                self.rect.centerx = self.player.rect.centerx + 2
                self.img_boat_rect.centerx = self.player.rect.centerx + 35
            else:
                self.rect.centerx = self.player.rect.centerx
                self.img_boat_rect.centerx = self.player.rect.centerx + 35
            self.rect.bottom = self.player.rect.top + 4
            self.screen.blit(self.image, self.rect)
            self.screen.blit(self.img_blue, self.img_blue_rect)
            self.screen.blit(self.img_blue, self.img_blue_rect2)
            self.screen.blit(self.img_boat, self.img_boat_rect)
            self.screen.blit(self.img_grass, self.img_grass_rect)
            self.screen.blit(self.img_grass, self.img_grass_rect2)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect((0, 0), (1200, 35)))

class main_player(game_object):
    def __init__(self, window, imgleft, imgright):
        super().__init__(window, imgleft, imgright)
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.top = 100
        self.move_down = False
        self.move_up = False
        self.move_left = False
        self.move_right = False
        self.hand = True
        self.y = self.rect.centery
        self.x = self.rect.centerx
        self.image_move = 0
        self.image = self.imgleft
        self.image_move_left = pygame.image.load('moveL.png')
        self.image_move_right = pygame.image.load('moveR.png')

    def move(self):
        speed_walk = 0.2
        speed = 0.5
        if self.move_down:
            if self.rect.bottom < 710:
                self.y += speed
                self.rect.centery = float(self.y)
        if self.move_up:
            if self.rect.top > 100:
                self.y -= speed
                self.rect.centery = float(self.y)
        if self.move_left:
            self.walk_animation('Left')
            if self.rect.bottom >= 710:
                self.x -= speed_walk
            else:
                self.x -= speed
            self.rect.centerx = self.x
            if self.rect.right < self.screen.get_rect().left + 5:
                self.x = self.screen.get_rect().right - 5
                self.rect.left = self.x
        if self.move_right:
            self.walk_animation('Right')
            if self.rect.bottom >= 710:
                self.x += speed_walk
            else:
                self.x += speed
            self.rect.centerx = float(self.x)
            if self.rect.left > self.screen.get_rect().right + 5:
                self.x = self.screen.get_rect().left + 5
                self.rect.left = self.x

    def check_touch(self):
        pass
    def walk_animation(self, direction):
        if self.rect.bottom < 709:
            if self.image != self.imgright and direction == 'Right':
                self.image = self.imgright
            if self.image != self.imgleft and direction == 'Left':
                self.image = self.imgleft
            return
        if direction == 'Left':
            if self.image_move % 40 == 0:
                if self.image == self.imgleft:
                    self.image = self.image_move_left
                else:
                    self.image = self.imgleft
        if direction == 'Right':
            if self.image_move % 40 == 0:
                if self.image == self.imgright:
                    self.image = self.image_move_right

                else:
                    self.image = self.imgright
        self.image_move += 1

class monsters(game_object):
    def __init__(self, window, imgleft, imgright):
        super().__init__(window, imgleft, imgright)
        self.rect.centerx = 0
        self.rect.top = random.randint(110, 680)
        self.new_point = True
        self.distance = 0
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.speed = random.randint(23, 35) / 100

    def move(self):
        speed = self.speed
        if self.new_point:
            self.distance = random.randint(0, 1200)
            self.new_point = False
        if self.rect.centerx > self.distance:
            self.image = self.imgleft
            self.x -= speed
            self.rect.centerx = self.x
            if self.rect.centerx <= self.distance:
                self.new_point = True
        else:
            self.image = self.imgright
            self.x += speed
            self.rect.centerx = self.x
            if self.rect.centerx >= self.distance:
                self.new_point = True

class meduse(monsters):
    def __init__(self, window, image):
        super().__init__(window, image, image)
        self.speed = 0.2
        self.new_pointy = True
        self.distancey = 0

    def move(self):
        speed = self.speed
        if self.new_point:
            self.distance = random.randint(self.rect.x-150, self.rect.x+150)
            if self.distance < 0:
                self.distance = 0
            if self.distance > 1200:
                self.distance = 1200
            self.new_point = False
        if self.rect.centerx > self.distance:
            self.x -= speed
            self.rect.centerx = self.x
            if self.rect.centerx <= self.distance:
                self.new_point = True
        else:
            self.x += speed
            self.rect.centerx = self.x
            if self.rect.centerx >= self.distance:
                self.new_point = True
        if self.new_pointy:
            self.distancey = random.randint(self.rect.y - 100, self.rect.y + 100)
            if self.distancey < 100:
                self.distancey = 100
            if self.distancey > 650:
                self.distancey = 650
            self.new_pointy = False
        if self.rect.centery > self.distancey:
            self.y -= speed
            self.rect.centery = self.y
            if self.rect.centery <= self.distancey:
                self.new_pointy = True
        else:
            self.y += speed
            self.rect.centery = self.y
            if self.rect.centery >= self.distancey:
                self.new_pointy = True

class crab(monsters):
    def __init__(self, window, image):
        super().__init__(window, image, image)
        self.speed = 0.3
        self.rect.top = 680

class prize(game_object):
    def __init__(self, window, image, glug):
        super().__init__(window, image, image)
        self.glug = glug
        self.default_value()

    def default_value(self):
        self.rect.centerx = random.randint(35, 1165)
        self.rect.bottom = 710
        self.free = True
        self.prize_at_boat = False
        self.get_points = False
        self.show = True

    def move(self):
        if self.free == False and self.show == True:
            self.rect.x = self.glug.rect.x
            self.rect.y = self.glug.y + 20
            if self.glug.rect.top < 105:
                self.show = False
                self.glug.hand = True
                self.prize_at_boat = True

class game_state():
    def __init__(self, window):
        self.level = 1
        self.point = 0
        self.hearts = 5
        self.screen = window
        self.font = pygame.font.Font(None, 25)
        self.text_points = self.font.render(f'1:{self.get_text_points()}', True, (200, 200, 200), (0, 0, 0))
        self.text_points_rect = self.text_points.get_rect()
        self.text_points_rect.top = 5
        self.text_points_rect.left = 5
        self.is_move_rope = False
        self.get_prize = 2
        #self.text_points()
    def create_text_points(self):
        self.text_points = self.font.render(f'1:{self.get_text_points()}', True, (200, 200, 200), (0, 0, 0))
        self.text_points_rect = self.text_points.get_rect()
        self.text_points_rect.top = 5
        self.text_points_rect.left = 5
    def show_state(self):
        self.screen.blit(self.text_points, self.text_points_rect)

    def get_text_points(self):
        strpoints = str(self.point)
        while len(strpoints) < 6:
            strpoints = '0'+strpoints
        print(strpoints)
        return strpoints

    def show_level(self):
        img_level = pygame.image.load(f'L{self.level}.png')
        img_level_rect = img_level.get_rect()
        img_level_rect.centerx = 600
        img_level_rect.centery = 350
        self.screen.blit(img_level, img_level_rect)

