import pygame
import math
import random

# To create a class template for ship and future to use.
# To create the a good ratio for the size of the game. Square mostly or rectuce
# To create a main game loop.
# To create other class for the weapons/equipment that effect the stats
# And to create

class Asteroid:
    def __init__(self, x, y, asteroid_type, resolution):
        self.x = x
        self.y = y
        self.type = asteroid_type
        self.resolution = resolution

        if asteroid_type == "large":
            self.radius = 60
            self.hp = 60
            self.dmg = 30
            self.score = 100
        elif asteroid_type == "medium":
            self.radius = 35
            self.hp = 35
            self.dmg = 20
            self.score = 50
        elif asteroid_type == "small":
            self.radius = 15
            self.hp = 15
            self.dmg = 10
            self.score = 25
        self.angle = random.random() * math.pi * 2
        self.speed = random.uniform(1, 3)
    
    def update(self):
        self.x +=math.cos(self.angle) * self.speed
        self.y +=math.sin(self.angle) * self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, (180, 180, 180), (int(self.x), int(self.y)), int(self.radius))
    
class AsteroidCheck:
    def __init__(self, resolution):
        self.resolution = resolution
        self.asteroids = []

    def update(self):
         self._update_asteroids()

    def spawn_asteroids(self, amounts=8):
        asteroids = []
        for i in range(amounts):
            x = random.randint(0, self.resolution[0])
            y = random.randint(0, self.resolution[1])
            asteroid_type = random.choice(["large", "medium", "small"])
            self.asteroids.append(Asteroid(x, y, asteroid_type, self.resolution))
        return asteroids
    
    def _update_asteroids(self):
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if self._asteroid_is_offscreen(asteroid):
                self.asteroids.remove(asteroid)

    def _asteroid_is_offscreen(self, asteroid):
        asteroid_is_offscreen = (asteroid.x < 0 or asteroid.x > self.resolution[0] or
                                   asteroid.y < 0 or asteroid.y > self.resolution[1])
        return asteroid_is_offscreen

    def add_asteroid(self, x, y, angle, asteroid_type):
        asteroid = Asteroid(x,y,angle, asteroid_type, self.resolution)
        self.asteroids.insert(0, asteroid)
    
    def draw(self, screen):
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        

class Weapon:
    def __init__(self, name, dmg, projectile_speed, fire_rate, projectile_img=None):
        self.name = name
        self.dmg = dmg
        self.projectile_speed = projectile_speed
        self.fire_rate = fire_rate
        self.projectile_img = projectile_img

class Projectile:
    def __init__(self, x, y, angle, Weapon):
        self.pos = pygame.Vector2(x,y)
        self.angle = angle
        self.speed = Weapon.projectile_speed
        self.dmg = Weapon.dmg
        self.direction = pygame.Vector2(1,0).rotate(-angle)
        self.radius = 3
        self.original_img = None
        self.use_img = False
        if Weapon.projectile_img:
            self.original_img = pygame.image.load(Weapon.projectile_img).convert_alpha()
            self.original_img = pygame.transform.scale(self.original_img, (20, 20)) # This will tranform the scale to be x,y pixel size.
            self.image = self.original_img
            self.use_img = True 
    
    def update(self):
        self.pos += self.direction * self.speed
    
    def draw(self, screen):
        if self.use_img:
            rotated = pygame.transform.rotate(self.original_img, -self.angle)
            rect = rotated.get_rect(center=(self.pos.x, self.pos.y))
            screen.blit(rotated, rect)
        else:
            pygame.draw.circle(screen, (255, 255, 255),(int(self.pos.x),int(self.pos.y)),self.radius)

class ProjectileCheck:
    def __init__(self, resolution):
        self.resolution = resolution
        self.projectiles = []

    def update(self):
         self._update_projectiles()
    
    def _update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()
            if self._projectile_is_offscreen(projectile):
                self.projectiles.remove(projectile)

    def _projectile_is_offscreen(self, projectile):
        projectile_is_offscreen = (projectile.pos.x < 0 or projectile.pos.x > self.resolution[0] or
                                   projectile.pos.y < 0 or projectile.pos.y > self.resolution[1])
        return projectile_is_offscreen

    def add_projectile(self, x, y, angle, weapon):
        projectile = Projectile(x,y,angle, weapon)
        self.projectiles.insert(0, projectile)
    
    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
        
class Ship_template:
    def __init__(self, hp, dmg, speed, turn_speed, resolution, weapon, image=None):
        self.hp = hp
        self.dmg = dmg
        self.speed = speed
        self.turn_speed = turn_speed
        self.weapon = weapon
        self.cooldown = 0
        self.radius = 15

        # Postion should start at the middle of the resolution
        self.x = resolution[0] // 2
        self.y = resolution[1] // 2
        self.angle = 0

        self.pos = pygame.Vector2(self.x, self.y)
        self.direction = pygame.Vector2(1, 0)

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
        self.direction = pygame.Vector2(1,0).rotate(-self.angle)
        if keys[pygame.K_w]: # Moving forward based on the angle it is facing
            self.x +=self.direction.x * self.speed
            self.y +=self.direction.y * self.speed
        if keys[pygame.K_s]: # Moving backward based on the angle it is facing
            self.x -=self.direction.x * self.speed
            self.y -=self.direction.y * self.speed
    
    def shoot(self, ProjectileCheck):
        if self.cooldown == 0:
            ProjectileCheck.add_projectile(self.x, self.y, self.angle, self.weapon)
            self.cooldown = self.weapon.fire_rate
    
    def update(self):
        if self.cooldown >0:
            self.cooldown -= 1
    
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

      
def projectile_hit_asteroid(asteroid, projectile):
        dx = asteroid.x - projectile.pos.x
        dy = asteroid.y - projectile.pos.y
        return math.hypot(dx, dy) < asteroid.radius

def ship_hit_asteroid(asteroid, ship):
        dx = asteroid.x - ship.x
        dy = asteroid.y - ship.y
        return math.hypot(dx, dy) < asteroid.radius + ship.radius

def main():
    pygame.init()
    pygame.display.set_caption("Asteroid_Destroyer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)
    score = 0
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)
    single_laser = Weapon("Single_Lazer", dmg=10,projectile_speed=20,fire_rate=10)
    starter_ship = Ship_template(100, 10, 10, 5, resolution, single_laser)
    project_m = ProjectileCheck(resolution)
    asteroid_m = AsteroidCheck(resolution)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
        
        keys = pygame.key.get_pressed()
        starter_ship.movement(keys)
        starter_ship.update()

        if keys[pygame.K_SPACE]:
            starter_ship.shoot(project_m)
        project_m.update()  
        asteroid_m.update()

        while len(asteroid_m.asteroids) < 8:
            asteroid_m.spawn_asteroids(1)
        
        for projectile in project_m.projectiles[:]:
            for asteroid in asteroid_m.asteroids[:]:
                if projectile_hit_asteroid(asteroid, projectile):
                    asteroid.hp -= projectile.dmg
                    if projectile in project_m.projectiles:
                        project_m.projectiles.remove(projectile)
                    if asteroid.hp <= 0:
                        asteroid_m.asteroids.remove(asteroid)
                        score += asteroid.score
                    break
        if starter_ship.hp > 0:
            for asteroid in asteroid_m.asteroids[:]:
                if ship_hit_asteroid(asteroid, starter_ship):
                    starter_ship.hp -= asteroid.dmg
                    asteroid_m.asteroids.remove(asteroid)

        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        ui = font.render( f"HP: {starter_ship.hp}   Score: {score}", True, (255, 255, 255))
        screen.blit(ui, (20,20))
        if starter_ship.hp <= 0:
            game_over = font.render( "GAME OVER", True, (255, 255, 255))
            screen.blit(game_over,(resolution[0] // 2, resolution[1] // 2)) #Put the game over at the center

        starter_ship.draw(screen)
        project_m.draw(screen)
        asteroid_m.draw(screen)
        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()

if __name__ == "__main__":
    main()