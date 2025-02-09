import pygame
from math import cos, sin, radians
import random

# Initialize Pygame
pygame.init()

# Set up the window dimensions
width = 800
height = 600

# Create the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
BLACK = (0, 0, 0)
RED = (255, 140, 140)

class Ball:
    def __init__(self):
        self.radius = 30
        self.x = width // 2 - self.radius
        self.y = height // 2 - self.radius
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, 0)

    def update(self):
        # Apply gravity (acceleration due to gravity in y-direction)
        g = 1.5
        damping_factor = 0.7

        # Update velocity and position
        self.vy += g
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def create_hexagon(center_x, center_y, radius=100):
    hex_points = []
    for i in range(6):
        x = cos(radians(i * 60)) * radius + center_x
        y = sin(radians(i * 60)) * radius + center_y
        hex_points.append((x, y))
    return hex_points

def point_in_polygon(x, y, polygon):
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n+1):
        p2x, p2y = polygon[i % n]
        if (y > min(p1y, p2y)):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersect = ((p2x - p1x) * (y - p1y)) / (p2y - p1y) + p1x
                    else:
                        x_intersect = 9e+307

                    if (p1x == p2x or x <= x_intersect):
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def main():
    # Initialize objects and variables
    ball = Ball()

    center_x, center_y = width // 2, height // 2
    hexagon_radius = 300

    angle = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Update ball position and check collisions with hexagon walls
        ball.update()

        # Check collision with hexagon boundary using point-in-polygon test
        polygon = create_hexagon(center_x, center_y, hexagon_radius)

        for i in range(6):
            p1 = polygon[i]
            p2 = polygon[(i+1) % 6]

            dx = ball.x - (p1[0] + p2[0]) / 2
            dy = ball.y - (p1[1] + p2[1]) / 2

            dist_line_segment = abs((dx * (p2[1] - p1[1])) - (dy * (p2[0] - p1[0])))
            len_segment = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) ** 0.5

            if dist_line_segment <= ball.radius:
                x_intersect, y_intersect = (dx / (dist_line_segment)) * ball.radius + p1[0], (dy / (dist_line_segment)) * ball.radius + p1[1]

                # Reflect velocity
                normal_x = -(y - ((p2[1] - p1[1])/(p2[0]-p1[0]))*(x - p1[0]))
                normal_y =  x - (p1[0])

                dot_product = ball.vx * normal_x + ball.vy * normal_y
                if abs(dot_product) > 0:
                    reflection_factor = -(2*dot_product)/(normal_x**2 + normal_y**2)

                    new_vx = ball.vx + reflection_factor * (normal_x - (ball.x - p1[0]))
                    new_vy = ball.vy + reflection_factor * (normal_y - (ball.y - p1[1]))

                    damping_factor = 0.7
                    ball.vx *= damping_factor
                    ball.vy *= damping_factor

        # Keep the hexagon centered while rotating it
        rotated_hexagon_points = []
        for point in polygon:
            x, y = point
            relative_x = x - center_x
            relative_y = y - center_y

            new_x = (relative_x * cos(radians(angle)) + relative_y * sin(radians(angle)))
            new_y = (-relative_x * sin(radians(angle)) + relative_y * cos(radians(angle)))

            rotated_hexagon_points.append((new_x, new_y))

        # Draw the spinning hexagon
        pygame.draw.polygon(screen, BLACK, [(int(p[0]), int(p[1])) for p in rotated_hexagon_points], 2)

        # Draw ball
        ball.draw()

        # Update display and angle increment
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()