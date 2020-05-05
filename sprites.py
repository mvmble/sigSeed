import pygame
from settings import *
import colors

vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.images = []
        self.images_right = []
        self.images_right.append(pygame.image.load("./img/p0.png"))
        self.images_right.append(pygame.image.load("./img/p1.png"))
        self.images_right.append(pygame.image.load("./img/p2.png"))
        self.images_right.append(pygame.image.load("./img/p3.png"))
        self.images_right = [pygame.transform.scale(
            image, (int(image.get_size()[0]/2), int(image.get_size()[1]/2))) for image in self.images_right]
        self.ctime = 0
        self.images = self.images_right
        self.images_left = [pygame.transform.flip(
            image, True, False) for image in self.images_right]
        self.index = 0
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.jumping = False
        self.lastTouched = False
        self.rect.midbottom = (WIDTH / 2, HEIGHT / 2)
        self.pos = vector(WIDTH / 2, HEIGHT / 2)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.seedCounter = 0
        self.oldTouchedPlatform = None
        self.lastTouched = None

    def update(self):
        self.ctime += 0.064
        if self.ctime >= 1:
            self.index += 1
            self.ctime = 0
            if self.index >= len(self.images):
                self.index = 0
            if self.vel.x > 0:
                self.images = self.images_right
            elif self.vel.x < 0:
                self.images = self.images_left
        self.image = self.images[self.index]
        self.jump()
        self.acc = vector(0, 0.5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -P_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = P_ACC
        self.acc.x += self.vel.x * P_FRI
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        if pygame.sprite.spritecollide(self, self.game.platforms, False) and self.vel.y > -5:
            self.jumping = True
            self.vel.y = - 20
        elif self.game.isOnAPlatform:
            self.game.score -= 1
            self.game.isOnAPlatform[0].used = False
            self.game.isOnAPlatform[0].time = None
            self.game.isOnAPlatform = None


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(colors.MARRONE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self. p = False
        self.used = False
        self.seeded = False
        self.time = None

    def sow(self):
        self.image.fill(colors.MARRONE)


class Seed(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./img/seed.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.state = 0
        self.x = x
        self.y = y
        self.ctime = 0
        self.update()

    def update(self):
        if self.state <= 2:
            self.ctime += 0.096
        if self.ctime >= 1 and self.state <= 2:
            self.state += 1
            self.ctime = 0
        self.image = pygame.image.load(
            "./img/tree/" + str(self.state) + ".png").convert_alpha()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(
            self.image, (int(self.size[0]*4), int(self.size[1]*4)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.time = pygame.time.get_ticks()
