import pygame
import math
import random

# To create a class template for ship and future to use.
# To create the a good ratio for the size of the game. Square mostly or rectuce
# To create a main game loop.
# To create other class for the weapons/equipment that effect the stats
# And to create
Ship_types = {
    "Scout": {
        "hp" : 80, "speed" : 12, "turn_speed" : 7, "radius" : 12, "weapon_slots" : 1
    },
    "Fighter": {
        "hp" : 100, "speed" : 10, "turn_speed" : 6, "radius" : 15, "weapon_slots" : 2
    },
    "Tank": {
        "hp" : 180, "speed" : 5, "turn_speed" : 3, "radius" : 22, "weapon_slots" : 3
    },
    "Interceptor": {
        "hp" : 70, "speed" : 15, "turn_speed" : 9, "radius" : 10, "weapon_slots" : 1
    }
}
    
Weapon_types = {
    "Single Laser": {
        "dmg" : 10, "projectile_speed" : 20, "fire_rate" : 10, "slots_required" : 1
    },
    "Rapid Laser": {
        "dmg" : 5, "projectile_speed" : 24, "fire_rate" : 4, "slots_required" : 1
    },
    "Missile": {
        "dmg" : 50, "projectile_speed" : 8, "fire_rate" : 40, "slots_required" : 2
    },
    "Heavy Cannon": {
        "dmg" : 30, "projectile_speed" : 12, "fire_rate" : 35, "slots_required" : 2
    }
}       

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

    def generate_random_location(self):
        spawn_offset = 150 # To spawn off screen
        while True:
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(0, self.resolution[0])
                y = -spawn_offset
            elif side == "bottom":
                x = random.randint(0, self.resolution[0])
                y = self.resolution[1] + spawn_offset
            elif side == "left":
                x = -spawn_offset
                y = random.randint(0, self.resolution[1])
            elif side == "right":
                x = self.resolution[0] + spawn_offset
                y = random.randint(0, self.resolution[1])
            return pygame.Vector2(x,y)
        

    def spawn_asteroids(self, amounts=8):
        for i in range(amounts):
            asteroid_type = random.choice(["large", "medium", "small"])
            location = self.generate_random_location()
            self.asteroids.append(Asteroid(location.x, location.y, asteroid_type, self.resolution))
    
    def _update_asteroids(self):
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if self._asteroid_is_offscreen(asteroid):
                self.asteroids.remove(asteroid)

    def _asteroid_is_offscreen(self, asteroid):
        extra_distance = 200 #200 pixel off screen since it now genrate random 150 off screen.
        asteroid_is_offscreen = (asteroid.x < -extra_distance or asteroid.x > self.resolution[0] + extra_distance or
                                   asteroid.y < -extra_distance or asteroid.y > self.resolution[1] + extra_distance)
        return asteroid_is_offscreen

    def add_asteroid(self, x, y, asteroid_type):
        asteroid = Asteroid(x,y, asteroid_type, self.resolution)
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
    def __init__(self, hp, speed, turn_speed, radius, resolution, weapon, image=None):
        self.hp = hp
        self.speed = speed
        self.turn_speed = turn_speed
        self.radius = radius
        self.weapon = weapon
        self.cooldown = 0

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
      
def create_weapon(weapon_name):
    weapon_data = Weapon_types[weapon_name]
    return Weapon(weapon_name, dmg=weapon_data["dmg"],projectile_speed=weapon_data["projectile_speed"],fire_rate=weapon_data["fire_rate"])

def can_equip_weapon(ship_stats, weapon_name):
    return Weapon_types[weapon_name]["slots_required"] <= ship_stats["weapon_slots"]

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
    game_over = False
    resolution = (1920, 1080)
    screen = pygame.display.set_mode(resolution)

    selected_ship_name = "Fighter"
    selected_weapon_name = "Single Laser"

    selected_ship_stats = Ship_types[selected_ship_name]

    if not can_equip_weapon(selected_ship_stats, selected_weapon_name):
        print("Ship is too small or weapon is too big.")
        pygame.quit()
        return
    
    selected_weapon = create_weapon(selected_weapon_name)

    selected_ship = Ship_template(hp=selected_ship_stats["hp"], speed=selected_ship_stats["speed"],
                                  turn_speed=selected_ship_stats["turn_speed"], radius=selected_ship_stats["radius"],
                                  resolution=resolution, weapon=selected_weapon)

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

        if not game_over: # This should freeze the movement when it game over and not let move anymore
            selected_ship.movement(keys)
            selected_ship.update()

            if keys[pygame.K_SPACE]:
                selected_ship.shoot(project_m)
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
            
            for asteroid in asteroid_m.asteroids[:]:
                if ship_hit_asteroid(asteroid, selected_ship):
                    selected_ship.hp -= asteroid.dmg
                    asteroid_m.asteroids.remove(asteroid)

            if selected_ship.hp <= 0:
                game_over = True

        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        ui = font.render( f"Ship: {selected_ship_name}   Weapon: {selected_weapon_name}   HP: {selected_ship.hp}   Score: {score}", True, (255, 255, 255))
        screen.blit(ui, (20,20))
        if selected_ship.hp <= 0:
            game_over_text = font.render( "GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text,(resolution[0] // 2, resolution[1] // 2)) #Put the game over at the center

        selected_ship.draw(screen)
        project_m.draw(screen)
        asteroid_m.draw(screen)
        pygame.display.flip()
        dt = clock.tick(24)
    pygame.quit()

if __name__ == "__main__":
    main()