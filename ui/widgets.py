import pygame

def draw_glass_panel(surface, rect, bg_color=(15, 23, 42), alpha=215, border_color=(255, 255, 255, 45), radius=12, border_width=1):
    """
    Renders a sleek, modern glassmorphic panel with translucency and subtle border glow.
    """
    rect = pygame.Rect(rect)
    if rect.width <= 0 or rect.height <= 0:
        return

    # Glass surface
    glass_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    fill_rgba = (*bg_color[:3], alpha)
    pygame.draw.rect(glass_surf, fill_rgba, (0, 0, rect.width, rect.height), border_radius=radius)

    # Top highlight line
    highlight_rgba = (255, 255, 255, min(80, alpha))
    pygame.draw.line(glass_surf, highlight_rgba, (radius, 1), (rect.width - radius, 1), 1)

    # Border
    if border_color and border_width > 0:
        border_rgba = border_color if len(border_color) == 4 else (*border_color[:3], 60)
        pygame.draw.rect(glass_surf, border_rgba, (0, 0, rect.width, rect.height), border_width, border_radius=radius)

    surface.blit(glass_surf, rect.topleft)

def draw_progress_bar(surface, rect, val, min_val=0, max_val=100, fill_color=(56, 189, 248), bg_color=(30, 41, 59), border_radius=4):
    """
    Renders a sleek telemetry progress bar with color fill and subtle track border.
    """
    rect = pygame.Rect(rect)
    if rect.width <= 0 or rect.height <= 0:
        return

    # Track background
    pygame.draw.rect(surface, bg_color, rect, border_radius=border_radius)
    pygame.draw.rect(surface, (71, 85, 105, 120), rect, 1, border_radius=border_radius)

    # Fill calculation
    ratio = max(0.0, min(1.0, (val - min_val) / max(1, (max_val - min_val))))
    fill_width = int(rect.width * ratio)
    if fill_width > 0:
        fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
        pygame.draw.rect(surface, fill_color, fill_rect, border_radius=border_radius)

        # Highlight stripe
        if fill_rect.height > 4:
            highlight_y = rect.y + 1
            highlight_w = fill_width
def draw_chip_stack(surface, x, y, amount, radius=9):
    """
    Renders stacked 3D poker chips ($10 red, $50 blue, $100 green, $500 black, $1000 gold).
    """
    if amount <= 0:
        return

    chips = []
    rem = amount
    counts = [(1000, (245, 158, 11)), (500, (15, 23, 42)), (100, (16, 185, 129)), (50, (59, 130, 246)), (10, (239, 68, 68))]
    for val, color in counts:
        num = rem // val
        if num > 0:
            chips.extend([color] * min(4, num))
            rem %= val
            if len(chips) >= 6:
                break

    if not chips:
        chips = [(239, 68, 68)]

    chip_y = y
    for color in reversed(chips[:6]):
        pygame.draw.ellipse(surface, (15, 23, 42, 120), (x - radius - 1, chip_y - radius // 2 + 3, radius * 2 + 2, radius + 2))
        pygame.draw.ellipse(surface, color, (x - radius, chip_y - radius // 2, radius * 2, radius))
        pygame.draw.ellipse(surface, (255, 255, 255, 180), (x - radius, chip_y - radius // 2, radius * 2, radius), 1)
        pygame.draw.ellipse(surface, (255, 255, 255, 100), (x - radius + 3, chip_y - radius // 2 + 2, radius * 2 - 6, radius - 4), 1)
        chip_y -= 3

class Button:
    """
    Sleek Pygame Button widget with gradient fill, hover glow, and press effect.
    """

    def __init__(self, rect, text, callback=None, bg_color=(37, 99, 235), hover_color=(29, 78, 216), text_color=(255, 255, 255), font_size=14, radius=8):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.radius = radius
        self.hovered = False
        self.pressed = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback:
                    self.callback()
                return True
            self.pressed = False
        return False

    def draw(self, surface):
        draw_rect = self.rect.copy()
        if self.pressed:
            draw_rect.y += 1  # Subtle depth press shift

        base_color = self.hover_color if self.hovered else self.bg_color
        
        # Render gradient button surface
        btn_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        top_color = tuple(min(255, int(c * 1.15)) for c in base_color)
        bottom_color = tuple(max(0, int(c * 0.85)) for c in base_color)
        
        for y in range(draw_rect.height):
            ratio = y / max(1, draw_rect.height)
            r = int(top_color[0] + ratio * (bottom_color[0] - top_color[0]))
            g = int(top_color[1] + ratio * (bottom_color[1] - top_color[1]))
            b = int(top_color[2] + ratio * (bottom_color[2] - top_color[2]))
            pygame.draw.line(btn_surf, (r, g, b, 255), (0, y), (draw_rect.width, y))

        # Top shine line
        pygame.draw.line(btn_surf, (255, 255, 255, 90), (self.radius, 1), (draw_rect.width - self.radius, 1), 1)

        # Apply rounded corner mask / rect
        masked_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(masked_surf, (255, 255, 255, 255), (0, 0, draw_rect.width, draw_rect.height), border_radius=self.radius)
        btn_surf.blit(masked_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        # Render button onto target surface
        surface.blit(btn_surf, draw_rect.topleft)

        # Outer border / hover glow
        border_color = (255, 255, 255, 160) if self.hovered else (255, 255, 255, 60)
        border_width = 2 if self.hovered else 1
        border_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, border_color, (0, 0, draw_rect.width, draw_rect.height), border_width, border_radius=self.radius)
        surface.blit(border_surf, draw_rect.topleft)

        # Button Text
        font = pygame.font.SysFont("arial", max(10, int(self.font_size)), bold=True)
        text_surf = font.render(str(self.text), True, self.text_color)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        surface.blit(text_surf, text_rect)

class TextInput:
    """
    Interactive Editable Text Box widget with sleek glass background and focus glow.
    """

    def __init__(self, rect, initial_text="", max_length=14, on_change=None):
        self.rect = pygame.Rect(rect)
        self.text = initial_text
        self.max_length = max_length
        self.on_change = on_change
        self.focused = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focused = self.rect.collidepoint(event.pos)
            return self.focused
        elif event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.focused = False
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
            
            if self.on_change:
                self.on_change(self.text)
            return True
        return False

    def draw(self, surface):
        bg_color = (15, 23, 42) if self.focused else (30, 41, 59)
        border_color = (56, 189, 248) if self.focused else (71, 85, 105)

        draw_glass_panel(surface, self.rect, bg_color=bg_color, alpha=230, border_color=border_color, radius=6, border_width=2 if self.focused else 1)

        font = pygame.font.SysFont("arial", max(11, int(self.rect.height * 0.55)), bold=True)
        disp_text = self.text + ("|" if self.focused else "")
        text_surf = font.render(disp_text, True, (241, 245, 249))
        surface.blit(text_surf, (self.rect.x + 8, self.rect.centery - text_surf.get_height() // 2))

class Slider:
    """
    Responsive Bet / Value Slider control with neon gradient track and glowing thumb handle.
    """

    def __init__(self, rect, min_val, max_val, initial_val=None, step=1, label="Amount"):
        self.rect = pygame.Rect(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.label = label
        self.val = initial_val if initial_val is not None else min_val
        self.dragging = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_val_from_mouse(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_val_from_mouse(event.pos[0])
            return True
        return False

    def _update_val_from_mouse(self, mouse_x):
        rel_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        ratio = rel_x / max(1, self.rect.width)
        raw_val = self.min_val + ratio * (self.max_val - self.min_val)
        stepped = round(raw_val / self.step) * self.step
        self.val = int(max(self.min_val, min(stepped, self.max_val)))

    def draw(self, surface):
        track_height = max(6, int(self.rect.height * 0.3))
        track_y = self.rect.centery - track_height // 2
        track_rect = pygame.Rect(self.rect.x, track_y, self.rect.width, track_height)
        
        # Track background
        pygame.draw.rect(surface, (30, 41, 59), track_rect, border_radius=4)
        pygame.draw.rect(surface, (71, 85, 105), track_rect, 1, border_radius=4)

        # Active fill track
        ratio = (self.val - self.min_val) / max(1, (self.max_val - self.min_val))
        fill_width = int(self.rect.width * ratio)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, track_y, fill_width, track_height)
            pygame.draw.rect(surface, (16, 185, 129), fill_rect, border_radius=4)

        # Glowing Thumb Handle
        knob_x = self.rect.x + fill_width
        knob_radius = max(9, int(self.rect.height * 0.45))
        
        # Glow ring
        glow_surf = pygame.Surface((knob_radius * 4, knob_radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (16, 185, 129, 60), (knob_radius * 2, knob_radius * 2), knob_radius + 4)
        surface.blit(glow_surf, (knob_x - knob_radius * 2, self.rect.centery - knob_radius * 2))

        pygame.draw.circle(surface, (241, 245, 249), (knob_x, self.rect.centery), knob_radius)
        pygame.draw.circle(surface, (16, 185, 129), (knob_x, self.rect.centery), knob_radius - 3)

class Dropdown:
    """
    Responsive Dropdown Select Menu widget with glass styling.
    """

    def __init__(self, rect, options, initial_index=0, on_select=None):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.selected_index = initial_index
        self.on_select = on_select
        self.expanded = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            elif self.expanded:
                for i, opt in enumerate(self.options):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if opt_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.expanded = False
                        if self.on_select:
                            self.on_select(self.options[i])
                        return True
                self.expanded = False
        return False

    def get_selected(self):
        if 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return ""

    def draw(self, surface):
        draw_glass_panel(surface, self.rect, bg_color=(30, 41, 59), alpha=230, border_color=(100, 116, 139), radius=6)

        font = pygame.font.SysFont("arial", max(10, int(self.rect.height * 0.45)), bold=True)
        text_surf = font.render(str(self.get_selected()), True, (241, 245, 249))
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 8, self.rect.centery))
        surface.blit(text_surf, text_rect)

        arrow = "▲" if self.expanded else "▼"
        arrow_surf = font.render(arrow, True, (148, 163, 184))
        surface.blit(arrow_surf, (self.rect.right - 20, self.rect.centery - arrow_surf.get_height() // 2))

        if self.expanded:
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                color = (51, 65, 85) if i == self.selected_index else (15, 23, 42)
                draw_glass_panel(surface, opt_rect, bg_color=color, alpha=240, border_color=(71, 85, 105), radius=4)

                opt_surf = font.render(str(opt), True, (241, 245, 249))
                surface.blit(opt_surf, (opt_rect.x + 8, opt_rect.centery - opt_surf.get_height() // 2))
