import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 980.0  # pixels per second squared
ELASTICITY = 0.8  # bounce elasticity
FRICTION = 0.99   # friction coefficient
FPS = 60

# Hexagon properties
HEXAGON_RADIUS = 150
hexagon_angle = 0
ROTATION_SPEED = 1  # degrees per frame

# Ball properties
BALL_RADIUS = 15
ball_pos = np.array([WIDTH/2, HEIGHT/2], dtype=float)
ball_vel = np.array([200.0, 0.0], dtype=float)

def rotate_point(point, center, angle):
    """Rotate a point around a center by an angle (in degrees)"""
    angle_rad = math.radians(angle)
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)

    dx = point[0] - center[0]
    dy = point[1] - center[1]

    new_x = center[0] + (dx * cos_val - dy * sin_val)
    new_y = center[1] + (dx * sin_val + dy * cos_val)

    return [new_x, new_y]

def get_hexagon_points():
    """Get the vertices of the hexagon"""
    points = []
    center = [WIDTH/2, HEIGHT/2]
    for i in range(6):
        angle_deg = 60 * i + hexagon_angle
        angle_rad = math.radians(angle_deg)
        x = center[0] + HEXAGON_RADIUS * math.cos(angle_rad)
        y = center[1] + HEXAGON_RADIUS * math.sin(angle_rad)
        points.append([x, y])
    return points

def get_line_segment(p1, p2):
    """Return the coefficients (A, B, C) of the line Ax + By + C = 0"""
    A = p2[1] - p1[1]
    B = p1[0] - p2[0]
    C = p2[0]*p1[1] - p1[0]*p2[1]
    return A, B, C

def distance_point_to_line(point, line_p1, line_p2):
    """Calculate the distance from a point to a line segment"""
    A, B, C = get_line_segment(line_p1, line_p2)
    distance = abs(A*point[0] + B*point[1] + C) / math.sqrt(A*A + B*B)
    return distance

def check_collision(ball_pos, hexagon_points):
    """Check and handle collisions between the ball and hexagon walls"""
    for i in range(6):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i+1)%6]

        # Calculate distance to line segment
        distance = distance_point_to_line(ball_pos, p1, p2)

        if distance <= BALL_RADIUS:
            # Calculate normal vector of the wall
            wall_vector = np.array([p2[0]-p1[0], p2[1]-p1[1]])
            normal = np.array([-wall_vector[1], wall_vector[0]])
            normal = normal / np.linalg.norm(normal)

            # Reflect velocity vector
            global ball_vel
            dot_product = np.dot(ball_vel, normal)
            ball_vel = ball_vel - (1 + ELASTICITY) * dot_product * normal

            # Move ball out of wall
            overlap = BALL_RADIUS - distance
            ball_pos[0] += normal[0] * overlap
            ball_pos[1] += normal[1] * overlap

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update physics
    dt = 1/FPS

    # Update ball position and velocity
    ball_vel[1] += GRAVITY * dt
    ball_vel *= FRICTION
    ball_pos += ball_vel * dt

    # Rotate hexagon
    hexagon_angle += ROTATION_SPEED
    hexagon_points = get_hexagon_points()

    # Check for collisions
    check_collision(ball_pos, hexagon_points)

    # Draw everything
    screen.fill(BLACK)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon_points, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, ball_pos.astype(int), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()