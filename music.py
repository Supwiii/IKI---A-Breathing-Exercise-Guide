import os
import pygame
from config import MODE_MUSIC

MUSIC_END_EVENT = pygame.USEREVENT + 1

_current_music_path = None
_current_music_volume = 0.9


def music_play(mode, volume=0.9):
    
    global _current_music_path, _current_music_volume

    path = MODE_MUSIC.get(mode)
    if not path:
        return
    if not os.path.exists(path):
        print(f"[MUSIC ERROR] File not found: {path}")
        return

    _current_music_path = path
    _current_music_volume = volume

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(0)
        print("[MUSIC] Playing (manual loop):", path)
    except pygame.error as e:
        print(f"[MUSIC ERROR] {path} -> {e}")


def music_restart():
    

    if not _current_music_path:
        return
    try:
        pygame.mixer.music.play(0)
    except pygame.error:
        try:
            pygame.mixer.music.load(_current_music_path)
            pygame.mixer.music.set_volume(_current_music_volume)
            pygame.mixer.music.play(0)
        except pygame.error as e:
            print("[MUSIC ERROR] restart failed:", e)


def music_stop():
    
    global _current_music_path
    _current_music_path = None
    try:
        pygame.mixer.music.set_endevent()
        pygame.mixer.music.stop()
    except pygame.error:
        pass