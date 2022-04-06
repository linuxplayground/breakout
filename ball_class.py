import pygame
from random import choice
from particles import Trail
from settings import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.radius = 4
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.Surface((8,8))
        self.trail_group = pygame.sprite.Group()

        pygame.draw.circle(self.image, GREY, (4,4), self.radius)
        # self.image.fill(GREY)
        self.rect = self.image.get_rect(midbottom = pos)
    
        self.speed = SPEED
        self.set_initial_dir()

    def set_initial_dir(self):
        self.dir = pygame.math.Vector2(choice([-0.5, 0.5]), -1)

    def update(self, playing, player_pos):
        if not playing:

            self.pos.y = HEIGHT - 17
            self.pos.x = player_pos.x
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
        else:
            self.pos += self.dir.normalize() * self.speed
            self.rect.center = self.pos

    def draw(self, screen, playing = False):
        screen.blit(self.image, self.rect)
        if playing:
            self.trail_group.add(Trail(self.pos, GREY, screen, self.dir))
            self.trail_group.update()