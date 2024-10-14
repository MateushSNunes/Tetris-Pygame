import pygame
import random

# Inicializando o pygame
pygame.init()
pygame.mixer.init() 

# Dimensões da tela e da área de jogo
screen_width = 450 
screen_height = 600
block_size = 30

# Definindo cores
colors = [
    (0, 0, 0),        # Preto (fundo)
    (227, 91, 91),    # Vermelho Suave
    (105, 199, 89),   # Verde Suave
    (91, 155, 213),   # Azul Suave
    (255, 230, 109),  # Amarelo Suave
    (255, 176, 99),   # Laranja Suave
    (170, 106, 200),  # Roxo Suave
    (86, 197, 191),   # Ciano Suave
]

# Dimensões do grid
cols = 10  # 10 colunas
rows = 20  # 20 linhas

# Criando a tela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris Suave com Pontuação")

# Carregando sons
pygame.mixer.music.load('tetris_theme.mp3')  # Música de fundo
pygame.mixer.music.set_volume(0.3)  # Volume da música de fundo (ajustável)

# Definindo a velocidade do jogo (FPS maior para transições suaves)
fps = 60
clock = pygame.time.Clock()

# Estrutura das peças (tetrominoes)
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 4, 4, 4]],

    [[5, 5, 5],
     [0, 0, 5]],

    [[6, 6, 6],
     [6, 0, 0]],

    [[7, 7],
     [7, 7]]
]

# Função para rotacionar uma peça
def rotate(shape):
    return [list(reversed(col)) for col in zip(*shape)]

# Função para criar uma nova peça
def new_piece():
    return random.choice(shapes)

# Função para desenhar uma célula com sombreamento
def draw_block(x, y, color):
    # Bloco principal
    pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size), 0)
    # Borda externa
    pygame.draw.rect(screen, (255, 255, 255), (x * block_size, y * block_size, block_size, block_size), 1)
    # Sombra na parte inferior direita
    pygame.draw.line(screen, (50, 50, 50), (x * block_size, (y + 1) * block_size), ((x + 1) * block_size, (y + 1) * block_size), 2)
    pygame.draw.line(screen, (50, 50, 50), ((x + 1) * block_size, y * block_size), ((x + 1) * block_size, (y + 1) * block_size), 2)

# Função para verificar colisões (com checagem de limites)
def check_collision(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if y + off_y >= rows or x + off_x < 0 or x + off_x >= cols:
                    return True
                if grid[y + off_y][x + off_x]:
                    return True
    return False

# Função para desenhar o grid e as peças
def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            draw_block(x, y, colors[cell])
    # Desenhar as linhas do grid
    for x in range(cols):
        for y in range(rows):
            pygame.draw.rect(screen, (50, 50, 50), (x * block_size, y * block_size, block_size, block_size), 1)

# Função para remover linhas completas
def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    num_cleared = rows - len(new_grid)
    new_grid = [[0] * cols for _ in range(num_cleared)] + new_grid
    return new_grid, num_cleared

# Função para desenhar a pontuação e o nível
def draw_score_level(score, level):
    font = pygame.font.SysFont('comicsans', 30)
    # Texto da pontuação
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width - 150, 50))  # Desenha à direita do grid

    # Texto do nível
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (screen_width - 150, 100))  # Desenha abaixo da pontuação

# Função principal do jogo
def game():
    grid = [[0] * cols for _ in range(rows)]

    current_piece = new_piece()
    current_pos = [cols // 2 - len(current_piece[0]) // 2, 0]

    score = 0
    lines_cleared = 0
    level = 1
    game_over = False
    drop_speed = fps // 2  # Velocidade inicial de queda

    # Inicia a música de fundo em loop
    pygame.mixer.music.play(-1)

    while not game_over:
        screen.fill((0, 0, 0))

        # Movimentação das peças
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, current_piece, (current_pos[0] - 1, current_pos[1])):
                        current_pos[0] -= 1
                if event.key == pygame.K_RIGHT:
                    if not check_collision(grid, current_piece, (current_pos[0] + 1, current_pos[1])):
                        current_pos[0] += 1
                if event.key == pygame.K_DOWN:
                    if not check_collision(grid, current_piece, (current_pos[0], current_pos[1] + 1)):
                        current_pos[1] += 1
                if event.key == pygame.K_UP:
                    rotated_piece = rotate(current_piece)
                    if not check_collision(grid, rotated_piece, current_pos):
                        current_piece = rotated_piece

        # Movimento suave: as peças caem com base no tempo
        if pygame.time.get_ticks() % drop_speed == 0:
            if not check_collision(grid, current_piece, (current_pos[0], current_pos[1] + 1)):
                current_pos[1] += 1
            else:
                # Colocando a peça no grid
                for y, row in enumerate(current_piece):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[current_pos[1] + y][current_pos[0] + x] = cell

                # Limpa as linhas completas
                grid, cleared = clear_rows(grid)
                #if cleared > 0:
                    #clear_line_sound.play()  # Toca o som ao limpar linha
                score += cleared * 100
                lines_cleared += cleared

                # Aumenta o nível a cada 10 linhas removidas
                if lines_cleared // 10 > level - 1:
                    level += 1
                    drop_speed = max(10, drop_speed - 5)  # Aumenta a velocidade, com limite mínimo

                # Gera nova peça
                current_piece = new_piece()
                current_pos = [cols // 2 - len(current_piece[0]) // 2, 0]

                # Verifica se a nova peça colide logo no início (game over)
                if check_collision(grid, current_piece, current_pos):
                    game_over = True

        # Desenhar o grid e as peças
        draw_grid(grid)

        # Desenhar a peça atual
        for y, row in enumerate(current_piece):
            for x, cell in enumerate(row):
                if cell:
                    draw_block(current_pos[0] + x, current_pos[1] + y, colors[cell])

        # Desenhar a pontuação e o nível
        draw_score_level(score, level)

        pygame.display.flip()
        clock.tick(fps)

    # Game over
    pygame.mixer.music.stop()  # Para a música de fundo
    #game_over_sound.play()  # Toca o som de game over
    print(f"Game Over! Sua pontuação: {score}")
    pygame.quit()

if __name__ == "__main__":
    game()
