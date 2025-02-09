import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon parameters
HEXAGON_RADIUS = 150
HEXAGON_LINE_WIDTH = 3
HEXAGON_COLOR = BLUE
HEXAGON_CENTER = (WIDTH // 2, HEIGHT // 2)
HEXAGON_ROTATION_SPEED = 0.5  # degrees per frame
HEXAGON_ROTATION_DIRECTION = 1 # 1 for clockwise, -1 for counterclockwise

# Ball parameters
BALL_RADIUS = 20
BALL_COLOR = RED
BALL_START_X = WIDTH // 2
BALL_START_Y = HEIGHT // 2
BALL_MASS = 1  # Adjust for realistic bounce
BALL_RESTITUTION = 0.8  # Adjust for bounce damping (0 to 1)
GRAVITY = 0.5  # Adjust for gravity strength

# Ball initial state
ball_x = BALL_START_X
ball_y = BALL_START_Y
ball_velocity_x = random.uniform(-5, 5)
ball_velocity_y = random.uniform(-5, 5)

# Rotation angle
hexagon_angle = 0

def calculate_hexagon_points(center_x, center_y, radius, angle):
    """Calculates the vertices of a hexagon based on center, radius, and rotation."""
    points = []
    for i in range(6):
        angle_rad = math.radians(angle + i * 60)  # 60 degrees between vertices
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

def is_point_inside_hexagon(x, y, hexagon_points):
    """Determines if a point is inside a hexagon using the winding number algorithm."""
    winding_number = 0
    for i in range(len(hexagon_points)):
        x1, y1 = hexagon_points[i]
        x2, y2 = hexagon_points[(i + 1) % len(hexagon_points)]

        if y1 <= y:
            if y2 > y:
                if (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) > 0:
                    winding_number += 1
        else:
            if y2 <= y:
                if (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) < 0:
                    winding_number -= 1

    return winding_number != 0


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_a:
                HEXAGON_ROTATION_DIRECTION = -1  # Counterclockwise
            if event.key == pygame.K_d:
                HEXAGON_ROTATION_DIRECTION = 1   # Clockwise
            if event.key == pygame.K_UP:
                HEXAGON_ROTATION_SPEED += 0.1
                print(f"Hexagon Rotation Speed: {HEXAGON_ROTATION_SPEED}")
            if event.key == pygame.K_DOWN:
                HEXAGON_ROTATION_SPEED = max(0, HEXAGON_ROTATION_SPEED - 0.1)  # Prevent negative speed
                print(f"Hexagon Rotation Speed: {HEXAGON_ROTATION_SPEED}")
            if event.key == pygame.K_SPACE:
                # Add random force to the ball
                angle = random.uniform(0, 2 * math.pi) #Random angle
                force = random.uniform(5, 15) # Random force magnitude
                ball_velocity_x += force * math.cos(angle)
                ball_velocity_y += force * math.sin(angle)


    # Update game state

    # Rotate the hexagon
    hexagon_angle += HEXAGON_ROTATION_SPEED * HEXAGON_ROTATION_DIRECTION

    # Calculate hexagon vertices
    hexagon_points = calculate_hexagon_points(
        HEXAGON_CENTER[0], HEXAGON_CENTER[1], HEXAGON_RADIUS, hexagon_angle
    )

    # Apply gravity to the ball
    ball_velocity_y += GRAVITY

    # Update ball position
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Collision detection and response (Hexagon edges)
    for i in range(len(hexagon_points)):
        x1, y1 = hexagon_points[i]
        x2, y2 = hexagon_points[(i + 1) % len(hexagon_points)]

        # Calculate distance from ball center to the line segment
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:  # Handle case where points are the same
            continue # skip to next point
        t = ((ball_x - x1) * dx + (ball_y - y1) * dy) / (dx * dx + dy * dy)

        # Clamp t to the range [0, 1] to find the closest point on the segment
        t = max(0, min(1, t))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        distance = math.sqrt((ball_x - closest_x) ** 2 + (ball_y - closest_y) ** 2)

        if distance <= BALL_RADIUS:
            # Collision detected!
            # Calculate normal vector (perpendicular to the line)
            normal_x = -(y2 - y1)
            normal_y = dx

            # Normalize the normal vector
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            normal_x /= normal_length
            normal_y /= normal_length

            # Calculate relative velocity
            relative_velocity_x = ball_velocity_x
            relative_velocity_y = ball_velocity_y

            # Calculate dot product of relative velocity and normal vector
            dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

            # Calculate impulse (change in momentum)
            impulse = (1 + BALL_RESTITUTION) * dot_product * BALL_MASS

            # Update ball velocity
            ball_velocity_x -= impulse * normal_x / BALL_MASS
            ball_velocity_y -= impulse * normal_y / BALL_MASS

            # Move the ball slightly out of the collision to prevent sticking
            ball_x += normal_x * (BALL_RADIUS - distance)
            ball_y += normal_y * (BALL_RADIUS - distance)

    # Keep the ball inside the hexagon
    if not is_point_inside_hexagon(ball_x, ball_y, hexagon_points):
        # Calculate the closest point on the hexagon to the ball
        min_distance = float('inf')
        closest_point = None
        for i in range(len(hexagon_points)):
            x1, y1 = hexagon_points[i]
            x2, y2 = hexagon_points[(i + 1) % len(hexagon_points)]

            dx = x2 - x1
            dy = y2 - y1
            if dx == 0 and dy == 0:
                continue
            t = ((ball_x - x1) * dx + (ball_y - y1) * dy) / (dx * dx + dy * dy)
            t = max(0, min(1, t))
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy
            distance = math.sqrt((ball_x - closest_x) ** 2 + (ball_y - closest_y) ** 2)

            if distance < min_distance:
                min_distance = distance
                closest_point = (closest_x, closest_y)


        if closest_point:
            closest_x, closest_y = closest_point
            # Calculate the normal vector from the closest point on the hexagon to the ball
            normal_x = ball_x - closest_x
            normal_y = ball_y - closest_y

            # Normalize the normal vector
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            if normal_length > 0: # avoid division by zero
                normal_x /= normal_length
                normal_y /= normal_length

                # Reflect the ball's velocity around the normal
                dot_product = ball_velocity_x * normal_x + ball_velocity_y * normal_y
                ball_velocity_x -= 2 * dot_product * normal_x
                ball_velocity_y -= 2 * dot_product * normal_y

                # Move the ball slightly inside the hexagon
                ball_x = closest_x + normal_x * BALL_RADIUS
                ball_y = closest_y + normal_y * BALL_RADIUS


    # Clear the screen
    screen.fill(WHITE)

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