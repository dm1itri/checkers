import pygame
from additional_functions.load_image import load_image
import sys
import copy

WHITE = 'white'
BLACK = 'black'
COLOR = WHITE
MY_COLOR = WHITE
main_font = None
COUNT_WHITE_KILLED = 0
COUNT_BLACK_KILLED = 0


# def load_board(filename):
#     filename = "data/" + filename
#     # читаем уровень, убирая символы перевода строки
#     try:
#         with open(filename, 'r') as mapFile:
#             level_map = [line.strip() for line in mapFile]
#     except FileNotFoundError:
#         print(f'Файл {filename} не найден')
#         return False
#     # и подсчитываем максимальную длину
#     max_width = max(map(len, level_map))
#
#     # дополняем каждую строку пустыми клетками ('.')
#     maps = list(map(lambda x: list(x.ljust(max_width, '.')), level_map))
#     return maps


def color_opponent():
    if COLOR == BLACK:
        return WHITE
    return BLACK


def check_wqueen(board):  # проверка есть ли белые шашки расположенные на линии дамок
    sp = []
    for i in range(1, 8, 2):
        b = board[0][i]
        if b is not None:
            if b.color == WHITE and b.__class__.__name__ == 'Usual':
                sp.append(i)
    return sp


def check_bqueen(board):
    sp = []
    for i in range(0, 7, 2):
        b = board[7][i]
        if b is not None:
            if b.color == BLACK and b.__class__.__name__ == 'Usual':
                sp.append(i)
    return sp


class Shapes(pygame.sprite.Sprite):
    # image = load_image("white.png")

    def __init__(self, group, color):
        super().__init__(group)
        self.color = color
        self.image = load_image("white.png" if color == WHITE else "black.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def kill(self):
        all_sprites.remove(self)


# class GameOver(pygame.sprite.Sprite):
#     image = load_image("gameover.png")
#
#     def __init__(self, group):
#         # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
#         # Это очень важно !!!
#         super().__init__(group)
#         self.image = GameOver.image
#         self.rect = self.image.get_rect()
#         self.width = self.rect.width
#         self.rect.x = -self.width
#         self.rect.y = 0
#         self.right = True
#
#     def update(self, *args):
#         if self.rect.x == 0:
#             self.right = False
#         if self.right:
#             self.rect.x += 1


class Queen(Shapes):
    def __init__(self, group, color):
        super().__init__(group, color)
        self.image = load_image("white_queen.png" if color == WHITE else "black_queen.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

    def can_move(self, board, x, y, pos_att):
        sp_kill = []
        for i, j in pos_att:
            sp_kill1 = []
            if abs(j - y) == abs(i - x) and board[j][i] is None:
                for i1 in range(1, abs(j - y) + 1):
                    iv = -i1 if j < y else i1
                    ih = -i1 if i < x else i1
                    if board[y + iv][x + ih] is not None:
                        if board[y + iv][x + ih].color == COLOR:
                            return False
                        sp_kill1.append([x + ih, y + iv])

                if len(sp_kill1) > 1:
                    return False
                sp_kill.extend(sp_kill1)
                x, y = i, j
            else:
                return False

        if sp_kill == []:  # было sp_kill is []
            return 1

        return sp_kill


class Usual(Shapes):
    def can_move(self, board, x, y, pos_att):
        if (pos_att[0][0] == x + 1 or pos_att[0][0] == x - 1) and pos_att[0][1] == y + 1\
                and len(pos_att) == 1 and self.color == BLACK:
            if board[pos_att[0][1]][pos_att[0][0]] is None:
                return 1

        elif (pos_att[0][0] == x + 1 or pos_att[0][0] == x - 1) and pos_att[0][1] == y - 1\
                and len(pos_att) == 1 and self.color == WHITE:
            if board[pos_att[0][1]][pos_att[0][0]] is None:
                return 1

        else:
            sp_kill = []
            print('can_move: ', pos_att)
            for i, j in pos_att:
                print('wbrk')
                if (i == x + 2 or i == x - 2) and (j == y + 2 or j == y - 2) and board[j][i] is None:
                    kill = board[(j + y) // 2][(i + x) // 2]
                    print('kill: ', (j + y) // 2, (i + x) // 2)
                    if kill is None:
                        return False

                    if kill.color == COLOR:
                        return False

                    sp_kill.append([(i + x) // 2, (j + y) // 2])
                    x, y = i, j
            return sp_kill


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[None] * 8 for _ in range(8)]

        self.field[0][1] = Usual(all_sprites, BLACK)
        self.field[0][3] = Usual(all_sprites, BLACK)
        self.field[0][5] = Usual(all_sprites, BLACK)
        self.field[0][7] = Usual(all_sprites, BLACK)
        self.field[1][0] = Usual(all_sprites, BLACK)
        self.field[1][2] = Usual(all_sprites, BLACK)
        self.field[1][4] = Usual(all_sprites, BLACK)
        self.field[1][6] = Usual(all_sprites, BLACK)
        self.field[2][1] = Usual(all_sprites, BLACK)
        self.field[2][3] = Usual(all_sprites, BLACK)
        self.field[2][5] = Usual(all_sprites, BLACK)
        self.field[2][7] = Usual(all_sprites, BLACK)
        self.field[5][0] = Usual(all_sprites, WHITE)
        self.field[5][2] = Usual(all_sprites, WHITE)
        self.field[5][4] = Usual(all_sprites, WHITE)
        self.field[5][6] = Usual(all_sprites, WHITE)
        self.field[6][1] = Usual(all_sprites, WHITE)
        self.field[6][3] = Usual(all_sprites, WHITE)
        self.field[6][5] = Usual(all_sprites, WHITE)
        self.field[6][7] = Usual(all_sprites, WHITE)
        self.field[7][0] = Usual(all_sprites, WHITE)
        self.field[7][2] = Usual(all_sprites, WHITE)
        self.field[7][4] = Usual(all_sprites, WHITE)
        self.field[7][6] = Usual(all_sprites, WHITE)
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 70
        self.mouse_coords = []

    # настройка внешнего вида  (пока не тестировалось)
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, my_color, network, sounds):
        self.my_color = my_color
        self.network = network
        self.sounds = sounds

        screen.fill('#368613')  # если не нравится, то меняй, я не уверен в этом цвете (была просто черная заливка)
        screen.fill('#ac9362', (
            self.left - 10, self.top - 10, self.cell_size * self.width + 20, self.cell_size * self.height + 20))
        font = pygame.font.Font(None, 40)

        font = pygame.font.Font(main_font, 35)
        text = font.render(f"{'Ваш ход' if COLOR == my_color else 'Ход противника'}", True, (255, 255, 255))
        screen.blit(text, (500 // 2 - (text.get_size()[0] // 2), 10))

        text = font.render(f"{COUNT_BLACK_KILLED}", True, (255, 255, 255))
        screen.blit(text, (self.left + 0.5 * self.cell_size * self.width - text.get_width() - 5,
                           self.top + self.cell_size * self.height + 10))
        text = font.render(":", True, '#964b00')
        screen.blit(text,
                    (self.left + 0.5 * self.cell_size * self.width - 1, self.top + self.cell_size * self.height + 10))
        text = font.render(f"{COUNT_WHITE_KILLED}", True, (0, 0, 0))
        screen.blit(text,
                    (self.left + 0.5 * self.cell_size * self.width + 10, self.top + self.cell_size * self.height + 10))
        text = font.render(f"Вы играете за {'белых' if my_color == WHITE else 'черных'}", True, (255, 255, 255))
        screen.blit(text,
                    (500 // 2 - (text.get_size()[0] // 2), self.top + self.cell_size * self.height + 50))

        font = pygame.font.Font(None, 17)
        text = font.render(
            f"A{''.join(' ' for i in range(13))}B              C              D              E              F              G              H",
            True, (0, 0, 0))
        screen.blit(text, (self.left + self.cell_size / 2, 40))
        for i in range(1, 9):
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (self.left - 8, self.top + self.cell_size * (i - 0.5)))

        for i in range(self.height):
            for j in range(self.width):
                if i % 2:
                    color = '#f5f5dc' if j % 2 else '#964b00'
                else:
                    color = '#f5f5dc' if j % 2 == 0 else '#964b00'
                screen.fill(pygame.Color(color),
                            (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size,
                             self.cell_size), 0)
                if self.field[i][j]:
                    checker = self.field[i][j]
                    checker.rect.x = self.left + self.cell_size * j
                    checker.rect.y = self.top + self.cell_size * i

                    # if self.field[i][j].__class__.__name__ == 'Queen':
                    #     checker.image = load_image("white_queen.png" if checker.color == WHITE else "black_queen.png")

        if self.mouse_coords:
            x, y = self.mouse_coords[0]
            if self.field[y][x]:
                if self.field[y][x].color == self.my_color:
                    screen.fill('blue', (
                        self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.cell_size))

                    for i in range(self.height):
                        for j in range(self.width):
                            if self.field[y][x].can_move(self.field, x, y, ([j, i],)):
                                screen.fill('green',
                                            (self.left + self.cell_size * j, self.top + self.cell_size * i,
                                             self.cell_size, self.cell_size))

    def move(self, x, y, pos_att, mine):
        global COUNT_WHITE_KILLED, COUNT_BLACK_KILLED
        x1, y1, pos_att1 = x, y, pos_att

        if len(pos_att) < 1:
            return False
        for i, j in pos_att:
            if i > 7 or i < 0 or j < 0 or j > 7:
                return False

        print(x, y, pos_att)
        s = self.field[y][x]
        print(self.field)
        print('вошел в move', s)

        if s is None:
            return False
        if s.color != self.my_color and mine:
            return False

        rez = s.can_move(self.field, x, y, pos_att)
        print(rez)
        if not rez:
            return False
        if rez == 1:
            checker = self.field[y][x]
            self.field[y][x] = None

            self.animation(checker, x, y, pos_att[0][0], pos_att[0][1])
            self.field[pos_att[0][1]][pos_att[0][0]] = checker

        elif len(rez) == len(pos_att):  # при атаке должно совпадать кол-во убранных шашек с кол-вом позиций атак
            checker = self.field[y][x]
            self.field[y][x] = None
            for i in range(len(pos_att)):
                if i:
                    pygame.time.wait(300)
                rez_i = rez[i]
                pos_att_i = pos_att[i]
                self.field[rez_i[1]][rez_i[0]].kill()
                self.field[rez_i[1]][rez_i[0]] = None

                self.animation(checker, x, y, pos_att_i[0], pos_att_i[1])
                x, y = pos_att_i
            self.field[pos_att[-1][1]][pos_att[-1][0]] = checker
            if COLOR == BLACK:
                COUNT_WHITE_KILLED += len(rez)
            else:
                COUNT_BLACK_KILLED += len(rez)
        else:
            return False
        sp_bq = check_bqueen(self.field)
        sp_wq = check_wqueen(self.field)
        print(sp_wq, sp_bq)
        for i in sp_bq:
            self.field[7][i].kill()
            self.field[7][i] = Queen(all_sprites, BLACK)
        for i in sp_wq:
            self.field[0][i].kill()
            self.field[0][i] = Queen(all_sprites, WHITE)
            print(2)
        if mine and self.network is not None:
            print('до отправки')
            data = self.network.send(send_move((x1, y1), pos_att1))
            print('после отправки')
        return True

    def animation(self, checker, x, y, x1, y1):
        '''Анимация перемещения шашек'''
        if self.sounds['on_sounds']:
            self.sounds['move'].play(0)

        delta_x = (x1 - x) * 0.1 * self.cell_size
        delta_y = (y1 - y) * 0.1 * self.cell_size
        for i in range(10):
            checker.rect.x += delta_x
            checker.rect.y += delta_y
            self.render(screen, self.my_color, self.network, self.sounds)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(50)

    def bot_move(self):
        """ИИ для бота"""
        return False

    def load_sprites(self, group):
        for lst_sprites in list(map(lambda x: list(filter(lambda y: y is not None, x)), self.field)):
            for sprite in lst_sprites:
                group.add(sprite)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos[0], mouse_pos[1]
        if self.left <= x <= self.left + self.width * self.cell_size and\
                self.top <= y <= self.top + self.height * self.cell_size:
            for i in range(self.height):
                for j in range(self.width):
                    if self.left + self.cell_size * j <= x <= self.left + self.cell_size * (j + 1) and\
                            self.top + self.cell_size * i <= y <= self.top + self.cell_size * (i + 1):
                        return j, i
        else:
            return None

    def on_click(self, cell_coords):
        global COLOR
        if cell_coords is not None:
            if len(self.mouse_coords) >= 1:
                # если второй раз нажимаешь на одну и ту же клетку
                if len(self.mouse_coords) == 1 and self.mouse_coords[-1] == cell_coords:
                    self.mouse_coords = []
                    return
                self.mouse_coords.append(cell_coords)
                if self.move(self.mouse_coords[0][0], self.mouse_coords[0][1], self.mouse_coords[1:], True):
                    COLOR = color_opponent()
                self.mouse_coords = []
            else:
                self.mouse_coords = [cell_coords]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def load_move(data):
    if data == 'None':
        return False
    print(f'{data} = data')

    data = data.split('%')
    last = int(data[0]), int(data[1])
    new = list(map(int, data[2:]))
    new = [(new[i], new[i + 1]) for i in range(0, len(new), 2)]
    return last, new


def send_move(last, new):
    new = '%'.join('%'.join([str(i[0]), str(i[1])]) for i in new)
    return '%'.join([str(last[0]), str(last[1]), new])


pygame.init()
size = None
# screen — холст, на котором нужно рисовать:
screen = None
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
board = None


def online_run(network, MY_COLOR, color, sounds):
    global screen, all_sprites, clock, COLOR, COUNT_WHITE_KILLED, COUNT_BLACK_KILLED
    try:

        COUNT_WHITE_KILLED = 0
        COUNT_BLACK_KILLED = 0
        COLOR = color

        flag_winner = None
        flag_quit = False

        pygame.init()
        size = 500, 550
        # screen — холст, на котором нужно рисовать:
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Шашки')
        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()

        board = Board(8, 8)
        board.set_view(50, 50, 50)
        board.load_sprites(all_sprites)

        screen.fill((0, 0, 0))
        board.render(screen, MY_COLOR, network, sounds)
        all_sprites.draw(screen)
        pygame.display.flip()
        running = True
        count_fps = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    flag_quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if COLOR == MY_COLOR:
                        if event.button == 1:
                            board.get_click(event.pos)
                        elif event.button == 3:
                            board.mouse_coords.append(board.get_cell(event.pos))
                    print(board.mouse_coords)

            count_fps += 1
            if count_fps % 100 == 0:
                data = network.send('get_move')
                print(data)
                if data == 'end':
                    print('вышел', COUNT_WHITE_KILLED, COUNT_BLACK_KILLED)
                    break

                elif COLOR != MY_COLOR:
                    if count_fps % 100 == 0:
                        if data is not None and data != 'None' and data != '-':
                            if load_move(data):
                                last, new = load_move(data)
                                board.move(last[0], last[1], new, False)
                                COLOR = color_opponent()

            flag_winner = winner(MY_COLOR)
            if flag_winner is not None:
                network.send('winner')
                running = False
                continue

            screen.fill((0, 0, 0))
            board.render(screen, MY_COLOR, network, sounds)
            all_sprites.draw(screen)
            pygame.display.flip()

        if flag_quit:
            network.send('end')
        network.close()
        return flag_winner

    except Exception as E:
        print(E)


def offline_run(sounds):
    global screen, all_sprites, board, clock, nlo_sprites, nlo, FPS, COLOR
    pygame.init()
    FPS = 50
    size = 500, 550
    COLOR = WHITE
    MY_COLOR = WHITE
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шашки')
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    nlo_sprites = pygame.sprite.Group()

    board = Board(8, 8)
    board.set_view(50, 50, 50)

    board.render(screen, MY_COLOR, None, sounds)
    all_sprites.draw(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if COLOR == MY_COLOR:
                    if event.button == 1:
                        board.get_click(event.pos)
                    elif event.button == 3:
                        board.mouse_coords.append(board.get_cell(event.pos))

        if COLOR != MY_COLOR:
            board.bot_move()

        board.render(screen, MY_COLOR, None, sounds)
        all_sprites.draw(screen)
        pygame.display.flip()


def winner(MY_COLOR):
    if COUNT_BLACK_KILLED == 12:
        if MY_COLOR == WHITE:
            return True
        else:
            return False

    if COUNT_WHITE_KILLED == 12:
        if MY_COLOR == BLACK:
            return True
        else:
            return False
    return None


def remove_spites(group):
    for sprite in group:
        sprite.kill()
