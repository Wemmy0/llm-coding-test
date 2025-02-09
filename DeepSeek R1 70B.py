import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

GRAVITY = 0.5
BOUNCE_DAMPENING = 0.8  # Energy loss on bounce

class Hexagon:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = 0

    def draw(self, screen):
        vertices = []
        for i in range(6):
            theta = self.angle + i * math.pi / 3
            x = self.x + math.cos(theta) * self.radius
            y = self.y + math.sin(theta) * self.radius
            vertices.append((x, y))

        # Draw the hexagon
        pygame.draw.polygon(screen, BLUE, vertices, 2)

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 5  # Initial horizontal velocity
        self.vy = -10  # Initial upward velocity

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, 100)
    ball = Ball(hexagon.x, hexagon.y, 8)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # Update hexagon
        hexagon.angle += 0.02  # Spin speed
        hexagon.draw(screen)

        # Update ball physics
        ball.vy += GRAVITY
        ball.x += ball.vx
        ball.y += ball.vy

        # Simple collision with hexagon edges (simplified for demonstration)
        # Calculate distance from ball to center
        dx = ball.x - hexagon.x
        dy = ball.y - hexagon.y
        distance_to_center = math.hypot(dx, dy)

        # If the ball is outside the hexagon, reflect the velocity
        if distance_to_center > hexagon.radius - ball.radius:
            # Normalize the collision normal
            normal_x = dx / distance_to_center
            normal_y = dy / distance_to_center

            # Reflect velocity
            dot_product = ball.vx * normal_x + ball.vy * normal_y
            ball.vx -= 2 * dot_product * normal_x
            ball.vy -= 2 * dot_product * normal_y

            # Move the ball back inside
            ball.x = hexagon.x + normal_x * (hexagon.radius - ball.radius)
            ball.y = hexagon.y + normal_y * (hexagon.radius - ball.radius)

            # Apply dampening
            speed = math.hypot(ball.vx, ball.vy)
            if speed > 0:
                ball.vx *= BOUNCE_DAMPENING
                ball.vy *= BOUNCE_DAMPENING

        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()