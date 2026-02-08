import pygame
from config import *

def clamp(x, a, b):
    return max(a, min(b, x))

def lerp(a, b, t):
    return a + (b - a) * t

class HomeButton:
    def __init__(self, rect, text, mode_index):
        self.base = pygame.Rect(rect)
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.SysFont("arial", 26)
        self.mode_index = mode_index
        self.scale = 1.0
        self.hover = False

    def update(self, mouse, dt):
        self.hover = self.base.collidepoint(mouse)
        target = 1.02 if self.hover else 1.0
        self.scale = lerp(self.scale, target, clamp(dt * 12, 0, 1))
        self.rect.size = (int(self.base.w * self.scale), int(self.base.h * self.scale))
        self.rect.center = self.base.center

    def draw(self, screen):
        shadow_offset = 4
        shadow_rect = pygame.Rect(self.rect.x + shadow_offset, self.rect.y + shadow_offset, self.rect.w, self.rect.h)
        sh = pygame.Surface((shadow_rect.w, shadow_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(sh, SHADOW, (0, 0, shadow_rect.w, shadow_rect.h), border_radius=12)
        screen.blit(sh, shadow_rect.topleft)

        pygame.draw.rect(screen, CARD_BG, self.rect, border_radius=12)
        pygame.draw.rect(screen, CARD_BORDER, self.rect, width=2, border_radius=12)

        label = self.font.render(self.text, True, HOME_TEXT)
        screen.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))

    def clicked(self, e):
        return e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos)

class BackButton:
    def __init__(self):
        self.base = pygame.Rect(30, 30, 50, 50)
        self.rect = pygame.Rect(30, 30, 50, 50)
        self.text = "←"
        self.font = pygame.font.SysFont("arial", 32, bold=True)
        self.scale = 1.0
        self.hover = False

    def update(self, mouse, dt):
        self.hover = self.base.collidepoint(mouse)
        target = 1.05 if self.hover else 1.0
        self.scale = lerp(self.scale, target, clamp(dt * 12, 0, 1))
        self.rect.size = (int(self.base.w * self.scale), int(self.base.h * self.scale))
        self.rect.center = self.base.center

    def draw(self, screen, text_color):
        s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        bg_alpha = 180 if self.hover else 120
        pygame.draw.rect(s, (255, 255, 255, bg_alpha), (0, 0, self.rect.w, self.rect.h), border_radius=8)
        pygame.draw.rect(s, (*text_color, 150), (0, 0, self.rect.w, self.rect.h), width=2, border_radius=8)
        screen.blit(s, self.rect.topleft)

        label = self.font.render(self.text, True, text_color)
        screen.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))

    def clicked(self, e):
        return e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos)

def create_buttons():
    bw, bh = 640, 72
    cx = WIDTH // 2
    start_y = 245
    gap = 20

    labels = [
        "Sleep Mode",
        "Anger Relief Mode",
        "Anxiety Relief Mode",
        "Meditation Preparation Mode",
    ]
    return [HomeButton((cx - bw // 2, start_y + i * (bh + gap), bw, bh), labels[i], i + 1) for i in range(4)]

def draw_home(screen, mouse, dt, buttons):
    screen.fill(HOME_BG)

    title_font_names = ["segoe script", "gabriola", "comic sans ms"]
    available = {f.lower(): f for f in pygame.font.get_fonts()}
    title_font = None
    for name in title_font_names:
        key = name.lower().replace(" ", "")
        for av in available:
            if key in av:
                title_font = pygame.font.SysFont(available[av], 74)
                break
        if title_font:
            break
    if not title_font:
        title_font = pygame.font.SysFont(None, 74)

    title = title_font.render("Iki", True, HOME_TEXT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 105))

   
    for b in buttons:
        b.update(mouse, dt)
        b.draw(screen)

    hint_font = pygame.font.SysFont(None, 22)
    hint = hint_font.render("Click a mode or press 1–4 (ESC to quit)", True, (140, 120, 100))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 70))
