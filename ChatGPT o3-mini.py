import pygame
import math
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Red Ball")
clock = pygame.time.Clock()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# ----------------------------
# Hexagon parameters
# ----------------------------
hex_center = (WIDTH // 2, HEIGHT // 2)
hex_radius = 250           # distance from center to vertex
num_sides = 6              # hexagon has 6 sides
hex_angle = 0              # current rotation angle (in radians)
hex_angular_velocity = 0.01  # radians per frame

# ----------------------------
# Ball parameters
# ----------------------------
ball_radius = 15
# Start the ball somewhere inside the hexagon.
ball_pos = [hex_center[0] + 100, hex_center[1] - 50]
ball_vel = [3, -5]         # initial velocity (pixels per frame)
gravity = 0.5              # gravitational acceleration (pixels per frame²)
restitution = 0.9          # bounce coefficient (1 = elastic bounce)

# ----------------------------
# Helper functions
# ----------------------------

def closest_point_on_segment(p, a, b):
    """
    Given point p and segment defined by endpoints a and b,
    return the closest point on the segment to p.
    """
    ax, ay = a
    bx, by = b
    px, py = p
    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay
    ab_len_sq = abx * abx + aby * aby
    if ab_len_sq == 0:
        return a
    # Compute the projection factor (clamped between 0 and 1)
    t = (apx * abx + apy * aby) / ab_len_sq
    t = max(0, min(1, t))
    return (ax + t * abx, ay + t * aby)

def get_hexagon_vertices(center, radius, angle_offset):
    """
    Compute the vertices of a regular polygon (hexagon) centered at 'center',
    with the given 'radius' and rotated by 'angle_offset' radians.
    """
    cx, cy = center
    vertices = []
    for i in range(num_sides):
        angle = (2 * math.pi * i / num_sides) + angle_offset
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

# ----------------------------
# Main loop
# ----------------------------
running = True
while running:
    dt = clock.tick(60)  # Aim for 60 FPS

    # Process events (quit when the window is closed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the hexagon’s rotation angle
    hex_angle += hex_angular_velocity
    vertices = get_hexagon_vertices(hex_center, hex_radius, hex_angle)

    # ----------------------------
    # Update ball physics
    # ----------------------------
    # Apply gravity (increases downward velocity)
    ball_vel[1] += gravity
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # ----------------------------
    # Collision detection and resolution
    # ----------------------------
    # Because the hexagon is convex, we check the ball against each edge.
    # If the distance from the ball’s center to an edge is less than ball_radius,
    # we have a collision.
    #
    # Note: Since the hexagon is rotating, the wall has an instantaneous velocity.
    # We approximate that by computing the velocity at the contact point.
    # The collision response reflects the ball’s velocity relative to the wall.
    for _ in range(3):  # Do several iterations to resolve multiple collisions
        collision_occurred = False
        for i in range(num_sides):
            a = vertices[i]
            b = vertices[(i + 1) % num_sides]
            closest = closest_point_on_segment(ball_pos, a, b)
            dx = ball_pos[0] - closest[0]
            dy = ball_pos[1] - closest[1]
            dist = math.hypot(dx, dy)
            if dist < ball_radius:
                collision_occurred = True
                # Compute the collision normal.
                # If the ball center is exactly at the closest point, use the edge’s perpendicular.
                if dist == 0:
                    edge_dx = b[0] - a[0]
                    edge_dy = b[1] - a[1]
                    # Choose one of the perpendicular directions.
                    n = (-edge_dy, edge_dx)
                    n_len = math.hypot(n[0], n[1])
                    normal = (n[0] / n_len, n[1] / n_len)
                else:
                    normal = (dx / dist, dy / dist)

                # Reposition the ball so it’s no longer intersecting.
                penetration = ball_radius - dist
                ball_pos[0] += normal[0] * penetration
                ball_pos[1] += normal[1] * penetration

                # Compute the wall velocity at the contact point.
                # Since the hexagon rotates about its center,
                # the instantaneous velocity at any point p is:
                #    v_wall = omega x (p - center)
                # In 2D, this is computed as:
                wx = -hex_angular_velocity * (closest[1] - hex_center[1])
                wy =  hex_angular_velocity * (closest[0] - hex_center[0])
                wall_velocity = (wx, wy)

                # Compute the relative velocity of the ball to the wall.
                rel_vel = (ball_vel[0] - wall_velocity[0],
                           ball_vel[1] - wall_velocity[1])
                # Only resolve if the ball is moving into the wall.
                rel_dot_n = rel_vel[0] * normal[0] + rel_vel[1] * normal[1]
                if rel_dot_n < 0:
                    # Reflect the relative velocity using the restitution coefficient.
                    # v' = v_rel - (1 + restitution) * (v_rel · n) * n
                    new_rel_vel = (rel_vel[0] - (1 + restitution) * rel_dot_n * normal[0],
                                   rel_vel[1] - (1 + restitution) * rel_dot_n * normal[1])
                    # The new ball velocity is the wall velocity plus the new relative velocity.
                    ball_vel[0] = new_rel_vel[0] + wall_velocity[0]
                    ball_vel[1] = new_rel_vel[1] + wall_velocity[1]
                break  # Break out to recheck collisions after adjusting
        if not collision_occurred:
            break

    # ----------------------------
    # Rendering
    # ----------------------------
    screen.fill(BLACK)
    # Draw the hexagon (white outline)
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    # Draw the red ball (filled circle)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.display.flip()

pygame.quit()
sys.exit()
