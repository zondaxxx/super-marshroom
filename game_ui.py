import pygame
from game_logic import GameState
from game_objects import *

# Colors for UI
UI_COLORS = {
    'background': (0, 0, 0, 180),
    'text_primary': (255, 255, 255),
    'text_secondary': (255, 255, 0),
    'text_danger': (255, 0, 0),
    'text_success': (0, 255, 0),
    'health_bg': (100, 0, 0),
    'health_fg': (0, 255, 0),
    'menu_bg': (50, 50, 100, 200)
}

def draw_game_ui(game):
    """Draw main game UI"""
    screen = game.screen
    
    # Background gradient
    for y in range(900):  # SCREEN_HEIGHT
        color_r = int(135 + (50 * y / 900))
        color_g = int(206 - (50 * y / 900))
        color_b = 235
        color = (min(255, color_r), max(0, color_g), color_b)
        pygame.draw.line(screen, color, (0, y), (1400, y))  # SCREEN_WIDTH
    
    # Draw platforms
    for platform in game.platforms:
        x = platform.rect.x - game.camera_x
        if -100 < x < 1500:  # Only visible platforms
            platform_img = game.platform_images.get(platform.platform_type, game.platform_images['normal'])
            # Tile the platform image
            for i in range(0, platform.rect.width, 40):
                if x + i > -40 and x + i < 1440:
                    screen.blit(platform_img, (x + i, platform.rect.y))
    
    # Draw obstacles
    for obstacle in game.obstacles:
        x = obstacle.rect.x - game.camera_x
        if -100 < x < 1500:
            # Create obstacle sprite on the fly for now
            obs_surf = pygame.Surface((obstacle.rect.width, obstacle.rect.height))
            if obstacle.obstacle_type == 'spike':
                obs_surf.fill(GRAY)
                # Simple spike representation
                for i in range(0, obstacle.rect.width, 15):
                    pygame.draw.polygon(obs_surf, BLACK, [(i+7, 0), (i, obstacle.rect.height), (i+14, obstacle.rect.height)])
            elif obstacle.obstacle_type == 'lava':
                obs_surf.fill((255, 50, 0))
            elif obstacle.obstacle_type == 'saw':
                obs_surf.fill(GRAY)
                pygame.draw.circle(obs_surf, BLACK, (obstacle.rect.width//2, obstacle.rect.height//2), 
                                 min(obstacle.rect.width, obstacle.rect.height)//2, 3)
            
            screen.blit(obs_surf, (x, obstacle.rect.y))
    
    # Draw Mario
    mario_x = game.mario.rect.x - game.camera_x
    if -100 < mario_x < 1500:
        screen.blit(game.mario.image, (mario_x, game.mario.rect.y))
        # Mario health bar above head
        if game.mario.health < game.mario.max_health:
            health_bg = pygame.Rect(mario_x, game.mario.rect.y - 15, 70, 8)
            health_fg = pygame.Rect(mario_x, game.mario.rect.y - 15, 
                                  int(70 * game.mario.health / game.mario.max_health), 8)
            pygame.draw.rect(screen, UI_COLORS['health_bg'], health_bg)
            pygame.draw.rect(screen, UI_COLORS['health_fg'], health_fg)
    
    # Draw mushrooms
    for mushroom in game.mushrooms:
        mushroom_x = mushroom.rect.x - game.camera_x
        if -100 < mushroom_x < 1500:
            screen.blit(mushroom.image, (mushroom_x, mushroom.rect.y))
            # Highlight player mushroom
            if mushroom == game.player_mushroom:
                pygame.draw.rect(screen, YELLOW, 
                               (mushroom_x, mushroom.rect.y, mushroom.rect.width, mushroom.rect.height), 4)
                # Arrow above player
                arrow_points = [
                    (mushroom_x + mushroom.rect.width//2, mushroom.rect.y - 20),
                    (mushroom_x + mushroom.rect.width//2 - 10, mushroom.rect.y - 10),
                    (mushroom_x + mushroom.rect.width//2 + 10, mushroom.rect.y - 10)
                ]
                pygame.draw.polygon(screen, YELLOW, arrow_points)
                
                # Player health bar above
                if mushroom.health < mushroom.max_health:
                    health_bg = pygame.Rect(mushroom_x, mushroom.rect.y - 30, 60, 8)
                    health_fg = pygame.Rect(mushroom_x, mushroom.rect.y - 30, 
                                          int(60 * mushroom.health / mushroom.max_health), 8)
                    pygame.draw.rect(screen, UI_COLORS['health_bg'], health_bg)
                    pygame.draw.rect(screen, UI_COLORS['health_fg'], health_fg)
    
    # Draw enemies
    for enemy in game.enemies:
        enemy_x = enemy.rect.x - game.camera_x
        if -100 < enemy_x < 1500:
            screen.blit(enemy.image, (enemy_x, enemy.rect.y))
            # Enemy health bar
            if enemy.health < enemy.max_health:
                health_bg = pygame.Rect(enemy_x, enemy.rect.y - 12, 50, 6)
                health_fg = pygame.Rect(enemy_x, enemy.rect.y - 12, 
                                      int(50 * enemy.health / enemy.max_health), 6)
                pygame.draw.rect(screen, UI_COLORS['health_bg'], health_bg)
                pygame.draw.rect(screen, (255, 100, 100), health_fg)
            
            # Enemy type indicator
            type_colors = {
                EnemyType.EVIL_MUSHROOM: DARK_RED,
                EnemyType.SPIKY_MUSHROOM: PURPLE,
                EnemyType.POISON_MUSHROOM: GREEN,
                EnemyType.FIRE_MUSHROOM: ORANGE
            }
            color = type_colors.get(enemy.enemy_type, RED)
            pygame.draw.circle(screen, color, (enemy_x + 5, enemy.rect.y + 5), 3)
    
    # Draw power-ups
    for powerup in game.powerups:
        powerup_x = powerup.rect.x - game.camera_x
        if -100 < powerup_x < 1500:
            powerup_img = game.powerup_images[powerup.type]
            screen.blit(powerup_img, (powerup_x, powerup.rect.y))
            # Glowing effect
            if powerup.timer % 30 < 15:
                pygame.draw.circle(screen, WHITE, 
                                 (powerup_x + 15, powerup.rect.y + 15), 20, 2)
    
    # Draw HUD
    draw_hud(game)

def draw_hud(game):
    """Draw heads-up display"""
    screen = game.screen
    
    # HUD background
    hud_bg = pygame.Surface((1400, 120), pygame.SRCALPHA)
    hud_bg.fill(UI_COLORS['background'])
    screen.blit(hud_bg, (0, 0))
    
    # Main info
    hud_items = [
        f"Level: {game.current_level}",
        f"Score: {game.score}",
        f"Lives: {game.lives}",
        f"Time: {game.time_left}",
        f"Health: {game.player_mushroom.health}"
    ]
    
    for i, item in enumerate(hud_items):
        color = UI_COLORS['text_primary'] if i < 3 else UI_COLORS['text_danger'] if 'Health' in item and game.player_mushroom.health < 30 else UI_COLORS['text_secondary']
        text = game.font_small.render(item, True, color)
        screen.blit(text, (20 + (i % 3) * 250, 20 + (i // 3) * 30))
    
    # Controls info
    controls = "WASD/Arrows - Move, SPACE - Jump, P - Pause"
    control_text = game.font_small.render(controls, True, UI_COLORS['text_secondary'])
    screen.blit(control_text, (20, 80))
    
    # Power-up status
    powerup_y = 20
    if game.player_mushroom.speed_boost_timer > 0:
        speed_text = game.font_small.render(f"Speed Boost: {game.player_mushroom.speed_boost_timer//60}s", True, BLUE)
        screen.blit(speed_text, (1000, powerup_y))
        powerup_y += 25
    
    if game.player_mushroom.super_jump_timer > 0:
        jump_text = game.font_small.render(f"Super Jump: {game.player_mushroom.super_jump_timer//60}s", True, YELLOW)
        screen.blit(jump_text, (1000, powerup_y))
        powerup_y += 25
    
    if game.player_mushroom.invincibility_timer > 0:
        inv_text = game.font_small.render(f"Invincible: {game.player_mushroom.invincibility_timer//60}s", True, PURPLE)
        screen.blit(inv_text, (1000, powerup_y))
        powerup_y += 25
    
    if game.player_mushroom.magnet_timer > 0:
        mag_text = game.font_small.render(f"Magnet: {game.player_mushroom.magnet_timer//60}s", True, ORANGE)
        screen.blit(mag_text, (1000, powerup_y))

def draw_menu(game):
    """Draw main menu"""
    screen = game.screen
    screen.fill((20, 30, 60))
    
    # Title
    title = game.font_large.render("SUPER MUSHROOM", True, UI_COLORS['text_secondary'])
    title_rect = title.get_rect(center=(700, 200))
    screen.blit(title, title_rect)
    
    subtitle = game.font_medium.render("Battle Edition", True, UI_COLORS['text_primary'])
    subtitle_rect = subtitle.get_rect(center=(700, 270))
    screen.blit(subtitle, subtitle_rect)
    
    # Menu items
    menu_items = [
        "ENTER - Start Game",
        "L - Level Select",
        "ESC - Exit",
        f"Current Level: {game.current_level}",
        f"Total Score: {game.score}"
    ]
    
    for i, item in enumerate(menu_items):
        color = UI_COLORS['text_primary'] if i < 3 else UI_COLORS['text_secondary']
        text = game.font_small.render(item, True, color)
        text_rect = text.get_rect(center=(700, 400 + i * 50))
        screen.blit(text, text_rect)
    
    # Feature highlights
    features = [
        "🍄 Play as mushroom vs Mario!",
        "⚔️ Fight enemy mushrooms!",
        "💎 Collect power-ups!",
        "🏔️ 5 challenging levels!"
    ]
    
    for i, feature in enumerate(features):
        text = game.font_small.render(feature, True, UI_COLORS['text_success'])
        text_rect = text.get_rect(center=(700, 700 + i * 30))
        screen.blit(text, text_rect)

def draw_level_select(game):
    """Draw level selection"""
    screen = game.screen
    screen.fill((30, 20, 60))
    
    title = game.font_large.render("SELECT LEVEL", True, UI_COLORS['text_secondary'])
    title_rect = title.get_rect(center=(700, 150))
    screen.blit(title, title_rect)
    
    # Level buttons
    level_names = [
        "1 - Tutorial",
        "2 - Ice World", 
        "3 - Lava World",
        "4 - Sky World",
        "5 - Final Boss"
    ]
    
    for i, name in enumerate(level_names):
        level_num = i + 1
        color = UI_COLORS['text_success'] if level_num <= game.current_level else UI_COLORS['health_bg']
        text = game.font_medium.render(name, True, color)
        text_rect = text.get_rect(center=(700, 250 + i * 80))
        
        # Highlight available levels
        if level_num <= game.current_level:
            bg_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(screen, UI_COLORS['menu_bg'], bg_rect)
            pygame.draw.rect(screen, color, bg_rect, 3)
        
        screen.blit(text, text_rect)
    
    # Instructions
    instruction = game.font_small.render("Press number key to select level or ESC to go back", True, UI_COLORS['text_primary'])
    instruction_rect = instruction.get_rect(center=(700, 750))
    screen.blit(instruction, instruction_rect)

def draw_pause_overlay(game):
    """Draw pause overlay"""
    screen = game.screen
    overlay = pygame.Surface((1400, 900), pygame.SRCALPHA)
    overlay.fill(UI_COLORS['background'])
    screen.blit(overlay, (0, 0))
    
    pause_text = game.font_large.render("PAUSED", True, UI_COLORS['text_primary'])
    pause_rect = pause_text.get_rect(center=(700, 450))
    screen.blit(pause_text, pause_rect)
    
    instruction = game.font_medium.render("Press P to continue", True, UI_COLORS['text_secondary'])
    instruction_rect = instruction.get_rect(center=(700, 520))
    screen.blit(instruction, instruction_rect)

def draw_level_complete(game):
    """Draw level completion screen"""
    screen = game.screen
    overlay = pygame.Surface((1400, 900), pygame.SRCALPHA)
    overlay.fill(UI_COLORS['background'])
    screen.blit(overlay, (0, 0))
    
    # Title
    complete_text = game.font_large.render("LEVEL COMPLETE!", True, UI_COLORS['text_success'])
    complete_rect = complete_text.get_rect(center=(700, 300))
    screen.blit(complete_text, complete_rect)
    
    # Stats
    stats = [
        f"Score: {game.score}",
        f"Time Bonus: {game.time_left * 10}",
        f"Health Remaining: {game.player_mushroom.health}",
        f"Next Level: {game.current_level + 1 if game.current_level < game.max_level else 'GAME COMPLETE!'}"
    ]
    
    for i, stat in enumerate(stats):
        text = game.font_medium.render(stat, True, UI_COLORS['text_primary'])
        text_rect = text.get_rect(center=(700, 400 + i * 50))
        screen.blit(text, text_rect)
    
    # Instructions
    if game.current_level < game.max_level:
        instruction = game.font_small.render("ENTER - Next Level, ESC - Menu", True, UI_COLORS['text_secondary'])
    else:
        instruction = game.font_small.render("ENTER - Back to Menu", True, UI_COLORS['text_secondary'])
    instruction_rect = instruction.get_rect(center=(700, 650))
    screen.blit(instruction, instruction_rect)

def draw_game_over(game):
    """Draw game over screen"""
    screen = game.screen
    screen.fill((40, 0, 0))
    
    game_over_text = game.font_large.render("GAME OVER", True, UI_COLORS['text_danger'])
    game_over_rect = game_over_text.get_rect(center=(700, 300))
    screen.blit(game_over_text, game_over_rect)
    
    # Final stats
    stats = [
        f"Final Score: {game.score}",
        f"Levels Reached: {game.current_level}",
        f"Lives Lost: {3 - game.lives}"
    ]
    
    for i, stat in enumerate(stats):
        text = game.font_medium.render(stat, True, UI_COLORS['text_primary'])
        text_rect = text.get_rect(center=(700, 400 + i * 50))
        screen.blit(text, text_rect)
    
    # Instructions
    restart_text = game.font_small.render("ENTER - Try Again, ESC - Menu", True, UI_COLORS['text_secondary'])
    restart_rect = restart_text.get_rect(center=(700, 600))
    screen.blit(restart_text, restart_rect)

def draw_ui(game):
    """Main UI drawing function"""
    if game.state == GameState.MENU:
        draw_menu(game)
    elif game.state == GameState.LEVEL_SELECT:
        draw_level_select(game)
    elif game.state == GameState.PLAYING:
        draw_game_ui(game)
    elif game.state == GameState.PAUSED:
        draw_game_ui(game)
        draw_pause_overlay(game)
    elif game.state == GameState.LEVEL_COMPLETE:
        draw_game_ui(game)
        draw_level_complete(game)
    elif game.state == GameState.GAME_OVER:
        draw_game_over(game)
    
    pygame.display.flip()