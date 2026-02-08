import os

WIDTH, HEIGHT = 1000, 800
FPS = 60

HOME_BG = (245, 235, 225)
HOME_TEXT = (80, 70, 60)
CARD_BG = (235, 220, 205)
CARD_BORDER = (200, 185, 170)
SHADOW = (0, 0, 0, 30)


MODE_COLORS = {
    1: {  
        'bg': (232, 230, 242),
        'circle': (150, 140, 180),
        'aura': (180, 170, 210),
        'particle': (200, 190, 225),
        'text': (90, 80, 120)
    },
    2: { 
        'bg': (245, 238, 232),
        'circle': (200, 130, 100),
        'aura': (230, 160, 130),
        'particle': (240, 190, 170),
        'text': (120, 70, 50)
    },
    3: {  
        'bg': (235, 242, 240),
        'circle': (120, 170, 165),
        'aura': (160, 200, 195),
        'particle': (190, 220, 215),
        'text': (70, 110, 105)
    },
    4: { 
        'bg': (245, 242, 235),
        'circle': (190, 160, 120),
        'aura': (220, 190, 150),
        'particle': (235, 215, 185),
        'text': (110, 90, 60)
    }
}

PATTERNS = {
    1: [4, 4, 8, 0],
    2: [4, 4, 6, 0],
    3: [4, 7, 8, 0],
    4: [4, 4, 4, 4]
}

PATTERN_NAMES = {
    1: "Sleep Mode",
    2: "Anger Relief",
    3: "Anxiety Relief",
    4: "Meditation Preparation"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODE_MUSIC = {
    1: os.path.join(BASE_DIR, "assets", "music", "sleep.mp3"),
    2: os.path.join(BASE_DIR, "assets", "music", "anger.mp3"),
    3: os.path.join(BASE_DIR, "assets", "music", "anxiety.mp3"),
    4: os.path.join(BASE_DIR, "assets", "music", "meditation.mp3"),
}
