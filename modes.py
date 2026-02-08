import pygame
import math
from config import *
from bg import lerp, draw_glowy_polyline

class Particle:
    def __init__(self, x, y, angle, speed, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.life = 1.0
        self.size = 4

    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt * 60
        self.y += math.sin(self.angle) * self.speed * dt * 60
        self.life -= dt * 0.8

    def draw(self, screen):
        if self.life > 0:
            alpha = int(self.life * 180)
            size = int(self.size * self.life)
            s = pygame.Surface((size * 2 + 4, size * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (size + 2, size + 2), size)
            screen.blit(s, (int(self.x - size - 2), int(self.y - size - 2)))

class BreathingController:
    def __init__(self, mode):
        self.mode = mode
        self.pattern = PATTERNS[mode]
        self.colors = MODE_COLORS[mode]
        self.phase = 0
        self.time = 0
        self.radius = 60
        self.target_radius = 60
        self.particles = []
        self.rotation = 0
        self.glow_intensity = 0

        self.phase_durations = self.pattern
        self.total_time = sum(self.pattern) if sum(self.pattern) > 0 else 1

    def update(self, dt):
        self.time += dt

        elapsed = self.time % self.total_time
        cumulative = 0
        phase_progress = 0.0
        for i, duration in enumerate(self.phase_durations):
            if duration <= 0:
                cumulative += duration
                continue
            if elapsed < cumulative + duration:
                self.phase = i
                phase_progress = (elapsed - cumulative) / duration
                break
            cumulative += duration

        if self.phase == 0:  
            self.target_radius = lerp(60, 120, phase_progress)
            self.glow_intensity = phase_progress * 0.8
        elif self.phase == 1: 
            self.target_radius = 120
            self.glow_intensity = 0.8
        elif self.phase == 2: 
            self.target_radius = lerp(120, 60, phase_progress)
            self.glow_intensity = 0.8 - phase_progress * 0.6
        else:  
            self.target_radius = 60
            self.glow_intensity = 0.2

        self.radius = lerp(self.radius, self.target_radius, dt * 4)
        self.rotation += dt * 15

        if self.phase == 0 and phase_progress > 0.1:
            if len(self.particles) < 20:
                angle = math.radians(self.rotation * 2 + len(self.particles) * 18)
                self.particles.append(Particle(WIDTH // 2, HEIGHT // 2, angle, 1.5, self.colors['particle']))

        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        cx, cy = WIDTH // 2, HEIGHT // 2

     
        for p in self.particles:
            p.draw(screen)

        
        num_aura_layers = 8
        for layer in range(num_aura_layers):
            aura_radius = self.radius + 40 + layer * 15
            points = []
            num_points = 60
            for i in range(num_points + 1):
                angle = (i / num_points) * 2 * math.pi
                wave1 = math.sin(angle * 3 + self.rotation * 0.03 + layer * 0.5) * 8
                wave2 = math.cos(angle * 5 - self.rotation * 0.02 + layer * 0.3) * 5
                wave3 = math.sin(angle * 2 + self.rotation * 0.025) * 4
                current_radius = aura_radius + (wave1 + wave2 + wave3)
                x = cx + math.cos(angle) * current_radius
                y = cy + math.sin(angle) * current_radius
                points.append((x, y))

            alpha = int(40 - layer * 4 + self.glow_intensity * 30)
            if alpha > 0:
                draw_glowy_polyline(screen, points, self.colors['aura'], alpha, 2)

        
        for i in range(int(self.radius), 0, -3):
            t = i / self.radius
            color = tuple(int(lerp(self.colors['circle'][j] * 1.2, self.colors['circle'][j], t)) for j in range(3))
            alpha = int(180 + self.glow_intensity * 75)
            s = pygame.Surface((i * 2 + 4, i * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, alpha), (i + 2, i + 2), i)
            screen.blit(s, (cx - i - 2, cy - i - 2))

        pygame.draw.circle(screen, self.colors['circle'], (cx, cy), int(self.radius), 3)

       
        inner_glow_radius = int(self.radius * 0.7)
        for i in range(4):
            glow_r = inner_glow_radius - i * 10
            if glow_r > 0:
                alpha = int(60 - i * 12 + self.glow_intensity * 40)
                s = pygame.Surface((glow_r * 2 + 10, glow_r * 2 + 10), pygame.SRCALPHA)
                lighter_color = tuple(min(255, int(c * 1.3)) for c in self.colors['aura'])
                pygame.draw.circle(s, (*lighter_color, alpha), (glow_r + 5, glow_r + 5), glow_r)
                screen.blit(s, (cx - glow_r - 5, cy - glow_r - 5))

        
        phase_texts = ["INHALE", "HOLD", "EXHALE", "HOLD"]
        if self.phase_durations[self.phase] > 0:
            font = pygame.font.SysFont("arial", 36, bold=True)
            text = font.render(phase_texts[self.phase], True, self.colors['text'])
            screen.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))

       
        elapsed = self.time % self.total_time
        cumulative = sum(self.phase_durations[:self.phase])
        remaining = self.phase_durations[self.phase] - (elapsed - cumulative)
        if remaining > 0 and self.phase_durations[self.phase] > 0:
            count_font = pygame.font.SysFont("arial", 24)
            count_text = count_font.render(f"{int(remaining) + 1}", True, self.colors['text'])
            screen.blit(count_text, (cx - count_text.get_width() // 2, cy + 35))
