import pygame

# To create a class template for ship and future to use.
# To create the a good ratio for the size of the game. Square mostly or rectuce
# To create a main game loop.
# To create other class for the weapons/equipment that effect the stats
# And to create

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