import pygame
import sys

ROW_COUNT = 6
COL_COUNT = 7
BLUE = (0,0,250)
BLACK = (0,0,0)
RED = (250,0,0)
YELLOW = (250,250,0)



def create_board():
    arr = ['R']*42
    return arr


# for piece can use i from other function
def winning_move(board, piece):
    row = 0
    col = 0

    for i in range(len(board)):
        # Horizantle WINS
        if (i % COL_COUNT <= (ROW_COUNT/2)):
            if (board[i] == piece and board[i + 1] == piece and board[i + 2] == piece and board[i + 3] == piece):
                return True

        # Verticle Wins
        if i <= ((ROW_COUNT - (ROW_COUNT/2)) * COL_COUNT - 1):
            if board[i] == piece and board[i + COL_COUNT] == piece and board[i + 2 * COL_COUNT] == piece and board[i + 3 * COL_COUNT] == piece:
                return True

        #Positve Diagonal Wins
        if (i + (3*COL_COUNT+(ROW_COUNT/2)) < len(board)-1) and (col<4):
            if board[i] == piece and board[i+COL_COUNT+1] == piece and board[i+(2*COL_COUNT+2)] == piece and board[i+(3*COL_COUNT+3)] == piece:
                return True

        # Negative Diagonal Wins
        if (i + (3*COL_COUNT-(ROW_COUNT/2)) < len(board)-1) and (col>=(ROW_COUNT/2)):
            if board[i] == piece and board[i+COL_COUNT-1] == piece and board[i+(2*COL_COUNT-2)] == piece and board[i+(3*COL_COUNT-3)] == piece:
                return True

        #ALGO for the col and row variables (changed the placement of col+=1)

        if col == ROW_COUNT:
            col = -1
            row += 1
        col += 1


def empty_board(arr):
    for i in range(len(arr)):
        arr[i] = "*"


def print_board(arr):
    printed = 0
    str = ''
    for i in arr:
        str += i + " "
        printed += 1
        if printed == COL_COUNT:
            print(str)
            printed = 0
            str = ''
    print("\n")


def drop_piece(arr, col, turn):
    i = col
    while i < (len(arr) - COL_COUNT):
        if arr[i+COL_COUNT] == "*":
            i += 7
        elif arr[i+COL_COUNT] != "*":
            break
    if turn == 0:
        arr[i] = "R"
    else:
        arr[i] = "Y"


def is_valid_location(board, col):
    if board[col] == '*':
        return True
    return False

def draw_board(arr):
    row = 0
    col = 0

    for i in range(len(board)):
        pygame.draw.rect(screen, BLUE, (col*square_size, row*square_size+square_size, square_size, square_size))
        if board[i] == "R":
            pygame.draw.circle(screen, RED, (col * square_size + (square_size / 2), row * square_size + square_size + (square_size / 2)), radius)
        elif board[i] == "Y":
            pygame.draw.circle(screen, YELLOW, (col * square_size + (square_size / 2), row * square_size + square_size + (square_size / 2)), radius)
        else:
            pygame.draw.circle(screen, BLACK, (col*square_size+(square_size/2), row*square_size+square_size+(square_size/2)), radius)

        if col == ROW_COUNT:
            col = -1
            row += 1
        col += 1


pygame.init()
print("start")
restart = True
red_wins = 0
yellow_wins = 0

while restart:
    board = create_board()
    empty_board(board)
    print_board(board)
    turn = 0


    square_size = 100
    radius = square_size/2 -6

    width = COL_COUNT * square_size
    height = (1+ROW_COUNT) * square_size

    size = (width, height)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    font = pygame.font.SysFont("monospace", 75)

    btnYes_colour = RED
    btnNo_colour = RED

    game_over = False
    running = True

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                game_over = True

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, square_size))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(square_size/2)), radius)
                if turn == 1:
                    pygame.draw.circle(screen, YELLOW, (posx, int(square_size/2)), radius)

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
                if turn == 0:
                    selection = int(event.pos[0]/100)
                    if not is_valid_location(board, selection):
                        print("Column is full. TRY AGAIN")
                        turn -= 1
                    else:
                        drop_piece(board, selection, turn)
                    if winning_move(board, "R"):
                        game_over = True
                        label = font.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40,10))
                        print_board(board)
                        draw_board(board)
                        pygame.display.update()
                        print("YOU WIN PLAYER 1")
                elif turn == 1:
                    selection = int(event.pos[0]/100)
                    if not is_valid_location(board, selection):
                        print("Column is full. TRY AGAIN")
                        turn -= 1
                    else:
                        drop_piece(board, selection, turn)
                    if winning_move(board, "Y"):
                        game_over = True
                        label = font.render("Player 2 Wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        print_board(board)
                        draw_board(board)
                        pygame.display.update()
                        print("YOU WIN PLAYER 2")

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)
                pygame.display.update()

            if game_over:
                pygame.time.wait(2000)


    screen = pygame.display.set_mode(size)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if btnYes.collidepoint(pos):
                    print("yes")
                    btnYes_colour = BLUE
                    running = False
                elif btnNo.collidepoint(pos):
                    print("No")
                    btnNo_colour = BLUE
                    running = False
                    restart = False

            pygame.draw.rect(screen, BLACK, (0,265, width, 170))
            label = pygame.font.SysFont("monospace", 50).render("PLAY AGAIN?", 1, YELLOW)
            screen.blit(label, (202, 285))

            btnYes = pygame.draw.rect(screen, btnYes_colour, (216, 350, width/7, 50), 3)
            label = pygame.font.SysFont("monospace", 40).render("YES", 1, YELLOW)
            screen.blit(label, (230, 352))

            btnNo = pygame.draw.rect(screen, btnNo_colour, (396, 350, width / 7, 50), 3)
            label = pygame.font.SysFont("monospace", 40).render("NO", 1, YELLOW)
            screen.blit(label, (423, 352))

            pygame.display.update()



print("done")