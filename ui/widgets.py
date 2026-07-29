import pygame

class Button:
    """
    Sleek Pygame Button widget with smooth hover/active states.
    """

    def __init__(self, rect, text, callback=None, bg_color=(37, 99, 235), hover_color=(29, 78, 216), text_color=(255, 255, 255), font_size=16, radius=8):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.radius = radius
        self.hovered = False

    def update_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
        pygame.draw.rect(surface, (255, 255, 255, 50), self.rect, 1, border_radius=self.radius)

        font = pygame.font.SysFont("arial", max(10, int(self.font_size)), bold=True)
        text_surf = font.render(str(self.text), True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class TextInput:
    """
    Interactive Editable Text Box widget.
    Allows changing player names directly by clicking and typing!
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
        bg_color = (30, 41, 59) if not self.focused else (15, 23, 42)
        border_color = (59, 130, 246) if self.focused else (71, 85, 105)

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, 2 if self.focused else 1, border_radius=6)

        font = pygame.font.SysFont("arial", max(11, int(self.rect.height * 0.55)), bold=True)
        disp_text = self.text + ("|" if self.focused else "")
        text_surf = font.render(disp_text, True, (241, 245, 249))
        surface.blit(text_surf, (self.rect.x + 8, self.rect.centery - text_surf.get_height() // 2))


class Slider:
    """
    Responsive Bet / Value Slider control.
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
        track_height = max(4, int(self.rect.height * 0.25))
        track_y = self.rect.centery - track_height // 2
        track_rect = pygame.Rect(self.rect.x, track_y, self.rect.width, track_height)
        pygame.draw.rect(surface, (71, 85, 105), track_rect, border_radius=3)

        ratio = (self.val - self.min_val) / max(1, (self.max_val - self.min_val))
        fill_width = int(self.rect.width * ratio)
        fill_rect = pygame.Rect(self.rect.x, track_y, fill_width, track_height)
        pygame.draw.rect(surface, (16, 185, 129), fill_rect, border_radius=3)

        knob_x = self.rect.x + fill_width
        knob_radius = max(8, int(self.rect.height * 0.4))
        pygame.draw.circle(surface, (255, 255, 255), (knob_x, self.rect.centery), knob_radius)
        pygame.draw.circle(surface, (16, 185, 129), (knob_x, self.rect.centery), knob_radius - 3)


class Dropdown:
    """
    Responsive Dropdown Select Menu widget.
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
        pygame.draw.rect(surface, (30, 41, 59), self.rect, border_radius=4)
        pygame.draw.rect(surface, (100, 116, 139), self.rect, 1, border_radius=4)

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
                pygame.draw.rect(surface, color, opt_rect)
                pygame.draw.rect(surface, (71, 85, 105), opt_rect, 1)

                opt_surf = font.render(str(opt), True, (241, 245, 249))
                surface.blit(opt_surf, (opt_rect.x + 8, opt_rect.centery - opt_surf.get_height() // 2))
