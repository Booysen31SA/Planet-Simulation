import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000 #distamce from earth to the sun
    G = 6.67428e-11
    SCALE = 250 / AU #1AU = 100 pixels
    TIMESTEP = 3600*24 #1 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []

        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y= self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"Distance to SUN: {round(self.distance_to_sun/1000, 1)} KM", 1, WHITE)
            name_text = FONT.render(f"{self.name}", 1, WHITE)
            win.blit(name_text, ( x - name_text.get_width() / 2, y + 10))
            win.blit(distance_text, ( x - distance_text.get_width() / 2, y + 25))
        else:
            name_text = FONT.render(f"{self.name}", 1, WHITE)
            win.blit(name_text, ( x - name_text.get_width() / 2, y + 30))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        #disance between this object and other object
        distance_x = other_x - self.x 
        distance_y = other_y - self.y 

        distance = math.sqrt(distance_x**2 + distance_y**2)

        # if other object is the sun
        if other.sun:
            self.distance_to_sun = distance
        
        #force of attraction
        force = (self.G * self.mass * other.mass) / (distance**2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planents):
        total_fx, total_fy = 0, 0 
        for planet in planents:
            if self == planet:
                continue
        
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 'Earth')
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 'Mars')
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, 'Mercury')
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, 'Venus')
    venus.y_vel = -35.02 * 1000

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 'Sun')
    sun.sun = True

    planets = [sun, earth, mars, mercury, venus]
    
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()


main()