import os
import sys

from game_objects import *

all_sprites = pygame.sprite.Group()
all_platforms = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_portals = pygame.sprite.Group()
all_knives = pygame.sprite.Group()
pygame.mixer.init()  # добавляем музыку
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.04)
levels = ['level1.txt', 'level2.txt']
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.init()


def start_screen():
    intro_text = ["                                                              ITS MEEE MAAAARIOOO", "",
                  "                                                             Правила и управление игры:",
                  "                                             Стрелочки работают по своему назначению :)",
                  "                                             SPACE - начать игру и перезапустить её",
                  "                                             Правила: не использовать баги, ",
                  "                                                               убить врагов обязательно ,",
                  "                                               наслаждаться музычкой и радоваться жизни <3"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    pygame.display.set_caption("Mario")
    player = generate_level(load_level(levels[0]))
    bg = load_image('bg.jpg')
    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    end = load_image('game over.png')
    end = pygame.transform.scale(end, (WIN_WIDTH, WIN_HEIGHT))
    win = load_image('win.jpg')
    win = pygame.transform.scale(win, (WIN_WIDTH, WIN_HEIGHT))
    current_level_index = 0
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
                if event.key == pygame.K_SPACE:
                    clear_text()
                    player = generate_level(load_level(levels[0]))
                    current_level_index = 0
                    player.platforms = all_platforms
                    bg = load_image('bg.jpg')
                    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))

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

        if pygame.sprite.spritecollide(player, all_knives, False):
            for knife in all_knives:
                player.can_kill = True
                player.image = player.image_kn
                knife.kill()

        if pygame.sprite.spritecollide(player, all_enemies, False):
            for enemy in pygame.sprite.spritecollide(player, all_enemies, False):
                if player.can_kill:
                    enemy.kill()
                else:
                    cursor = pygame.sprite.Sprite(all_sprites)
                    cursor.image = end
                    cursor.rect = cursor.image.get_rect()

        if pygame.sprite.spritecollide(player, all_portals, False):
            clear_text()
            current_level_index += 1
            if current_level_index == len(levels):
                cursor = pygame.sprite.Sprite(all_sprites)
                cursor.image = win
                cursor.rect = cursor.image.get_rect()
            else:
                player = generate_level(load_level(levels[current_level_index]))
                player.platforms = all_platforms
                bg = load_image('bg.jpg')
                bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))

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
            elif col == "&":
                en = Enemy(x, y)
                all_sprites.add(en)
                all_enemies.add(en)
            elif col == "*":
                po = Portals(x, y)
                all_sprites.add(po)
                all_portals.add(po)
            if col == "!":
                kn = Knife(x, y)
                all_sprites.add(kn)
                all_knives.add(kn)
            x += PL_WIDTH
        y += PL_HEIGHT
        x = 0
    # вернем игрока
    return new_player


def clear_text():
    all_sprites.empty()
    all_platforms.empty()
    all_enemies.empty()
    all_portals.empty()


start_screen()
if __name__ == "__main__":
    sys.exit(main())
