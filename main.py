import os
import sys
from game_objects import *
from constants import *
import pygame


all_sprites = pygame.sprite.Group()
all_platforms = pygame.sprite.Group()


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Mario")
    player = generate_level(load_level('level1.txt'))
    clock = pygame.time.Clock()
    bg = load_image('bg.jpg')
    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    player.platforms = all_platforms
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # обновление спрайтов
        all_sprites.update()

        # Ограничение по правой стороне
        if player.rect.right > WIN_WIDTH:
            player.rect.right = WIN_WIDTH

        # Ограничение по левой стороне
        if player.rect.left < 0:
            player.rect.left = 0

        # Рисуем объекты на окне
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        # обновление экрана
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    fullname = os.path.join('data', filename)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    # читаем уровень, убирая символы перевода строки
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # дополняем каждую строку пустыми клетками ('.')
    return level_map


def generate_level(level):
    new_player = None
    x = y = 0
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                all_sprites.add(pf)
                all_platforms.add(pf)
            elif col == '@':
                new_player = Player(x, y)
                all_sprites.add(new_player)
            x += PL_WIDTH
        y += PL_HEIGHT
        x = 0
    # вернем игрока
    return new_player


if __name__ == "__main__":
    sys.exit(main())
