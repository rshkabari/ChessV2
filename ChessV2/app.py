import pygame
import chess
import random


# Initialize pygame
pygame.init()

# Constants
SQUARE_SIZE = 100
WIDTH = HEIGHT = 8 * SQUARE_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
DARK_GRAY = (80, 80, 80)
HIGHLIGHT_COLOR = (175, 175, 0, 70)  # Yellow shade for highlighting
player_color = chess.WHITE


# Display and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()

# Load piece images
background_image = pygame.image.load("background.png")
piece_images = {}
for color in ["white", "black"]:
    for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
        image_name = f"{color}_{piece}.png"
        piece_images[f"{color}_{piece}"] = pygame.image.load(image_name)



def piece_to_string(piece_symbol):
    mapping = {
        'P': 'pawn', 'p': 'pawn',
        'R': 'rook', 'r': 'rook',
        'N': 'knight', 'n': 'knight',
        'B': 'bishop', 'b': 'bishop',
        'Q': 'queen', 'q': 'queen',
        'K': 'king', 'k': 'king',
    }
    return mapping.get(piece_symbol)

board = chess.Board()

def draw_board(possible_moves=[]):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else DARK_GRAY
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            square = chess.square(col, 7 - row)
            if square == selected_square:
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)  # Per-pixel alpha
                highlight.fill(HIGHLIGHT_COLOR)  # Yellow highlight for the selected piece
                screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            square = chess.square(col, 7 - row)
            if square in possible_moves:
                piece_at_destination = board.piece_at(square)
                
                if piece_at_destination and piece_at_destination.color != player_color:
                    highlight_color = (255, 0, 0, 70)  # Red for capture
                else:
                    highlight_color = (0, 0, 255, 70)  # Blue for normal move
                
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)  # Per-pixel alpha
                highlight.fill(highlight_color)  # Color for transparent highlight
                screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            piece = board.piece_at(square)
            if piece:
                piece_string = piece_to_string(piece.symbol())
                color_string = "white" if piece.color == chess.WHITE else "black"
                piece_image = piece_images[f"{color_string}_{piece_string}"]

                x_position = col * SQUARE_SIZE + (SQUARE_SIZE - piece_image.get_width()) // 2
                y_position = row * SQUARE_SIZE + (SQUARE_SIZE - piece_image.get_height()) // 2
                screen.blit(piece_image, (x_position, y_position))



def computer_move():
    legal_moves = list(board.legal_moves)
    if legal_moves:  # Check if the list is not empty
        move = random.choice(legal_moves)
        board.push(move)
    else:
        # Handle the situation where the computer has no legal moves.
        # Depending on the context, this can be a checkmate, stalemate, or some other endgame condition.
        pass


font = pygame.font.SysFont(None, 36) 

def display_starting_menu(screen):
    """Displays a starting menu with Start and Exit buttons on the Pygame screen.

    Args:
    - screen: The main Pygame display surface.

    Returns:
    The action the player chose: "Start" or "Exit".
    """

    # Constants for the screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Darken the screen
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)  # Set the alpha value
    overlay.fill((0, 0, 0))  # This creates a black overlay

    screen.blit(background_image, (0, 0))
    screen.blit(overlay, (0, 0))

    # Font setup
    font = pygame.font.Font(None, 36)

    # Display the welcome message
    welcome_message = "Welcome!"
    text = font.render(welcome_message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - 40))
    screen.blit(text, text_rect)

    # Draw the buttons and store their rects for click detection
    start_button = pygame.draw.rect(screen, (100, 100, 100), (screen_width/2 - 70, screen_height/2, 140, 40))
    exit_button = pygame.draw.rect(screen, (100, 100, 100), (screen_width/2 - 70, screen_height/2 + 50, 140, 40))

    # Render and position the text for the buttons
    start_text = font.render("Start", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    exit_text = font.render("Exit", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    # Event loop to detect button clicks
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "Start"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()


def display_endgame_message(screen, winner):
    """Displays an endgame message with Restart and Exit buttons on the Pygame screen.

    Args:
    - screen: The main Pygame display surface.
    - winner: A string indicating the endgame message.

    Returns:
    None.
    """

    # Constants for the screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Darken the screen
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(200)  # More opaque
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Font setup
    font = pygame.font.Font(None, 36)
    
    # Display the message
    message = winner
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - 40))
    screen.blit(text, text_rect)

    # Draw the buttons and store their rects for click detection
    restart_button = pygame.draw.rect(screen, (100, 100, 100), (screen_width/2 - 70, screen_height/2, 140, 40))
    exit_button = pygame.draw.rect(screen, (100, 100, 100), (screen_width/2 - 70, screen_height/2 + 50, 140, 40))

    # Render and position the text for the buttons
    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    exit_text = font.render("Exit", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    # Event loop to detect button clicks
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    
                    return "Restart"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

running = True
player_turn = True
selected_piece = None
selected_square = None
possible_moves = []

result = display_starting_menu(screen)
if result == "Exit":
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            square = chess.square(col, 7 - row)

            # If a piece is already selected
            if selected_piece:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    player_turn = False
                # Reset selection
                selected_piece = None
                selected_square = None
                possible_moves = []
            else:
                # Select a piece if there's one on the clicked square
                if board.piece_at(square):
                    selected_piece = board.piece_at(square)
                    selected_square = square
                    possible_moves = [move.to_square for move in board.legal_moves if move.from_square == square]






    if not player_turn:
        computer_move()
        player_turn = True

    draw_board(possible_moves)
    # Check endgame conditions and show the popup dialog
    if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        winner = None
        result = None
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                winner = "Black"
            else:
                winner = "White"
            result = display_endgame_message(screen, f"{winner} wins by checkmate!")
            if result == "Restart":
                board = chess.Board()
                player_turn = True
                selected_piece = None
                selected_square = None
                possible_moves = []
        elif board.is_stalemate():
            result = display_endgame_message(screen, "Game is a stalemate!")
            if result == "Restart":
                board = chess.Board()
                player_turn = True
                selected_piece = None
                selected_square = None
                possible_moves = []
        elif board.is_insufficient_material():
            result = display_endgame_message(screen, "Game is a draw due to insufficient material!")
            if result == "Restart":
                board = chess.Board()
                player_turn = True
                selected_piece = None
                selected_square = None
                possible_moves = []
        elif board.is_seventyfive_moves():
            result = display_endgame_message(screen, "Game is a draw due to 75 move rule!")
            if result == "Restart":
                board = chess.Board()
                player_turn = True
                selected_piece = None
                selected_square = None
                possible_moves = []
        elif board.is_fivefold_repetition():
            result = display_endgame_message(screen, "Game is a draw due to fivefold repetition!")
            if result == "Restart":
                board = chess.Board()
                player_turn = True
                selected_piece = None
                selected_square = None
                possible_moves = []
        
        

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()