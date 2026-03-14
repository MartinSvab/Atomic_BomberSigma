import os
import pygame

sounds = {}
music_tracks = {}
channels = {}

_SOUND_VOLUME_DEFAULT = 0.5
_MUSIC_VOLUME_DEFAULT = 0.35


def initialize_audio():
    """
    Initialize mixer once.
    Call this before loading sounds.
    """
    if pygame.mixer.get_init() is None:
        pygame.mixer.init()


def initialize_sounds():
    """
    Load all short sound effects and register music tracks.
    """
    initialize_audio()

    path_to_sounds = "../audio/sounds/"
    path_to_music = "../audio/music/"

    # ---- sound effects ----
    sound_files = {
        "button_click": "button_click.wav",
        "bomb_place": "bomb_place.wav",
        "explosion": "explosion.wav",
        "pickup": "pickup.wav",
        "player_death": "player_death.wav",
    }

    for sound_name, filename in sound_files.items():
        full_path = os.path.join(path_to_sounds, filename)
        if os.path.exists(full_path):
            sounds[sound_name] = pygame.mixer.Sound(full_path)
            sounds[sound_name].set_volume(_SOUND_VOLUME_DEFAULT)
        else:
            print(f"[SOUND WARNING] Missing sound file: {full_path}")

    # ---- music ----
    music_files = {
        "menu_theme": "menu_theme.mp3",
        "game_theme": "game_theme.mp3",
    }

    for track_name, filename in music_files.items():
        full_path = os.path.join(path_to_music, filename)
        if os.path.exists(full_path):
            music_tracks[track_name] = full_path
        else:
            print(f"[SOUND WARNING] Missing music file: {full_path}")

    # ---- channels ----
    channels["ui"] = pygame.mixer.Channel(0)
    channels["explosion"] = pygame.mixer.Channel(1)
    channels["gameplay"] = pygame.mixer.Channel(2)


def play_sound(name, channel=None):
    sound = sounds.get(name)
    if sound is None:
        return

    if channel is not None and channel in channels:
        channels[channel].play(sound)
    else:
        sound.play()


def stop_sound_channel(channel):
    if channel in channels:
        channels[channel].stop()


def set_sound_volume(name, volume):
    if name in sounds:
        sounds[name].set_volume(max(0.0, min(1.0, volume)))


def play_music(name, loops=-1, fade_ms=300):
    track_path = music_tracks.get(name)
    if track_path is None:
        return

    try:
        pygame.mixer.music.fadeout(fade_ms)
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.set_volume(_MUSIC_VOLUME_DEFAULT)
        pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
    except pygame.error as e:
        print(f"[SOUND ERROR] Failed to play music '{name}': {e}")


def stop_music(fade_ms=300):
    pygame.mixer.music.fadeout(fade_ms)


def set_music_volume(volume):
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))