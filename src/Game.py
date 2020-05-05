import pygame
import settings
import colors
import random
import time
from sprites import *
from Menu import Menu


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.score = 0
        self.running = True
        self.playing = False
        self.inMenu = True
        self.noAbuse = True
        self.firstTime = True
        self.menu = Menu(self)
        self.isOnAPlatform = None
        self.platformTouched = 0
        self.font = pygame.font.Font("pixelart.ttf", 32)
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()

    def new(self):
        pygame.mixer.Channel(0).set_volume(0.1)
        self.menu.new()
        self.score = 0
        self.platformTouched = 0
        self.noAbuse = True
        self.firstTime = True
        self.boost = 0
        self.platformCounter = 0

        backgroundImage = pygame.image.load('../img/background.png')

        self.background = pygame.transform.scale(backgroundImage,
                                                 (int(backgroundImage.get_size()[0]*8), int(backgroundImage.get_size()[1]*8)))

        self.bW, self.bH = self.background.get_size()
        self.bX = 0
        self.bY = 0
        self.x1 = 0
        self.y1 = -self.bH + HEIGHT
        self.platforms = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.seeds = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.player = Player(self)
        self.sprites.add(self.player)
        p1 = Platform(WIDTH / 2 - 50, HEIGHT/2 + 150, 100, 20)
        p1.seeded = True
        p1.image.fill(colors.RED)
        p1.image.get_rect().midbottom = (WIDTH / 2, HEIGHT/2 + 100)
        p1.time = pygame.time.get_ticks()
        self.platforms.add(p1)
        self.sprites.add(p1)
        s = Seed(250, 250)
        self.seeds.add(s)
        self.sprites.add(s)

    def run(self):
        while self.running:
            self.new()
            self.playing = True
            if self.inMenu:
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('../sound/home.ogg'), loops=-1)
            while self.inMenu and self.running:
                self.menu.draw()
                self.menu.update()
            if self.firstTime:
                self.firstTime = False
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('../sound/game.ogg'), loops=-1)
            while self.playing:
                self.events()
                self.update()
                self.draw()
                self.clock.tick(settings.FPS)

    def update(self):
        self.isOnAPlatform = pygame.sprite.spritecollide(
            self.player, self.platforms, False)
        takeSeed = pygame.sprite.spritecollide(
            self.player, self.seeds, False)
        if self.player.jumping:
            for _ in range(abs(settings.NPLATFORM - self.platformCounter)):
                self.platformCounter += 1
                p = None
                while True:
                    isGood = True
                    p = Platform(random.randint(0, WIDTH-100), random.randint(
                        0, int(self.player.pos.y)) - 50, random.randint(50, 100), 20)
                    if not pygame.sprite.spritecollide(p, self.platforms, True):
                        for platform in self.platforms:
                            if abs(p.rect.y - platform.rect.y) <= 40 and abs(p.rect.x - platform.rect.x) <= 40:
                                isGood = False
                                break
                    else:
                        isGood = False
                        p.kill()
                    if isGood:
                        break

                self.platforms.add(p)
                self.sprites.add(p)
        if len(self.seeds) < 5:
            r = random.randint(0, 250)
            if r == 420 or r == 17 or r == 99 or r == 200:
                s = None
                while True:
                    s = Seed(random.randint(0, WIDTH),
                             random.randint(0, int(self.player.pos.y)))
                    if not pygame.sprite.spritecollide(s, self.seeds, False) and not pygame.sprite.spritecollide(s, self.platforms, False):
                        break
                self.seeds.add(s)
                self.sprites.add(s)
        if takeSeed:
            pygame.mixer.Channel(1).play(
                pygame.mixer.Sound('../sound/tick.ogg'))
            self.player.seedCounter += 1
            takeSeed[0].kill()
            del takeSeed[0]
        if self.isOnAPlatform:
            if not self.isOnAPlatform[0].used:
                self.score += 1
                self.isOnAPlatform[0].used = True
                self.platformTouched += 1
            self.noAbuse = False
            self.player.lastTouched = self.isOnAPlatform[0]
        if self.player.lastTouched and self.player.lastTouched.used and not self.player.lastTouched.seeded:
            if self.player.lastTouched.time is not None:
                self.player.lastTouched.rect.y += 10
                if not self.player.lastTouched.p:
                    self.player.lastTouched.p = True
                    pygame.mixer.Channel(2).play(
                        pygame.mixer.Sound('../sound/p.wav'))
                if pygame.time.get_ticks() - self.player.lastTouched.time >= 300:
                    self.player.lastTouched.kill()
                    self.platformCounter -= 1
                    self.player.lastTouched = None
            else:
                self.isOnAPlatform[0].time = pygame.time.get_ticks()

        if self.player.rect.y < HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for platfrom in self.platforms:
                platfrom.rect.y += abs(self.player.vel.y)
                if platfrom.rect.y > HEIGHT:
                    platfrom.kill()
                    self.platformCounter -= 1
                    del platfrom
            for seed in self.seeds:
                seed.rect.y += abs(self.player.vel.y)
                if seed.rect.y > HEIGHT:
                    seed.kill()
                    del seed
            for tree in self.trees:
                tree.y += abs(self.player.vel.y)
                if tree.y > HEIGHT:
                    tree.kill()
                    del tree
        for tree in self.trees:
            tree.update()
        if self.player.pos.y > HEIGHT + 50:
            time.sleep(0.75)
            self.playing = False
            self.inMenu = True
        self.sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.new()
                elif event.key == 27:
                    self.inMenu = True
                    self.playing = False
                elif event.key == pygame.K_s or event.key == pygame.K_SPACE:
                    if self.player.seedCounter:
                        if self.player.lastTouched and self.player.lastTouched.time and pygame.time.get_ticks() - self.player.lastTouched.time <= 300:
                            if not self.player.lastTouched.seeded:
                                pygame.mixer.Channel(1).play(
                                    pygame.mixer.Sound('../sound/seed.wav'))
                                self.player.lastTouched.seeded = True
                                self.player.lastTouched.sow()
                                self.score += 4
                                self.boost += 1
                                self.player.seedCounter -= 1
                                t = Tree(self.player.rect.x,
                                         self.player.lastTouched.rect.y - 50)
                                t.time = pygame.time.get_ticks()
                                self.trees.add(t)
                                self.sprites.add(t)
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    if self.boost and not self.noAbuse:
                        if self.platformTouched >= 3:
                            pygame.mixer.Channel(1).play(
                                pygame.mixer.Sound('../sound/boost.ogg'))
                            self.noAbuse = True
                            self.boost -= 1
                            self.player.vel.y -= 20
                            self.platformTouched = 0

    def draw(self):
        self.screen.fill(colors.BLACK)
        self.y1 += 1
        self.bY += 1
        self.screen.blit(self.background, (self.bX, self.bY))
        self.screen.blit(self.background, (self.x1, self.y1))
        if self.bY > self.bH - HEIGHT:
            self.bY = -self.bH + HEIGHT/4*3
        if self.y1 > self.bH:
            self.y1 = -self.bH + HEIGHT/4*3
        self.sprites.draw(self.screen)
        if self.platformTouched >= 3 and self.boost:
            self.scoreText = self.font.render(str(self.score), 1, colors.BLUE)
        else:
            self.scoreText = self.font.render(str(self.score), 1, colors.WHITE)
        self.seedText = pygame.font.Font("pixelart.ttf", 16).render(
            str(self.player.seedCounter), 1, colors.WHITE)
        self.boostText = pygame.font.Font("pixelart.ttf", 16).render(
            str(self.boost), 1, colors.WHITE)
        self.screen.blit(self.seedText, (WIDTH/2 - (self.scoreText.get_rect()
                                                    [2]/2)*2 - (self.seedText.get_rect()[2]/2), HEIGHT - 84))
        self.screen.blit(self.scoreText, (WIDTH/2 -
                                          (self.scoreText.get_rect()[2]/2), HEIGHT - 100))
        self.screen.blit(self.boostText, (WIDTH/2 + (self.scoreText.get_rect()
                                                     [2]/2)*2 + (self.boostText.get_rect()[2]/2), HEIGHT - 84))

        pygame.display.update()
