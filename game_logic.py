import pygame
import json
import os
from enum import Enum
from game_objects import *
from level_generator import *

# Screen constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5
    LEVEL_SELECT = 6

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Супер Гриб: Битва с Врагами!")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Game data
        self.current_level = 1
        self.max_level = 5
        self.score = 0
        self.lives = 3
        self.time_left = 120
        self.timer = 0
        
        # Load game data
        self.load_game_data()
        self.load_textures()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Camera
        self.camera_x = 0
        
        # Game objects
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.mushrooms = pygame.sprite.Group()
    
    def load_game_data(self):
        """Load save game"""
        try:
            with open('savegame.json', 'r') as f:
                data = json.load(f)
                self.current_level = data.get('current_level', 1)
                self.score = data.get('total_score', 0)
        except FileNotFoundError:
            self.save_game_data()
    
    def save_game_data(self):
        """Save game"""
        data = {'current_level': self.current_level, 'total_score': self.score}
        with open('savegame.json', 'w') as f:
            json.dump(data, f)
    
    def load_textures(self):
        """Create sprites"""
        if not os.path.exists('images'):
            os.makedirs('images')
        
        # Main character sprites
        self.mario_image = create_mario_sprite()
        self.player_mushroom_image = create_player_mushroom_sprite()
        self.mushroom_image = create_mushroom_sprite()
        
        # Enemy sprites
        self.enemy_images = {
            EnemyType.EVIL_MUSHROOM: create_enemy_mushroom_sprite(EnemyType.EVIL_MUSHROOM),
            EnemyType.SPIKY_MUSHROOM: create_enemy_mushroom_sprite(EnemyType.SPIKY_MUSHROOM),
            EnemyType.POISON_MUSHROOM: create_enemy_mushroom_sprite(EnemyType.POISON_MUSHROOM),
            EnemyType.FIRE_MUSHROOM: create_enemy_mushroom_sprite(EnemyType.FIRE_MUSHROOM)
        }
        
        # Platform sprites
        self.platform_images = {
            'normal': create_platform_sprite(GREEN),
            'ice': create_platform_sprite((173, 216, 230)),
            'lava': create_platform_sprite((255, 69, 0)),
            'cloud': create_platform_sprite(WHITE),
            'metal': create_platform_sprite(GRAY)
        }
        
        # Power-up sprites
        self.powerup_images = {
            PowerUpType.SPEED_BOOST: create_powerup_sprite(BLUE),
            PowerUpType.SUPER_JUMP: create_powerup_sprite(YELLOW),
            PowerUpType.INVINCIBILITY: create_powerup_sprite(PURPLE),
            PowerUpType.MAGNET: create_powerup_sprite(ORANGE)
        }
        
        print("All textures created!")
    
    def load_level(self, level_num):
        """Load level with enhanced generation"""
        # Clear all sprite groups
        self.platforms.empty()
        self.enemies.empty()
        self.powerups.empty()
        self.obstacles.empty()
        self.mushrooms.empty()
        
        self.time_left = 120
        self.timer = 0
        
        # Generate level content
        platform_data, obstacle_data, enemy_data, powerup_data = create_level_platforms(level_num)
        
        # Create platforms
        for data in platform_data:
            if len(data) == 5:
                x, y, w, h, p_type = data
                platform = Platform(x, y, w, h, p_type)
                self.platforms.add(platform)
        
        # Create obstacles
        for obs_data in obstacle_data:
            x, y, w, h, obs_type = obs_data
            obstacle = Obstacle(x, y, w, h, obs_type)
            self.obstacles.add(obstacle)
        
        # Create enemies
        for enemy_data in enemy_data:
            x, y, enemy_type = enemy_data
            enemy_image = self.enemy_images[enemy_type]
            enemy = EnemyMushroom(x, y, enemy_type, enemy_image)
            self.enemies.add(enemy)
        
        # Create power-ups
        for powerup_data in powerup_data:
            x, y, powerup_type = powerup_data
            powerup = PowerUp(x, y, powerup_type)
            self.powerups.add(powerup)
        
        # Create Mario and player
        mario_x = 1000 + (level_num * 200)
        self.mario = Mario(mario_x, SCREEN_HEIGHT - 200, self.mario_image, level_num)
        
        player_x = 100
        self.player_mushroom = PlayerMushroom(player_x, SCREEN_HEIGHT - 200, self.player_mushroom_image)
        self.mushrooms.add(self.player_mushroom)
        
        # Create ally mushrooms (fewer due to enemy threat)
        ally_count = max(1, 3 - level_num // 2)
        for i in range(ally_count):
            mushroom = Mushroom(400 + i * 300, SCREEN_HEIGHT - 250, self.mushroom_image)
            self.mushrooms.add(mushroom)
        
        print(f"Level {level_num} loaded with {len(self.enemies)} enemies and {len(self.obstacles)} obstacles!")
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game_data()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    
    def handle_keydown(self, key):
        """Handle key presses"""
        if self.state == GameState.MENU:
            if key == pygame.K_RETURN:
                self.load_level(self.current_level)
                self.state = GameState.PLAYING
            elif key == pygame.K_l:
                self.state = GameState.LEVEL_SELECT
        elif self.state == GameState.LEVEL_SELECT:
            if key >= pygame.K_1 and key <= pygame.K_5:
                level = key - pygame.K_0
                if level <= self.current_level:  # Can only play unlocked levels
                    self.current_level = level
                    self.load_level(level)
                    self.state = GameState.PLAYING
            elif key == pygame.K_ESCAPE:
                self.state = GameState.MENU
        elif self.state == GameState.PLAYING:
            if key == pygame.K_SPACE:
                self.player_mushroom.jump()
            elif key == pygame.K_p:
                self.state = GameState.PAUSED
            elif key == pygame.K_ESCAPE:
                self.state = GameState.MENU
        elif self.state == GameState.PAUSED:
            if key == pygame.K_p:
                self.state = GameState.PLAYING
        elif self.state == GameState.LEVEL_COMPLETE:
            if key == pygame.K_RETURN:
                self.next_level()
        elif self.state == GameState.GAME_OVER:
            if key == pygame.K_RETURN:
                self.restart_game()
    
    def update(self):
        """Update game"""
        if self.state != GameState.PLAYING:
            return
        
        # Update timer
        self.timer += 1
        if self.timer >= 60:
            self.timer = 0
            self.time_left -= 1
            if self.time_left <= 0:
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GameState.GAME_OVER
                else:
                    self.load_level(self.current_level)
        
        # Update camera
        self.update_camera()
        
        # Update objects
        self.mario.update_ai(self.platforms, self.player_mushroom, self.enemies)
        self.player_mushroom.update(self.platforms)
        
        for mushroom in self.mushrooms:
            if mushroom != self.player_mushroom:
                mushroom.update(self.platforms, self.mario)
        
        for enemy in self.enemies:
            enemy.update(self.platforms, self.player_mushroom, self.mario)
        
        for powerup in self.powerups:
            powerup.update()
        
        for obstacle in self.obstacles:
            obstacle.update()
        
        # Check collisions
        self.check_collisions()
    
    def update_camera(self):
        """Update camera"""
        target_x = self.player_mushroom.rect.centerx - SCREEN_WIDTH // 2
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.camera_x, SCREEN_WIDTH * 2 - SCREEN_WIDTH))
    
    def check_collisions(self):
        """Check all collisions"""
        # Player vs Mario
        for mushroom in self.mushrooms:
            if mushroom.rect.colliderect(self.mario.rect):
                if mushroom.rect.bottom <= self.mario.rect.top + 15 and mushroom.vel_y >= 0:
                    mushroom.on_mario = True
                    mushroom.vel_y = 0
                    mushroom.rect.bottom = self.mario.rect.top
                    if mushroom == self.player_mushroom:
                        self.score += 100
                        self.check_level_complete()
        
        # Player vs Power-ups
        for powerup in self.powerups:
            if powerup.rect.colliderect(self.player_mushroom.rect):
                self.player_mushroom.apply_powerup(powerup.type)
                powerup.kill()
                self.score += 50
        
        # Player vs Enemies
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player_mushroom.rect):
                if self.player_mushroom.take_damage(enemy.damage):
                    print(f"Player hit by {enemy.enemy_type}! Health: {self.player_mushroom.health}")
                    if self.player_mushroom.health <= 0:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.state = GameState.GAME_OVER
                        else:
                            self.load_level(self.current_level)
        
        # Player vs Obstacles
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(self.player_mushroom.rect):
                if self.player_mushroom.take_damage(obstacle.damage):
                    print(f"Player hit obstacle! Health: {self.player_mushroom.health}")
                    if self.player_mushroom.health <= 0:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.state = GameState.GAME_OVER
                        else:
                            self.load_level(self.current_level)
    
    def check_level_complete(self):
        """Check level completion"""
        if self.player_mushroom.on_mario:
            self.state = GameState.LEVEL_COMPLETE
            self.score += self.time_left * 10
            # Unlock next level
            if self.current_level < self.max_level:
                self.current_level = max(self.current_level, self.current_level + 1)
    
    def next_level(self):
        """Next level"""
        if self.current_level < self.max_level:
            self.current_level += 1
            self.load_level(self.current_level)
            self.state = GameState.PLAYING
        else:
            self.state = GameState.MENU
    
    def draw(self):
        """Draw function - handled by game_ui module"""
        # Drawing is now handled by the game_ui module
        pass
    
    def restart_game(self):
        """Restart game"""
        self.lives = 3
        self.player_mushroom.health = self.player_mushroom.max_health
        self.load_level(self.current_level)
        self.state = GameState.PLAYING