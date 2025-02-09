# DOESN'T RUN - SYNTAX ERRORS

import pygame
import math

# Initialize Pygame and display
pygame.init()
screen_width = 800
screen_height = 600
background_color = (128, 128, 128)  # Dark gray background

# Ball properties
ball_radius = 15
gravity = -9.8 / 3600.0  # Adjust gravity strength [pixels per second]
vertical_bounce_max_speed = 10.0  # Maximum vertical speed when bouncing
dampening_factor = 0.5  # Energy loss on each bounce

# Hexagon properties
hexagon_radius = screen_height // (2 * math.sqrt(3)) / 2 + ball_radius
angle_step = 6.28 / len(range(12))

# Ball position, velocity, angle and spin speed
ball_pos_x = screen_width / 2 - ball_radius
ball_pos_y = screen_height / 2 - ball_radius

velocity_y = vertical_bounce_max_speed * (dampening_factor)
velocity_x = 0.0

angle = math.radians(90)  # Initial rotation angle for the hexagon
spin_step = 6.28 / len(range(12))  # Rotation speed in radians per frame

# Mouse interaction variables
dragging = False
mouse_x, mouse_y = screen_width // 2 - ball_radius, screen_height // 2 - ball_radius

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling for mouse dragging and releasing
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (pos[0] - ball_pos_x) ** 2 + (pos[1] - ball_pos_y) ** 2 <= ball_radius * 2:
                dragging = True
                mouse_x, mouse_y = pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # Release the ball with physics based on mouse position relative to center
            delta_x = mouse_x - screen_width // 2
            delta_y = mouse_y - screen_height // 2

            velocity_x += (delta_x / ball_radius) * 10.0
            velocity_y -= (delta_y / ball_radius) * gravity

            dragging = False

    # Update physics and positions
    if not dragging:
        # Apply gravity
        position_change_y = velocity_y + gravity

        # Bounce off the top/bottom edges
        if ball_pos_y < 0 or ball_pos_y > screen_height - ball_radius:
            velocity_y *= -1.0

        new_ball_pos_y = ball_pos_y + position_change_y
        if (ball_pos_x, new_ball_pos_y) not in [0, screen_width-1]:
            # Apply vertical bounce and damping
            velocity_y -= max(new_ball_pos_y - ball_pos_y, 0) / ball_radius * dampening_factor

        # Apply horizontal movement with some minor friction
        if abs(velocity_x) > 0.000001:
            velocity_x *= (dampening_factor)

        ball_pos_x += velocity_x
        ball_pos_y = new_ball_pos_y

    else:
        # Simulate manual dragging with the mouse position
        delta_x = mouse_x - screen_width // 2
        delta_y = mouse_y - screen_height // 2

        # Keep in bounds
        current_ball_pos_x = max(0, min(ball_pos_x + (delta_x / ball_radius) * 10.0, screen_width-1))
        current_ball_pos_y = max(0, min(ball_pos_y + (delta_y / ball_radius) * -gravity*2, screen_height-1))

        # Update position
        ball_pos_x = int(current_ball_pos_x)
        ball_pos_y = int(current_ball_pos_y)

    # Spin the hexagon
    angle += spin_step

    # Clear and redraw everything
    pygame.draw.rect(screen, background_color, (0, 0), screen_width, screen_height)

    # Draw the spinning hexagon
    for i in range(6):
        x = hexagon_radius * math.cos(angle + i * math.radians(60))
        y = -hexagon_radius * math.sin(angle + i * math.radians(60))
        if i < 3:
            pygame.draw.line(screen, (255,0,0),
                             (screen_width // 2 - x - ball_pos_x, screen_height // 2 - y - ball_pos_y),
                             (screen_width // 2 + x - ball_pos_x, screen_height // 2 + y - ball_pos_y))
        else:
            pygame.draw.line(screen, (255,0,0),
                             (screen_width // 2 + x - ball_pos_x, screen_height // 2 - y - ball_pos_y),
                             (screen_width // 2 - x - ball_pos_x, screen_height // 2 + y - ball_pos_y))

    # Draw the ball
    pygame.draw.circle(screen, (255,0,0),
                       (int(ball_pos_x) + int(ball_radius), int(ball_pos_y) + int(ball_radius)), ball_radius)

    pygame.display.flip()
    clock.tick(60)