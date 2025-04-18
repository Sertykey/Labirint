from pygame import *
font.init()
window = display.set_mode((700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h , x, y):
        super().__init__()
        self.image =  transform.scale(
            image.load(picture),
            (w ,h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        self.rect.y += self.y_speed
        if self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
    def fire(self):
        bullet = Bullet("Booles.png", 15,10, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self,picture, w, h, x, y,speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = "left"
    def update(self):
        if self.rect.x <=470:
            self.direction = "right"
        elif self.rect.x >=600:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()

        
display.set_caption("Лабиринт")
run = True
background = transform.scale(
    image.load("background.jpg"),
    (700, 500)
)
wall_1 = GameSprite("wall.png", 80, 200, 200, 250)#w,h,x,y
wall_2 = GameSprite("wall.png", 40, 180, 250, 150)
wall_3 = GameSprite("wall.png", 200, 80, 210, 200)
walls = sprite.Group()
walls.add(wall_1, wall_2, wall_3)
shrek = GameSprite('Shrek.png', 100, 100, 400, 400)
herous = Player("enemy2.png", 80, 80 , 140, 100, 0, 0)
enemy = Enemy("Osel.png", 80, 80, 200, 200, 3)
enemys = sprite.Group()
enemys.add(enemy)
font1 = font.SysFont("Arial", 40)
bullets = sprite.Group()
finish = False
win = font1.render(
    "YOU WIN", True, (255, 215, 0)
)
loser = font1.render(
    "YOU LOSER!", True, (255, 215, 0)
)

while run:
    for e in event.get() :
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                herous.y_speed = -10
            elif e.key == K_DOWN:
                herous.y_speed = 10
            elif e.key == K_LEFT:
                herous.x_speed = -10
            elif e.key == K_RIGHT:
                herous.x_speed = 10
            elif e.key == K_SPACE:
                herous.fire()
        elif e.type == KEYUP:
            if e.key == K_UP:
                herous.y_speed = 0
            elif e.key == K_DOWN:
                herous.y_speed = 0
            elif e.key == K_LEFT:
                herous.x_speed = 0
            elif e.key == K_RIGHT:
                herous.x_speed = 0    
    if finish == False:    
        window.blit(background, (0, 0))
        walls.draw(window)
        sprite.groupcollide(bullets, walls, True, False)
        herous.update()
        shrek.reset()
        herous.reset()
        bullets.update()
        bullets.draw(window)
        enemy.update()
        enemys.draw(window)

        hits = sprite.groupcollide(bullets, enemys, True, True)
        if len(hits)>0:
            enemy.rect.x = 1000
        if sprite.collide_rect(herous, shrek):
            finish = True
            window.blit(win, (320, 250))
        elif sprite.collide_rect(herous, enemy):
            finish = True
            window.blit(loser, (320, 250))
        
    time.delay(50)
    display.update()
