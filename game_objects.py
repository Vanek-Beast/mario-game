import pygame
from constants import *


class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self, x, y):  # инициализация игрока
        super().__init__()
        self.image = pygame.image.load('data/hum.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PL_WIDTH, PL_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, PL_WIDTH, PL_HEIGHT)

        self.change_x = 0  # передвижение по горизонтали
        self.change_y = 0  # передвижение по вертикали
        self.platforms = pygame.sprite.Group()  # все платформы

    def gravity(self):  # гравитация
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.5
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y > 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height

    def update(self):
        self.gravity()
        self.rect.x += self.change_x

        # Список платформ, с которыми мы столкнулись по горизонтали
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if pygame.sprite.collide_mask(self, block):
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

        # Передвигаемся вверх/вниз
        self.rect.y += self.change_y

        # Список платформ, с которыми мы столкнулись по вертикали
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if pygame.sprite.collide_mask(self, block):
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                self.change_y = 0

    def jump(self):
        self.rect.y += 5  # спускаемся вниз, чтобы удедиться, что под нами есть платформа
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 5

        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -14

    def go_left(self):
        self.change_x -= 6
        if self.right:
            self.flip()
            self.right = False

    def go_right(self):
        self.change_x += 6
        if not self.right:
            self.flip()
            self.right = True

    def stop(self):
        self.change_x = 0

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("data/pl.png")
        self.image = pygame.transform.scale(self.image, (PL_WIDTH, PL_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, PL_WIDTH, PL_HEIGHT)

