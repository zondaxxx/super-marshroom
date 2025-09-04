import pygame
import random
import math
from enum import Enum

# Constants
GRAVITY = 0.8
JUMP_SPEED = -16
MARIO_SPEED = 4
MUSHROOM_SPEED = 3
ENEMY_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_RED = (139, 0, 0)
PINK = (255, 192, 203)

class PowerUpType(Enum):
    SPEED_BOOST = 1
    SUPER_JUMP = 2
    INVINCIBILITY = 3
    MAGNET = 4

class EnemyType(Enum):
    EVIL_MUSHROOM = 1
    SPIKY_MUSHROOM = 2
    POISON_MUSHROOM = 3
    FIRE_MUSHROOM = 4

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, image, level):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.direction = 1
        self.ai_timer = 0
        self.jump_cooldown = 0
        self.level = level
        self.max_health = 100
        self.health = 100
        self.invulnerable_timer = 0
    
    def update_ai(self, platforms, player_mushroom, enemies=None):
        """Enhanced Mario AI with enemy awareness"""
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        
        self.jump_cooldown = max(0, self.jump_cooldown - 1)
        self.ai_timer += 1
        
        # Enhanced behavior based on level
        speed_multiplier = 1 + (self.level - 1) * 0.3
        detection_range = 180 + (self.level - 1) * 60
        
        distance_to_player = player_mushroom.rect.centerx - self.rect.centerx
        
        # Check for nearby enemies and avoid them too
        enemy_threat = False
        if enemies:
            for enemy in enemies:
                enemy_distance = abs(enemy.rect.centerx - self.rect.centerx)
                if enemy_distance < 100:
                    enemy_threat = True
                    break
        
        if abs(distance_to_player) < detection_range or enemy_threat:
            # Enhanced panic behavior
            panic_multiplier = 2.0 if enemy_threat else 1.5
            if distance_to_player > 0:
                self.vel_x = -MARIO_SPEED * speed_multiplier * panic_multiplier
                self.direction = -1
            else:
                self.vel_x = MARIO_SPEED * speed_multiplier * panic_multiplier
                self.direction = 1
            
            # More frequent jumping when threatened
            jump_threshold = 60 if enemy_threat else 80
            if abs(distance_to_player) < jump_threshold and self.on_ground and self.jump_cooldown == 0:
                self.jump()
                self.jump_cooldown = 30
        else:
            # Normal movement with more variation
            if self.ai_timer % (70 - self.level * 8) == 0:
                choices = [-MARIO_SPEED * speed_multiplier, 0, MARIO_SPEED * speed_multiplier]
                if self.level >= 3:  # Add standing still less often on higher levels
                    choices.extend([MARIO_SPEED * speed_multiplier, -MARIO_SPEED * speed_multiplier])
                self.vel_x = random.choice(choices)
                if self.vel_x > 0:
                    self.direction = 1
                elif self.vel_x < 0:
                    self.direction = -1
        
        # Movement
        self.rect.x += self.vel_x
        
        # Enhanced boundary checking with screen wrapping on higher levels
        screen_width = 1400 * 2  # Extended world width
        if self.rect.x < 0:
            if self.level >= 4:  # Screen wrapping on higher levels
                self.rect.x = screen_width - self.rect.width
            else:
                self.rect.x = 0
                self.vel_x = MARIO_SPEED * speed_multiplier
                self.direction = 1
        elif self.rect.right > screen_width:
            if self.level >= 4:
                self.rect.x = 0
            else:
                self.rect.right = screen_width
                self.vel_x = -MARIO_SPEED * speed_multiplier
                self.direction = -1
        
        # Physics
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ground collision - prevent falling through floor
        if self.rect.bottom >= 900 - 50:  # SCREEN_HEIGHT - ground_height
            self.rect.bottom = 900 - 50
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
    
    def jump(self):
        """Mario jump"""
        if self.on_ground:
            self.vel_y = JUMP_SPEED * 1.1
    
    def take_damage(self, damage):
        """Take damage"""
        if self.invulnerable_timer == 0:
            self.health -= damage
            self.invulnerable_timer = 60
            if self.health <= 0:
                self.health = 0


class PlayerMushroom(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.on_mario = False
        self.max_health = 100
        self.health = 100
        self.invulnerable_timer = 0
        
        # Power-ups
        self.speed_boost_timer = 0
        self.super_jump_timer = 0
        self.invincibility_timer = 0
        self.magnet_timer = 0
        
        # Visual effects
        self.damage_flash_timer = 0
    
    def update(self, platforms):
        """Update player mushroom"""
        # Update timers
        self.invulnerable_timer = max(0, self.invulnerable_timer - 1)
        self.damage_flash_timer = max(0, self.damage_flash_timer - 1)
        
        # Controls
        keys = pygame.key.get_pressed()
        base_speed = MUSHROOM_SPEED * 1.5
        
        # Speed boost
        if self.speed_boost_timer > 0:
            base_speed *= 2
            self.speed_boost_timer -= 1
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= base_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += base_speed
        
        # Boundaries
        screen_width = 1400 * 2
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        
        # Jump off Mario
        if self.on_mario and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]):
            self.on_mario = False
            self.vel_y = JUMP_SPEED * 0.5
        
        # Physics - only apply if not on Mario
        if not self.on_mario:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            
            # Ground collision - prevent falling through floor
            if self.rect.bottom >= 900 - 50:  # SCREEN_HEIGHT - ground_height
                self.rect.bottom = 900 - 50
                self.vel_y = 0
                self.on_ground = True
            else:
                self.on_ground = False
            
            # Platform collisions
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.vel_y > 0:  # Falling down
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Jumping up
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0
        
        # Update power-up timers
        self.super_jump_timer = max(0, self.super_jump_timer - 1)
        self.invincibility_timer = max(0, self.invincibility_timer - 1)
        self.magnet_timer = max(0, self.magnet_timer - 1)
        
        # Visual effects for invincibility
        if self.invincibility_timer > 0:
            # Make the sprite flash
            if (self.invincibility_timer // 5) % 2:
                self.image = self.original_image.copy()
                overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 128))
                self.image.blit(overlay, (0, 0))
            else:
                self.image = self.original_image
        elif self.damage_flash_timer > 0:
            # Red flash when taking damage
            self.image = self.original_image.copy()
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, 128))
            self.image.blit(overlay, (0, 0))
        else:
            self.image = self.original_image
    
    def jump(self):
        """Player jump"""
        if self.on_ground and not self.on_mario:
            jump_power = JUMP_SPEED * 1.3
            if self.super_jump_timer > 0:
                jump_power *= 1.5
            self.vel_y = jump_power
    
    def apply_powerup(self, powerup_type):
        """Apply power-up"""
        if powerup_type == PowerUpType.SPEED_BOOST:
            self.speed_boost_timer = 300
        elif powerup_type == PowerUpType.SUPER_JUMP:
            self.super_jump_timer = 300
        elif powerup_type == PowerUpType.INVINCIBILITY:
            self.invincibility_timer = 300
        elif powerup_type == PowerUpType.MAGNET:
            self.magnet_timer = 300
    
    def take_damage(self, damage):
        """Take damage from enemies"""
        if self.invulnerable_timer == 0 and self.invincibility_timer == 0:
            self.health -= damage
            self.health = max(0, self.health)
            self.invulnerable_timer = 120  # 2 seconds of invulnerability
            self.damage_flash_timer = 30
            return True
        return False


class EnemyMushroom(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, image):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.on_ground = False
        self.ai_timer = 0
        self.attack_cooldown = 0
        self.damage = self._get_damage()
        self.health = self._get_health()
        self.max_health = self.health
        
        # Special abilities based on type
        self.special_timer = 0
        self.patrol_start_x = x
        self.patrol_range = 200
    
    def _get_damage(self):
        """Get damage based on enemy type"""
        damage_map = {
            EnemyType.EVIL_MUSHROOM: 15,
            EnemyType.SPIKY_MUSHROOM: 25,
            EnemyType.POISON_MUSHROOM: 20,
            EnemyType.FIRE_MUSHROOM: 30
        }
        return damage_map.get(self.enemy_type, 15)
    
    def _get_health(self):
        """Get health based on enemy type"""
        health_map = {
            EnemyType.EVIL_MUSHROOM: 30,
            EnemyType.SPIKY_MUSHROOM: 50,
            EnemyType.POISON_MUSHROOM: 40,
            EnemyType.FIRE_MUSHROOM: 60
        }
        return health_map.get(self.enemy_type, 30)
    
    def update(self, platforms, player_mushroom, mario=None):
        """Update enemy mushroom"""
        self.ai_timer += 1
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        self.special_timer += 1
        
        # AI behavior based on type
        if self.enemy_type == EnemyType.EVIL_MUSHROOM:
            self._evil_mushroom_ai(player_mushroom, mario)
        elif self.enemy_type == EnemyType.SPIKY_MUSHROOM:
            self._spiky_mushroom_ai(player_mushroom)
        elif self.enemy_type == EnemyType.POISON_MUSHROOM:
            self._poison_mushroom_ai(player_mushroom)
        elif self.enemy_type == EnemyType.FIRE_MUSHROOM:
            self._fire_mushroom_ai(player_mushroom)
        
        # Physics
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ground collision - prevent falling through floor
        if self.rect.bottom >= 900 - 50:  # SCREEN_HEIGHT - ground_height
            self.rect.bottom = 900 - 50
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # Screen boundaries
        screen_width = 1400 * 2
        if self.rect.x < 0 or self.rect.right > screen_width:
            self.vel_x = -self.vel_x
    
    def _evil_mushroom_ai(self, player_mushroom, mario):
        """Basic evil mushroom - chases player"""
        distance_to_player = player_mushroom.rect.centerx - self.rect.centerx
        
        if abs(distance_to_player) < 300:
            # Chase player
            if distance_to_player > 0:
                self.vel_x = ENEMY_SPEED * 1.2
            else:
                self.vel_x = -ENEMY_SPEED * 1.2
                
            # Jump towards player
            if abs(distance_to_player) < 100 and self.on_ground and player_mushroom.rect.y < self.rect.y:
                self.vel_y = JUMP_SPEED * 0.8
        else:
            # Patrol behavior
            self._patrol_behavior()
        
        self.rect.x += self.vel_x
    
    def _spiky_mushroom_ai(self, player_mushroom):
        """Spiky mushroom - jumps frequently and is aggressive"""
        distance_to_player = player_mushroom.rect.centerx - self.rect.centerx
        
        if abs(distance_to_player) < 250:
            # Aggressive chase
            if distance_to_player > 0:
                self.vel_x = ENEMY_SPEED * 1.5
            else:
                self.vel_x = -ENEMY_SPEED * 1.5
            
            # Frequent jumping
            if self.on_ground and self.ai_timer % 60 == 0:
                self.vel_y = JUMP_SPEED * 1.1
        else:
            self._patrol_behavior()
        
        self.rect.x += self.vel_x
    
    def _poison_mushroom_ai(self, player_mushroom):
        """Poison mushroom - slower but more persistent"""
        distance_to_player = player_mushroom.rect.centerx - self.rect.centerx
        
        if abs(distance_to_player) < 400:  # Larger detection range
            # Slow but persistent chase
            if distance_to_player > 0:
                self.vel_x = ENEMY_SPEED * 0.8
            else:
                self.vel_x = -ENEMY_SPEED * 0.8
        else:
            self._patrol_behavior()
        
        self.rect.x += self.vel_x
    
    def _fire_mushroom_ai(self, player_mushroom):
        """Fire mushroom - fast and jumps high"""
        distance_to_player = player_mushroom.rect.centerx - self.rect.centerx
        
        if abs(distance_to_player) < 200:
            # Fast aggressive movement
            if distance_to_player > 0:
                self.vel_x = ENEMY_SPEED * 2.0
            else:
                self.vel_x = -ENEMY_SPEED * 2.0
            
            # High jumping
            if abs(distance_to_player) < 120 and self.on_ground and player_mushroom.rect.y < self.rect.y:
                self.vel_y = JUMP_SPEED * 1.3
        else:
            self._patrol_behavior()
        
        self.rect.x += self.vel_x
    
    def _patrol_behavior(self):
        """Default patrol behavior"""
        # Simple patrol between two points
        if abs(self.rect.x - self.patrol_start_x) > self.patrol_range:
            self.vel_x = -self.vel_x
        elif self.ai_timer % 120 == 0:  # Change direction occasionally
            self.vel_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        
        self.rect.x += self.vel_x


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = random.choice([-MUSHROOM_SPEED, MUSHROOM_SPEED])
        self.on_ground = False
        self.on_mario = False
        self.jump_cooldown = 0
    
    def update(self, platforms, mario):
        """Update ally mushroom"""
        self.jump_cooldown = max(0, self.jump_cooldown - 1)
        
        if self.on_mario:
            self.rect.centerx = mario.rect.centerx
            self.rect.bottom = mario.rect.top
            if random.randint(1, 240) == 1:
                self.on_mario = False
                self.vel_y = JUMP_SPEED
                self.vel_x = random.choice([-MUSHROOM_SPEED * 2, MUSHROOM_SPEED * 2])
            return
        
        # AI movement towards Mario
        distance = mario.rect.centerx - self.rect.centerx
        if abs(distance) > 60:
            self.vel_x = MUSHROOM_SPEED if distance > 0 else -MUSHROOM_SPEED
        
        self.rect.x += self.vel_x
        
        # Jumping
        if abs(distance) < 100 and self.on_ground and self.jump_cooldown == 0 and mario.rect.y < self.rect.y:
            self.jump()
            self.jump_cooldown = 120
        
        # Physics
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Ground collision - prevent falling through floor
        if self.rect.bottom >= 900 - 50:  # SCREEN_HEIGHT - ground_height
            self.rect.bottom = 900 - 50
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # Screen boundaries
        screen_width = 1400 * 2
        if self.rect.x < 0 or self.rect.right > screen_width:
            self.vel_x = -self.vel_x
    
    def jump(self):
        """Ally mushroom jump"""
        if self.on_ground:
            self.vel_y = JUMP_SPEED * 1.2


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type='normal'):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.platform_type = platform_type


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.type = powerup_type
        self.rect = pygame.Rect(x, y, 30, 30)
        self.timer = 0
        self.float_offset = 0
        self.base_y = y
    
    def update(self):
        """Update power-up"""
        self.timer += 1
        self.float_offset = math.sin(self.timer * 0.1) * 5
        self.rect.y = int(self.base_y + self.float_offset)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, obstacle_type='spike'):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.obstacle_type = obstacle_type
        self.damage = 30 if obstacle_type == 'spike' else 20
        self.timer = 0
    
    def update(self):
        """Update obstacle"""
        self.timer += 1
        # Some obstacles might have animation or movement