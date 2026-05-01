import pygame
import math

# To create a class template for ship and future to use.
# To create the a good ratio for the size of the game. Square mostly or rectuce
# To create a main game loop.
# To create other class for the weapons/equipment that effect the stats
# And to create
class Ship_template:
    def __init__(self, hp, dmg, speed, turn_speed, fire_rate, resolution):
        self.hp = hp
        self.dmg = dmg
        self.speed = speed
        self.turn_speed = turn_speed
        self.fire_rate = fire_rate

        # Postion should start at the middle of the resolution
        self.x = resolution[0] // 2
        self.y = resolution[1] // 2
        self.angle = 0
    
    def movement(self, keys):
        if keys[pygame.K_a]: # Turning to left
            self.angle += self.turn_speed
        if keys[pygame.K_d]: # Turning to Right
            self.angle -= self.turn_speed
        if keys[pygame.K_w]: # Moving forward based on the angle it is facing

        if keys[pygame.K_s]: # Moving backward based on the angle it is facing
            

def main():
    pygame.init()
    pygame.display.set_caption("Asteroid_Destroyer")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()

if __name__ == "__main__":
    main()