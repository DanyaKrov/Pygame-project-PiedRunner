import pygame, random, os, sys, pyganim
from win32api import GetSystemMetrics
from pygame.locals import *
from pygame import *
from pygame.math import Vector2
from random import randrange
import time, datetime


class menu:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        load_sound('japan_' + str(randrange(1, 6)) + '.mp3').play()
        self.size = self.width, self.height = int(GetSystemMetrics(0)), int(GetSystemMetrics(1))
        self.screen = pygame.display.set_mode(self.size)
        self.running = True
        self.window_menu()

    def window_menu(self):
        font = pygame.font.Font(None, 70)
        font1 = pygame.font.Font(None, 40)
        font2 = pygame.font.Font(None, 35)
        self.name1 = font.render("Pied ", True, ("red"))  # создание текста
        self.name2 = font.render("Runner", True, ("purple"))
        self.text = font1.render("Кампания", True, ("black"))
        self.text1 = font1.render("Бесконечный режим", True, ("black"))
        self.text2 = font2.render("нажмите Enter, чтобы продолжить ", True, ("gray"))
        self.text_x = self.width // 2 - self.text.get_width() // 2
        self.text_y = self.height // 2 - self.text.get_height() // 2
        self.text_w = self.text.get_width()
        self.text_h = self.text.get_height()
        self.text1_w = self.text1.get_width()
        self.text1_h = self.text1.get_height()
        while self.running:
            self.screen.fill(('white'))
            main_button = pygame.draw.rect(self.screen, ("black"), (self.text_x - 5, self.text_y - 10,
                                           self.text_w + 10, self.text_h + 20), 1)
            main_button1 = pygame.draw.rect(self.screen, ("black"), (self.text_x - 5, self.text_y + 190,
                                                                    self.text1_w + 10, self.text1_h + 20), 1)
            self.screen.blit(self.name1, (40, 10)) #вывод текста
            self.screen.blit(self.text, (self.text_x, self.text_y))
            self.screen.blit(self.text1, (self.text_x, self.text_y + 200))
            self.screen.blit(self.text2, (10, self.height - self.text2.get_height()))
            self.screen.blit(self.name2, (10 + self.name1.get_width() // 4 * 3,
                                          self.name1.get_height() + 10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.start_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_check(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()
            pygame.display.flip() #обновление экрана

    def button_check(self, pos):
        if self.text_x - 5 + self.text_w + 10 >= pos[0] >= self.text_x - 5 and\
            self.text_y - 10 + self.text_h + 20 >= pos[1] >= self.text_y - 10:
            self.start_game()
        if self.text_x - 5 + self.text1_w + 10 >= pos[0] >= self.text_x - 5 and\
            self.text_y + 190 + self.text1_h + 20 >= pos[1] >= self.text_y + 190:
            running_infinity()

    def start_game(self):
        Camera()
        storyline()


class storyline:
    @classmethod
    def __init__(self, number=0):
        pygame.init()
        self.running = True
        if number == 4:
            self.running = False
        while self.running:
            self.screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)))
            self.screen.blit(load_image('loc_' + str(number + 1) + '.png', True), (0, 0)) #показ катсцен
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    self.running = False
                    break
            pygame.display.update()
        main_game(number)


class loose:
    @classmethod
    def __init__(self, number=0):
        pygame.init()
        self.running = True
        while self.running:
            self.screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)))
            self.screen.blit(load_image('dead.png', True), (0, 0)) #показ катсцен
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    self.running = False
                    break
            pygame.display.update()


class main_game:
    def __init__(self, wins=0, infinity=False):
        try:
            self.clock = pygame.time.Clock()
            self.clock.tick(80)
            self.wins = wins
            player()
            sprites()
            if self.wins == 0:
                stone()
            level(self.wins)
            if self.wins == 1:
                tank()
            if self.wins == 2:
                samurai()
            if self.wins == 3:
                villain()
            self.size = self.width, self.height = GetSystemMetrics(0), GetSystemMetrics(1)
            total_level_width, total_level_height = level.get_size()
            self.start('pied runner', True, '',
                            int(self.height * 0.05))
            self.running = True

            while self.running:
                right = left = up = down = False
                self.clock.tick(80) #фпс
                shift = False
                self.start('pied runner', True, '',
                           int(self.height * 0.05))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LSHIFT:
                            shift = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]: #реакцмя на нажатие клавиш
                    player.attack(False)
                elif keys[pygame.K_d]:
                    player.attack(True)
                elif keys[pygame.K_g]:
                    player.wep_out()
                else:
                    if keys[pygame.K_UP]:
                        up = True
                    if keys[pygame.K_DOWN]:
                        down = True
                    if keys[pygame.K_LEFT]:
                        left = True
                    if keys[pygame.K_RIGHT]:
                        right = True
                    player.move(left, right, up, down, shift, self.screen, self.wins)
                if self.wins == 0:
                    load_sound('stone_middle.mp3').play()
                    stone.move()
                if self.wins == 1:
                    tank.move()
                if self.wins == 2:
                    samurai.move(right, left, up, down, self.screen)
                if self.wins == 3:
                    villain.move()
                if not infinity:
                    Camera.update(player.hero)
                else:
                    running_infinity.update(player.hero)
                sprites.collide(self.wins)
                self.clock.tick(60)
            pygame.quit()
        except TimeoutError as exc:
            print(exc)


    def continue1(self):
        pass


    def start(self, name_page, not_error_log, exc, radius, *args):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(name_page)
        if self.wins == 0:
            self.screen.blit(load_image('white.png', True), (0, 0))
        if self.wins == 1:
            self.screen.blit(load_image('green.png', True), (0, 0))
        if self.wins == 2:
            self.screen.blit(load_image('gray.png', True), (0, 0))
        if self.wins == 3:
            self.screen.blit(load_image('blue.png', True), (0, 0))
        player.draw()
        if self.wins == 0:
            stone.draw()
        if self.wins == 1:
            tank.draw()
        if self.wins == 2:
            samurai.draw()
        if self.wins == 3:
            villain.draw()
        level.draw()
        sprites.draw(self.screen)
        pygame.display.update()
        if not_error_log:
            pass
        else:
            times = pygame.font.Font(None, 100)
            text2 = times.render(str(exc), True, "red")
            screen.blit(text2, [80, 70])


class Camera(object):
    @classmethod
    def __init__(self):
        self.wins = 0

    @classmethod
    def update(self, target):
        if target.rect.x + target.image.get_width() >= GetSystemMetrics(0):
            pygame.mixer.stop()  # остановка всех звуков
            self.wins += 1
            if self.wins == 4:
                load_sound('hero_win.mp3').play()
                menu()
            storyline(self.wins)

    @classmethod
    def loose(self):
        loose()
        storyline(self.wins)


def main():
    menu()


class player(sprite.Sprite):
    @classmethod
    def __init__(self):
        self.width, self.height = 20, 20
        self.hero = pygame.sprite.Sprite()
        self.hp = pygame.sprite.Sprite()
        self.speed = 25
        self.jump = 90
        self.hero.image = Surface((load_image('hero_calm1.png').get_size()), pygame.SRCALPHA)
        self.hero.image.set_alpha(256)
        self.hp.image = load_image('hp100.png')
        self.hero.rect = self.hero.image.get_rect()
        self.hp.rect = self.hp.image.get_rect()
        self.hp.rect.x, self.hp.rect.y = 10, (GetSystemMetrics(1) // 80) * 80
        self.hero.rect.x, self.hero.rect.y = 10, GetSystemMetrics(1) - 570
        self.gravity = 10
        self.hp_number = 100
        self.ground = False
        self.shift = False
        self.death = False
        self.right, self.left = True, False #главный герой смотрит направо изначально

        self.anim_delay = 80
        self.animation_walk_right = [('hero_walk_1.png'), ('hero_walk_2.png'), ('hero_walk_3.png'),
                              ('hero_walk_4.png'), ('hero_walk_5.png'), ('hero_walk_6.png'),
                                     ('hero_walk_7.png'), ('hero_walk_8.png')]
        self.animation_run_right = [('hero_run_1.png'), ('hero_run_2.png'), ('hero_run_3.png'),
                              ('hero_run_4.png'), ('hero_run_5.png'), ('hero_run_6.png'),
                                    ('hero_run_7.png'), ('hero_run_8.png'), ('hero_run_9.png'),
                                    ('hero_run_10.png')]

        self.animation_walk_left = [('hero_walk_1l.png'), ('hero_walk_2l.png'), ('hero_walk_3l.png'),
                                     ('hero_walk_4l.png'), ('hero_walk_5l.png'), ('hero_walk_6l.png'),
                                     ('hero_walk_7l.png'), ('hero_walk_8l.png')]
        self.animation_run_left = [('hero_run_1l.png'), ('hero_run_2l.png'), ('hero_run_3l.png'),
                                    ('hero_run_4l.png'), ('hero_run_5l.png'), ('hero_run_6l.png'),
                                    ('hero_run_7l.png'), ('hero_run_8l.png')]
        self.animation_wep_right = [('hero_wep_1.png'), ('hero_wep_2.png'), ('hero_wep_3.png'),
                                   ('hero_wep_4.png'), ('hero_wep_5.png'), ('hero_wep_6.png'),
                                   ('hero_wep_7.png'), ('hero_wep_8.png')]
        self.animation_wep_left = [('hero_wep_1l.png'), ('hero_wep_2l.png'), ('hero_wep_3l.png'),
                                   ('hero_wep_4l.png'), ('hero_wep_5l.png'), ('hero_wep_6l.png'),
                                   ('hero_wep_7l.png'), ('hero_wep_8l.png')]
        self.animation_jump_right = [('hero_jump_1.png'), ('hero_fall_1.png')]
        self.animation_jump_left = [('hero_jump_1l.png'), ('hero_fall_1l.png')]
        self.animation_wep_out = [('hero_wep_1.png'), ('hero_wep_2.png'), ('hero_out.png')]
        self.animation_wep_in = [('hero_out.png'), ('hero_wep_2.png'), ('hero_wep_2.png')]
        boltAnim = []
        for i in self.animation_jump_right:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimJumpRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpRight.play()
        boltAnim = []
        for i in self.animation_jump_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimJumpLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpLeft.play()
        boltAnim = []
        for anim in self.animation_walk_right:
            boltAnim.append((load_image(anim), self.anim_delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimStay = pyganim.PygAnimation([(load_image('hero_calm1.png'), self.anim_delay)])
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.hero.image, (0, 0))
        boltAnim = []
        for i in self.animation_run_right:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimRunright = pyganim.PygAnimation(boltAnim)
        self.boltAnimRunright.play()
        boltAnim = []
        for i in self.animation_walk_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWalkLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalkLeft.play()
        boltAnim = []
        for i in self.animation_run_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimRunLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimRunLeft.play()
        boltAnim = []
        for i in self.animation_wep_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepLeft.play()
        boltAnim = []
        for i in self.animation_wep_right:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepRight.play()
        boltAnim = []
        for i in self.animation_wep_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepLeft.play()
        boltAnim = []
        for i in self.animation_wep_out:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepOut = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepOut.play()
        boltAnim = []
        for i in self.animation_wep_in:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepIn = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepIn.play()

    @classmethod
    def get_position(self):
        return self.hero.rect.x #возврат координаты x спрайта главного героя

    @classmethod
    def collide_with_sam(self, villain): #проверка на столкновение с врагом-самураем на 2 уровне
        if self.hero.image.get_width() not in [85, 116, 107]:
            self.hp_number -= 5 # главный герой получил урон, нужно отнять от здоровья
        else:
            if randrange(1, 3) == 2:
                samurai.hit() #главный геро ударил злодея, нужно отнять количество здоровья врага
        load_sound('hero_fight.mp3').play()


    @classmethod
    def draw(self):
        sprites.add_sprites(self.hero) #добавление спрайта в группу всех спрайтв дял отрисовки
        sprites.add_sprites(self.hp)

    @classmethod
    def move(self, left, right, up, down, shift, screen, wins):
        self.wins = wins
        self.xvec, self.yvec = 0, 0
        if not self.ground:
            left = right = up = down = False
            self.yvec += self.gravity #герой падает
        if self.shift and shift: #переключение режима с бега на шаг и наоборот
            self.shift = False
        elif shift:
            self.shift = True
        if left:
            if not self.shift:
                self.hero.image = Surface((load_image('hero_walk_1l.png').get_size()), pygame.SRCALPHA) #создание прозрачного прямоугольнкиа нужных размеров
                self.hero.image.set_alpha(256)
                self.boltAnimWalkLeft.blit(self.hero.image, (0, 0))
                self.xvec -= self.speed // 2
            else:
                self.hero.image = Surface((load_image('hero_run_1l.png').get_size()), pygame.SRCALPHA)
                self.hero.image.set_alpha(256)
                self.boltAnimRunLeft.blit(self.hero.image, (0, 0))
                self.xvec -= self.speed
        if right:
            if not self.shift:
                self.hero.image = Surface((load_image('hero_walk_1.png').get_size()), pygame.SRCALPHA)
                self.hero.image.set_alpha(256)
                self.xvec += self.speed // 2
                self.boltAnimRight.blit(self.hero.image, (0, 0))
            else:
                self.hero.image = Surface((load_image('hero_run_1.png').get_size()), pygame.SRCALPHA)
                self.hero.image.set_alpha(256)
                self.xvec += self.speed
                self.boltAnimRunright.blit(self.hero.image, (0, 0))
        if up:
            if self.ground:
                if left:
                    self.hero.image = Surface((load_image('hero_jump_1l.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimJumpLeft.blit(self.hero.image, (0, 0))
                    self.yvec -= self.jump
                    self.xvec = -self.speed * 2
                if right:
                    self.xvec = self.speed * 2
                    if wins == 3:
                        self.xvec = self.speed * 4
                if not left:
                    self.hero.image = Surface((load_image('hero_jump_1.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimJumpRight.blit(self.hero.image, (0, 0))
                    self.yvec -= self.jump
        if down:
            pass
        if not down and not left and not right and not up and self.ground:
            if self.right:
                self.hero.image = load_image('hero_calm1.png')
            else:
                self.hero.image = load_image('hero_calm1l.png')
        if right or left:
            self.right, self.left = right, left
        self.ground = False

    @classmethod
    def collide(self, sprites, fire, patron):
        self.hero.rect = self.hero.rect.move(self.xvec, self.yvec)
        if pygame.sprite.spritecollideany(self.hero, sprites):
            self.yvec = -self.yvec
            self.ground = True
        if pygame.sprite.spritecollideany(self.hero, fire):
            self.hp_number -= 21
            self.hero.rect.x -= self.speed * 2
            self.hero.rect.y -= self.jump * 2
        if pygame.sprite.spritecollideany(self.hero, patron) and\
            self.hero.image.get_width() not in [85, 116, 107]:
            self.hp_number -= 100
            load_sound('boom.mp3').play()
        if self.hp_number in range(60, 81): #обновление иконки здоровья
            self.hp.image = load_image('hp80.png')
        if self.hp_number in range(20, 61):
            self.hp.image = load_image('hp50.png')
        if self.hp_number in range(1, 21):
            self.hp.image = load_image('hp20.png')
        if self.hp_number <= 0 and not self.death:
            self.death = True
            self.hp.image = load_image('hp0.png')
            load_sound('hero_death.mp3').play()
            try:
                Camera.loose()
            except Exception:
                running_infinity()

    @classmethod
    def attack(self, right):
        if self.ground:
            if right: #проверка на направление атаки
                for i in range(8):
                    self.hero.image = Surface((load_image('hero_wep_4.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimWepRight.blit(self.hero.image, (0, 0))  # анимация
            else:
                for i in range(8):
                    self.hero.image = Surface((load_image('hero_wep_4l.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimWepLeft.blit(self.hero.image, (0, 0))
            load_sound('hero_attack_' + str(randrange(1, 4)) + '.mp3').play()
            if self.wins == 3:
                villain.collide1(self.hero) #проверка столкновения героя с врагом

    @classmethod
    def wep_out(self):
        self.hero.image = Surface((load_image('hero_out.png').get_size()), pygame.SRCALPHA)
        self.hero.image.set_alpha(256)
        self.boltAnimWepOut.blit(self.hero.image, (0, 0))
        self.hero.image = Surface((load_image('hero_out.png').get_size()), pygame.SRCALPHA)
        self.hero.image.set_alpha(256)
        self.boltAnimWepIn.blit(self.hero.image, (0, 0))
        load_sound('hero_out.mp3').play()


class level(sprite.Sprite):
    @classmethod
    def __init__(self, wins):
        self.level = []
        for i in range(GetSystemMetrics(1) // 80 - 5):
            if wins == 1:
                str = ' ' * 60 #уровень
                for i in range(10):
                    str += random.choice((' ', '_'))
                str += ' ' * 20
                for i in range(10):
                    str += random.choice((' ', '_'))
                self.level.append(str)
            else:
                self.level.append(' ' * 100)
        for i in range(5):
            self.level.append('-' * 100)
        self.n = randrange(1, 8)

    @classmethod
    def draw(self):
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "-":
                    pf = pygame.sprite.Sprite()
                    pf.image = load_image('texture_snow_' + str(self.n) + '.png')
                    pf.rect = pf.image.get_rect()
                    pf.rect.x = x
                    pf.rect.y = y
                    sprites.add_sprites(pf)
                    sprites.add_floor(pf)
                if col == '_':
                    hedgehog(x, y)
                x += 80
            y += 80
            x = 0

    @classmethod
    def get_size(self):
        return (len(self.level[0]) * 80, len(self.level) * 80) #возврат размеров уровня


class hedgehog(sprite.Sprite):
    @classmethod
    def __init__(self, x, y):
        self.hedg = pygame.sprite.Sprite()
        self.hedg.image = load_image('fire.png')
        self.hedg.rect = self.hedg.image.get_rect()
        self.hedg.rect.x, self.hedg.rect.y = x, y
        self.draw()

    @classmethod
    def update(self):
        self.hedg.rect = self.hedg.rect.move(self.vx, self.vy)

    @classmethod
    def check(self):
        pass

    @classmethod
    def draw(self):
        sprites.add_sprites(self.hedg)
        sprites.add_fire(self.hedg)


class sprites(pygame.sprite.Sprite):
    @classmethod
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.fire = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.patron = pygame.sprite.Group()

    @classmethod
    def add_sprites(self, spr):
        self.sprites.add(spr)

    @classmethod
    def add_floor(self, spr):
        self.floor.add(spr)

    @classmethod
    def add_patron(self, spr):
        self.patron.add(spr)

    @classmethod
    def collide(self, wins):
        player.collide(self.floor, self.fire, self.patron)
        if wins == 0:
            stone.collide(self.floor)
        if wins == 1:
            tank.collide(self.floor)
        if wins == 2:
            samurai.collide(self.floor, self.floor)
        if wins == 3:
            villain.collide(self.floor)
        self.floor = pygame.sprite.Group()
        self.fire = pygame.sprite.Group()
        self.patron = pygame.sprite.Group()

    @classmethod
    def draw(self, screen):
        self.sprites.draw(screen)
        self.sprites1 = self.sprites
        self.sprites = pygame.sprite.Group()

    @classmethod
    def get_sprites(self):
        return self.sprites_nohero

    @classmethod
    def add_fire(self, sprite):
        self.fire.add(sprite)


class stone(pygame.sprite.Sprite):
    @classmethod
    def __init__(self):
        self.st_1 = pygame.sprite.Sprite()
        self.st_2 = pygame.sprite.Sprite()
        self.st_3 = pygame.sprite.Sprite()
        self.make(self.st_1)
        self.make(self.st_2, 1)
        self.make(self.st_3, 2)
        self.ground = False
        self.animation_stone = [('stone_4.png'), ('stone_3.png'), ('stone_2.png'), ('stone_1.png')]
        self.gravity = 20
        self.speed = 30
        boltAnim = []
        for i in self.animation_stone:
            boltAnim.append((load_image(i), 50))
        self.boltAnimStone = pyganim.PygAnimation(boltAnim)
        self.boltAnimStone.play()

    @classmethod
    def collide(self, sprites):
        self.collide1(self.st_1, sprites)
        self.collide1(self.st_2, sprites)
        self.collide1(self.st_3, sprites)

    @classmethod
    def collide1(self, name, sprites):
        name.rect = name.rect.move(self.xvec, self.yvec)
        if pygame.sprite.spritecollideany(name, sprites):
            name.rect = name.rect.move(self.xvec, -self.yvec)
            self.ground = True
        if name.rect.x < 0:
            load_sound('stone_fall.mp3').play()
            self.make(name, 2)

    @classmethod
    def make(self, name, number=0):
        name.image = Surface((load_image('stone_1.png').get_size()), pygame.SRCALPHA)
        name.image.set_alpha(256)
        name.rect = name.image.get_rect()
        name.rect.x, name.rect.y = GetSystemMetrics(0) - 50 + 720 * number, GetSystemMetrics(1) - 480

    @classmethod
    def moving(self, name):
        name.image = Surface((load_image('stone_1.png').get_size()), pygame.SRCALPHA)
        name.image.set_alpha(256)
        self.boltAnimStone.blit(name.image, (0, 0))

    @classmethod
    def move(self):
        self.moving(self.st_1)
        self.moving(self.st_2)
        self.moving(self.st_3)
        self.xvec, self.yvec = -self.speed, 0
        if not self.ground:
            self.yvec = self.gravity

    @classmethod
    def draw(self):
        sprites.add_sprites(self.st_1)
        sprites.add_fire(self.st_1)
        sprites.add_sprites(self.st_2)
        sprites.add_fire(self.st_2)
        sprites.add_sprites(self.st_3)
        sprites.add_fire(self.st_3)


class tank(pygame.sprite.Sprite):
    @classmethod
    def __init__(self):
        self.st = pygame.sprite.Sprite()
        self.speed = 0
        self.st.image = Surface((load_image('tank_1.png').get_size()), pygame.SRCALPHA)
        self.st.image.set_alpha(256)
        self.st.rect = self.st.image.get_rect()
        self.st.rect.x, self.st.rect.y = GetSystemMetrics(0) - 400, GetSystemMetrics(1) - 500
        self.animation_tank = [('tank_1.png'), ('tank_2.png'), ('tank_3.png'), ('tank_4.png'),
                            ('tank_5.png'), ('tank_6.png'), ('tank_7.png'), ('tank_8.png'),
                            ('tank_9.png'), ('tank_10.png'), ('tank_11.png')]
        self.fire1 = False
        self.gravity = 10
        self.ground = False
        boltAnim = []
        for i in self.animation_tank:
            boltAnim.append((load_image(i), 20))
        self.boltAnimTank = pyganim.PygAnimation(boltAnim)
        self.boltAnimTank.play()
        self.cr = pygame.sprite.Sprite()
        self.cr.image = load_image('cart.png')
        self.cr.rect = self.cr.image.get_rect()

    @classmethod
    def collide(self, sprites):
        self.st.rect = self.st.rect.move(self.xvec, self.yvec)
        if pygame.sprite.spritecollideany(self.st, sprites):
            self.yvec = -self.yvec
            self.ground = True

    @classmethod
    def move(self):
        if self.fire1:
            self.cr.rect.x -= 70
            if self.cr.rect.x < 0:
                self.fire1 = False
            sprites.add_patron(self.cr)
        if not self.fire1:
            for i in range(11):
                self.st.image = Surface((load_image('tank_1.png').get_size()), pygame.SRCALPHA)
                self.st.image.set_alpha(256)
                self.boltAnimTank.blit(self.st.image, (0, 0))
            self.fire()
        self.xvec, self.yvec = -self.speed, 0
        if not self.ground:
            self.yvec = self.gravity

    @classmethod
    def draw(self):
        sprites.add_sprites(self.st)
        sprites.add_floor(self.st)
        if self.fire1:
            sprites.add_sprites(self.cr)

    @classmethod
    def fire(self):
        load_sound('tank_fire.mp3').play()
        self.cr.rect.x, self.cr.rect.y = GetSystemMetrics(0) - 400, GetSystemMetrics(1) - 480
        self.fire1 = True


class villain(pygame.sprite.Sprite):
    @classmethod
    def __init__(self):
        self.time = datetime.datetime.utcnow() +datetime.timedelta(seconds=3)
        self.st = pygame.sprite.Sprite()
        self.speed = 0
        self.st.image = load_image('villain_1.png')
        self.st.rect = self.st.image.get_rect()
        self.st.rect.x, self.st.rect.y = GetSystemMetrics(0) - 400, GetSystemMetrics(1) - 530
        self.fire1 = False
        self.gravity = 10
        self.bomb = True
        self.ground = False
        self.cr = pygame.sprite.Sprite()
        self.cr.image = load_image('cart.png')
        self.cr.rect = self.cr.image.get_rect()
        self.bm = pygame.sprite.Sprite()
        self.bm.image = load_image('boom1.png')
        self.bm.rect = self.cr.image.get_rect()
        self.bm.rect.x, self.bm.rect.y = GetSystemMetrics(0) - 400, GetSystemMetrics(1) - 490

    @classmethod
    def collide(self, sprites):
        self.st.rect = self.st.rect.move(self.xvec, self.yvec)
        if pygame.sprite.spritecollideany(self.st, sprites):
            self.yvec = -self.yvec
            self.ground = True
        self.bm.rect = self.bm.rect.move(self.xb, self.yb)
        if pygame.sprite.spritecollideany(self.bm, sprites):
            self.xb = -self.xb
            self.bomb = False

    @classmethod
    def collide1(self, hero):
        if pygame.sprite.collide_mask(self.st, hero):
            self.st.rect.y += 5000
            self.cr.rect.y += 5000
            self.cr.rect.x += 50000
        if pygame.sprite.collide_mask(self.cr, hero):
            self.cr.rect.y += 5000
            self.cr.rect.x += 5000

    @classmethod
    def move(self):
        self.xb = self.yb = 0
        if self.fire1:
            self.cr.rect.x -= 100
        if self.bomb:
            if datetime.datetime.utcnow() > self.time:
                self.yb = 20
            else:
                self.xb = -30
                self.yb = -10
        if self.cr.rect.x < 0:
            self.fire1 = False
        sprites.add_patron(self.cr)
        self.st.image = load_image('villain_2.png')
        if not self.fire1:
            self.fire()
        self.xvec, self.yvec = -self.speed, 0
        if not self.ground:
            self.yvec = self.gravity

    @classmethod
    def draw(self):
        sprites.add_sprites(self.st)
        sprites.add_floor(self.st)
        if self.fire1:
            sprites.add_sprites(self.cr)
        sprites.add_sprites(self.bm)
        sprites.add_patron(self.bm)

    @classmethod
    def fire(self):
        self.fire1 = True
        self.cr.rect.x, self.cr.rect.y = GetSystemMetrics(0) - 400, GetSystemMetrics(1) - 505
        load_sound('villain_fire_' + str(randrange(1, 3)) + '.mp3').play()


def load_image(name, size_convert=False):
    fullname = os.path.join("PiedRunner_data", name)
    if not os.path.isfile(fullname):
        print(name, 'file isnt in folder(')
        sys.exit()
    image = pygame.image.load(fullname)
    if size_convert:
        image= pygame.transform.scale(
            image, (GetSystemMetrics(0),
                    GetSystemMetrics(1)))
    return image

def load_sound(name):
    fullname = os.path.join("PiedRunner_data", name)
    if not os.path.isfile(fullname):
        print(name, ' - isnt in folder(')
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound


class samurai(sprite.Sprite):
    @classmethod
    def __init__(self):
        self.width, self.height = 20, 20
        self.hero = pygame.sprite.Sprite() #создание спрайтов
        self.hp = pygame.sprite.Sprite()
        self.speed = 25
        self.jump = 80
        self.hero.image = Surface((load_image('hero_calm1.png').get_size()), pygame.SRCALPHA) #создание прозрачного прямоугольника нужных размеров
        self.hero.image.set_alpha(256)
        self.hero.rect = self.hero.image.get_rect()
        self.hero.rect.x, self.hero.rect.y = GetSystemMetrics(0) - 10, GetSystemMetrics(1) - 570
        self.gravity = 10
        self.hp_number = 100 #количество здоровья
        self.ground = False #состояние персонажа в воздухе он или на земле
        self.death = False

        self.anim_delay = 80 #fps проигывания анимаций
        self.animation_run_right = [('sam_run_1.png'), ('sam_run_2.png'), ('sam_run_3.png'),
                              ('sam_run_4.png'), ('sam_run_5.png'), ('sam_run_6.png'),
                                    ('sam_run_7.png'), ('sam_run_8.png'), ('sam_run_9.png'),
                                    ('sam_run_10.png')]
        self.animation_run_left = [('sam_run_1l.png'), ('sam_run_2l.png'), ('sam_run_3l.png'),
                                    ('sam_run_4l.png'), ('sam_run_5l.png'), ('sam_run_6l.png'),
                                    ('sam_run_7l.png'), ('sam_run_8l.png')]
        self.animation_wep_right = [('sam_wep_1.png'), ('sam_wep_2.png'), ('sam_wep_3.png'),
                                   ('sam_wep_4.png'), ('sam_wep_5.png'), ('sam_wep_6.png'),
                                   ('sam_wep_7.png'), ('sam_wep_8.png')]
        self.animation_wep_left = [('sam_wep_1l.png'), ('sam_wep_2l.png'), ('sam_wep_3l.png'),
                                   ('sam_wep_4l.png'), ('sam_wep_5l.png'), ('sam_wep_6l.png'),
                                   ('sam_wep_7l.png'), ('sam_wep_8l.png')]
        self.animation_jump_right = [('sam_jump_1.png'), ('sam_fall_1.png')]
        self.animation_jump_left = [('sam_jump_1l.png'), ('sam_fall_1l.png')]
        boltAnim = []
        for i in self.animation_jump_right:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimJumpRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpRight.play()
        boltAnim = []
        for i in self.animation_jump_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimJumpLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpLeft.play()
        self.boltAnimStay = pyganim.PygAnimation([(load_image('sam_calm1l.png'), self.anim_delay)])
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.hero.image, (0, 0))
        boltAnim = [] #список анимаций
        for i in self.animation_run_right:
            boltAnim.append((load_image(i), self.anim_delay)) #добавление пнг картинок для анимаций
        self.boltAnimRunright = pyganim.PygAnimation(boltAnim)
        self.boltAnimRunright.play() #создание анимации
        boltAnim = []
        for i in self.animation_run_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimRunLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimRunLeft.play()
        boltAnim = []
        for i in self.animation_wep_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepLeft.play()
        boltAnim = []
        for i in self.animation_wep_right:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepRight.play()
        boltAnim = []
        for i in self.animation_wep_left:
            boltAnim.append((load_image(i), self.anim_delay))
        self.boltAnimWepLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimWepLeft.play()

    @classmethod
    def get_position(self):
        return self.hero.rect.x

    @classmethod
    def draw(self):
        sprites.add_sprites(self.hero)

    @classmethod
    def move(self, left, right, up, down, screen):
        self.sam = pygame.sprite.Group()
        self.xvec, self.yvec = 0, 0
        self.attack = False #переменная для отслеживания атаки, чтобы анимация спокойствия не мешала анимации атаки
        if not self.ground:
            left = right = up = down = False #если он в воздухе, то двигаться в сторону и прыгать не может
            self.yvec += self.gravity
        if player.get_position() in range(self.hero.rect.x, self.hero.rect.x + 120):
            right = left = up = False
            self.attack = True
            self.attack1(True)
        if player.get_position() in range(self.hero.rect.x - 120, self.hero.rect.x):
            self.attack = True
            self.attack1(False)
        if left:
            self.hero.image = Surface((load_image('hero_run_1l.png').get_size()), pygame.SRCALPHA)
            self.hero.image.set_alpha(256)
            self.boltAnimRunLeft.blit(self.hero.image, (0, 0))
            self.xvec -= self.speed
        if right:
            self.hero.image = Surface((load_image('hero_run_1.png').get_size()), pygame.SRCALPHA)
            self.hero.image.set_alpha(256)
            self.xvec += self.speed
            self.boltAnimRunright.blit(self.hero.image, (0, 0))
        if up:
            if self.ground:
                if left:
                    self.hero.image = Surface((load_image('hero_jump_1l.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimJumpLeft.blit(self.hero.image, (0, 0))
                    self.yvec -= self.jump
                    self.xvec = -self.speed * 2
                if right:
                    self.xvec = self.speed * 2
                if not left:
                    self.hero.image = Surface((load_image('hero_jump_1.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimJumpRight.blit(self.hero.image, (0, 0))
                    self.yvec -= self.jump
        if down:
            pass
        if not down and not left and not right and not up and self.ground and not self.attack:
            if player.get_position() > self.hero.rect.x:
                self.hero.image = load_image('sam_calm1.png')
            else:
                self.hero.image = load_image('sam_calm1l.png')
        self.ground = False

    @classmethod
    def collide(self, sprites, fire):
        self.hero.rect = self.hero.rect.move(self.xvec, self.yvec)
        if pygame.sprite.spritecollideany(self.hero, sprites):
            self.yvec = -self.yvec
            self.ground = True
        if self.hp_number <= 0:
            self.hero.rect.x -= 3600
            load_sound('hero_win.mp3').play()
            self.hp_number = 100

    @classmethod
    def attack1(self, right):
        if self.ground:
            if right:
                for i in range(8):
                    self.hero.image = Surface((load_image('sam_wep_4.png').get_size()), pygame.SRCALPHA)
                    self.hero.image.set_alpha(256)
                    self.boltAnimWepRight.blit(self.hero.image, (0, 0))
            else:
                self.hero.image = Surface((load_image('hero_wep_4l.png').get_size()), pygame.SRCALPHA)
                self.hero.image.set_alpha(256)
                self.boltAnimWepLeft.blit(self.hero.image, (0, 0))
            load_sound('hero_attack_' + str(randrange(1, 4)) + '.mp3').play()
            self.sam.add(self.hero)
            player.collide_with_sam(self.sam)

    @classmethod
    def hit(self):
        self.hp_number -= 10


class running_infinity:
    @classmethod
    def __init__(self):
        self.new_map()

    @classmethod
    def new_map(self):
        self.choice_map() #выбор карты
        main_game(self.choice % 4, True)

    @classmethod
    def choice_map(self):
        self.choice = randrange(0, 4)

    @classmethod
    def update(self, target):
        if target.rect.x > GetSystemMetrics(0):
            self.new_map()




if __name__ == '__main__':
    main()