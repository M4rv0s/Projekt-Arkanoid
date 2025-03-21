import pygame
import random

# Inicializace pygame
pygame.init()

# Konstanty
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 7
BLOCK_ROWS, BLOCK_COLS = 5, 8
BLOCK_WIDTH, BLOCK_HEIGHT = WIDTH // BLOCK_COLS, 30

# Barvy
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Nastavení okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

def create_blocks():
    return [pygame.Rect(col * BLOCK_WIDTH, row * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT) for row in range(BLOCK_ROWS) for col in range(BLOCK_COLS)], \
           [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(BLOCK_ROWS * BLOCK_COLS)]

def reset_game():
    global ball, ball_dx, ball_dy, paddle, blocks, block_colors
    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 20, 120, 10)
    ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 20, 20)
    ball_dx, ball_dy = BALL_SPEED, -BALL_SPEED
    
    if not blocks:
        blocks, block_colors = create_blocks()

# Pálka a míček
blocks, block_colors = create_blocks()
reset_game()

def draw_objects():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, block_colors[i], block)
    
    pygame.display.flip()

def show_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render("Stiskněte ENTER pro start", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def pause_game():
    show_menu()

running = True
clock = pygame.time.Clock()

show_menu()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

    # Pohyb míčku
    ball.x += ball_dx
    ball.y += ball_dy

    # Kolize se stěnami
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0:
        ball_dy = -ball_dy

    # Kolize s pálkou
    if ball.colliderect(paddle):
        ball_dy = -BALL_SPEED

    # Kolize s bloky
    for i, block in enumerate(blocks[:]):
        if ball.colliderect(block):
            blocks.pop(i)
            block_colors.pop(i)
            ball_dy = -ball_dy
            break
    
    # Obnova horní řady bloků
    if not blocks:
        blocks, block_colors = create_blocks()

    # Reset hry místo ukončení
    if ball.bottom >= HEIGHT:
        reset_game()
    
    draw_objects()

pygame.quit()
