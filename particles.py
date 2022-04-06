import pygame
import random

def reduceColor(rgb, step):
    r = rgb[0] - step if rgb[0] - step >= 0 else 0
    g = rgb[1] - step if rgb[1] - step >= 0 else 0
    b = rgb[2] - step if rgb[2] - step >= 0 else 0
    return (r,g,b)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, win, color):
        super(Explosion, self).__init__()
        self.x = x
        self.y = y
        self.win = win
        self.color = color
        self.size = random.randint(4,8)
        self.life = 20
        self.lifetime = 0

        self.x_vel = random.randrange(-2, 2)
        self.y_vel = random.randrange(-5, -1)
        self.gravity = 1

            
    def update (self):
        self.gravity += 0.5
        self.size -= 0.2
        self.lifetime += 1
        # self.color = reduceColor(self.color, 6)
        if self.lifetime <= self.life:
            self.x += self.x_vel
            self.y += self.y_vel + self.gravity
            s = int(self.size)
            pygame.draw.rect(self.win, self.color, (self.x - self.size // 2, self.y - self.size // 2, self.size, self.size))
        else:
            self.kill()

class Trail(pygame.sprite.Sprite):
    def __init__(self, pos, color, win, rel):
        super(Trail, self).__init__()
        self.p = pos
        self.color = color
        self.win = win

        self.x, self.y = self.p.x, self.p.y
        rel_normal = rel.normalize() if rel.x != 0 or rel.y != 0 else rel
        xm = rel_normal.x
        xy = rel_normal.y
        
        self.dx = xm
        self.dy = xy
        self.size = 4

        self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.size)

    def update(self):
        self.x -= self.dx
        self.y -= self.dy
        self.size -= 0.5

        if self.size <= 0:
            self.kill()

        self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.size)