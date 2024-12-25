#Создай собственный Шутер!

from pygame import *
from random import *


# импорт модулей

window = display.set_mode((700, 500))
#Создание окна
display.set_caption('шутер')
#название окна
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
#создание фона


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed

        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
            bullet = Bullet('bullet.png', self.rect.x, self.rect.y - 60, 7)
            bullets.add(bullet)

lost = 0

class Enemy(GameSprite):
    def update(self):
        global lost 
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 500:
            self.kill


player = Player('rocket.png',350 , 350, 10)

monster1 = Enemy('ufo.png', randint(0, 600), 0, 1)
monster2 = Enemy('ufo.png', randint(0, 600), 0, 1)
monster3 = Enemy('ufo.png', randint(0, 600), 0, 1)
monster4 = Enemy('ufo.png', randint(0, 600), 0, 1)
monster5 = Enemy('ufo.png', randint(0, 600), 0, 1)

monsters = sprite.Group()
#Создание группы
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

bullets = sprite.Group()

asteroid1 = Enemy('asteroid.png', randint(0, 600), 0, 1)
asteroid2 = Enemy('asteroid.png', randint(0, 600), 0, 1)
asteroid3 = Enemy('asteroid.png', randint(0, 600), 0, 1)

asteroids = sprite.Group()

asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)

run = True
finish = False

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullet_s = mixer.Sound('fire.ogg')


font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
lose = font2.render('YOU LOSE', True, (255, 0, 0))
win = font2.render('YOU WIN' , True, (0, 255, 0))


FPS = 60
clock = time.Clock()

score = 0
loser = 0
num_fire = 0
rel_time = False
HP = 2

while run:  
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                bullet_s.play()
                num_fire += 1
    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        monsters.draw(window) 
        bullets.draw(window)
        asteroids.draw(window)
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        #создание группы столкновений
        collide_h = sprite.spritecollide(player, monsters, False)
        collide_ast = sprite.spritecollide(player, asteroids, False)
        for i in collides:
            score += 1
            monsterx = Enemy('ufo.png', randint(0, 600), 0, 1)
            monsters.add(monsterx)
            
        if collide_h:
            loser = True          

        if collide_ast:
                HP -= 1


        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255) )
        text_score = font1.render('Счет:' + str(score), 1 , (255, 255, 255))
        window.blit(text_score, (0, 0))
        window.blit(text_lose, (0, 20))


        if lost >= 3 or HP <= 0:
            finish = True
            window.blit(lose, (200, 200))

        if loser:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 100:
            finish = True
            window.blit(win, (200, 200))

    display.update()
