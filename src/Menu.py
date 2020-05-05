import pygame
import colors
import sys
from settings import *
from collections import deque


class Menu:
    def __init__(self, game):
        self.out = True
        self.color = (3, 252, 198)
        self.game = game
        self.fadeI = 0
        self.selections = [1, 0, 0]

    def new(self):
        self.selections = [1, 0]
        self.texts = [pygame.font.Font("pixelart.ttf", 48).render(CAPTION, 1, colors.WHITE), self.game.font.render("Start", 1, colors.WHITE),
                      self.game.font.render("Exit", 1, colors.WHITE), pygame.font.Font("pixelart.ttf", 12).render("Developed by Mumble. Team", 1, colors.WHITE)]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 273:
                    if self.selections[0]:
                        self.selections[1] = 1
                        self.selections[0] = 0
                    else:
                        self.selections[0] = 1
                        self.selections[1] = 0
                elif event.key == 274:
                    if self.selections[0]:
                        self.selections[1] = 1
                        self.selections[0] = 0
                    else:
                        self.selections[0] = 1
                        self.selections[1] = 0
                elif event.key == 27:
                    if self.game.playing:
                        self.game.playing = False
                    self.game.running = False
                elif event.key == 13:
                    i = 0
                    for i in range(len(self.selections)):
                        if self.selections[i]:
                            break
                    if i == 0:
                        self.game.inMenu = False
                    else:
                        if self.game.playing:
                            self.game.playing = False
                        self.game.running = False
        self.game.clock.tick(FPS)

    def draw(self):

        if self.color[2] == 255:
            self.out = False
        elif self.color[2] == 0:
            self.out = True
        self.color = list(self.color)
        if self.out:
            self.color[2] += 1
        else:
            self.color[2] -= 1
        self.color = tuple(self.color)
        self.game.screen.fill(self.color)
        t = [CAPTION, "Start", "Exit", "Developed by Mumble. Team"]
        rects = []
        y = 80
        i = 0
        self.texts = [pygame.font.Font("pixelart.ttf", 48).render(CAPTION, 1, colors.WHITE), self.game.font.render("Start", 1, colors.WHITE),
                      self.game.font.render("Exit", 1, colors.WHITE), pygame.font.Font("pixelart.ttf", 12).render("Developed by Mumble. Team", 1, colors.WHITE)]
        for i in range(len(self.selections)):
            if self.selections[i]:
                break
        self.texts[i+1] = self.game.font.render(t[i+1], 1, colors.BLACK)
        for text in self.texts:
            self.game.screen.blit(text, (WIDTH/2 - (text.get_rect()[2]/2), y))
            if y == 80:
                y = 300
            elif y >= 350:
                y = HEIGHT - 50
            else:
                y += 50
        howToText = pygame.font.Font("pixelart.ttf", 16).render(
            "Arrow keys for movements", 1, colors.WHITE)
        plantingText = pygame.font.Font("pixelart.ttf", 16).render(
            "Space for planting", 1, colors.WHITE)
        boostText = pygame.font.Font("pixelart.ttf", 16).render(
            "Shift for boosting", 1, colors.WHITE)
        self.game.screen.blit(
            howToText, (WIDTH/2 - (howToText.get_rect()[2]/2), 600))
        self.game.screen.blit(
            plantingText, (WIDTH/2 - (plantingText.get_rect()[2]/2), 620))
        self.game.screen.blit(
            boostText, (WIDTH/2 - (boostText.get_rect()[2]/2), 640))
        pygame.display.update()
