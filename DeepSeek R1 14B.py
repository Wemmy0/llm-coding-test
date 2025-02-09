# DOESN'T RUN - SYNTAX ERRORS

import pygame
import math

# Initialize Pygame and set up the screen
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Set center of the screen as (cx, cy)
cx, cy = screen_width // 2, screen_height // 2

# Create a spinning hexagon in the center
hex_size = 150
hex_points = [
    (cx + hex_size * math.cos(angle), cy + hex_size * math.sin(angle))
    for angle in [math.radians(60*i) for i in range(6)]
]

# Ball properties
ball_radius = 20
ball_color = (255, 0, 0)
velocity_x = 3.5
velocity_y = -4.0

# Gravity and friction constants
gravity = 0.5
friction = 0.98

# Calculate the hexagon's edges for collision detection
hex_edges = []
points = [(cx + hex_size * math.cos(math.radians(60*i)), cy + hex_size * math.sin(math.radians(60*i))) for i in range(6)]
for i in range(len(points)):
    p1 = points[i]
    p2 = points[(i+1)%len(points)]
    edge = (p1, p2)
    hex_edges.append(edge)

# Function to check collision between circle and polygon
def check_collision(circle_pos, circle_radius, edges):
    for edge in edges:
        point_a, point_b = edge

        # Calculate the closest point on the edge to the center of the circle
        min_dist_sq = float('inf')
        closest_point = None

        t = 0.0
        if (point_b[1] - point_a[1]) != 0:
            t = (circle_pos[1] - point_a[1]) / (point_b[1] - point_a[1])

        x_intersect = point_a[0] + t * (point_b[0] - point_a[0])
        y_intersect = circle_pos[1]

        # Project the center onto the edge
        projection_t = 0.5
        if (point_b[0] - point_a[0]) != 0:
            slope_inv = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
            t_proj = ((circle_pos[0] - point_a[0]) + slope_inv * (circle_pos[1] - point_a[1]))
            if 0 <= t_proj <= 1:
                x_intersect = point_a[0] + t_proj * (point_b[0] - point_a[0])
                y_intersect = point_a[1] + t_proj * (point_b[1] - point_a[1])

        # Calculate distance from circle center to edge
        dx = x_intersect - circle_pos[0]
        dy = y_intersect - circle_pos[1]
        dist_sq = dx**2 + dy**2

        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest_point = (x_intersect, y_intersect)

    # Calculate the distance from center to edge
    min_distance = math.sqrt(min_dist_sq)

    return {
        'colliding': True,
        'distance': abs(circle_radius - min_distance),
        'point': closest_point
    }

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Rotate hexagon each frame
    rotation_angle += 1
    rotated_hex_points = [
        (cx + hex_size * math.cos(math.radians(60*i + rotation_angle)), cy + hex_size * math.sin(math.radians(60*i + rotation_angle)))
        for i in range(6)
    ]

    # Draw the spinning hexagon
    pygame.draw.polygon(screen, (0, 255, 0), rotated_hex_points)

    # Update ball position and physics
    new_x = int(ball_pos[0] + velocity_x * dt)
    new_y = int(ball_pos[1] + velocity_y * dt)

    # Apply gravity
    if not collision:
        velocity_y += gravity

    # Apply friction to x and y velocities
    velocity_x *= 0.98
    velocity_y *= 0.98

    ball_pos = (new_x, new_y)

    # Check for collisions with hexagon edges
    collision_data = check_collision(ball_pos, ball_radius, hex_edges)

    if collision_data['colliding']:
        # Reflect the velocity based on the normal vector of the edge
        dx = closest_point[0] - ball_pos[0]
        dy = closest_point[1] - ball_pos[1]

        angle = math.atan2(dy, dx)

        velocity_x += 3 * math.cos(angle)
        velocity_y += 3 * math.sin(angle)

    # Draw the ball
    pygame.draw.circle(screen, (255, 0, 0), ball_pos, ball_radius)

    # Update screen and clock
    pygame.display.flip()
    dt = clock.tick(60)

# Quit Pygame
pygame.quit()