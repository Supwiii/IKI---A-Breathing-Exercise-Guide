import pygame
import math
import random

def lerp(a, b, t):
    return a + (b - a) * t

def _soft_lighten(rgb, k=0.18):
    return tuple(min(255, int(c + (255 - c) * k)) for c in rgb)

def _soft_darken(rgb, k=0.12):
    return tuple(max(0, int(c * (1 - k))) for c in rgb)

_BG_STARS = None

def _init_bg_stars(size, n=160):
    global _BG_STARS
    if _BG_STARS is not None:
        return _BG_STARS

    w, h = size
    stars = []
    for _ in range(n):
        x = random.uniform(0, w)
        y = random.uniform(0, h)
        r = random.choice([1, 1, 1, 2])
        a = random.randint(14, 34)
        sp = random.uniform(8, 22)
        stars.append([x, y, r, a, sp])
    _BG_STARS = stars
    return _BG_STARS

def draw_bg_gradient(screen, base_rgb):
    w, h = screen.get_size()
    top = tuple(min(255, int(c * 1.06) + 6) for c in base_rgb)
    bot = tuple(max(0, int(c * 0.92) - 6) for c in base_rgb)

    for y in range(h):
        t = y / (h - 1)
        r = int(lerp(top[0], bot[0], t))
        g = int(lerp(top[1], bot[1], t))
        b = int(lerp(top[2], bot[2], t))
        pygame.draw.line(screen, (r, g, b), (0, y), (w, y))

def draw_radial_spotlight(screen, center, color, radius):
    cx, cy = center
    w, h = screen.get_size()
    s = pygame.Surface((w, h), pygame.SRCALPHA)

    for mul, alpha in [(2.0, 28), (1.4, 45), (1.0, 70)]:
        rr = int(radius * mul)
        pygame.draw.circle(s, (*color, alpha), (cx, cy), rr)

    screen.blit(s, (0, 0))

def draw_glowy_polyline(screen, points, rgb, base_alpha, thickness):
    w, h = screen.get_size()
    s = pygame.Surface((w, h), pygame.SRCALPHA)

    pygame.draw.lines(s, (*rgb, max(0, base_alpha // 3)), False, points, thickness + 6)
    pygame.draw.lines(s, (*rgb, max(0, base_alpha // 2)), False, points, thickness + 3)
    pygame.draw.lines(s, (*rgb, base_alpha), False, points, thickness)

    screen.blit(s, (0, 0))

def draw_soft_blobs(screen, c1, c2, t):
    w, h = screen.get_size()
    s = pygame.Surface((w, h), pygame.SRCALPHA)

    c1a = _soft_lighten(c1, 0.12)
    c2a = _soft_lighten(c2, 0.08)
    c1b = _soft_darken(c1, 0.06)
    c2b = _soft_darken(c2, 0.08)

    blobs = [
        (w * 0.20 + math.sin(t * 0.22) * 110, h * 0.26 + math.cos(t * 0.20) * 85, 310, c1a, 34),
        (w * 0.82 + math.cos(t * 0.21) * 120, h * 0.28 + math.sin(t * 0.23) * 80, 360, c2a, 28),
        (w * 0.58 + math.sin(t * 0.17) * 90,  h * 0.82 + math.cos(t * 0.19) * 105, 330, c1b, 22),
        (w * 0.36 + math.cos(t * 0.19) * 80,  h * 0.60 + math.sin(t * 0.18) * 70, 260, c2b, 18),
    ]

    for x, y, r, col, a in blobs:
        pygame.draw.circle(s, (*col, a), (int(x), int(y)), int(r))
        pygame.draw.circle(s, (*col, int(a * 1.25)), (int(x), int(y)), int(r * 0.72))
        pygame.draw.circle(s, (*col, int(a * 1.55)), (int(x), int(y)), int(r * 0.45))

    screen.blit(s, (0, 0))

def draw_bg_drift_dots(screen, dot_color, t):
    w, h = screen.get_size()
    stars = _init_bg_stars((w, h), n=160)

    s = pygame.Surface((w, h), pygame.SRCALPHA)
    dx = math.sin(t * 0.25) * 12
    dy = math.cos(t * 0.22) * 10

    for st in stars:
        st[1] -= st[4] * 1.0
        if st[1] < -20:
            st[1] = h + 20
            st[0] = random.uniform(0, w)

        x = st[0] + dx
        y = st[1] + dy
        r = st[2]
        a = st[3]
        pygame.draw.circle(s, (*dot_color, a), (int(x), int(y)), r)

    screen.blit(s, (0, 0))

def draw_mode_decor(screen, colors, t):
    draw_soft_blobs(screen, colors['aura'], colors['particle'], t)
    draw_bg_drift_dots(screen, colors['particle'], t)

    w, _ = screen.get_size()
    top = pygame.Surface((w, 170), pygame.SRCALPHA)
    for y in range(170):
        a = int(28 * (1 - y / 169))
        pygame.draw.line(top, (0, 0, 0, a), (0, y), (w, y))
    screen.blit(top, (0, 0))
