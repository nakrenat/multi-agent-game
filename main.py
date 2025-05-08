import pygame
import sys
import random
import json
import os
import math
from grid import Grid
from agent import Agent, Strategy

# Initialize Pygame
pygame.init()

# Screen settings
WINDOW_SIZE = (800, 600)
GRID_SIZE = (20, 15)
CELL_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)

# Modern color palette
MODERN_COLORS = {
    'background': (18, 18, 18),
    'grid': (40, 40, 40),
    'accent': (0, 150, 255),
    'success': (46, 204, 113),
    'warning': (241, 196, 15),
    'danger': (231, 76, 60),
    'text': (236, 240, 241),
    'button': (52, 152, 219),
    'button_hover': (41, 128, 185)
}

# Difficulty settings
class Difficulty:
    EASY = 0
    MEDIUM = 1
    HARD = 2

DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {
        'agent_speed': 3,
        'agent_count': 3,
        'score_multiplier': 1,
        'target_score': 50,
        'agent_behaviors': {
            'random': {'move_chance': 0.3, 'detection_range': 3},
            'defensive': {'move_chance': 0.4, 'detection_range': 4},
            'patrol': {'move_chance': 0.5, 'detection_range': 3}
        }
    },
    Difficulty.MEDIUM: {
        'agent_speed': 4,
        'agent_count': 4,
        'score_multiplier': 2,
        'target_score': 100,
        'agent_behaviors': {
            'random': {'move_chance': 0.5, 'detection_range': 4},
            'defensive': {'move_chance': 0.6, 'detection_range': 5},
            'patrol': {'move_chance': 0.7, 'detection_range': 4}
        }
    },
    Difficulty.HARD: {
        'agent_speed': 5,
        'agent_count': 5,
        'score_multiplier': 3,
        'target_score': 150,
        'agent_behaviors': {
            'random': {'move_chance': 0.7, 'detection_range': 5},
            'defensive': {'move_chance': 0.8, 'detection_range': 6},
            'patrol': {'move_chance': 0.9, 'detection_range': 5}
        }
    }
}

# Create screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Multi-Agent Game Simulation")

# Load user agent image
try:
    user_image = pygame.image.load("me.jpg")
    user_image = pygame.transform.scale(user_image, (CELL_SIZE, CELL_SIZE))
except:
    print("Image could not be loaded, using default circle")
    user_image = None

# Load defensive agent image
try:
    defensive_image = pygame.image.load("raz.jpeg")
    defensive_image = pygame.transform.scale(defensive_image, (CELL_SIZE, CELL_SIZE))
except:
    print("Defensive agent image could not be loaded, using default circle")
    defensive_image = None

# Create grid
grid = Grid(GRID_SIZE[0], GRID_SIZE[1], CELL_SIZE)

# High scores file
HIGH_SCORES_FILE = "high_scores.json"

# Create fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
floating_font = pygame.font.Font(None, 48)
score_font = pygame.font.Font(None, 72)
input_font = pygame.font.Font(None, 48)
title_font = pygame.font.Font(None, 96)

class FloatingScore:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.lifetime = 30
        self.alpha = 255
        
    def update(self):
        self.y -= 1
        self.lifetime -= 1
        self.alpha = int((self.lifetime / 30) * 255)
        return self.lifetime > 0
    
    def draw(self, screen):
        if self.lifetime > 0:
            text = floating_font.render(f"+{self.score}", True, GREEN)
            text.set_alpha(self.alpha)
            screen.blit(text, (self.x, self.y))

class WelcomeAnimation:
    def __init__(self):
        self.particles = []
        self.create_particles()
        
    def create_particles(self):
        for _ in range(50):
            x = random.randint(0, WINDOW_SIZE[0])
            y = random.randint(0, WINDOW_SIZE[1])
            speed = random.uniform(1, 3)
            angle = random.uniform(0, 2 * math.pi)
            size = random.randint(2, 4)
            self.particles.append({
                'x': x, 'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': size,
                'color': random.choice([GOLD, WHITE, CYAN])
            })
    
    def update(self):
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            
            if p['x'] < 0 or p['x'] > WINDOW_SIZE[0]:
                p['dx'] *= -1
            if p['y'] < 0 or p['y'] > WINDOW_SIZE[1]:
                p['dy'] *= -1
    
    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, p['color'],
                             (int(p['x']), int(p['y'])), p['size'])

class Confetti:
    def __init__(self):
        self.x = random.randint(0, WINDOW_SIZE[0])
        self.y = random.randint(-100, 0)
        self.size = random.randint(5, 15)
        self.speed = random.uniform(2, 5)
        self.color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, GOLD])
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.shape = random.choice(['circle', 'square', 'triangle'])
    
    def update(self):
        self.y += self.speed
        self.rotation += self.rotation_speed
        return self.y < WINDOW_SIZE[1]
    
    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        elif self.shape == 'square':
            points = [
                (self.x - self.size, self.y - self.size),
                (self.x + self.size, self.y - self.size),
                (self.x + self.size, self.y + self.size),
                (self.x - self.size, self.y + self.size)
            ]
            rotated_points = []
            for point in points:
                # Rotate point around center
                dx = point[0] - self.x
                dy = point[1] - self.y
                angle = math.radians(self.rotation)
                new_x = self.x + dx * math.cos(angle) - dy * math.sin(angle)
                new_y = self.y + dx * math.sin(angle) + dy * math.cos(angle)
                rotated_points.append((new_x, new_y))
            pygame.draw.polygon(screen, self.color, rotated_points)
        else:  # triangle
            points = [
                (self.x, self.y - self.size),
                (self.x - self.size, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ]
            rotated_points = []
            for point in points:
                dx = point[0] - self.x
                dy = point[1] - self.y
                angle = math.radians(self.rotation)
                new_x = self.x + dx * math.cos(angle) - dy * math.sin(angle)
                new_y = self.y + dx * math.sin(angle) + dy * math.cos(angle)
                rotated_points.append((new_x, new_y))
            pygame.draw.polygon(screen, self.color, rotated_points)

class VictoryScreen:
    def __init__(self):
        self.confetti = []
        self.create_confetti()
    
    def create_confetti(self):
        for _ in range(100):  # Create 100 confetti pieces
            self.confetti.append(Confetti())
    
    def update(self):
        # Update existing confetti
        self.confetti = [c for c in self.confetti if c.update()]
        
        # Add new confetti if needed
        while len(self.confetti) < 100:
            self.confetti.append(Confetti())
    
    def draw(self, screen):
        for confetti in self.confetti:
            confetti.draw(screen)

class TextCache:
    def __init__(self):
        self.cache = {}
        self.last_scale = 1.0
        self.last_score = 0
        self.last_target = 0
    
    def get_text(self, text, font, color, scale=1.0):
        key = (text, font, color, scale)
        if key not in self.cache:
            text_surface = font.render(text, True, color)
            if scale != 1.0:
                text_surface = pygame.transform.scale(text_surface,
                    (int(text_surface.get_width() * scale),
                     int(text_surface.get_height() * scale)))
            self.cache[key] = text_surface
        return self.cache[key]
    
    def clear(self):
        self.cache.clear()
        self.last_scale = 1.0
        self.last_score = 0
        self.last_target = 0

def load_high_scores():
    """Load high scores from file"""
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_high_score(name, score):
    """Save new high score"""
    high_scores = load_high_scores()
    high_scores.append({"name": name, "score": score})
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    high_scores = high_scores[:5]
    
    with open(HIGH_SCORES_FILE, 'w') as f:
        json.dump(high_scores, f)
    
    return high_scores

def get_random_position():
    """Get random position on grid"""
    return (random.randint(0, GRID_SIZE[0]-1), random.randint(0, GRID_SIZE[1]-1))

def show_difficulty_selection():
    """Show difficulty selection screen"""
    screen.fill(BLACK)
    
    # Draw animated particles
    welcome_animation.update()
    welcome_animation.draw(screen)
    
    # Title
    title = title_font.render('Select Difficulty', True, GOLD)
    title_rect = title.get_rect(center=(WINDOW_SIZE[0]//2, 150))
    
    # Glow effect
    for i in range(3):
        glow = title_font.render('Select Difficulty', True, (GOLD[0]//2, GOLD[1]//2, GOLD[2]//2))
        glow_rect = glow.get_rect(center=(WINDOW_SIZE[0]//2 + i*2, 150 + i*2))
        screen.blit(glow, glow_rect)
    
    screen.blit(title, title_rect)
    
    # Difficulty buttons
    difficulties = [
        ("Easy", GREEN, 250),
        ("Medium", YELLOW, 350),
        ("Hard", RED, 450)
    ]
    
    for text, color, y_pos in difficulties:
        button = pygame.Rect(WINDOW_SIZE[0]//2 - 100, y_pos, 200, 50)
        pygame.draw.rect(screen, color, button)
        pygame.draw.rect(screen, WHITE, button, 2)
        
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)
    
    # Instructions
    instruction = font.render('Click to select difficulty', True, WHITE)
    instruction_rect = instruction.get_rect(center=(WINDOW_SIZE[0]//2, 550))
    screen.blit(instruction, instruction_rect)

def show_welcome_screen():
    """Show welcome screen with animations"""
    screen.fill(BLACK)
    
    welcome_animation.update()
    welcome_animation.draw(screen)
    
    title = title_font.render('Multi-Agent Game', True, GOLD)
    title_rect = title.get_rect(center=(WINDOW_SIZE[0]//2, 150))
    
    for i in range(3):
        glow = title_font.render('Multi-Agent Game', True, (GOLD[0]//2, GOLD[1]//2, GOLD[2]//2))
        glow_rect = glow.get_rect(center=(WINDOW_SIZE[0]//2 + i*2, 150 + i*2))
        screen.blit(glow, glow_rect)
    
    screen.blit(title, title_rect)
    
    input_box = pygame.Rect(WINDOW_SIZE[0]//2 - 150, 300, 300, 50)
    for i in range(3):
        pygame.draw.rect(screen, (GOLD[0]//(i+1), GOLD[1]//(i+1), GOLD[2]//(i+1)),
                        input_box.inflate(i*2, i*2), 1)
    
    name_text = input_font.render(player_name, True, WHITE)
    name_rect = name_text.get_rect(center=input_box.center)
    screen.blit(name_text, name_rect)
    
    alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.003))
    instruction1 = font.render('Enter your name and press ENTER', True, WHITE)
    instruction1.set_alpha(alpha)
    instruction1_rect = instruction1.get_rect(center=(WINDOW_SIZE[0]//2, 400))
    screen.blit(instruction1, instruction1_rect)
    
    instruction2 = font.render('Press ESC to exit', True, WHITE)
    instruction2_rect = instruction2.get_rect(center=(WINDOW_SIZE[0]//2, 450))
    screen.blit(instruction2, instruction2_rect)

def show_high_scores():
    """Show high scores"""
    high_scores = load_high_scores()
    
    overlay = pygame.Surface(WINDOW_SIZE)
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    title = game_over_font.render('High Scores', True, GOLD)
    title_rect = title.get_rect(center=(WINDOW_SIZE[0]//2, 100))
    screen.blit(title, title_rect)
    
    for i, score_data in enumerate(high_scores):
        score_text = font.render(f"{i+1}. {score_data['name']}: {score_data['score']}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_SIZE[0]//2, 200 + i*50))
        screen.blit(score_text, score_rect)
    
    continue_text = font.render('Press SPACE to continue', True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1] - 100))
    screen.blit(continue_text, continue_rect)

def draw_modern_button(screen, text, x, y, width, height, color=MODERN_COLORS['button'], hover_color=MODERN_COLORS['button_hover']):
    """Draw a modern button with hover effect"""
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = (x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height)
    
    # Button background
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    
    # Button shadow
    shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 50))
    screen.blit(shadow_surface, (x + 2, y + 2))
    
    # Button text
    text_surface = text_cache.get_text(text, font, MODERN_COLORS['text'])
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surface, text_rect)
    
    return is_hovered

def draw_modern_grid():
    """Draw a modern grid with gradient lines"""
    for x in range(GRID_SIZE[0] + 1):
        alpha = int(100 * (1 - x/GRID_SIZE[0]))
        pygame.draw.line(screen, (*MODERN_COLORS['grid'], alpha),
                        (x * CELL_SIZE, 0),
                        (x * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE))
    for y in range(GRID_SIZE[1] + 1):
        alpha = int(100 * (1 - y/GRID_SIZE[1]))
        pygame.draw.line(screen, (*MODERN_COLORS['grid'], alpha),
                        (0, y * CELL_SIZE),
                        (GRID_SIZE[0] * CELL_SIZE, y * CELL_SIZE))

def draw_modern_score_box():
    """Draw a modern score box with glass effect"""
    box_width = 200
    box_height = 100
    box_x = 20
    box_y = 20
    
    # Glass effect background
    glass_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    glass_surface.fill((255, 255, 255, 30))
    screen.blit(glass_surface, (box_x, box_y))
    
    # Border
    pygame.draw.rect(screen, MODERN_COLORS['accent'], 
                    (box_x, box_y, box_width, box_height), 
                    2, border_radius=10)
    
    # Score text
    score_text = text_cache.get_text(str(user_score), score_font, MODERN_COLORS['accent'])
    score_rect = score_text.get_rect(center=(box_x + box_width//2, box_y + box_height//2))
    screen.blit(score_text, score_rect)
    
    # Target score
    target_score = DIFFICULTY_SETTINGS[current_difficulty]['target_score']
    target_text = text_cache.get_text(f"Target: {target_score}", font, MODERN_COLORS['text'])
    target_rect = target_text.get_rect(center=(box_x + box_width//2, box_y + box_height + 20))
    screen.blit(target_text, target_rect)

def show_modern_victory_screen():
    """Show a modern victory screen"""
    # Dark overlay with blur effect
    overlay = pygame.Surface(WINDOW_SIZE)
    overlay.set_alpha(200)
    overlay.fill(MODERN_COLORS['background'])
    screen.blit(overlay, (0, 0))
    
    # Update and draw confetti
    victory_screen.update()
    victory_screen.draw(screen)
    
    # Victory text with glow effect
    scale = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
    if scale != text_cache.last_scale:
        text_cache.clear()
        text_cache.last_scale = scale
    
    victory_text = text_cache.get_text('VICTORY!', game_over_font, MODERN_COLORS['success'], scale)
    text_rect = victory_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 50))
    
    # Glow effect
    for i in range(3):
        glow = text_cache.get_text('VICTORY!', game_over_font, 
                                 (*MODERN_COLORS['success'], 100 - i*30), scale)
        glow_rect = glow.get_rect(center=(WINDOW_SIZE[0]//2 + i*2, WINDOW_SIZE[1]//2 - 50 + i*2))
        screen.blit(glow, glow_rect)
    
    screen.blit(victory_text, text_rect)
    
    # Score display
    score_text = text_cache.get_text(f'Final Score: {user_score}', font, MODERN_COLORS['text'])
    score_rect = score_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 50))
    screen.blit(score_text, score_rect)
    
    # Modern buttons
    button_width = 200
    button_height = 50
    button_x = WINDOW_SIZE[0]//2 - button_width//2
    
    play_again_rect = pygame.Rect(button_x, WINDOW_SIZE[1]//2 + 100, button_width, button_height)
    exit_game_rect = pygame.Rect(button_x, WINDOW_SIZE[1]//2 + 170, button_width, button_height)
    
    play_again = draw_modern_button(screen, 'Play Again', 
                                  button_x, WINDOW_SIZE[1]//2 + 100,
                                  button_width, button_height)
    
    exit_game = draw_modern_button(screen, 'Exit Game',
                                 button_x, WINDOW_SIZE[1]//2 + 170,
                                 button_width, button_height,
                                 MODERN_COLORS['danger'],
                                 (200, 50, 50))
    
    return play_again_rect, exit_game_rect

def show_modern_game_over():
    """Show a modern game over screen"""
    # Dark overlay with blur effect
    overlay = pygame.Surface(WINDOW_SIZE)
    overlay.set_alpha(200)
    overlay.fill(MODERN_COLORS['background'])
    screen.blit(overlay, (0, 0))
    
    # Game over text with glow effect
    scale = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
    if scale != text_cache.last_scale:
        text_cache.clear()
        text_cache.last_scale = scale
    
    game_over_text = text_cache.get_text('GAME OVER', game_over_font, MODERN_COLORS['danger'], scale)
    text_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 50))
    
    # Glow effect
    for i in range(3):
        glow = text_cache.get_text('GAME OVER', game_over_font,
                                 (*MODERN_COLORS['danger'], 100 - i*30), scale)
        glow_rect = glow.get_rect(center=(WINDOW_SIZE[0]//2 + i*2, WINDOW_SIZE[1]//2 - 50 + i*2))
        screen.blit(glow, glow_rect)
    
    screen.blit(game_over_text, text_rect)
    
    # Score display
    score_text = text_cache.get_text(f'Score: {user_score}', font, MODERN_COLORS['text'])
    score_rect = score_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 50))
    screen.blit(score_text, score_rect)
    
    # Modern buttons
    button_width = 200
    button_height = 50
    button_x = WINDOW_SIZE[0]//2 - button_width//2
    
    try_again_rect = pygame.Rect(button_x, WINDOW_SIZE[1]//2 + 100, button_width, button_height)
    exit_game_rect = pygame.Rect(button_x, WINDOW_SIZE[1]//2 + 170, button_width, button_height)
    
    try_again = draw_modern_button(screen, 'Try Again',
                                 button_x, WINDOW_SIZE[1]//2 + 100,
                                 button_width, button_height)
    
    exit_game = draw_modern_button(screen, 'Exit Game',
                                 button_x, WINDOW_SIZE[1]//2 + 170,
                                 button_width, button_height,
                                 MODERN_COLORS['danger'],
                                 (200, 50, 50))
    
    return try_again_rect, exit_game_rect

def reset_game():
    """Reset game state"""
    global user_agent, user_score, game_over, agents, floating_scores
    user_agent = Agent(10, 7, None, PURPLE, grid)
    user_score = 0
    game_over = False
    game_won = False
    floating_scores.clear()
    
    # Create agents based on difficulty
    settings = DIFFICULTY_SETTINGS[current_difficulty]
    behaviors = settings['agent_behaviors']
    
    agents = [
        Agent(5, 5, Strategy.RANDOM, RED, grid),
        Agent(15, 5, Strategy.GREEDY, GREEN, grid)
    ]
    
    if settings['agent_count'] >= 3:
        defensive_agent = Agent(5, 10, Strategy.DEFENSIVE, BLUE, grid)
        defensive_agent.move_chance = behaviors['defensive']['move_chance']
        defensive_agent.detection_range = behaviors['defensive']['detection_range']
        defensive_agent.image = defensive_image  # Set the defensive agent image
        agents.append(defensive_agent)
    
    if settings['agent_count'] >= 4:
        patrol_agent = Agent(15, 10, Strategy.PATROL, YELLOW, grid)
        patrol_agent.move_chance = behaviors['patrol']['move_chance']
        patrol_agent.detection_range = behaviors['patrol']['detection_range']
        patrol_agent.image = defensive_image  # Set the defensive agent image for patrol agent
        agents.append(patrol_agent)
    
    if settings['agent_count'] >= 5:
        random_agent = Agent(10, 12, Strategy.RANDOM, CYAN, grid)
        random_agent.move_chance = behaviors['random']['move_chance']
        random_agent.detection_range = behaviors['random']['detection_range']
        random_agent.image = defensive_image  # Set the defensive agent image for random agent
        agents.append(random_agent)

def respawn_target():
    """Respawn target agent (green) to new position"""
    new_x, new_y = get_random_position()
    while any(abs(new_x - a.x) < 3 and abs(new_y - a.y) < 3 for a in agents + [user_agent]):
        new_x, new_y = get_random_position()
    agents[1].x = new_x
    agents[1].y = new_y

# Game state
clock = pygame.time.Clock()
running = True
game_over = False
game_won = False
showing_high_scores = False
showing_welcome = True
showing_difficulty = False
current_difficulty = Difficulty.EASY
player_name = ""

# Create welcome animation
welcome_animation = WelcomeAnimation()

# Create victory screen
victory_screen = VictoryScreen()

# Create text cache
text_cache = TextCache()

# Create initial agents
agents = [
    Agent(5, 5, Strategy.RANDOM, RED, grid),
    Agent(15, 5, Strategy.GREEDY, GREEN, grid)
]

# Create user agent
user_agent = Agent(10, 7, None, PURPLE, grid)
user_score = 0

# Floating scores list
floating_scores = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                if game_over or game_won:
                    reset_game()
                elif showing_high_scores:
                    showing_high_scores = False
            elif event.key == pygame.K_RETURN:
                if showing_welcome and player_name.strip():
                    showing_welcome = False
                    showing_difficulty = True
                elif game_over or game_won:
                    save_high_score(player_name, user_score)
                    showing_high_scores = True
            elif showing_welcome or (game_over and not showing_high_scores):
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 10:
                    if event.unicode.isalnum():
                        player_name += event.unicode
            elif not game_over and not showing_high_scores:
                if event.key == pygame.K_UP:
                    if grid.is_valid_position(user_agent.x, user_agent.y - 1):
                        user_agent.y -= 1
                elif event.key == pygame.K_DOWN:
                    if grid.is_valid_position(user_agent.x, user_agent.y + 1):
                        user_agent.y += 1
                elif event.key == pygame.K_LEFT:
                    if grid.is_valid_position(user_agent.x - 1, user_agent.y):
                        user_agent.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if grid.is_valid_position(user_agent.x + 1, user_agent.y):
                        user_agent.x += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if showing_difficulty:
                if 250 <= mouse_pos[1] <= 300:  # Easy
                    current_difficulty = Difficulty.EASY
                    showing_difficulty = False
                    reset_game()
                elif 350 <= mouse_pos[1] <= 400:  # Medium
                    current_difficulty = Difficulty.MEDIUM
                    showing_difficulty = False
                    reset_game()
                elif 450 <= mouse_pos[1] <= 500:  # Hard
                    current_difficulty = Difficulty.HARD
                    showing_difficulty = False
                    reset_game()
            elif game_won:
                play_again_rect, exit_game_rect = show_modern_victory_screen()
                if play_again_rect.collidepoint(mouse_pos):
                    reset_game()
                elif exit_game_rect.collidepoint(mouse_pos):
                    running = False
            elif game_over:
                try_again_rect, exit_game_rect = show_modern_game_over()
                if try_again_rect.collidepoint(mouse_pos):
                    reset_game()
                elif exit_game_rect.collidepoint(mouse_pos):
                    running = False
    
    screen.fill(MODERN_COLORS['background'])
    
    if showing_welcome:
        show_welcome_screen()
    elif showing_difficulty:
        show_difficulty_selection()
    elif showing_high_scores:
        show_high_scores()
    else:
        draw_modern_grid()
        
        if not game_over and not game_won:
            for i, agent in enumerate(agents):
                if i != 1:  # Skip the green target agent
                    other_agents = [a for a in agents if a != agent] + [user_agent]
                    agent.move(other_agents)
                
                # Draw agent with image if available
                if agent.image:  # Check if agent has an image
                    for j in range(3):
                        glow = pygame.transform.scale(agent.image,
                            (CELL_SIZE + j*2, CELL_SIZE + j*2))
                        glow.set_alpha(100 - j*30)
                        screen.blit(glow,
                            (agent.x * CELL_SIZE - j,
                             agent.y * CELL_SIZE - j))
                    screen.blit(agent.image,
                        (agent.x * CELL_SIZE,
                         agent.y * CELL_SIZE))
                else:
                    for j in range(3):
                        glow_size = CELL_SIZE // 3 + j
                        pygame.draw.circle(screen, agent.color,
                                         (agent.x * CELL_SIZE + CELL_SIZE // 2,
                                          agent.y * CELL_SIZE + CELL_SIZE // 2),
                                         glow_size, 1)
                    
                    pygame.draw.circle(screen, agent.color,
                                     (agent.x * CELL_SIZE + CELL_SIZE // 2,
                                      agent.y * CELL_SIZE + CELL_SIZE // 2),
                                     CELL_SIZE // 3)
                
                if agent.x == user_agent.x and agent.y == user_agent.y:
                    if i == 1:
                        score_increase = 10 * DIFFICULTY_SETTINGS[current_difficulty]['score_multiplier']
                        user_score += score_increase
                        floating_scores.append(FloatingScore(
                            agent.x * CELL_SIZE,
                            agent.y * CELL_SIZE,
                            score_increase
                        ))
                        respawn_target()
                        
                        # Check for win condition
                        if user_score >= DIFFICULTY_SETTINGS[current_difficulty]['target_score']:
                            game_won = True
                    elif agent.strategy == Strategy.DEFENSIVE:
                        user_score -= 5
                        floating_scores.append(FloatingScore(
                            agent.x * CELL_SIZE,
                            agent.y * CELL_SIZE,
                            -5
                        ))
                    else:
                        game_over = True
            
            if user_image:
                for j in range(3):
                    glow = pygame.transform.scale(user_image,
                        (CELL_SIZE + j*2, CELL_SIZE + j*2))
                    glow.set_alpha(100 - j*30)
                    screen.blit(glow,
                        (user_agent.x * CELL_SIZE - j,
                         user_agent.y * CELL_SIZE - j))
                screen.blit(user_image,
                    (user_agent.x * CELL_SIZE,
                     user_agent.y * CELL_SIZE))
            else:
                for j in range(3):
                    pygame.draw.circle(screen, user_agent.color,
                                     (user_agent.x * CELL_SIZE + CELL_SIZE // 2,
                                      user_agent.y * CELL_SIZE + CELL_SIZE // 2),
                                     CELL_SIZE // 3 + j, 1)
                pygame.draw.circle(screen, user_agent.color,
                                 (user_agent.x * CELL_SIZE + CELL_SIZE // 2,
                                  user_agent.y * CELL_SIZE + CELL_SIZE // 2),
                                 CELL_SIZE // 3)
            
            floating_scores = [score for score in floating_scores if score.update()]
            for score in floating_scores:
                score.draw(screen)
            
            draw_modern_score_box()
            
            # Draw modern controls info
            controls_text = text_cache.get_text('Controls: Arrow Keys', font, MODERN_COLORS['text'])
            screen.blit(controls_text, (WINDOW_SIZE[0] - 300, GRID_SIZE[1] * CELL_SIZE + 10))
            
            target_text = text_cache.get_text('Target: Green Dot (+10 points)', font, MODERN_COLORS['success'])
            screen.blit(target_text, (WINDOW_SIZE[0]//2 - 150, GRID_SIZE[1] * CELL_SIZE + 10))
        elif game_won:
            show_modern_victory_screen()
        else:
            show_modern_game_over()
    
    pygame.display.flip()
    clock.tick(DIFFICULTY_SETTINGS[current_difficulty]['agent_speed'])

pygame.quit()
sys.exit() 