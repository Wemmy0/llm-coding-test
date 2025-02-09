import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Hexagon parameters
HEXAGON_RADIUS = 150
HEXAGON_COLOR = (0, 128, 255)  # Blue
HEXAGON_LINE_WIDTH = 3
HEXAGON_CENTER = (WIDTH // 2, HEIGHT // 2)
rotation_angle = 0
rotation_speed = 0.5  # Degrees per frame

# Ball parameters
BALL_RADIUS = 20
BALL_COLOR = RED
ball_x = WIDTH // 2
ball_y = HEIGHT // 2 - HEXAGON_RADIUS // 2  # Start near the top
ball_speed_x = random.uniform(-5, 5)  # Initial random horizontal speed
ball_speed_y = 0
GRAVITY = 0.5
DAMPING = 0.8  # Energy loss on collision (0 to 1)

# Function to calculate hexagon vertices
def hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        angle_rad = math.radians(angle + 60 * i)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices


# Function to check for collision between ball and a line segment
def collide_line(ball_x, ball_y, ball_radius, p1, p2):
    # Calculate distance from the ball's center to the line
    x1, y1 = p1
    x2, y2 = p2
    x0, y0 = ball_x, ball_y

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:  # Handle the case where the line is a point
        distance = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
        return distance <= ball_radius, None, None  # Treat as collision

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx**2 + dy**2)

    # Clamp t to the range [0, 1] to check only the segment
    t = max(0, min(1, t))

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    distance = math.sqrt((x0 - closest_x)**2 + (y0 - closest_y)**2)

    if distance <= ball_radius:
        # Calculate normal vector (perpendicular to the line)
        normal_x = -(y2 - y1)
        normal_y = (x2 - x1)

        # Normalize the normal vector
        normal_magnitude = math.sqrt(normal_x**2 + normal_y**2)
        normal_x /= normal_magnitude
        normal_y /= normal_magnitude

        return True, normal_x, normal_y
    else:
        return False, None, None


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update game logic ---
    # Rotate the hexagon
    rotation_angle += rotation_speed

    # Calculate hexagon vertices
    hexagon_points = hexagon_vertices(HEXAGON_CENTER, HEXAGON_RADIUS, rotation_angle)

    # Apply gravity to the ball
    ball_speed_y += GRAVITY

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision detection with hexagon edges
    for i in range(6):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i + 1) % 6]  # Wrap around to the first vertex
        collided, normal_x, normal_y = collide_line(ball_x, ball_y, BALL_RADIUS, p1, p2)

        if collided:
            # Separate the ball from the edge (avoid sticking)
            separation = BALL_RADIUS - math.sqrt((ball_x - (p1[0] + normal_x*BALL_RADIUS))**2 + (ball_y - (p1[1] + normal_y*BALL_RADIUS))**2)
            ball_x += normal_x * separation
            ball_y += normal_y * separation

            # Reflect the ball's velocity (realistic collision response)
            dot_product = ball_speed_x * normal_x + ball_speed_y * normal_y
            ball_speed_x -= 2 * dot_product * normal_x * DAMPING
            ball_speed_y -= 2 * dot_product * normal_y * DAMPING


    # Collision with screen edges (optional, but keeps the ball in view)
    if ball_x + BALL_RADIUS > WIDTH or ball_x - BALL_RADIUS < 0:
        ball_speed_x = -ball_speed_x * DAMPING
        ball_x = max(BALL_RADIUS, min(ball_x, WIDTH - BALL_RADIUS))  # Keep inside screen
    if ball_y + BALL_RADIUS > HEIGHT or ball_y - BALL_RADIUS < 0:
        ball_speed_y = -ball_speed_y * DAMPING
        ball_y = max(BALL_RADIUS, min(ball_y, HEIGHT - BALL_RADIUS))  # Keep inside screen

    # --- Draw everything ---
    screen.fill(BLACK)

    # Draw the hexagon
    pygame.draw.polygon(screen, HEXAGON_COLOR, hexagon_points, HEXAGON_LINE_WIDTH)

    # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()