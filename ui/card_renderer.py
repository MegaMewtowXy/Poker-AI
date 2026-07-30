import pygame

class CardRenderer:
    """
    Ultra-Modern Procedural Playing Card Renderer for Pygame.
    Generates crisp, high-contrast playing cards with elegant typography, HD suit graphics, and drop-shadows.
    """

    SUIT_COLORS = {
        "H": (239, 68, 68),     # Crimson Red
        "D": (239, 68, 68),     # Crimson Red
        "C": (15, 23, 42),      # Midnight Black
        "S": (15, 23, 42),      # Midnight Black
    }

    SUIT_SYMBOLS = {
        "H": "♥", "D": "♦", "C": "♣", "S": "♠"
    }

    def __init__(self):
        self._cache = {}

    def _parse_rank(self, rank):
        if hasattr(rank, "symbol"):
            return str(rank.symbol)
        if hasattr(rank, "value"):
            rank = rank.value
        if isinstance(rank, (tuple, list)) and len(rank) > 0:
            return str(rank[0])
        if isinstance(rank, int):
            mapping = {14: "A", 13: "K", 12: "Q", 11: "J", 10: "10"}
            return mapping.get(rank, str(rank))
        s = str(rank).strip().upper()
        s = s.replace("(", "").replace(")", "").replace("'", "").replace('"', "").strip()
        if "ACE" in s or s == "A": return "A"
        if "KING" in s or s == "K": return "K"
        if "QUEEN" in s or s == "Q": return "Q"
        if "JACK" in s or s == "J": return "J"
        return s[:2]

    def _parse_suit(self, suit):
        if hasattr(suit, "symbol"):
            sym = suit.symbol
            code = "H" if sym == "♥" else ("D" if sym == "♦" else ("C" if sym == "♣" else "S"))
            return code, sym
        if hasattr(suit, "value"):
            suit = suit.value
        s = str(suit).strip().upper()
        if "H" in s or "♥" in s:
            return "H", "♥"
        if "D" in s or "♦" in s:
            return "D", "♦"
        if "C" in s or "♣" in s:
            return "C", "♣"
        return "S", "♠"

    def get_card_surface(self, rank, suit, width=70, height=100, face_down=False):
        width = max(32, int(width))
        height = max(46, int(height))

        rank_str = self._parse_rank(rank)
        suit_code, suit_symbol = self._parse_suit(suit)

        key = (rank_str, suit_code, width, height, face_down)
        if key in self._cache:
            return self._cache[key]

        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, width, height)
        radius = max(5, int(width * 0.11))

        if face_down:
            # High-Definition Card Back
            pygame.draw.rect(surface, (241, 245, 249), rect, border_radius=radius)
            inner_rect = rect.inflate(-int(width * 0.12), -int(height * 0.12))
            
            # Deep Navy Fill
            pygame.draw.rect(surface, (15, 23, 42), inner_rect, border_radius=max(2, radius - 2))

            # Gold Accent Border
            pygame.draw.rect(surface, (245, 158, 11), inner_rect, 1, border_radius=max(2, radius - 2))

            # Pattern Lines
            pattern_color = (30, 41, 59)
            step = max(5, int(width * 0.18))
            for x in range(inner_rect.left - height, inner_rect.right + height, step):
                pygame.draw.line(surface, pattern_color, (x, inner_rect.top), (x + height, inner_rect.bottom), 1)

            # Outer Border
            pygame.draw.rect(surface, (148, 163, 184), rect, 2, border_radius=radius)
        else:
            # Face Up Card
            pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=radius)
            pygame.draw.rect(surface, (203, 213, 225), rect, 1, border_radius=radius)

            color = self.SUIT_COLORS.get(suit_code, (15, 23, 42))

            font_size = max(11, int(height * 0.25))
            font = pygame.font.SysFont("arial", font_size, bold=True)

            rank_surf = font.render(rank_str, True, color)
            symbol_surf = font.render(suit_symbol, True, color)

            # Top Left Corner
            surface.blit(rank_surf, (int(width * 0.08), int(height * 0.05)))
            surface.blit(symbol_surf, (int(width * 0.08), int(height * 0.28)))

            # Bottom Right Corner (Inverted)
            br_rank = pygame.transform.rotate(rank_surf, 180)
            br_symbol = pygame.transform.rotate(symbol_surf, 180)
            surface.blit(br_symbol, (width - int(width * 0.08) - br_symbol.get_width(), height - int(height * 0.05) - br_symbol.get_height() - br_rank.get_height()))
            surface.blit(br_rank, (width - int(width * 0.08) - br_rank.get_width(), height - int(height * 0.05) - br_rank.get_height()))

            # Center Symbol
            center_font_size = max(14, int(height * 0.38))
            center_font = pygame.font.SysFont("segoe ui symbol", center_font_size, bold=True)
            center_surf = center_font.render(suit_symbol, True, color)
            center_rect = center_surf.get_rect(center=(width // 2, height // 2))
            surface.blit(center_surf, center_rect)

        self._cache[key] = surface
        return surface

card_renderer = CardRenderer()
