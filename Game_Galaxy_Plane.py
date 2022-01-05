import pygame
import random
import time
from os import path
from win32api import GetSystemMetrics

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (242, 148, 0)
YELLOW = (255, 2555, 0)

WIDTH = 480
HEIGHT = GetSystemMetrics(1) - 200  # = 780 # (Узнает высоту экрана)о
FPS = 60

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # окно программы
pygame.display.set_caption("Game")
clock = pygame.time.Clock()  # убедиться, что игра работает с заданной частотой кадров


# Создаем Объекты
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        self.mob_x = 30
        self.mob_y = 15
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.mob_x, self.mob_y))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(5, WIDTH - self.rect.width, self.mob_x + 3)
        self.rect.y = random.randrange(-115, -5, self.mob_y + 3)
        self.speedy = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(5, WIDTH - self.rect.width, self.mob_x + 3)
            self.rect.y = random.randrange(-115, -5, self.mob_y + 3)
            self.speedy = random.randrange(1, 5)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.bullet_x = 10
        self.bullet_y = 20
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.bullet_x, self.bullet_y))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.level = 1

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.speedx += 8
        if keys[pygame.K_a]:
            self.speedx -= 8
        if keys[pygame.K_RIGHT]:
            self.speedx += 8
        if keys[pygame.K_LEFT]:
            self.speedx -= 8

        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Создание Объектов (Спрайтов)
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
number_of_mobs = 8
for i in range(number_of_mobs):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)
score = 0

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Теперь необходимо создать игровой цикл:

running = True
while running:

    # 1) Ввод процесса (события)
    # 2) Обновление
    # 3) Визуализация (сборка)

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        if score % 10 == 0:
            mob = Mob()
            all_sprites.add(mob)
            mobs.add(mob)

        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        time.sleep(3)
        running = False

    # Рендеринг
    screen.fill(BLACK)
    # screen.blit(background, backgound_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
# Выбрать шрифт для использования.
# Стандартный шрифт, размером в 25.
# font = pygame.font.Font(None, 25)
# score = 9999
# text = font.render("Score: "+str(score), True, GREEN)
# screen.blit(text, [300, 300])
