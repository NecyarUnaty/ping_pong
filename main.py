from pygame import *
from time import sleep
from time import clock
from random import randint

width = 700
height = 500

#self.rect.colliderect(rect2)

window = display.set_mode((width, height))
display.set_caption('Пинг-понг')
clock = time.Clock()
FPS = 60

background_color = (150, 200, 255) # light cyan
lose_color = (0, 0, 0) # black
winner_color_left = (0, 0, 255) # blue
winner_color_right = (255, 0, 0) # red

font.init()
font1 = font.SysFont('Arial', 50)
text_you_win_left = font1.render('Победа левого игрока!', 1, (255, 255, 255))
text_you_win_right = font1.render('Победа правого игрока!', 1, (255, 255, 255))

sleeping = 1.0


def lose(left_or_right, lose_color, winner_color, sleeping):
    window.fill(lose_color)
    for i in range(12):
        sleep(sleeping)
        window.fill(winner_color)
        if left_or_right == 'right':
            window.blit(text_you_win_left, (randint(20, 260), randint(20, 440)))
        else:
            window.blit(text_you_win_right, (randint(20, 240), randint(20, 440)))
        display.update()
        if sleeping > 0.05:
            sleeping -= 0.05
        sleep(sleeping)
        window.fill(lose_color)
        if left_or_right == 'right':
            window.blit(text_you_win_left, (randint(20, 260), randint(20, 440)))
        else:
            window.blit(text_you_win_right, (randint(20, 240), randint(20, 440)))
        display.update()
        if sleeping > 0.05:
            sleeping -= 0.05


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, swidth, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (swidth, height)) # find sprites PNG only on the internet
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.swidth = swidth
        self.height = height

    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Left_player(GameSprite):


    def update(self):
       keys = key.get_pressed()
       #if keys[K_a] and self.rect.x > 5:
           #self.left()
       #if keys[K_d] and self.rect.x < width - 80:
           #self.right()
       if keys[K_w] and self.rect.y > 5:
           self.up()
       if keys[K_s] and self.rect.y < height - 80:
           self.down()
       #if self.rect.x > 5:
           #if self.speed > 0.2:
                #self.speed -= 0.01
       #else:
           #if self.speed < 5:
                #self.speed += 0.05

    def left(self):
        self.rect.x -= (self.speed*0.5)

    def right(self):
        self.rect.x += self.speed

    def up(self):
        self.rect.y -= self.speed

    def down(self):
        self.rect.y += self.speed


class Right_player(GameSprite):


    def update(self):
       keys = key.get_pressed()
       #if keys[K_LEFT] and self.rect.x > 5:
           #self.left()
       #if keys[K_RIGHT] and self.rect.x < width - 40:
           #self.right()
       if keys[K_UP] and self.rect.y > 5:
           self.up()
       if keys[K_DOWN] and self.rect.y < height - 80:
           self.down()
       #if self.rect.x < 640:
           #if self.speed > 0.02:
                #self.speed -= 0.01
       #else:
           #if self.speed < 5:
                #self.speed += 0.05

    def left(self):
        self.rect.x -= self.speed

    def right(self):
        self.rect.x += (self.speed)

    def up(self):
        self.rect.y -= self.speed

    def down(self):
        self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, swidth, height, player_speed):
        super().__init__(player_image, player_x, player_y, swidth, height, player_speed)
    
        self.horizontal_direction = randint(0, 1)
        self.vertical_direction = randint(0, 1)

    def update(self):
       global left_game
       global right_game

       if self.horizontal_direction == 0: #and self.rect.x > 5:
           self.left()

       if self.rect.colliderect(left_player):
            self.horizontal_direction = 1

       if self.rect.colliderect(right_player):
           self.horizontal_direction = 0


       if self.rect.x <= 5:
            left_game = False

       if self.horizontal_direction == 1: #and self.rect.x < width - 80: #width = 700
           self.right()

       if self.rect.x >= width - 35:
            right_game = False

       if self.vertical_direction == 1: #and self.rect.y > 5:
           self.up()

       if self.rect.y <= 10:
            self.change_vertical()

       if self.vertical_direction == 0: #and self.rect.y < height - 80:
           self.down()

       if self.rect.y >= height - 35:
            self.change_vertical()


    def left(self):
        self.rect.x -= self.speed

    def right(self):
        self.rect.x += self.speed

    def up(self):
        self.rect.y -= self.speed

    def down(self):
        self.rect.y += self.speed

    def change_horizont(self):
        if self.horizontal_direction == 1:
            self.horizontal_direction = 0
        else:
            self.horizontal_direction = 1
        self.speed += 0.01

    def change_vertical(self):
        if self.vertical_direction == 1:
            self.vertical_direction = 0
        else:
            self.vertical_direction = 1
        self.speed += 0.01


left_player = Left_player('Platform.png', 30, 220, 30, 80, 5)

right_player = Right_player('Platform.png', 640, 220, 30, 80, 5)

ball = Ball('Platform.png', 350, 220, 30, 30, 3)


left_game = True
right_game = True

while left_game and right_game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.fill(background_color)
    clock.tick(FPS)

    left_player.update()
    right_player.update()
    ball.update()
    left_player.reset()
    right_player.reset()
    ball.reset()

    if left_game == False:
        lose('left', lose_color, winner_color_right, sleeping)
    if right_game == False:
        lose('right', lose_color, winner_color_left, sleeping)

    display.update()