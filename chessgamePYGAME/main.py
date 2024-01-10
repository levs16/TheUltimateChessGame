import os
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BOARD_COLOR_W = (222, 184, 135)  # Wood color
BOARD_COLOR_B = (30, 30, 30)
GREEN = (0, 255, 0)

# Get the path to the "res" folder
current_dir = os.path.dirname(__file__)
res_folder = os.path.join(current_dir, 'res')

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load chess pieces images
pieces = {}
for color in ['w', 'b']:
    for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
        key = f'{color}_{piece}'
        img_path = os.path.join(res_folder, f"{color}{piece}.png")
        pieces[key] = pygame.image.load(img_path)

# Create the chess board
board = [
    ['b_rook', 'b_knight', 'b_bishop', 'b_queen', 'b_king', 'b_bishop', 'b_knight', 'b_rook'],
    ['b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn', 'b_pawn'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn', 'w_pawn'],
    ['w_rook', 'w_knight', 'w_bishop', 'w_queen', 'w_king', 'w_bishop', 'w_knight', 'w_rook']
]

# Variables for piece movement
selected_piece = None
available_moves = []

# Function to get available moves based on the piece type
def get_available_moves(piece, row, col):
    moves = []
    
    if 'pawn' in piece:
        # Pawn move rules
        direction = 1 if 'w' in piece else -1
        if board[row + direction][col] == '':
            moves.append((row + direction, col))
            if row == 1 and 'w' in piece or row == 6 and 'b' in piece:
                # Allow double move on the first move
                if board[row + 2 * direction][col] == '':
                    moves.append((row + 2 * direction, col))
        # Add capturing moves
        if 0 <= col - 1 < BOARD_SIZE and board[row + direction][col - 1] != '' and 'b' in piece:
            moves.append((row + direction, col - 1))
        if 0 <= col + 1 < BOARD_SIZE and board[row + direction][col + 1] != '' and 'b' in piece:
            moves.append((row + direction, col + 1))
        if 0 <= col - 1 < BOARD_SIZE and board[row + direction][col - 1] != '' and 'w' in piece:
            moves.append((row + direction, col - 1))
        if 0 <= col + 1 < BOARD_SIZE and board[row + direction][col + 1] != '' and 'w' in piece:
            moves.append((row + direction, col + 1))
            
    elif 'rook' in piece:
        # Rook move rules
        for i in range(row + 1, BOARD_SIZE):
            if board[i][col] == '':
                moves.append((i, col))
            else:
                if board[i][col][0] != piece[0]:
                    moves.append((i, col))
                break
        for i in range(row - 1, -1, -1):
            if board[i][col] == '':
                moves.append((i, col))
            else:
                if board[i][col][0] != piece[0]:
                    moves.append((i, col))
                break
        for j in range(col + 1, BOARD_SIZE):
            if board[row][j] == '':
                moves.append((row, j))
            else:
                if board[row][j][0] != piece[0]:
                    moves.append((row, j))
                break
        for j in range(col - 1, -1, -1):
            if board[row][j] == '':
                moves.append((row, j))
            else:
                if board[row][j][0] != piece[0]:
                    moves.append((row, j))
                break
    
    elif 'knight' in piece:
        # Knight move rules
        possible_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row - 1, col + 2),
            (row + 1, col - 2), (row - 1, col - 2)
        ]
        for move in possible_moves:
            r, c = move
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and (board[r][c] == '' or board[r][c][0] != piece[0]):
                moves.append(move)
    
    elif 'bishop' in piece:
        # Bishop move rules
        for i, j in zip(range(row + 1, BOARD_SIZE), range(col + 1, BOARD_SIZE)):
            if board[i][j] == '':
                moves.append((i, j))
            else:
                if board[i][j][0] != piece[0]:
                    moves.append((i, j))
                break
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, BOARD_SIZE)):
            if board[i][j] == '':
                moves.append((i, j))
            else:
                if board[i][j][0] != piece[0]:
                    moves.append((i, j))
                break
        for i, j in zip(range(row + 1, BOARD_SIZE), range(col - 1, -1, -1)):
            if board[i][j] == '':
                moves.append((i, j))
            else:
                if board[i][j][0] != piece[0]:
                    moves.append((i, j))
                break
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if board[i][j] == '':
                moves.append((i, j))
            else:
                if board[i][j][0] != piece[0]:
                    moves.append((i, j))
                break
    
    elif 'queen' in piece:
        # Queen move rules
        # Combine rook and bishop moves
        moves += get_available_moves(f"{piece[0]}_rook", row, col)
        moves += get_available_moves(f"{piece[0]}_bishop", row, col)
    
    elif 'king' in piece:
        # King move rules
        possible_moves = [
            (row + 1, col), (row - 1, col),
            (row, col + 1), (row, col - 1),
            (row + 1, col + 1), (row + 1, col - 1),
            (row - 1, col + 1), (row - 1, col - 1)
        ]
        for move in possible_moves:
            r, c = move
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and (board[r][c] == '' or board[r][c][0] != piece[0]):
                moves.append(move)
    
    return moves

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle piece selection
            col = event.pos[0] // SQUARE_SIZE
            row = event.pos[1] // SQUARE_SIZE
            selected_piece = board[row][col]
            available_moves = []  # Reset available moves

            if selected_piece:
                # Calculate available moves
                available_moves = get_available_moves(selected_piece, row, col)

        if event.type == pygame.MOUSEBUTTONUP:
            # Handle piece placement
            col = event.pos[0] // SQUARE_SIZE
            row = event.pos[1] // SQUARE_SIZE

            if (row, col) in available_moves:
                # Move the piece to the selected position
                board[row][col] = selected_piece
                selected_piece = None

                # Clear the original position
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if board[i][j] == selected_piece:
                            board[i][j] = ''

    # Draw the wood-colored board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = BOARD_COLOR_W if (row + col) % 2 == 0 else BOARD_COLOR_B
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw pieces on the board
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                piece_img = pieces[piece]
                screen.blit(piece_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Highlight available moves
    for move in available_moves:
        pygame.draw.rect(screen, GREEN, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

    # Update the display
    pygame.display.flip()

#v 0.5
# made by Yes and levs16