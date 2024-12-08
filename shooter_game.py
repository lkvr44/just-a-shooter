from random import *
from pygame import *

font.init()
font2=font.SysFont('Arial', 36)


class GameSprite(sprite.Sprite):
    def __init__(self,pl_x,pl_y,pl_picture,pl_speed, size_x, size_y, ):
        super().__init__()
        self.image = transform.scale(image.load(pl_picture),(size_x,size_y))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed=key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 440:
            self.rect.y += self.speed
        if keys_pressed[K_UP] and self.rect.y > 150:
            self.rect.y -= self.speed

    def shot(self):
        keys_pressed=key.get_pressed()
        if keys_pressed[K_SPACE]:
            bullet = Bullet(self.rect.centerx-7, self.rect.top+10, 'bullet.png', 15,20,20,0)
            bullets.add(bullet)
            bullet = Bullet(self.rect.centerx-7, self.rect.top+10, 'bullet.png', 15,20,20,5)
            bullets2.add(bullet)
            bullet = Bullet(self.rect.centerx-7, self.rect.top+10, 'bullet.png', 15,20,20,-5)
            bullets3.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 550:
            self.rect.x = randint(60, 640) 
            self.rect.y = -20
            lost = lost + 1
        

class Bullet(GameSprite):
    def __init__(self,pl_x,pl_y,pl_picture,pl_speed, size_x, size_y, speed2):
        super().__init__(pl_x,pl_y,pl_picture,pl_speed, size_x, size_y)
        self.speed2 = speed2
    def update(self):
        self.rect.y -= self.speed
        self.rect.x += self.speed2
        global score
        if self.rect.y < -30:
            self.kill()
    
        # if sprite.groupcollide(bullets,monsters,True,True):
        #     self.kill()
        #     score = score + 1


            





lost=0
score=0
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('shooter')

background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))

monsters = sprite.Group()
for i in range(1,10):
    monster = Enemy(randint(60, 640), -20, 'ufo.png', randint(1, 4), 60, 40)
    monsters.add(monster)

bullets = sprite.Group()
bullets2 = sprite.Group()
bullets3 = sprite.Group()

game=True
finish = False

player = Player(350, 400, 'rocket.png', 5, 65, 80)

clock = time.Clock()
FPS=60

font.init()
font= font.SysFont('Arial', 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose_f = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
fire= mixer.Sound('fire.ogg')
space_sound= mixer.Sound('space.ogg')
space_sound.play()

while game:
    for e in event.get():
            if e.type == QUIT:
                game= False

            elif e.type==KEYDOWN:
                if e.key==K_SPACE:
                    fire= mixer.Sound('fire.ogg')
                    fire.play()
                    player.shot()


                

    if not finish:

        window.blit(background,(0,0))

        player.update()
        monsters.update()
        bullets.update()
        bullets2.update()
        bullets3.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        bullets2.draw(window)
        bullets3.draw(window)

        text = font2.render('Счет: ' + str(score), 1, (255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose,(10,50))

        sprites_list = sprite.groupcollide(bullets,monsters,True,True)
        for nig in sprites_list:
            score = score + 1
            monster = Enemy(randint(60, 640), -20, 'ufo.png', randint(1, 4), 60, 40)
            monsters.add(monster)
            monster = Enemy(randint(60, 640), -20, 'ufo.png', randint(1, 4), 60, 40)
            monsters.add(monster)
            

        sprites_list = sprite.groupcollide(bullets2,monsters,True,True)
        for nig in sprites_list:
            score = score + 1
            monster = Enemy(randint(60, 640), -20, 'ufo.png', randint(1, 4), 60, 40)
            monsters.add(monster)

        sprites_list = sprite.groupcollide(bullets3,monsters,True,True)
        for nig in sprites_list:
            score = score + 1
            monster = Enemy(randint(60, 640), -20, 'ufo.png', randint(1, 4), 60, 40)
            monsters.add(monster)

        clock.tick(FPS)

        if score >= 601:
            finish = True
            window.blit(win, (200,200))

        if lost >= 51:
            finish = True
            window.blit(lose_f, (200,200))

    display.update()
