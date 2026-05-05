import pygame
import math

# To create a class template for ship and future to use.
# To create the a good ratio for the size of the game. Square mostly or rectuce
# To create a main game loop.
# To create other class for the weapons/equipment that effect the stats
# And to create
class Ship_template:
    def __init__(self, hp, dmg, speed, turn_speed, fire_rate, resolution, image=None):
        self.hp = hp
        self.dmg = dmg
        self.speed = speed
        self.turn_speed = turn_speed
        self.fire_rate = fire_rate

        # Postion should start at the middle of the resolution
        self.x = resolution[0] // 2
        self.y = resolution[1] // 2
        self.angle = 0

        # For Testing if there a png if not just using shapes
        self.original_img = None
        self.image = None
        self.use_img = False

        if image:
            self.original_img = pygame.image.load(image).convert_alpha()
            self.original_img = pygame.transform.scale(self.original_img, (80, 80)) # This will tranform the scale to be x,y pixel size.
            self.image = self.original_img
            self.use_img = True
    
    def movement(self, keys):
        if keys[pygame.K_a]: # Turning to left
            self.angle += self.turn_speed
        if keys[pygame.K_d]: # Turning to Right
            self.angle -= self.turn_speed
        # if keys[pygame.K_w]: # Moving forward based on the angle it is facing
            # Set up later.
        # if keys[pygame.K_s]: # Moving backward based on the angle it is facing
            # Set up later.
            
    def draw(self, screen):
        if self.use_img:
            rotated = pygame.transform.rotate(self.original_img, -self.angle)
            rect = rotated.get_rect(center=(self.x, self.y))
            screen.blit(rotated, rect)
        else: # When there are no img so default is triangle
            rad = math.radians(self.angle)
            front = (self.x + math.cos(rad) * 20, self.y - math.sin(rad) * 20)
            left = (self.x + math.cos(rad + 2.5) * 15, self.y - math.sin(rad + 2.5) * 15)
            right = (self.x + math.cos(rad - 2.5) * 15, self.y - math.sin(rad - 2.5) * 15)
            pygame.draw.polygon(screen, (255, 255, 255), [front, left, right])

def main():
    pygame.init()
    pygame.display.set_caption("Asteroid_Destroyer")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)
    starter_ship = Ship_template(100, 10, 10, 10, 5, resolution, "Testing_ship.png")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        keys = pygame.key.get_pressed()
        starter_ship.movement(keys)
        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        starter_ship.draw(screen)
        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()

if __name__ == "__main__":
    main()