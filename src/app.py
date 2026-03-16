import pygame
import sys
import os
from will_of_data_engine import WillOfDataEngine

# --- COSTANTI ---
WIDTH, HEIGHT = 1100, 750
FPS = 60
BG_COLOR = (15, 15, 25)
GOLD = (255, 215, 0)
WHITE = (240, 240, 240)
GRAY = (50, 50, 60)
BLACK = (0, 0, 0)
ACCENT = (200, 50, 50)


class WillOfDataApp:
    def __init__(self):
        # 1. Inizializzazione esplicita dei moduli
        pygame.display.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Will of Data - ML Grid Solver")
        self.clock = pygame.time.Clock()

        # Font (con fallback se il sistema non li trova)
        self.font_title = pygame.font.SysFont("Verdana", 55, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)

        # 2. Caricamento Engine
        try:
            self.engine = WillOfDataEngine()
        except Exception as e:
            print(f"❌ Errore critico Engine: {e}")
            pygame.quit()
            sys.exit()

        self.fase = "TITOLO"

        # Setup Dati Griglia
        self.rows = ["Pirata", "Marine", "Rivoluzionario"]
        self.cols = ["Haki_Armatura", "Fruit_Logia", "Fruit_Zoan"]
        self.grid_results = [[None for _ in range(3)] for _ in range(3)]

        # Rettangoli interattivi
        self.play_btn = pygame.Rect(WIDTH // 2 - 100, 450, 200, 60)
        self.solve_btn = pygame.Rect(835, 650, 220, 50)
        self.cells = [[pygame.Rect(250 + c * 180, 150 + r * 150, 160, 130) for c in range(3)] for r in range(3)]
        self.hover_data = None

    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(str(text), True, color)
        rect = img.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(img, rect)

    def draw_title_screen(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("WILL OF DATA", self.font_title, GOLD, WIDTH // 2, 300, True)
        self.draw_text("Machine Learning Project - 2026", self.font_small, (150, 150, 150), WIDTH // 2, 360, True)

        m_pos = pygame.mouse.get_pos()
        btn_color = (255, 240, 150) if self.play_btn.collidepoint(m_pos) else GOLD
        pygame.draw.rect(self.screen, btn_color, self.play_btn, border_radius=12)
        self.draw_text("GIOCA", self.font_ui, BLACK, self.play_btn.centerx, self.play_btn.centery, True)

    def draw_game_screen(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("🧩 Griglia di Inferenza", self.font_ui, GOLD, 30, 30)

        # Intestazioni
        for c in range(3):
            label = self.cols[c].split('_')[-1]
            self.draw_text(label, self.font_ui, WHITE, 250 + c * 180 + 80, 110, True)
        for r in range(3):
            self.draw_text(self.rows[r], self.font_ui, WHITE, 50, 150 + r * 150 + 60)

        # Griglia
        m_pos = pygame.mouse.get_pos()
        self.hover_data = None

        for r in range(3):
            for c in range(3):
                rect = self.cells[r][c]
                hover = rect.collidepoint(m_pos)
                pygame.draw.rect(self.screen, (60, 60, 80) if hover else GRAY, rect, border_radius=10)
                pygame.draw.rect(self.screen, GOLD, rect, 2, border_radius=10)

                res = self.grid_results[r][c]
                if res:
                    self.draw_text(res['Personaggio'], self.font_ui, WHITE, rect.centerx, rect.centery, True)
                    if hover: self.hover_data = res
                else:
                    self.draw_text("?", self.font_title, (40, 40, 50), rect.centerx, rect.centery, True)

        # Pannello Analisi (Right)
        p_rect = pygame.Rect(820, 150, 250, 430)
        pygame.draw.rect(self.screen, (25, 25, 40), p_rect, border_radius=15)
        pygame.draw.rect(self.screen, GRAY, p_rect, 2, border_radius=15)
        self.draw_text("📊 ANALISI ML", self.font_ui, GOLD, 845, 180)

        if self.hover_data:
            self.draw_text(f"Nome: {self.hover_data['Personaggio']}", self.font_small, WHITE, 840, 230)
            self.draw_text(f"Confidenza: {int(self.hover_data['Confidenza_ML'] * 100)}%", self.font_small, WHITE, 840,
                           260)
            self.draw_text(f"Rarity Score: {self.hover_data['Score']:.3f}", self.font_small, WHITE, 840, 290)
            # Progress bar
            pygame.draw.rect(self.screen, GRAY, (840, 330, 210, 8))
            pygame.draw.rect(self.screen, GOLD, (840, 330, 210 * self.hover_data['Confidenza_ML'], 8))
        else:
            self.draw_text("Passa sopra una cella", self.font_small, (100, 100, 100), 840, 230)

        # Tasto Solve
        pygame.draw.rect(self.screen, ACCENT, self.solve_btn, border_radius=8)
        self.draw_text("RISOLVI GRIGLIA", self.font_small, WHITE, self.solve_btn.centerx, self.solve_btn.centery, True)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.fase == "TITOLO" and self.play_btn.collidepoint(event.pos):
                        self.fase = "GIOCO"
                    elif self.fase == "GIOCO" and self.solve_btn.collidepoint(event.pos):
                        for r in range(3):
                            for c in range(3):
                                match = self.engine.get_best_match(self.rows[r], self.cols[c], top_n=1)
                                if match: self.grid_results[r][c] = match[0]

            if self.fase == "TITOLO":
                self.draw_title_screen()
            else:
                self.draw_game_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Assicuriamoci che la cartella di lavoro sia corretta
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    app = WillOfDataApp()
    app.run()