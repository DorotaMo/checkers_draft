import random

import pygame
import sys
from pygame.locals import *


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Checkers')

    custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 36)

    rect_width, rect_height = 380, 60
    center_x, center_y = 320, 240

    start_rect = pygame.Rect(center_x - rect_width // 2, center_y - rect_height // 2 - 30, rect_width, rect_height)
    quit_rect = pygame.Rect(center_x - rect_width // 2, center_y - rect_height // 2 + 40, rect_width, rect_height)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(mouse_pos):
                    select_game_mode()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))

        if start_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), start_rect)
            start_text = custom_font.render('Start Game', True, (0, 0, 0))
        else:
            start_text = custom_font.render('Start Game', True, (255, 255, 255))

        if quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), quit_rect)
            quit_text = custom_font.render('Quit', True, (0, 0, 0))
        else:
            quit_text = custom_font.render('Quit', True, (255, 255, 255))

        screen.blit(start_text, (start_rect.x + (start_rect.width - start_text.get_width()) // 2,
                                 start_rect.y + (start_rect.height - start_text.get_height()) // 2))
        screen.blit(quit_text, (quit_rect.x + (quit_rect.width - quit_text.get_width()) // 2,
                                quit_rect.y + (quit_rect.height - quit_text.get_height()) // 2))

        pygame.display.flip()


positions = {}
attack = {}

# position number and x, y coordinates
for key in range(1, 33):
    if (key - 1) // 4 % 2 == 0:
        col = (key - 1) % 4 + 1
        row = (key - 1) // 4 + 1
        x = (col * 2 - 1) * 80 + 40
        y = (row - 1) * 80 + 40
    else:
        col = (key - 1) % 4 + 1
        row = (key - 1) // 4 + 1
        x = (col * 2 - 2) * 80 + 40
        y = (row - 1) * 80 + 40
    positions[key] = [x, y]

piece_positions = {'red': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                   'white': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]}

queen_positions = {'red': [], 'white': []}
turn = 'white'


def run_game():
    global turn
    global attack

    pygame.init()
    screen = pygame.display.set_mode((760, 640), 0, 32)

    custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 12)
    custom_font_big = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 24)

    # reading the images
    white_pawn, red_pawn, white_queen, red_queen, background = image_read()

    menu_text = custom_font_big.render('Menu', True, (255, 255, 255))
    menu_rect = menu_text.get_rect(topleft=(650, 30))

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    chosen_piece = None
    possible_moves = []

    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        display_figures(red_pawn, white_pawn, white_queen, red_queen, screen, chosen_piece)

        timer_text = custom_font.render(f'Time: {(pygame.time.get_ticks() - start_time) // 1000}s', True,
                                        (255, 255, 255))
        timer_rect = timer_text.get_rect(topright=(750, 10))

        # Menu button
        if menu_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 255), menu_rect)
            menu_text = custom_font_big.render('Menu', True, (0, 0, 0))
        else:
            menu_text = custom_font_big.render('Menu', True, (255, 255, 255))

        # displaying the score
        white_score_text = custom_font.render(f'White: {len(piece_positions["white"])}', True, (255, 255, 255))
        white_score_rect = white_score_text.get_rect(topright=(755, 70))

        red_score_text = custom_font.render(f'Red: {len(piece_positions["red"])}', True, (255, 255, 255))
        red_score_rect = red_score_text.get_rect(topright=(755, 100))

        screen.blit(timer_text, timer_rect)
        screen.blit(menu_text, menu_rect)
        screen.blit(white_score_text, white_score_rect)
        screen.blit(red_score_text, red_score_rect)

        #
        for x, y in possible_moves:
            pygame.draw.rect(screen, (0, 255, 0), (x - 40, y - 40, 80, 80), 5)
        for key in attack:
            pygame.draw.rect(screen, (255, 0, 0), (key[0] - 40, key[1] - 40, 80, 80), 10)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # player move
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn == 'white':
                click_x, click_y = event.pos
                # clicked on the menu button
                if menu_rect.collidepoint((click_x, click_y)):
                    main_menu()
                    return

                for key in piece_positions:
                    for i in piece_positions[key]:
                        piece_x, piece_y = positions[i]
                        piece_rect = pygame.Rect(piece_x - 40, piece_y - 40, 80, 80)
                        # clicked on piece
                        if piece_rect.collidepoint(click_x, click_y):
                            chosen_piece = i
                            chosen_color = key

                            if chosen_color == 'white':
                                possible_moves, attacked_piece = display_possible_moves(chosen_piece, chosen_color)
                            else:
                                chosen_piece = None

                if chosen_piece is not None:
                    for x, y in possible_moves:
                        if x - 40 < click_x < x + 40 and y - 40 < click_y < y + 40:
                            attack = {}
                            piece_positions[chosen_color].remove(chosen_piece)
                            piece_positions[chosen_color].append(coordinates_to_position(x, y))

                            # promoting to queen
                            if is_queen(chosen_piece, chosen_color):
                                queen_positions[chosen_color].remove(chosen_piece)
                                queen_positions[chosen_color].append(coordinates_to_position(x, y))

                            # removing attacked piece
                            if attacked_piece is not None:
                                for team, pieces in piece_positions.items():
                                    if attacked_piece in pieces:
                                        pieces.remove(attacked_piece)

                            get_queen()

                            chosen_piece = None
                            possible_moves = []

                            turn = 'white' if turn == 'red' else 'red'
                            break

            #  random AI move
            elif turn == "red" and game_mode == "Random AI":
                possible_moves == []

                while not possible_moves:
                    chosen_piece = random.choice(piece_positions['red'])
                    chosen_color = 'red'
                    possible_moves, attacked_piece = display_possible_moves(chosen_piece, chosen_color)

                pygame.time.delay(500)
                random_move = random.choice(possible_moves)
                x, y = random_move

                piece_positions[chosen_color].remove(chosen_piece)
                piece_positions[chosen_color].append(coordinates_to_position(x, y))

                if is_queen(chosen_piece, chosen_color):
                    queen_positions[chosen_color].remove(chosen_piece)
                    queen_positions[chosen_color].append(coordinates_to_position(x, y))

                if attacked_piece is not None:
                    for team, pieces in piece_positions.items():
                        if attacked_piece in pieces:
                            pieces.remove(attacked_piece)

                get_queen()

                chosen_piece = None
                possible_moves = []

                turn = 'white' if turn == 'red' else 'red'

            # Minimax 1 depth AI move
            elif turn == "red" and game_mode == "Minimax AI":

                best_move = []
                eval_score = float('inf')

                for available_piece in piece_positions['red']:
                    possible_moves, attacked_piece = display_possible_moves(available_piece, "red")
                    if possible_moves:
                        for move in possible_moves:
                            eval = evaluate_function(attacked_piece)
                            if eval < eval_score:
                                best_move = [available_piece, move, attacked_piece]
                                eval_score = eval

                chosen_piece, move, attacked_piece = best_move
                x, y = move

                piece_positions['red'].remove(chosen_piece)
                piece_positions['red'].append(coordinates_to_position(x, y))

                if is_queen(chosen_piece, "red"):
                    queen_positions['red'].remove(chosen_piece)
                    queen_positions['red'].append(coordinates_to_position(x, y))

                if attacked_piece is not None:
                    for team, pieces in piece_positions.items():
                        if attacked_piece in pieces:
                            pieces.remove(attacked_piece)

                get_queen()

                chosen_piece = None
                possible_moves = []
                turn = 'white' if turn == 'red' else 'red'

            # second player move
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn == "red" and game_mode == "Player vs player":
                if menu_rect.collidepoint((click_x, click_y)):
                    main_menu()
                    return

                click_x, click_y = event.pos
                for key in piece_positions:
                    for i in piece_positions[key]:
                        piece_x, piece_y = positions[i]
                        piece_rect = pygame.Rect(piece_x - 40, piece_y - 40, 80, 80)
                        if piece_rect.collidepoint(click_x, click_y):
                            chosen_piece = i
                            chosen_color = key

                            if chosen_color == 'red':
                                possible_moves, attacked_piece = display_possible_moves(chosen_piece, chosen_color)
                            else:
                                chosen_piece = None

                if chosen_piece is not None:
                    for x, y in possible_moves:
                        if x - 40 < click_x < x + 40 and y - 40 < click_y < y + 40:
                            attack = {}
                            piece_positions[chosen_color].remove(chosen_piece)
                            piece_positions[chosen_color].append(coordinates_to_position(x, y))
                            if is_queen(chosen_piece, chosen_color):
                                queen_positions[chosen_color].remove(chosen_piece)
                                queen_positions[chosen_color].append(coordinates_to_position(x, y))
                            if attacked_piece is not None:
                                for team, pieces in piece_positions.items():
                                    if attacked_piece in pieces:
                                        pieces.remove(attacked_piece)

                            get_queen()

                            chosen_piece = None
                            possible_moves = []

                            turn = 'white' if turn == 'red' else 'red'
                            break

        pygame.display.update()
        clock.tick(60)

        check_winner()


# outline for the piece
def create_outline(image, screen, position, thickness=3, color=(0, 0, 255)):
    mask = pygame.mask.from_surface(image)
    offset = thickness - 1

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            if mask.get_at((x, y)):
                for dx in range(-offset, offset + 1):
                    for dy in range(-offset, offset + 1):
                        if not mask.get_at((x + dx, y + dy)):
                            screen.set_at((position[0] + x + dx, position[1] + y + dy), color)


# evaluation function for the minimax AI
def evaluate_function(fight_piece):
    result = len(piece_positions["red"]) * (-1) + len(piece_positions["white"]) - len(queen_positions["red"]) * (
        -1.5) + len(queen_positions["white"]) * 1.5
    if fight_piece is not None:
        result -= 1
    return result


# checks if there is a winner
def check_winner():
    winner = None
    if len(piece_positions['white']) == 0:
        winner = 'red'
    elif len(piece_positions['red']) == 0:
        winner = 'White'

    if winner:
        play_again_prompt(winner)


# maps coordinates to position number
def coordinates_to_position(x, y):
    for position in positions:
        if positions[position] == [x, y]:
            return position


def display_figures(red_pawn, white_pawn, white_queen, red_queen, screen, chosen_piece):
    for key in piece_positions:
        for i in piece_positions[key]:
            piece_x, piece_y = positions[i]
            if i in queen_positions[key]:
                piece_image = white_queen if key == 'white' else red_queen
            else:
                piece_image = white_pawn if key == 'white' else red_pawn
            screen.blit(piece_image, (piece_x - 40, piece_y - 40))
            if i == chosen_piece:
                create_outline(piece_image, screen, (piece_x - 40, piece_y - 40))


# checks possible moves for the piece
def display_possible_moves(chosen_piece, chosen_color):
    queen = is_queen(chosen_piece, chosen_color)

    if chosen_color == 'white' and not queen:
        possible_moves = [
            ('LU', positions[chosen_piece][0] - 80, positions[chosen_piece][1] - 80),
            ('PU', positions[chosen_piece][0] + 80, positions[chosen_piece][1] - 80)
        ]
    elif chosen_color == 'red' and not queen:
        possible_moves = [
            ('LD', positions[chosen_piece][0] - 80, positions[chosen_piece][1] + 80),
            ('PD', positions[chosen_piece][0] + 80, positions[chosen_piece][1] + 80)
        ]
    else:
        possible_moves = [
            ('LU', positions[chosen_piece][0] - 80, positions[chosen_piece][1] - 80),
            ('PU', positions[chosen_piece][0] + 80, positions[chosen_piece][1] - 80),
            ('LD', positions[chosen_piece][0] - 80, positions[chosen_piece][1] + 80),
            ('PD', positions[chosen_piece][0] + 80, positions[chosen_piece][1] + 80)
        ]

    to_remove = []
    to_add = []
    fight_mode = False

    attacked_piece = None

    def left(x, y, up):
        return x - 80, y - up * 80

    def right(x, y, up):
        return x + 80, y - up * 80

    for direction, x, y in possible_moves:
        next_position = coordinates_to_position(x, y)
        if next_position is None:
            to_remove.append((x, y))
        elif next_position in piece_positions[chosen_color]:
            to_remove.append((x, y))
        elif any(next_position in positions for positions in piece_positions.values()):
            if direction == 'LU':
                new_x, new_y = left(x, y, 1)
            elif direction == 'LD':
                new_x, new_y = left(x, y, -1)
            elif direction == 'PU':
                new_x, new_y = right(x, y, 1)
            else:
                new_x, new_y = right(x, y, -1)

            new_pos = coordinates_to_position(new_x, new_y)

            if new_pos is not None and not any(new_pos in positions for positions in piece_positions.values()):
                to_add.append((new_x, new_y))
                fight_mode = True
                attacked_piece = next_position
            to_remove.append((x, y))

    if fight_mode:
        new_possible_moves = to_add
    else:
        new_possible_moves = [(x, y) for direction, x, y in possible_moves if (x, y) not in to_remove]

    return new_possible_moves, attacked_piece


# check if the piece is a queen
def is_queen(chosen_piece, chosen_color):
    if chosen_piece in queen_positions[chosen_color]:
        return True
    return False


# attacking more than just one piece, white color only for now
def can_jump(x, y, piece_color):
    attack_left = False
    attack_right = False

    # left part
    xl1 = x - 80
    yl1 = y - 80
    xl2 = x - 160
    yl2 = y - 160
    p1 = coordinates_to_position(xl1, yl1)
    p2 = coordinates_to_position(xl2, yl2)
    if p1 is not None and p2 is not None:
        if p1 in piece_positions['red'] and p2 not in piece_positions[piece_color] and p2 not in piece_positions['red']:
            attack_left = True
            temp = attack[x, y][:]
            temp.append(p1)
            attack[xl2, yl2] = temp

    # right part
    xr1 = x + 80
    yr1 = y - 80
    xr2 = x + 160
    yr2 = y - 160
    p1 = coordinates_to_position(xr1, yr1)
    p2 = coordinates_to_position(xr2, yr2)
    if p1 is not None and p2 is not None:
        if p1 in piece_positions['red'] and p2 not in piece_positions[piece_color] and p2 not in piece_positions['red']:
            attack_right = True
            temp = attack[x, y][:]
            temp.append(p1)
            attack[xr2, yr2] = temp

    if attack_left or attack_right:
        del attack[x, y]
    if attack_left:
        can_jump(xl2, yl2, piece_color)
    if attack_right:
        can_jump(xr2, yr2, piece_color)


# loading images
def image_read():
    white_pawn = pygame.image.load('images/white_pawn.png').convert_alpha()
    white_pawn = pygame.transform.scale(white_pawn, (80, 80))

    red_pawn = pygame.image.load('images/red_pawn.png').convert_alpha()
    red_pawn = pygame.transform.scale(red_pawn, (80, 80))

    white_queen = pygame.image.load('images/white_queen.png').convert_alpha()
    white_queen = pygame.transform.scale(white_queen, (80, 80))

    red_queen = pygame.image.load('images/red_queen.png').convert_alpha()
    red_queen = pygame.transform.scale(red_queen, (80, 80))

    background = pygame.image.load('images/board.jpg').convert_alpha()
    background = pygame.transform.scale(background, (640, 640))

    return white_pawn, red_pawn, white_queen, red_queen, background


# promoting pieces to queens
def get_queen():
    for piece_position in piece_positions['white']:
        if piece_position in [1, 2, 3, 4]:
            queen_positions['white'].append(piece_position)
            break
    for piece_position in piece_positions['red']:
        if piece_position in [29, 30, 31, 32]:
            queen_positions['red'].append(piece_position)
            # piece_positions['red'].remove(piece_position)
            break


# display game over screen
def play_again_prompt(winner):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Game Over')

    # Font setup
    custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 36)

    # Messages setup for two lines
    message1 = f"{winner} wins!"
    message2 = "Play again?"

    # Render text for each line
    text1 = custom_font.render(message1, True, (255, 255, 255))
    text2 = custom_font.render(message2, True, (255, 255, 255))

    # Get rectangles for positioning
    text_rect1 = text1.get_rect(center=(320, 220))
    text_rect2 = text2.get_rect(center=(320, 260))

    # Buttons setup
    yes_button = pygame.Rect(160, 300, 130, 50)
    no_button = pygame.Rect(350, 300, 130, 50)

    while True:
        screen.fill((0, 0, 0))  # Clear the screen and fill it with black
        mouse_pos = pygame.mouse.get_pos()

        # Yes button interactivity
        if yes_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), yes_button)
            yes_text = custom_font.render('Yes', True, (0, 0, 0))
        else:
            pygame.draw.rect(screen, (0, 255, 0), yes_button)
            yes_text = custom_font.render('Yes', True, (255, 255, 255))

        # No button interactivity
        if no_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), no_button)
            no_text = custom_font.render('No', True, (0, 0, 0))
        else:
            pygame.draw.rect(screen, (255, 0, 0), no_button)
            no_text = custom_font.render('No', True, (255, 255, 255))

        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(yes_text, (yes_button.x + 10, yes_button.y + 10))
        screen.blit(no_text, (no_button.x + 20, no_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_button.collidepoint(event.pos):
                    reset_game_positions()
                    main_menu()  # Restart the game
                    return
                elif no_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# mode menu
def select_game_mode():
    global game_mode

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Game Mode')

    # Font setup
    custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 36)
    small_custom_font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 26)

    # Messages setup for two lines
    message1 = "Choose"
    message2 = "game mode"

    # Render text for each line
    text1 = custom_font.render(message1, True, (255, 255, 255))
    text2 = custom_font.render(message2, True, (255, 255, 255))

    # Get rectangles for positioning
    text_rect1 = text1.get_rect(center=(320, 100))
    text_rect2 = text2.get_rect(center=(320, 140))

    # Buttons setup
    button1 = pygame.Rect(100, 200, 450, 50)
    button2 = pygame.Rect(100, 250, 450, 50)
    button3 = pygame.Rect(100, 300, 450, 50)

    while True:
        screen.fill((0, 0, 0))  # Clear the screen and fill it with black
        mouse_pos = pygame.mouse.get_pos()

        # button1 button interactivity
        if button1.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), button1)
            button_text1 = small_custom_font.render('Player vs Player', True, (0, 0, 0))
        else:
            pygame.draw.rect(screen, (0, 0, 0), button1)
            button_text1 = small_custom_font.render('Player vs player', True, (255, 255, 255))

        # button2 button interactivity
        if button2.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), button2)
            button_text2 = small_custom_font.render('Random AI', True, (0, 0, 0))
        else:
            pygame.draw.rect(screen, (0, 0, 0), button2)
            button_text2 = small_custom_font.render('Random AI', True, (255, 255, 255))

        # button3 button interactivity
        if button3.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 255), button3)
            button_text3 = small_custom_font.render('Minimax AI', True, (0, 0, 0))
        else:
            pygame.draw.rect(screen, (0, 0, 0), button3)
            button_text3 = small_custom_font.render('Minimax AI', True, (255, 255, 255))

        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(button_text1, (button1.x + 10, button1.y + 10))
        screen.blit(button_text2, (button2.x + 20, button2.y + 10))
        screen.blit(button_text3, (button3.x + 20, button3.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button1.collidepoint(event.pos):
                    game_mode = "Player vs player"
                    reset_game_positions()
                    run_game()
                elif button2.collidepoint(event.pos):
                    game_mode = "Random AI"
                    reset_game_positions()
                    run_game()
                elif button3.collidepoint(event.pos):
                    game_mode = "Minimax AI"
                    reset_game_positions()
                    run_game()


def reset_game_positions():
    global piece_positions, queen_positions, turn
    piece_positions = {
        'red': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'white': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    }
    queen_positions = {
        'red': [],
        'white': []
    }
    turn = 'white'


if __name__ == "__main__":
    main_menu()
