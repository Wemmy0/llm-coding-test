import pygame
import math

# Initialize Pygame
pygame.init()

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon parameters
center = (width//2, height//2)
hex_radius = 200
rotation_angle = 0
rotation_speed = 1  # Degrees per frame

# Ball parameters
ball_pos = [center[0], center[1] - 150]
ball_vel = [3.0, 0.0]
ball_radius = 15
gravity = 0.5
damping = 0.8

def calculate_hexagon_vertices(radius, angle):
    vertices = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

def closest_point_on_segment(A, B, P):
    ax, ay = A
    bx, by = B
    px, py = P

    segment_vec = (bx - ax, by - ay)
    point_vec = (px - ax, py - ay)

    t = (point_vec[0] * segment_vec[0] + point_vec[1] * segment_vec[1]) / \
        (segment_vec[0]**2 + segment_vec[1]**2 + 1e-8)
    t = max(0, min(1, t))

    return (ax + t * segment_vec[0], ay + t * segment_vec[1])

def handle_collisions(vertices):
    global ball_pos, ball_vel

    for i in range(6):
        A = vertices[i]
        B = vertices[(i+1) % 6]
        closest = closest_point_on_segment(A, B, ball_pos)

        dx = ball_pos[0] - closest[0]
        dy = ball_pos[1] - closest[1]
        distance = math.hypot(dx, dy)

        if distance < ball_radius:
            edge_vec = (B[0]-A[0], B[1]-A[1])
            normal = (edge_vec[1], -edge_vec[0])
            length = math.hypot(normal[0], normal[1])

            if length == 0:
                continue

            normal = (normal[0]/length, normal[1]/length)
            penetration = ball_radius - distance

            # Position correction
            ball_pos[0] += normal[0] * penetration
            ball_pos[1] += normal[1] * penetration

            # Velocity reflection
            dot = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
            ball_vel[0] -= 2 * dot * normal[0]
            ball_vel[1] -= 2 * dot * normal[1]

            # Apply damping
            ball_vel[0] *= damping
            ball_vel[1] *= damping

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    rotation_angle = (rotation_angle + rotation_speed) % 360
    vertices = calculate_hexagon_vertices(hex_radius, rotation_angle)

    # Update ball physics
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Handle collisions
    handle_collisions(vertices)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.polygon(screen, BLUE, vertices, 3)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()