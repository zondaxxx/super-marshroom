import pygame
import random
import math
from game_objects import *

# Screen constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

def create_mario_sprite():
    """Create Mario sprite"""
    surf = pygame.Surface((70, 90), pygame.SRCALPHA)
    # Body
    pygame.draw.rect(surf, RED, (10, 25, 50, 40))
    # Head
    pygame.draw.ellipse(surf, (255, 220, 177), (15, 5, 40, 30))
    # Hat
    pygame.draw.ellipse(surf, RED, (10, 0, 50, 20))
    # Overalls
    pygame.draw.rect(surf, BLUE, (15, 40, 40, 30))
    # Legs
    pygame.draw.rect(surf, BROWN, (15, 70, 18, 20))
    pygame.draw.rect(surf, BROWN, (37, 70, 18, 20))
    # Eyes
    pygame.draw.circle(surf, BLACK, (30, 18), 3)
    pygame.draw.circle(surf, BLACK, (40, 18), 3)
    return surf

def create_player_mushroom_sprite():
    """Create player mushroom sprite"""
    surf = pygame.Surface((60, 60), pygame.SRCALPHA)
    # Stem
    pygame.draw.rect(surf, WHITE, (20, 30, 20, 30))
    pygame.draw.rect(surf, YELLOW, (20, 30, 20, 30), 3)
    # Cap
    pygame.draw.ellipse(surf, YELLOW, (5, 5, 50, 35))
    pygame.draw.ellipse(surf, ORANGE, (5, 5, 50, 35), 3)
    # Dots
    dots = [(18, 18), (35, 15), (42, 25), (25, 30)]
    for dot_x, dot_y in dots:
        pygame.draw.circle(surf, RED, (dot_x, dot_y), 4)
    # Eyes
    pygame.draw.circle(surf, BLACK, (25, 45), 3)
    pygame.draw.circle(surf, BLACK, (35, 45), 3)
    # Smile
    pygame.draw.arc(surf, BLACK, (22, 47, 16, 8), 0, math.pi, 2)
    return surf

def create_mushroom_sprite():
    """Create ally mushroom sprite"""
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    # Stem
    pygame.draw.rect(surf, WHITE, (15, 25, 20, 25))
    pygame.draw.rect(surf, BLACK, (15, 25, 20, 25), 2)
    # Cap
    pygame.draw.ellipse(surf, RED, (5, 5, 40, 30))
    pygame.draw.ellipse(surf, BLACK, (5, 5, 40, 30), 2)
    # Dots
    dots = [(15, 15), (30, 12), (25, 25)]
    for dot_x, dot_y in dots:
        pygame.draw.circle(surf, WHITE, (dot_x, dot_y), 3)
    return surf

def create_enemy_mushroom_sprite(enemy_type):
    """Create enemy mushroom sprite based on type"""
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    if enemy_type == EnemyType.EVIL_MUSHROOM:
        # Dark evil mushroom
        pygame.draw.rect(surf, (60, 60, 60), (15, 25, 20, 25))  # Dark stem
        pygame.draw.rect(surf, BLACK, (15, 25, 20, 25), 2)
        pygame.draw.ellipse(surf, DARK_RED, (5, 5, 40, 30))  # Dark red cap
        pygame.draw.ellipse(surf, BLACK, (5, 5, 40, 30), 3)
        # Evil eyes
        pygame.draw.circle(surf, RED, (18, 35), 3)
        pygame.draw.circle(surf, RED, (32, 35), 3)
        pygame.draw.circle(surf, BLACK, (18, 35), 1)
        pygame.draw.circle(surf, BLACK, (32, 35), 1)
        
    elif enemy_type == EnemyType.SPIKY_MUSHROOM:
        # Spiky mushroom with spikes
        pygame.draw.rect(surf, GRAY, (15, 25, 20, 25))  # Gray stem
        pygame.draw.rect(surf, BLACK, (15, 25, 20, 25), 2)
        pygame.draw.ellipse(surf, PURPLE, (5, 5, 40, 30))  # Purple cap
        pygame.draw.ellipse(surf, BLACK, (5, 5, 40, 30), 2)
        # Spikes on cap
        spikes = [(12, 8), (25, 5), (38, 8), (8, 20), (42, 20)]
        for spike_x, spike_y in spikes:
            pygame.draw.polygon(surf, BLACK, [(spike_x, spike_y), (spike_x-3, spike_y+6), (spike_x+3, spike_y+6)])
        # Angry eyes
        pygame.draw.circle(surf, YELLOW, (18, 35), 3)
        pygame.draw.circle(surf, YELLOW, (32, 35), 3)
        
    elif enemy_type == EnemyType.POISON_MUSHROOM:
        # Poison mushroom
        pygame.draw.rect(surf, (100, 200, 100), (15, 25, 20, 25))  # Green stem
        pygame.draw.rect(surf, BLACK, (15, 25, 20, 25), 2)
        pygame.draw.ellipse(surf, (50, 150, 50), (5, 5, 40, 30))  # Dark green cap
        pygame.draw.ellipse(surf, BLACK, (5, 5, 40, 30), 2)
        # Poison bubbles
        bubbles = [(15, 15), (30, 12), (25, 25), (12, 20)]
        for bubble_x, bubble_y in bubbles:
            pygame.draw.circle(surf, (0, 255, 0), (bubble_x, bubble_y), 2)
        # Sick eyes
        pygame.draw.circle(surf, (0, 255, 0), (18, 35), 3)
        pygame.draw.circle(surf, (0, 255, 0), (32, 35), 3)
        
    elif enemy_type == EnemyType.FIRE_MUSHROOM:
        # Fire mushroom
        pygame.draw.rect(surf, ORANGE, (15, 25, 20, 25))  # Orange stem
        pygame.draw.rect(surf, BLACK, (15, 25, 20, 25), 2)
        pygame.draw.ellipse(surf, (255, 100, 0), (5, 5, 40, 30))  # Fire orange cap
        pygame.draw.ellipse(surf, BLACK, (5, 5, 40, 30), 2)
        # Fire effects
        flames = [(15, 12), (25, 8), (35, 12)]
        for flame_x, flame_y in flames:
            pygame.draw.polygon(surf, YELLOW, [(flame_x, flame_y), (flame_x-2, flame_y+5), (flame_x+2, flame_y+5)])
            pygame.draw.polygon(surf, RED, [(flame_x, flame_y+2), (flame_x-1, flame_y+4), (flame_x+1, flame_y+4)])
        # Fire eyes
        pygame.draw.circle(surf, YELLOW, (18, 35), 3)
        pygame.draw.circle(surf, YELLOW, (32, 35), 3)
        pygame.draw.circle(surf, RED, (18, 35), 1)
        pygame.draw.circle(surf, RED, (32, 35), 1)
    
    return surf

def create_platform_sprite(color, width=40, height=20):
    """Create platform sprite"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, width, height))
    # Gradient for volume
    for i in range(height//2):
        light_color = tuple(min(255, c + 30) for c in color)
        pygame.draw.line(surf, light_color, (0, i), (width, i))
    # Dark border
    dark_color = tuple(max(0, c - 50) for c in color)
    pygame.draw.rect(surf, dark_color, (0, 0, width, height), 2)
    return surf

def create_powerup_sprite(color):
    """Create power-up sprite"""
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (15, 15), 12)
    pygame.draw.circle(surf, WHITE, (15, 15), 12, 2)
    pygame.draw.circle(surf, WHITE, (12, 12), 3)
    # Add symbol based on color
    if color == BLUE:  # Speed
        pygame.draw.polygon(surf, WHITE, [(10, 15), (20, 10), (20, 20)])
    elif color == YELLOW:  # Jump
        pygame.draw.polygon(surf, WHITE, [(15, 8), (12, 18), (18, 18)])
    elif color == PURPLE:  # Invincibility
        pygame.draw.circle(surf, WHITE, (15, 15), 6, 2)
    elif color == ORANGE:  # Magnet
        pygame.draw.rect(surf, WHITE, (12, 10, 6, 10))
        pygame.draw.rect(surf, WHITE, (10, 12, 10, 6))
    return surf

def create_obstacle_sprite(obstacle_type, width, height):
    """Create obstacle sprite"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    if obstacle_type == 'spike':
        # Create spikes
        pygame.draw.rect(surf, GRAY, (0, height-10, width, 10))  # Base
        num_spikes = width // 15
        for i in range(num_spikes):
            spike_x = i * 15 + 7
            pygame.draw.polygon(surf, GRAY, [
                (spike_x, height-10),
                (spike_x-7, height),
                (spike_x+7, height)
            ])
            pygame.draw.polygon(surf, BLACK, [
                (spike_x, height-10),
                (spike_x-7, height),
                (spike_x+7, height)
            ], 2)
    
    elif obstacle_type == 'saw':
        # Create rotating saw
        center_x, center_y = width//2, height//2
        radius = min(width, height)//2 - 2
        pygame.draw.circle(surf, GRAY, (center_x, center_y), radius)
        pygame.draw.circle(surf, BLACK, (center_x, center_y), radius, 2)
        # Saw teeth
        for angle in range(0, 360, 30):
            x = center_x + (radius-5) * math.cos(math.radians(angle))
            y = center_y + (radius-5) * math.sin(math.radians(angle))
            outer_x = center_x + radius * math.cos(math.radians(angle))
            outer_y = center_y + radius * math.sin(math.radians(angle))
            pygame.draw.line(surf, BLACK, (x, y), (outer_x, outer_y), 3)
    
    elif obstacle_type == 'lava':
        # Create lava pit
        pygame.draw.rect(surf, (255, 50, 0), (0, 0, width, height))
        # Lava bubbles
        for i in range(width//20):
            bubble_x = random.randint(5, width-5)
            bubble_y = random.randint(5, height-5)
            pygame.draw.circle(surf, YELLOW, (bubble_x, bubble_y), random.randint(2, 5))
    
    return surf

def create_level_platforms(level_num):
    """Generate platforms for a level with obstacles"""
    platforms = []
    obstacles = []
    enemies = []
    powerups = []
    
    # Create solid ground first - ensure continuous ground
    ground_y = SCREEN_HEIGHT - 50
    world_width = SCREEN_WIDTH * 2
    
    # Create continuous ground for all levels
    for x in range(0, world_width, 40):
        platform_type = ['normal', 'ice', 'lava', 'cloud', 'metal'][min(level_num - 1, 4)]
        # Make sure ground is solid
        platform = (x, ground_y, 40, 50, 'normal')  # Always use normal type for ground
        platforms.append(platform)
    
    # Add gaps in ground only for higher levels
    gap_positions = []
    if level_num >= 2:
        if level_num == 2:
            gap_positions = [(600, 700)]  # Small gap
        elif level_num == 3:
            gap_positions = [(500, 600), (1400, 1500)]  # Two gaps
        elif level_num == 4:
            gap_positions = [(400, 500), (900, 1000), (1600, 1700)]  # Three gaps
        elif level_num >= 5:
            gap_positions = [(300, 400), (800, 900), (1300, 1400), (1800, 1900)]  # Four gaps
    
    # Remove ground platforms where gaps should be
    if gap_positions:
        platforms_to_keep = []
        for platform in platforms:
            x, y, w, h, p_type = platform
            should_keep = True
            for gap_start, gap_end in gap_positions:
                if gap_start <= x < gap_end:
                    should_keep = False
                    break
            if should_keep:
                platforms_to_keep.append(platform)
        platforms = platforms_to_keep
    
    # Level-specific platforms and obstacles
    if level_num == 1:
        # Tutorial level - simple platforms
        platform_data = [
            (300, SCREEN_HEIGHT - 200, 200, 20, 'normal'),
            (600, SCREEN_HEIGHT - 350, 200, 20, 'normal'),
            (1000, SCREEN_HEIGHT - 250, 200, 20, 'normal'),
            (1400, SCREEN_HEIGHT - 400, 150, 20, 'normal'),
        ]
        # Simple obstacles
        obstacle_data = [
            (800, SCREEN_HEIGHT - 70, 60, 20, 'spike'),
        ]
        # Basic enemies
        enemy_data = [
            (500, SCREEN_HEIGHT - 100, EnemyType.EVIL_MUSHROOM),
        ]
        
    elif level_num == 2:
        # Ice level with slippery platforms
        platform_data = [
            (200, SCREEN_HEIGHT - 200, 150, 20, 'ice'),
            (450, SCREEN_HEIGHT - 350, 200, 20, 'ice'),
            (750, SCREEN_HEIGHT - 280, 100, 20, 'normal'),
            (950, SCREEN_HEIGHT - 500, 150, 20, 'ice'),
            (1300, SCREEN_HEIGHT - 300, 180, 20, 'ice'),
            (1600, SCREEN_HEIGHT - 450, 120, 20, 'cloud'),
        ]
        obstacle_data = [
            (520, SCREEN_HEIGHT - 70, 80, 20, 'spike'),
            (1100, SCREEN_HEIGHT - 70, 100, 20, 'spike'),
        ]
        enemy_data = [
            (400, SCREEN_HEIGHT - 100, EnemyType.EVIL_MUSHROOM),
            (850, SCREEN_HEIGHT - 100, EnemyType.SPIKY_MUSHROOM),
        ]
        
    elif level_num == 3:
        # Lava level with dangerous obstacles
        platform_data = [
            (150, SCREEN_HEIGHT - 200, 100, 20, 'lava'),
            (350, SCREEN_HEIGHT - 350, 120, 20, 'metal'),
            (550, SCREEN_HEIGHT - 180, 80, 20, 'normal'),
            (700, SCREEN_HEIGHT - 320, 100, 20, 'lava'),
            (900, SCREEN_HEIGHT - 480, 150, 20, 'metal'),
            (1150, SCREEN_HEIGHT - 250, 100, 20, 'lava'),
            (1350, SCREEN_HEIGHT - 400, 120, 20, 'metal'),
            (1550, SCREEN_HEIGHT - 300, 100, 20, 'normal'),
        ]
        obstacle_data = [
            (480, SCREEN_HEIGHT - 70, 100, 20, 'spike'),
            (820, SCREEN_HEIGHT - 70, 60, 20, 'lava'),
            (1280, SCREEN_HEIGHT - 70, 80, 20, 'spike'),
            (750, SCREEN_HEIGHT - 250, 30, 30, 'saw'),
        ]
        enemy_data = [
            (300, SCREEN_HEIGHT - 100, EnemyType.EVIL_MUSHROOM),
            (650, SCREEN_HEIGHT - 100, EnemyType.POISON_MUSHROOM),
            (1000, SCREEN_HEIGHT - 100, EnemyType.SPIKY_MUSHROOM),
        ]
        
    elif level_num == 4:
        # Sky level with cloud platforms
        platform_data = [
            (100, SCREEN_HEIGHT - 150, 80, 20, 'cloud'),
            (250, SCREEN_HEIGHT - 280, 100, 20, 'cloud'),
            (420, SCREEN_HEIGHT - 200, 90, 20, 'cloud'),
            (580, SCREEN_HEIGHT - 400, 100, 20, 'cloud'),
            (750, SCREEN_HEIGHT - 320, 80, 20, 'cloud'),
            (900, SCREEN_HEIGHT - 180, 100, 20, 'cloud'),
            (1080, SCREEN_HEIGHT - 450, 120, 20, 'cloud'),
            (1250, SCREEN_HEIGHT - 250, 100, 20, 'cloud'),
            (1420, SCREEN_HEIGHT - 380, 100, 20, 'cloud'),
            (1600, SCREEN_HEIGHT - 500, 80, 20, 'cloud'),
            (1750, SCREEN_HEIGHT - 300, 120, 20, 'cloud'),
        ]
        obstacle_data = [
            (350, SCREEN_HEIGHT - 120, 60, 20, 'spike'),
            (950, SCREEN_HEIGHT - 120, 80, 20, 'spike'),
            (1500, SCREEN_HEIGHT - 120, 60, 20, 'spike'),
        ]
        enemy_data = [
            (200, SCREEN_HEIGHT - 100, EnemyType.FIRE_MUSHROOM),
            (700, SCREEN_HEIGHT - 100, EnemyType.SPIKY_MUSHROOM),
            (1200, SCREEN_HEIGHT - 100, EnemyType.POISON_MUSHROOM),
        ]
        
    else:  # Level 5 - Final boss level
        platform_data = [
            (100, SCREEN_HEIGHT - 150, 60, 20, 'metal'),
            (220, SCREEN_HEIGHT - 250, 80, 20, 'normal'),
            (360, SCREEN_HEIGHT - 180, 70, 20, 'ice'),
            (480, SCREEN_HEIGHT - 350, 100, 20, 'lava'),
            (650, SCREEN_HEIGHT - 200, 80, 20, 'cloud'),
            (780, SCREEN_HEIGHT - 400, 90, 20, 'metal'),
            (920, SCREEN_HEIGHT - 280, 100, 20, 'normal'),
            (1080, SCREEN_HEIGHT - 450, 120, 20, 'ice'),
            (1250, SCREEN_HEIGHT - 320, 80, 20, 'lava'),
            (1380, SCREEN_HEIGHT - 500, 100, 20, 'cloud'),
            (1530, SCREEN_HEIGHT - 250, 90, 20, 'metal'),
            (1680, SCREEN_HEIGHT - 380, 120, 20, 'normal'),
        ]
        obstacle_data = [
            (300, SCREEN_HEIGHT - 70, 100, 20, 'spike'),
            (600, SCREEN_HEIGHT - 130, 80, 20, 'lava'),
            (850, SCREEN_HEIGHT - 70, 60, 20, 'spike'),
            (1150, SCREEN_HEIGHT - 70, 80, 20, 'spike'),
            (1450, SCREEN_HEIGHT - 120, 100, 20, 'lava'),
            (500, SCREEN_HEIGHT - 280, 30, 30, 'saw'),
            (800, SCREEN_HEIGHT - 330, 30, 30, 'saw'),
            (1300, SCREEN_HEIGHT - 420, 30, 30, 'saw'),
        ]
        enemy_data = [
            (250, SCREEN_HEIGHT - 100, EnemyType.EVIL_MUSHROOM),
            (550, SCREEN_HEIGHT - 100, EnemyType.FIRE_MUSHROOM),
            (750, SCREEN_HEIGHT - 100, EnemyType.SPIKY_MUSHROOM),
            (950, SCREEN_HEIGHT - 100, EnemyType.POISON_MUSHROOM),
            (1150, SCREEN_HEIGHT - 100, EnemyType.FIRE_MUSHROOM),
            (1400, SCREEN_HEIGHT - 100, EnemyType.SPIKY_MUSHROOM),
        ]
    
    # Add power-ups
    powerup_positions = []
    if level_num >= 2:
        powerup_positions = [
            (400 + level_num * 100, SCREEN_HEIGHT - 300, PowerUpType.SPEED_BOOST),
            (800 + level_num * 80, SCREEN_HEIGHT - 400, PowerUpType.SUPER_JUMP),
        ]
        if level_num >= 4:
            powerup_positions.append((1200, SCREEN_HEIGHT - 350, PowerUpType.INVINCIBILITY))
        if level_num == 5:
            powerup_positions.append((600, SCREEN_HEIGHT - 550, PowerUpType.MAGNET))
    
    return platforms + platform_data, obstacle_data, enemy_data, powerup_positions