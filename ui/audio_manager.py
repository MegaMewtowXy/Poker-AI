import math
import numpy as np
import pygame

class AudioManager:
    """
    Procedural Real-Time Audio Synthesizer for Pygame Poker Engine.
    Generates crisp card dealing slides, chip clinks, fold sweeps, and victory chimes
    without requiring external audio files!
    """

    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
        except Exception:
            self.enabled = False

        self._sounds = {}
        if self.enabled:
            self._init_sounds()

    def _generate_sound(self, samples):
        try:
            # Convert float samples (-1.0 to 1.0) to 16-bit signed stereo numpy array
            scaled = (samples * 32767).astype(np.int16)
            stereo = np.column_stack((scaled, scaled))
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def _init_sounds(self):
        sr = 22050

        # 1. Card Deal / Slide Sound (Soft noise burst with rapid decay)
        dur_card = 0.08
        t = np.linspace(0, dur_card, int(sr * dur_card), False)
        noise = np.random.uniform(-0.4, 0.4, len(t))
        env_card = np.exp(-t * 35)
        self._sounds["card"] = self._generate_sound(noise * env_card)

        # 2. Chip Clink Sound (High frequency metallic bell/sine chime)
        dur_chip = 0.12
        t = np.linspace(0, dur_chip, int(sr * dur_chip), False)
        sine1 = np.sin(2 * math.pi * 3200 * t)
        sine2 = np.sin(2 * math.pi * 4800 * t) * 0.5
        env_chip = np.exp(-t * 25)
        self._sounds["chip"] = self._generate_sound((sine1 + sine2) * 0.3 * env_chip)

        # 3. Fold Sound (Subtle low sweep)
        dur_fold = 0.10
        t = np.linspace(0, dur_fold, int(sr * dur_fold), False)
        freq = np.linspace(400, 150, len(t))
        sine_fold = np.sin(2 * math.pi * freq * t)
        env_fold = np.exp(-t * 20)
        self._sounds["fold"] = self._generate_sound(sine_fold * 0.25 * env_fold)

        # 4. Victory Win Chime (Arpeggiated triad C5 -> E5 -> G5)
        dur_win = 0.35
        t = np.linspace(0, dur_win, int(sr * dur_win), False)
        chime = (
            np.sin(2 * math.pi * 523.25 * t) * (t < 0.12) +
            np.sin(2 * math.pi * 659.25 * t) * ((t >= 0.10) & (t < 0.22)) +
            np.sin(2 * math.pi * 783.99 * t) * (t >= 0.20)
        )
        env_win = np.exp(-t * 6)
        self._sounds["win"] = self._generate_sound(chime * 0.3 * env_win)

    def play_card_deal(self):
        if self.enabled and self._sounds.get("card"):
            try: self._sounds["card"].play()
            except Exception: pass

    def play_chip_clink(self):
        if self.enabled and self._sounds.get("chip"):
            try: self._sounds["chip"].play()
            except Exception: pass

    def play_fold(self):
        if self.enabled and self._sounds.get("fold"):
            try: self._sounds["fold"].play()
            except Exception: pass

    def play_win(self):
        if self.enabled and self._sounds.get("win"):
            try: self._sounds["win"].play()
            except Exception: pass

audio_manager = AudioManager()
