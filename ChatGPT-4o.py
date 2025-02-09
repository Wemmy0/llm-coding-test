import pygame
import math
import sys

# Initialize pygame and set up the window.
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

# --- Parameters ---

# Hexagon (container) parameters
hex_center = (width / 2, height / 2)
hex_radius = 250               # distance from center to a vertex
hex_angle = 0.0                # starting rotation angle (radians)
hex_angular_velocity = 0.5     # constant rotation speed (radians per second)

# Ball parameters
ball_radius = 15
ball_pos = [hex_center[0], hex_center[1] - 100]  # initial ball position (inside the hexagon)
ball_vel = [200.0, 0.0]        # initial velocity (pixels per second)

# Gravity (pixels per second squared, downward)
# Gravity increased for a stronger effect:
gravity = 1000.0

# --- Helper functions ---

def get_hexagon_vertices(center, radius, angle_offset):
    """
    Compute the vertices of a regular hexagon centered at 'center' with the given radius.
    The hexagon is rotated by angle_offset (in radians).
    """
    vertices = []
    cx, cy = center
    for i in range(6):
        angle = angle_offset + math.radians(60 * i)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def point_line_closest_point(P, A, B):
    """
    Given point P and segment AB, return the closest point on AB to P.
    P, A, B are (x,y) tuples.
    """
    Ax, Ay = A
    Bx, By = B
    Px, Py = P
    ABx = Bx - Ax
    ABy = By - Ay
    # Compute t along AB for the projection of P onto the line
    t = ((Px - Ax) * ABx + (Py - Ay) * ABy) / (ABx * ABx + ABy * ABy)
    t = max(0.0, min(1.0, t))  # clamp t so that the point lies on the segment
    closest = (Ax + t * ABx, Ay + t * ABy)
    return closest

def vector_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def vector_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def vector_mul(a, scalar):
    return (a[0] * scalar, a[1] * scalar)

def vector_dot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def vector_length(a):
    return math.sqrt(a[0]*a[0] + a[1]*a[1])

def vector_normalize(a):
    length = vector_length(a)
    if length == 0:
        return (0, 0)
    return (a[0] / length, a[1] / length)

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds elapsed since last frame

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update Hexagon Rotation ---
    hex_angle += hex_angular_velocity * dt
    hex_vertices = get_hexagon_vertices(hex_center, hex_radius, hex_angle)

    # --- Update Ball Physics ---
    # Apply gravity (increasing downward velocity)
    ball_vel[1] += gravity * dt
    # Update ball position using its velocity
    ball_pos[0] += ball_vel[0] * dt
    ball_pos[1] += ball_vel[1] * dt

    # --- Collision Detection and Response ---
    # For each hexagon edge, check for collision with the ball.
    for i in range(6):
        A = hex_vertices[i]
        B = hex_vertices[(i + 1) % 6]
        # Find the closest point on this edge to the ball center.
        closest = point_line_closest_point(ball_pos, A, B)
        # Compute distance from ball center to this point.
        dx = ball_pos[0] - closest[0]
        dy = ball_pos[1] - closest[1]
        dist = math.hypot(dx, dy)
        if dist < ball_radius:
            # --- Collision has occurred ---
            # Compute the collision normal.
            if dist == 0:
                # In the unlikely event of a zero distance, use the edge’s perpendicular.
                edge_vec = vector_sub(B, A)
                normal = vector_normalize((-edge_vec[1], edge_vec[0]))
            else:
                normal = (dx / dist, dy / dist)

            # Compute the velocity of the wall at the collision point.
            # For a rigid rotation about hex_center, any point p has velocity:
            #   u = ω × (p - center)
            # (For counterclockwise rotation, u = (-ω*(p_y - cy), ω*(p_x - cx)))
            rel_x = closest[0] - hex_center[0]
            rel_y = closest[1] - hex_center[1]
            wall_velocity = (-hex_angular_velocity * rel_y, hex_angular_velocity * rel_x)

            # Compute the ball's velocity relative to the moving wall.
            rel_vel = (ball_vel[0] - wall_velocity[0], ball_vel[1] - wall_velocity[1])
            # Only respond if the ball is moving toward the wall.
            if vector_dot(rel_vel, normal) < 0:
                # Reflect the relative velocity about the normal:
                dot = vector_dot(rel_vel, normal)
                rel_vel_reflected = (rel_vel[0] - 2 * dot * normal[0],
                                     rel_vel[1] - 2 * dot * normal[1])
                # The new ball velocity is the reflected relative velocity plus the wall’s velocity.
                ball_vel = [wall_velocity[0] + rel_vel_reflected[0],
                            wall_velocity[1] + rel_vel_reflected[1]]
                # Re-position the ball so it is just touching the wall.
                penetration = ball_radius - dist
                ball_pos[0] += normal[0] * penetration
                ball_pos[1] += normal[1] * penetration

    # --- Drawing ---
    screen.fill((0, 0, 0))  # Clear the screen with black.
    # Draw the rotating hexagon (using a white outline).
    pygame.draw.polygon(screen, (255, 255, 255), hex_vertices, 3)
    # Draw the red ball.
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.display.flip()

pygame.quit()
sys.exit()
