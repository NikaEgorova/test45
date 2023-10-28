from pygame import *

mixer.init()
# фонова музика
mixer.music.load('rim.mp3')
mixer.music.set_volume(0.10) # гучність
mixer.music.play(-1) # запуск музики

# короткі звуки
bullet = mixer.Sound('polet.ogg')
bullet.set_volume(0.2)
winer = mixer.Sound('pobega.ogg')
losers = mixer.Sound('losers.ogg')
losers.set_volume(0.3)
coin = mixer.Sound('mario.ogg')



#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
    
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#клас головного гравця
class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self):  
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet('syriken.png', self.rect.centerx, self.rect.top, 20, 25, 20)
        bullets.add(bullet)

#клас спрайту-ворога
class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 =x1
        self.x2 =x2

   #рух ворога
    def update(self):
        if self.rect.x <= self.x1: 
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 =y1
        self.y2 =y2

   #рух ворога
    def update(self):
        if self.rect.y <= self.y1: #w1.wall_x + w1.wall_width
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

# клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога
    def update(self):
        self.rect.x += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x > win_width+10:
            self.kill()

#Створюємо віконце
win_width = 1500
win_height = 790
window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")
back = transform.scale(image.load("fon.jpg"), (win_width, win_height))

#Створюємо групу для стін
barriers = sprite.Group()

#створюємо групу для куль
bullets = sprite.Group()

#Створюємо групу для монстрів
monsters = sprite.Group()

#Створюємо стіни картинки
w1 = GameSprite('stena.jpg',130, win_height/2, 300, 50)
w2 = GameSprite('stena.jpg', 410, 300, 40, 300)
w3 = GameSprite('stena.jpg', 0, 100, 390, 40)
w4 = GameSprite('stena.jpg', 600, 370, 30, 430)
w5 = GameSprite('stena.jpg', 650, 200, 400, 40)
w6 = GameSprite('stena.jpg', 820, 350, 40, 300)
w7 = GameSprite('stena.jpg', 830, 430, 300, 40)
w8 = GameSprite('stena.jpg', 1100, 350, 40, 630)
w9 = GameSprite('stena.jpg', 1300, 150, 40, 530)
w10 = GameSprite('stena.jpg', 1300, 400, 330, 40)
bullets = sprite.Group()

#додаємо стіни до групи
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)

font.init()
font1 = font.SysFont('arial', 25)

coints_amount_1 = 0

coin1 = GameSprite('almaz.png', 350, 350, 60 ,60)
coin2 = GameSprite('almaz.png', 480, 510, 60 ,60)
coin3 = GameSprite('almaz.png', 1030, 480, 60 ,60)
coin4 = GameSprite('almaz.png', 1030, 350, 60 ,60)
coin5 = GameSprite('almaz.png', 1350, 330, 60 ,60)
coin6 = GameSprite('almaz.png', 850, 140, 60 ,60)
coins = sprite.Group()
coins.add(coin1)
coins.add(coin2)
coins.add(coin3)
coins.add(coin4)
coins.add(coin5)
coins.add(coin6)


#створюємо спрайти
packman = Player('mech.png', 5, win_height - 80, 80, 80, 0, 0)
monster2 = Enemy_h('Skelet.png', 0, 310, 80, 80, 14, 0, 280)
monster3 = Enemy_v('Skelet.png', 470, 60, 80, 80, 20, 60, 430)
monster4 = Enemy_h('Skelet.png', 600, 260, 80, 80, 20, 600, 920)
monster5 = Enemy_v('Skelet.png', 870, 720, 80, 80, 20, 480, 720)
monster6 = Enemy_h('Skelet.png', 1200, 100, 80, 80, 25, 600, 1200)
monster7 = Enemy_v('Skelet.png', 1350, 720, 80, 80, 25, 480, 720)
monster8 = Enemy_v('Skelet.png', 1350, 50, 80, 80, 20, 20, 300)
monster9 = Enemy_v('Skelet.png', 1180, 60, 80, 80, 20, 100, 600)
final_sprite = GameSprite('final.png', win_width - 85, win_height - 100, 80, 80)

#додаємо монстра до групи
#monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
monsters.add(monster6)
monsters.add(monster7)
monsters.add(monster8)
monsters.add(monster9)
#змінна, що відповідає за те, як закінчилася гра
finish = False
#ігровий цикл
run = True
while run:
    #цикл спрацьовує кожну 0.05 секунд
    time.delay(50)
        #перебираємо всі події, які могли статися
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -8
            elif e.key == K_RIGHT:
                packman.x_speed = 8
            elif e.key == K_UP:
                packman.y_speed = -8
            elif e.key == K_DOWN:
                packman.y_speed = 8
            elif e.key == K_SPACE:
                packman.fire()
                bullet.play()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0 
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

#перевірка, що гра ще не завершена
    if not finish:
        #оновлюємо фон кожну ітерацію
        window.blit(back, (0, 0))#зафарбовуємо вікно кольором

        #запускаємо рухи спрайтів
        packman.update()
        bullets.update()

        #оновлюємо їх у новому місці при кожній ітерації циклу
        packman.reset()
        #рисуємо стіни 2
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset() 
        coins.draw(window)
        if sprite.spritecollide(packman, coins, True):
            coints_amount_1 += 1
            coin.play()
        text = font1.render(f'Алмазів зібранно: {coints_amount_1}/6',True, (255,255,0))
        window.blit(text, (50,50))

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('lose.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            mixer.music.stop()
            losers.play()

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('winer.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            mixer.music.stop()
            winer.play()
    
    display.update()