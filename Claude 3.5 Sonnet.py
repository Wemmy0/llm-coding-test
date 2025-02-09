import pygame
import math
import sys
from pygame import Vector2

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 980  # pixels per second squared
BALL_RADIUS = 10
ELASTICITY = 0.7  # Energy retention after collision
FRICTION = 0.99  # Air/rolling friction
HEXAGON_SIZE = 100
ROTATION_SPEED = 1  # radians per second

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.pos = Vector2(WIDTH//2, HEIGHT//2 - 50)
        self.vel = Vector2(200, 0)
        self.radius = BALL_RADIUS
        self.color = RED

    def update(self, dt, hexagon_points):
        # Update position and velocity
        self.vel.y += GRAVITY * dt
        self.pos += self.vel * dt
        self.vel *= FRICTION

        # Check collision with hexagon sides
        for i in range(len(hexagon_points)):
            p1 = hexagon_points[i]
            p2 = hexagon_points[(i + 1) % len(hexagon_points)]

            # Check if ball collides with line segment
            collision = self.check_line_collision(p1, p2)
            if collision:
                normal = self.calculate_normal(p1, p2)
                self.handle_collision(normal)

    def check_line_collision(self, p1, p2):
        # Vector from p1 to p2
        line_vec = Vector2(p2[0] - p1[0], p2[1] - p1[1])
        # Vector from p1 to ball
        ball_vec = Vector2(self.pos.x - p1[0], self.pos.y - p1[1])

        line_len = line_vec.length()
        # Normalized dot product
        dot = ball_vec.dot(line_vec) / (line_len * line_len)
        # Closest point on line segment
        closest = Vector2(p1[0], p1[1]) + line_vec * max(0, min(1, dot))

        # Check if distance to closest point is less than ball radius
        dist = (Vector2(closest) - self.pos).length()
        return dist < self.radius

    def calculate_normal(self, p1, p2):
        # Calculate normal vector to the line
        line_vec = Vector2(p2[0] - p1[0], p2[1] - p1[1])
        normal = Vector2(-line_vec.y, line_vec.x).normalize()
        return normal

    def handle_collision(self, normal):
        # Reflect velocity vector off the normal
        dot = self.vel.dot(normal)
        self.vel -= (1 + ELASTICITY) * dot * normal

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class Hexagon:
    def __init__(self):
        self.center = Vector2(WIDTH//2, HEIGHT//2)
        self.size = HEXAGON_SIZE
        self.angle = 0

    def get_points(self):
        points = []
        for i in range(6):
            angle = self.angle + i * math.pi / 3
            x = self.center.x + self.size * math.cos(angle)
            y = self.center.y + self.size * math.sin(angle)
            points.append((x, y))
        return points

    def update(self, dt):
        self.angle += ROTATION_SPEED * dt

    def draw(self, screen):
        points = self.get_points()
        pygame.draw.polygon(screen, BLACK, points, 2)

def main():
    ball = Ball()
    hexagon = Hexagon()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate delta time
        dt = clock.tick(FPS) / 1000.0

        # Update
        hexagon.update(dt)
        ball.update(dt, hexagon.get_points())

        # Draw
        screen.fill(WHITE)
        hexagon.draw(screen)
        ball.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()