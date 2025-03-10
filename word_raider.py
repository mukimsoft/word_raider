import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
FONT_NAME = 'Arial'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_GRAY = (150, 150, 150)
GOLD = (218, 165, 32)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Load assets
background_img = pygame.image.load('background.jpg')  # Add your own background image
button_img = pygame.image.load('button.png')  # Add your own button image
icon = pygame.image.load('icon.png')  # Add your own icon

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Raider")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Game variables
word_bank = ["PYTHON", "PYGAME", "DEVELOPER", "ADVENTURE", "TREASURE", "CODING", "CHALLENGE"]
current_word = ""
scrambled_word = ""
input_text = ""
score = 0
time_left = 60
game_over = False
high_score = 0

# Load high score from file
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0


def save_high_score():
    with open("high_score.txt", "w") as File:
        File.write(str(high_score))


def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)  # This is correct

    screen.blit(text_surface, text_rect)

def scramble_word(word):
    word_letters = list(word)
    random.shuffle(word_letters)
    return ''.join(word_letters)


def new_word():
    global current_word, scrambled_word, input_text
    current_word = random.choice(word_bank)
    scrambled_word = scramble_word(current_word)
    input_text = ""


def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    draw_text(text, 20, WHITE, x + w / 2, y + h / 2)


def main_menu():
    global high_score
    menu = True
    while menu:
        screen.blit(background_img, (0, 0))
        draw_text("Word Raider", 75, GOLD, WIDTH / 2, HEIGHT / 4)
        draw_text(f"High Score: {high_score}", 30, WHITE, WIDTH / 2, HEIGHT / 2 - 50)

        button("Start Game", WIDTH / 2 - 100, HEIGHT / 2, 200, 50, GRAY, HOVER_GRAY, game_loop)
        button("Instructions", WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50, GRAY, HOVER_GRAY, instructions)
        button("Quit", WIDTH / 2 - 100, HEIGHT / 2 + 140, 200, 50, GRAY, HOVER_GRAY, quit_game)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def instructions():
    inst = True
    while inst:
        screen.blit(background_img, (0, 0))
        draw_text("Instructions", 50, GOLD, WIDTH / 2, HEIGHT / 4)
        draw_text("1. Unscramble the word before time runs out!", 25, WHITE, WIDTH / 2, HEIGHT / 2 - 50)
        draw_text("2. Type your guess in the input box", 25, WHITE, WIDTH / 2, HEIGHT / 2 - 20)
        draw_text("3. Correct answers give points and extra time", 25, WHITE, WIDTH / 2, HEIGHT / 2 + 10)
        draw_text("4. Wrong answers or time out ends the game", 25, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        button("Back", WIDTH / 2 - 50, HEIGHT - 100, 100, 50, GRAY, HOVER_GRAY, main_menu)

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def game_loop():
    global input_text, score, time_left, game_over, high_score

    new_word()
    input_active = False
    time_left = 60
    score = 0
    game_over = False

    input_box = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)
    color_inactive = GRAY
    color = color_inactive  # Removed unused color_active variable

    while not game_over:
        screen.blit(background_img, (0, 0))
        draw_text("Scrambled Word:", 30, WHITE, WIDTH / 2, HEIGHT / 4)
        draw_text(scrambled_word, 40, GOLD, WIDTH / 2, HEIGHT / 2 - 50)

        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(input_text, 30, WHITE, input_box.x + 10, input_box.y + 15, center=False)

        draw_text(f"Time: {int(time_left)}", 30, WHITE, WIDTH - 100, 50)
        draw_text(f"Score: {score}", 30, WHITE, 100, 50)

        if time_left > 0:
            time_left -= 1 / FPS
        else:
            game_over = True

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and input_active:
                if event.key == K_RETURN:
                    if input_text.upper() == current_word:
                        score += 10 * len(current_word)
                        time_left += 5
                        new_word()
                        input_text = ""
                    else:
                        game_over = True
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    if score > high_score:
        high_score = score
        save_high_score()

    game_over_screen()


def game_over_screen():
    while True:
        screen.blit(background_img, (0, 0))
        draw_text("Game Over", 75, RED, WIDTH / 2, HEIGHT / 3)
        draw_text(f"Your Score: {score}", 40, WHITE, WIDTH / 2, HEIGHT / 2)

        button("Play Again", WIDTH / 2 - 150, HEIGHT - 150, 140, 50, GRAY, HOVER_GRAY, game_loop)
        button("Main Menu", WIDTH / 2 + 10, HEIGHT - 150, 140, 50, GRAY, HOVER_GRAY, main_menu)

        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    save_high_score()
    pygame.quit()
    sys.exit()


# Start the game
main_menu()