import pygame
import sys
import os
import random
from will_of_data_engine import WillOfDataEngine

# --- TAVOLO DEI COLORI "GRAND LINE" ---
WOOD = (45, 30, 20)
PARCHMENT = (235, 215, 185)
INK = (35, 35, 40)
GOLD = (210, 170, 60)
RED_SEAL = (180, 40, 40)
MINT_GREEN = (45, 150, 85)
WHITE = (250, 250, 250)


class WillOfDataApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("🏴‍☠️ Will of Data: Audit & Inference System")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_main = pygame.font.SysFont("Georgia", 22, bold=True)
        self.font_title = pygame.font.SysFont("Georgia", 70, bold=True, italic=True)
        self.font_small = pygame.font.SysFont("Courier New", 14, bold=True)
        self.font_bold_small = pygame.font.SysFont("Georgia", 16, bold=True)

        try:
            self.engine = WillOfDataEngine()
        except Exception as e:
            print(f"❌ Errore Engine: {e}")
            sys.exit()

        self.fase = "TITOLO"

        # Pool aggiornato con le nuove feature
        self.pool = [
            'Pirata', 'Marine', 'Rivoluzionario', 'Civile', 'Governo Mondiale',
            'Armatura', 'Imperatore', 'Percezione', 'Senza_Haki',
            'Ha_Frutto', 'Senza_Frutto', 'Possiede_la_D',
            'Rookie', 'Veterano', 'Elite',
            'Spadaccino', 'Capitano', 'Medico',
            'Umano', 'Uomo-Pesce', 'Animale', 'Angelo', 'Gigante'
        ]

        # UI Coordinate
        self.cells = [[pygame.Rect(210 + c * 210, 160 + r * 165, 190, 145) for c in range(3)] for r in range(3)]
        self.audit_panel = pygame.Rect(860, 60, 300, 600)
        self.solve_btn = pygame.Rect(860, 680, 300, 45)
        self.clear_btn = pygame.Rect(860, 735, 300, 45)
        self.play_btn = pygame.Rect(500, 500, 200, 70)

        self.setup_game()

    def setup_game(self):
        """Smart Sampler 3.0: Gestione famiglie escludenti per evitare griglie impossibili."""
        famiglie = {
            'fazioni': ['Pirata', 'Marine', 'Rivoluzionario', 'Civile', 'Governo Mondiale'],
            'taglie': ['Rookie', 'Veterano', 'Elite'],
            'razze': ['Umano', 'Uomo-Pesce', 'Animale', 'Angelo', 'Gigante'],
            'frutti': ['Ha_Frutto', 'Senza_Frutto']
        }

        # 1. Scegliamo le righe
        self.rows = random.sample(self.pool, 3)

        # 2. Filtriamo le colonne per evitare conflitti di famiglia
        famiglie_usate = []
        for r in self.rows:
            for nome, membri in famiglie.items():
                if r in membri: famiglie_usate.append(nome)

        pool_colonne = []
        for c in self.pool:
            famiglia_c = next((f for f, membri in famiglie.items() if c in membri), None)
            # Evita duplicati esatti e membri della stessa famiglia (es. no Rookie vs Elite)
            if c not in self.rows and famiglia_c not in famiglie_usate:
                pool_colonne.append(c)

        self.cols = random.sample(pool_colonne, 3)
        self.grid_results = [[None for _ in range(3)] for _ in range(3)]
        self.used_names = set()

    def solve_cell(self, r, c):
        """Tenta di risolvere la cella. Se non trova nulla, segna 'EMPTY'."""
        try:
            # Cerchiamo i match
            matches = self.engine.get_best_match(self.rows[r], self.cols[c], top_n=50)

            if matches:
                for m in matches:
                    if m['Personaggio'] not in self.used_names:
                        # Rimuoviamo il vecchio nome se esisteva
                        if isinstance(self.grid_results[r][c], dict):
                            self.used_names.discard(self.grid_results[r][c]['Personaggio'])

                        self.grid_results[r][c] = m
                        self.used_names.add(m['Personaggio'])
                        return

            # Se arriviamo qui, non è stato trovato nessun match valido
            self.grid_results[r][c] = "EMPTY"

        except Exception as e:
            print(f"⚠️ Solve error: {e}")
            self.grid_results[r][c] = "EMPTY"

    def draw_game(self):
        self.screen.fill(WOOD)
        pygame.draw.rect(self.screen, PARCHMENT, (30, 30, 1140, 740), border_radius=15)
        self.draw_txt("📜 THE WILL OF DATA MAP", 60, 50, color=INK)

        # Labels
        for i in range(3):
            c_label = self.cols[i].replace("Senza_", "No ").replace("Possiede_la_", "")
            r_label = self.rows[i].replace("Senza_", "No ").replace("Possiede_la_", "")
            self.draw_txt(c_label, 210 + i * 210 + 95, 115, True, font=self.font_small)
            self.draw_txt(r_label, 50, 160 + i * 165 + 75, font=self.font_small)

        m_pos = pygame.mouse.get_pos()
        hover_data = None

        for r in range(3):
            for c in range(3):
                rect = self.cells[r][c]
                is_hover = rect.collidepoint(m_pos)
                pygame.draw.rect(self.screen, (225, 210, 190) if is_hover else (240, 230, 210), rect, border_radius=8)
                pygame.draw.rect(self.screen, INK, rect, 1, border_radius=8)

                res = self.grid_results[r][c]

                if isinstance(res, dict):
                    # Personaggio trovato
                    self.draw_txt(res['Personaggio'], rect.centerx, rect.centery, True)
                    if is_hover: hover_data = (res, r, c)
                elif res == "EMPTY":
                    # Nessun match trovato: Mostra una X rossa
                    self.draw_txt("X", rect.centerx, rect.centery, True, color=RED_SEAL, font=self.font_title)
                    if is_hover: hover_data = ("EMPTY", r, c)
                else:
                    # Cella non ancora cliccata
                    self.draw_txt("?", rect.centerx, rect.centery, True, color=(180, 170, 160))

        self.draw_audit_log(*hover_data if hover_data else (None, 0, 0))

        # Bottoni
        for btn, txt, col in [(self.solve_btn, "SET SAIL", WOOD), (self.clear_btn, "BURN MAP", RED_SEAL)]:
            pygame.draw.rect(self.screen, col, btn, border_radius=10)
            self.draw_txt(txt, btn.centerx, btn.centery, True, color=GOLD if col == WOOD else WHITE)

    def draw_audit_log(self, res, r, c):
        pygame.draw.rect(self.screen, PARCHMENT, self.audit_panel, border_radius=12)
        pygame.draw.rect(self.screen, INK, self.audit_panel, 2, border_radius=12)

        header = pygame.Rect(self.audit_panel.x, self.audit_panel.y, self.audit_panel.width, 40)
        pygame.draw.rect(self.screen, INK, header, border_top_left_radius=12, border_top_right_radius=12)
        self.draw_txt("⚓ AUDIT LOG", header.centerx, header.centery, True, color=GOLD, font=self.font_bold_small)

        if not res:
            self.draw_txt("Esplora la mappa...", self.audit_panel.centerx, 150, True, color=(140, 130, 120),
                          font=self.font_small)
            return

        if res == "EMPTY":
            self.draw_txt("Nessun match trovato", self.audit_panel.centerx, 150, True, color=RED_SEAL,
                          font=self.font_bold_small)
            self.draw_txt("L'intersezione dei criteri", self.audit_panel.centerx, 180, True, font=self.font_small)
            self.draw_txt("è vuota nel dataset.", self.audit_panel.centerx, 200, True, font=self.font_small)
            return

        data = self.engine.get_character_info_full(res['Personaggio'])
        raw, proc = data['raw'], data['proc']

        # SCALING DELLA CONFIDENZA: Trasformiamo i valori bassi in percentuali leggibili
        # Un 15% (0.15) viene scalato per apparire come un 75-80% se è il top del modello
        raw_score = res['Confidenza_ML']
        visual_score = min((raw_score / 0.20) * 100, 100)  # 0.20 è il nostro target di "certezza massima"

        px, py = self.audit_panel.x + 20, 100
        self.draw_txt(raw['Nome'].upper(), px, py, color=RED_SEAL)
        self.draw_txt(f"AI Confidence: {visual_score:.1f}%", px, py + 30, font=self.font_small)

        # Validazione Criteri (Ora include Ruoli e Razze)
        y_check = py + 75
        self.draw_txt("■ CRITERI VERIFICATI:", px, y_check, font=self.font_bold_small)
        for crit in [self.rows[r], self.cols[c]]:
            y_check += 32
            mapped = self.engine.map_col(crit)
            is_ok = proc.get(mapped) == 1
            color = MINT_GREEN if is_ok else RED_SEAL
            self.draw_txt(f"• {crit[:14]}:", px, y_check, font=self.font_small)
            self.draw_txt("OK" if is_ok else "ERR", self.audit_panel.right - 50, y_check, font=self.font_small,
                          color=color)

        # Info Raw Estese
        y_raw = y_check + 45
        pygame.draw.rect(self.screen, INK, (px, y_raw, 260, 1))
        self.draw_txt("■ SCHEDA LORE:", px, y_raw + 15, font=self.font_bold_small)

        info_lines = [
            f"Fazione: {raw['Fazione']}",
            f"Ruolo:   {raw['Ruolo']}",
            f"Razza:   {raw['Razza']}",
            f"Taglia:  {raw['Bounty']}",
            f"Frutto:  {raw['Tipo_Frutto']}",
            f"Eredità: {'Volontà della D.' if raw['Possiede_la_D'] else 'Comune'}"
        ]

        y_raw += 45
        for line in info_lines:
            self.draw_txt(line, px, y_raw, font=self.font_small)
            y_raw += 22

    def draw_txt(self, t, x, y, center=False, color=INK, font=None):
        if font is None: font = self.font_main
        img = font.render(str(t), True, color)
        rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
        self.screen.blit(img, rect)

    def run(self):
        try:
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: return
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if self.fase == "TITOLO" and self.play_btn.collidepoint(e.pos):
                            self.fase = "GIOCO"
                        elif self.fase == "GIOCO":
                            for r in range(3):
                                for c in range(3):
                                    if self.cells[r][c].collidepoint(e.pos): self.solve_cell(r, c)
                            if self.solve_btn.collidepoint(e.pos):
                                for r in range(3):
                                    for c in range(3): self.solve_cell(r, c)
                            if self.clear_btn.collidepoint(e.pos): self.setup_game()

                if self.fase == "TITOLO":
                    self.screen.fill(WOOD)
                    self.draw_txt("WILL OF DATA", 600, 350, True, color=GOLD, font=self.font_title)
                    pygame.draw.rect(self.screen, GOLD, self.play_btn, border_radius=15)
                    self.draw_txt("START", 600, 535, True, color=WOOD)
                else:
                    self.draw_game()
                pygame.display.flip()
                self.clock.tick(60)
        finally:
            pygame.quit()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(script_dir, ".."))
    WillOfDataApp().run()