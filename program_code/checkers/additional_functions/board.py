import pygame
from additional_functions.load_image import load_image
from sqlite3 import connect
from math import modf

WHITE = 'white'
BLACK = 'black'
COLOR = WHITE
MY_COLOR = WHITE
main_font = '../../program_code/checkers/additional_functions/data/fonts/main.ttf'
COUNT_WHITE_KILLED = 0
COUNT_BLACK_KILLED = 0


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

    def __init__(self, group, color, size):
        super().__init__(group)
        self.color = color
        self.image = load_image("white.png" if color == WHITE else "black.png")
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def kill(self):
        all_sprites.remove(self)


class Queen(Shapes):
    def __init__(self, group, color, size):
        super().__init__(group, color, size)
        self.image = load_image("white_queen.png" if color == WHITE else "black_queen.png")
        self.image = pygame.transform.scale(self.image, size)

    def can_move(self, board, x, y, pos_att, mine, offline):
        sp_kill = []
        for i, j in pos_att:
            sp_kill1 = []
            if abs(j - y) == abs(i - x) and board[j][i] is None:
                for i1 in range(1, abs(j - y) + 1):
                    iv = -i1 if j < y else i1
                    ih = -i1 if i < x else i1
                    if board[y + iv][x + ih] is not None:
                        if (board[y + iv][x + ih].color == WHITE and mine and not offline) or (
                                board[y + iv][x + ih].color == COLOR and offline):
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
    def can_move(self, board, x, y, pos_att, mine, offline=False):
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

                    if (kill.color == WHITE and mine and not offline) or (kill.color == COLOR and offline):
                        print(kill.color, WHITE)
                        return False

                    sp_kill.append([(i + x) // 2, (j + y) // 2])
                    x, y = i, j
            return sp_kill


class Board:
    # создание поля
    def __init__(self, width, height, offline=False):
        self.width = width
        self.height = height
        self.field = [[None] * 8 for _ in range(8)]
        self.offline = offline

        with open('../../program_code/checkers/additional_functions/data/settings.txt') as f:
            f = f.read()
            self.left, self.top, self.cell_size, self.illumination, self.animation_ = [int(i) for i in f.split()]

        self.field[0][1] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[0][3] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[0][5] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[0][7] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[1][0] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[1][2] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[1][4] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[1][6] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[2][1] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[2][3] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[2][5] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[2][7] = Usual(all_sprites, BLACK, size=(self.cell_size, self.cell_size))
        self.field[5][0] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[5][2] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[5][4] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[5][6] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[6][1] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[6][3] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[6][5] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[6][7] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[7][0] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[7][2] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[7][4] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.field[7][6] = Usual(all_sprites, WHITE, size=(self.cell_size, self.cell_size))
        self.mouse_coords = []

    def render(self, screen, my_color, network, sounds):
        self.my_color = my_color
        self.network = network
        self.sounds = sounds

        screen.fill('#368613')  # если не нравится, то меняй, я не уверен в этом цвете (была просто черная заливка)
        screen.fill('#ac9362', (
            self.left - 20, self.top - 20, self.cell_size * self.width + 40, self.cell_size * self.height + 40))

        font = pygame.font.Font(main_font, 35)
        text = font.render(f"{'Ваш ход' if COLOR == WHITE else 'Ход противника'}", True, (255, 255, 255))
        screen.blit(text, (self.left, self.top - 80))

        text = font.render(f"{COUNT_BLACK_KILLED}", True, (255, 255, 255))
        screen.blit(text, (self.left + 0.5 * self.cell_size * self.width - text.get_width() - 5,
                           self.top + self.cell_size * self.height + 20))
        text = font.render(":", True, '#964b00')
        screen.blit(text,
                    (self.left + 0.5 * self.cell_size * self.width - 1, self.top + self.cell_size * self.height + 20))
        text = font.render(f"{COUNT_WHITE_KILLED}", True, (0, 0, 0))
        screen.blit(text,
                    (self.left + 0.5 * self.cell_size * self.width + 10, self.top + self.cell_size * self.height + 20))
        font = pygame.font.Font(main_font, 17)
        for i in range(1, 9):
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (self.left - 15, self.top + self.cell_size * (i - 0.5)))
            screen.blit(text, (self.left + self.cell_size * self.width + 5, self.top + self.cell_size * (i - 0.5)))
            text = font.render('ABCDEFGH'[i - 1], True, (0, 0, 0))
            screen.blit(text, (self.left + self.cell_size * (i - 0.5), self.top - 20))
            screen.blit(text, (self.left + self.cell_size * (i - 0.5), self.top + self.cell_size * self.height))

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

        if self.mouse_coords:
            x, y = self.mouse_coords[0]
            if self.field[y][x]:
                if (self.field[y][x].color == WHITE and not self.offline) or (
                        self.field[y][x].color == COLOR and self.offline):
                    screen.fill('blue', (
                        self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.cell_size))

                    if self.illumination:
                        for i in range(self.height):
                            for j in range(self.width):
                                if self.field[y][x].can_move(self.field, x, y, ([j, i],), True, offline=self.offline):
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

        s = self.field[y][x]

        if s is None:
            return False
        if (s.color != WHITE and mine and not self.offline) or (s.color != COLOR and self.offline):
            return False

        rez = s.can_move(self.field, x, y, pos_att, mine, offline=self.offline)
        if not rez:
            return False
        if rez == 1:
            # checker = self.field[y][x]
            # self.field[y][x] = None
            #
            # self.animation(checker, x, y, pos_att[0][0], pos_att[0][1])
            # self.field[pos_att[0][1]][pos_att[0][0]] = checker

            if self.check_attack(mine):
                print('cxyesdterfd')
                checker = self.field[y][x]
                self.field[y][x] = None
                if self.animation_:
                    self.animation(checker, x, y, pos_att[0][0], pos_att[0][1])
                self.field[pos_att[0][1]][pos_att[0][0]] = checker
            else:
                return False

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

                if self.animation_:
                    self.animation(checker, x, y, pos_att_i[0], pos_att_i[1])
                x, y = pos_att_i
            self.field[pos_att[-1][1]][pos_att[-1][0]] = checker
            if COLOR == BLACK:
                COUNT_WHITE_KILLED += len(rez)
            else:
                COUNT_BLACK_KILLED += len(rez)
            print(COLOR, COUNT_WHITE_KILLED, COUNT_BLACK_KILLED)
        else:
            return False
        sp_bq = check_bqueen(self.field)
        sp_wq = check_wqueen(self.field)
        for i in sp_bq:
            self.field[7][i].kill()
            self.field[7][i] = Queen(all_sprites, BLACK, (self.cell_size, self.cell_size))
        for i in sp_wq:
            self.field[0][i].kill()
            self.field[0][i] = Queen(all_sprites, WHITE, (self.cell_size, self.cell_size))
            print(2)
        if mine and self.network is not None:
            data = self.network.send(send_move((x1, y1), pos_att1))
        return True

    def check_attack(self, mine):
        for i in range(8):
            for j in range(8):
                checker = self.field[j][i]
                if checker:
                    if (checker.color == WHITE and mine and not self.offline) or (
                            checker.color == COLOR and self.offline):
                        for i1 in range(8):
                            for j1 in range(8):
                                rez = checker.can_move(self.field, i, j, [(j1, i1)], mine, offline=self.offline)
                                if type(rez) == list:
                                    if len(rez) == 1:
                                        print(i, j, [(j1, i1)])
                                        return False
        return True

    def animation(self, checker, x, y, x1, y1):
        '''Анимация перемещения шашек'''
        if self.sounds['on_sounds']:
            self.sounds['move'].play(0)

        delta_x = (x1 - x) * 0.1 * self.cell_size
        delta_y = (y1 - y) * 0.1 * self.cell_size

        for i in range(10):
            checker.rect.x += delta_x + -modf(delta_x)[0]
            checker.rect.y += delta_y + -modf(delta_y)[0]

            self.render(screen, self.my_color, self.network, self.sounds)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(50)
        checker.rect.x += delta_x + -modf(delta_x)[0]
        checker.rect.y += delta_y + -modf(delta_y)[0]

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
        print(self.mouse_coords)

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
    global board, screen, all_sprites, clock, COLOR, COUNT_WHITE_KILLED, COUNT_BLACK_KILLED
    try:

        COUNT_WHITE_KILLED = 0
        COUNT_BLACK_KILLED = 0
        COLOR = MY_COLOR

        flag_winner = None
        flag_quit = False

        pygame.init()
        conn = connect('../../program_code/checkers/additional_functions/data/database/profile.sqlite')
        with conn:  # Начатые матчи
            conn.cursor().execute('UPDATE statistics_matches set count = count + 1')
            conn.commit()
        # size = 500, 550
        # screen — холст, на котором нужно рисовать:
        # screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Шашки')
        clock = pygame.time.Clock()

        board = Board(8, 8)
        screen = pygame.display.set_mode((board.left * 2 + board.cell_size * 8, board.top * 2 + board.cell_size * 8))
        all_sprites = pygame.sprite.Group()
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
                    if COLOR == WHITE:
                        if event.button == 1:
                            board.get_click(event.pos)
                        elif event.button == 3:
                            print('да')
                            if board.get_cell(event.pos) is not None:
                                board.mouse_coords.append(board.get_cell(event.pos))
            count_fps += 1
            if count_fps % 100 == 0:
                data = network.send('get_move')
                if data == 'end':
                    break

                elif COLOR != WHITE:
                    if count_fps % 100 == 0:
                        if data is not None and data != 'None' and data != '-':
                            if load_move(data):
                                last, new = load_move(data)

                                board.move(last[0], last[1], new, False)
                                COLOR = color_opponent()

            flag_winner = winner(MY_COLOR)
            if flag_winner is not None:
                with conn:  # кол-во выигранных матчей
                    if flag_winner:
                        conn.cursor().execute('UPDATE statistics_matches set count_win = count_win + 1')
                    conn.cursor().execute(
                        f'UPDATE statistics_matches set (count_compl, time_in) = (count_compl + 1, time_in + '
                        f'{pygame.time.get_ticks() // 1000})')
                    conn.commit()
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
    global screen, all_sprites, board, clock, nlo_sprites, nlo, FPS, COLOR, COUNT_WHITE_KILLED, COUNT_BLACK_KILLED
    COUNT_WHITE_KILLED = 0
    COUNT_BLACK_KILLED = 0

    pygame.init()
    FPS = 50
    size = 500, 550
    COLOR = WHITE
    MY_COLOR = WHITE
    flag_winner = None
    # screen — холст, на котором нужно рисовать:
    pygame.display.set_caption('Шашки')
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    nlo_sprites = pygame.sprite.Group()

    board = Board(8, 8, offline=True)

    screen = pygame.display.set_mode((board.left * 2 + board.cell_size * 8, board.top * 2 + board.cell_size * 8))
    board.render(screen, MY_COLOR, None, sounds)
    all_sprites.draw(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if COLOR == COLOR:
                    if event.button == 1:
                        board.get_click(event.pos)
                    elif event.button == 3:
                        if board.get_cell(event.pos) is not None:
                            board.mouse_coords.append(board.get_cell(event.pos))
        flag_winner = winner(MY_COLOR)
        if flag_winner is not None:
            running = False
            continue

        if COLOR != MY_COLOR:
            board.bot_move()

        board.render(screen, MY_COLOR, None, sounds)
        all_sprites.draw(screen)
        pygame.display.flip()
    return flag_winner


def winner(MY_COLOR):
    if COUNT_BLACK_KILLED == 12:
        return True
    if COUNT_WHITE_KILLED == 12:
        return False
    return None


def remove_spites(group):
    for sprite in group:
        sprite.kill()