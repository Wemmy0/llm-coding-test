import pygame
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
HEXAGON_SIZE = 150
BALL_RADIUS = 15
GRAVITY = 0.5  # Adjust for strength of gravity
BOUNCE_DAMPING = 0.8  # Energy loss on bounce (0.0 - 1.0)
ROTATION_SPEED = 0.02  # Radians per frame

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# --- Helper Functions ---

def rotate_point(point, angle, center=(WIDTH // 2, HEIGHT // 2)):
    """Rotates a point around a center point."""
    x, y = point
    cx, cy = center
    rotated_x = (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle) + cx
    rotated_y = (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle) + cy
    return rotated_x, rotated_y

def hexagon_vertices(size, center=(WIDTH // 2, HEIGHT // 2)):
    """Calculates the vertices of a regular hexagon."""
    cx, cy = center
    vertices = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)
        vertices.append((x, y))
    return vertices

def point_on_line(p1, p2, x):
    """Finds the y-coordinate of a point on a line given its x-coordinate.
       Handles vertical lines correctly."""
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:  # Vertical line
        if min(y1, y2) <= p1[1] <= max(y1,y2):
            return p1[1]  # Return the y-coordinate of the point (they're the same)
        else:
            return None # No point on the line

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m * x + b

def distance(p1, p2):
    """Calculates the distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_point_on_line(p1, p2, ball_center):
    """Finds the closest point on a line segment to a given point (the ball)."""
    x1, y1 = p1
    x2, y2 = p2
    bx, by = ball_center

    # Calculate the vector from p1 to p2
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:  # p1 and p2 are the same point
        return p1

    # Parameterize the line segment:  P = p1 + t * (p2 - p1)
    # Find t that minimizes the distance between P and the ball center.
    t = ((bx - x1) * dx + (by - y1) * dy) / (dx**2 + dy**2)

    # Clamp t to be between 0 and 1 (to stay within the line segment)
    t = max(0, min(1, t))

    # Calculate the closest point on the line segment
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return closest_x, closest_y



# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

# --- Ball Initial State ---
ball_x = WIDTH // 2
ball_y = HEIGHT // 2 - HEXAGON_SIZE + BALL_RADIUS + 10 #start just inside the top
ball_vx = 2  # Initial horizontal velocity
ball_vy = 0  # Initial vertical velocity

# --- Hexagon Rotation ---
angle = 0

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update ---
    # 1. Update Ball Position (Physics)
    ball_vy += GRAVITY
    ball_x += ball_vx
    ball_y += ball_vy


    # 2. Update Hexagon Rotation
    angle += ROTATION_SPEED
    rotated_vertices = [rotate_point(v, angle) for v in hexagon_vertices(HEXAGON_SIZE)]

    # 3. Collision Detection with Hexagon
    for i in range(6):
        p1 = rotated_vertices[i]
        p2 = rotated_vertices[(i + 1) % 6]  # Wrap around to the first vertex

        closest_point = closest_point_on_line(p1, p2, (ball_x, ball_y))
        dist = distance(closest_point, (ball_x, ball_y))

        if dist <= BALL_RADIUS:
            # Collision detected!  Calculate the normal vector.
            normal_x = ball_x - closest_point[0]
            normal_y = ball_y - closest_point[1]
            normal_length = math.sqrt(normal_x**2 + normal_y**2)

            if normal_length > 0: # Avoid division by zero.
                normal_x /= normal_length
                normal_y /= normal_length
            else:
                # If the ball is exactly *on* the closest point,
                # we need a fallback.  Use the line's perpendicular.
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                normal_x = -dy
                normal_y = dx
                normal_length = math.sqrt(normal_x**2 + normal_y**2)
                if normal_length > 0:
                    normal_x /= normal_length
                    normal_y /= normal_length
                else:
                    # Extremely unlikely, but handle the case where p1 == p2
                    normal_x = 0
                    normal_y = 1 # Arbitrary default


            # Project the velocity onto the normal vector
            dot_product = ball_vx * normal_x + ball_vy * normal_y

            # Reflect the velocity across the normal
            ball_vx -= 2 * dot_product * normal_x * BOUNCE_DAMPING
            ball_vy -= 2 * dot_product * normal_y * BOUNCE_DAMPING

            # Move the ball out of the hexagon to prevent sticking
            overlap = BALL_RADIUS - dist
            ball_x += normal_x * overlap
            ball_y += normal_y * overlap

    # --- Draw ---
    screen.fill(BLACK)

    # Draw Hexagon
    pygame.draw.polygon(screen, WHITE, rotated_vertices, 2)

    # Draw Ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), BALL_RADIUS)

    pygame.display.flip()

    # --- Tick ---
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
