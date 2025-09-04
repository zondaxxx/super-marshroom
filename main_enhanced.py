#!/usr/bin/env python3
"""
Super Mushroom: Enhanced Battle Edition
A platformer where you play as a mushroom trying to jump on Mario
while fighting enemy mushrooms and avoiding obstacles!
"""

import pygame
import sys
import os

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_logic import Game
from game_ui import draw_ui

def main():
    """Main function to run the enhanced mushroom game"""
    # Initialize pygame
    pygame.init()
    
    try:
        # Create and run the game
        game = Game()
        
        # Main game loop
        while game.running:
            game.handle_events()
            game.update()
            draw_ui(game)
            game.clock.tick(60)
            
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        pygame.quit()
        print("Game ended. Thanks for playing!")

if __name__ == "__main__":
    main()