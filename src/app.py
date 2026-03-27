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
        # Larghezza 1200 per ospitare comodamente il pannello di Audit
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
            print(f"❌ Errore caricamento Engine: {e}")
            sys.exit()

        self.fase = "TITOLO"
        self.pool = [
            'Pirata', 'Marine', 'Rivoluzionario', 'Civile', 'Governo Mondiale',
            'Armatura', 'Imperatore', 'Percezione', 'Senza_Haki',
            'Logia', 'Zoan', 'Paramecia', 'Senza_Frutto', 'Ha_Frutto',
            'Senza_Taglia', 'Rookie', 'Veterano', 'Elite'
        ]

        # --- COORDINATE UI ALLINEATE ---
        # Spostato tutto verso il centro per evitare bordi tagliati
        self.cells = [[pygame.Rect(210 + c * 210, 160 + r * 165, 190, 145) for c in range(3)] for r in range(3)]
        self.audit_panel = pygame.Rect(860, 60, 300, 560)
        self.solve_btn = pygame.Rect(860, 640, 300, 50)
        self.clear_btn = pygame.Rect(860, 710, 300, 50)
        self.play_btn = pygame.Rect(500, 500, 200, 70)

        self.setup_game()

    def setup_game(self):
        """
        Smart Sampler 2.0: Garantisce l'esclusione totale tra righe e colonne
        per evitare duplicati di categorie (es. Elite vs Elite).
        """
        # 1. Estraiamo 3 criteri casuali per le righe
        self.rows = random.sample(self.pool, 3)

        # 2. Creiamo un pool per le colonne escludendo TUTTI i criteri già usati nelle righe
        # Inoltre, per sicurezza, escludiamo le fazioni se ce n'è già una nelle righe
        # per evitare incroci impossibili (es. Marine vs Pirata)
        fazioni = ['Pirata', 'Marine', 'Rivoluzionario', 'Civile', 'Governo Mondiale']
        fazioni_in_righe = [c for c in self.rows if c in fazioni]

        pool_colonne = [
            c for c in self.pool
            if c not in self.rows and c not in fazioni_in_righe
        ]

        # 3. Estraiamo le colonne dal pool filtrato
        self.cols = random.sample(pool_colonne, 3)

        # Reset dei risultati e dei nomi usati
        self.grid_results = [[None for _ in range(3)] for _ in range(3)]
        self.used_names = set()

    def solve_cell(self, r, c):
        """Risoluzione con protezione anti-crash."""
        try:
            matches = self.engine.get_best_match(self.rows[r], self.cols[c], top_n=40)
            if matches:
                for m in matches:
                    if m['Personaggio'] not in self.used_names:
                        if self.grid_results[r][c]:
                            self.used_names.discard(self.grid_results[r][c]['Personaggio'])
                        self.grid_results[r][c] = m
                        self.used_names.add(m['Personaggio'])
                        return
        except Exception as e:
            print(f"⚠️ Errore solve_cell: {e}")

    def draw_txt(self, t, x, y, center=False, color=INK, font=None):
        if font is None: font = self.font_main
        img = font.render(str(t), True, color)
        rect = img.get_rect(center=(x, y)) if center else img.get_rect(topleft=(x, y))
        self.screen.blit(img, rect)

    def draw_audit_log(self, res, r, c):
        """Visualizza i dati RAW e PROCESSATI per il debugging live."""
        pygame.draw.rect(self.screen, PARCHMENT, self.audit_panel, border_radius=12)
        pygame.draw.rect(self.screen, INK, self.audit_panel, 2, border_radius=12)

        header = pygame.Rect(self.audit_panel.x, self.audit_panel.y, self.audit_panel.width, 40)
        pygame.draw.rect(self.screen, INK, header, border_top_left_radius=12, border_top_right_radius=12)
        self.draw_txt("⚓ AUDIT LOG", header.centerx, header.centery, True, color=GOLD, font=self.font_bold_small)

        if not res:
            self.draw_txt("Hover su un personaggio...", self.audit_panel.centerx, 150, True, color=(140, 130, 120),
                          font=self.font_small)
            return

        # FIX: Metodo corretto get_character_info_full
        data = self.engine.get_character_info_full(res['Personaggio'])
        if not data: return
        raw, proc = data['raw'], data['proc']

        px, py = self.audit_panel.x + 20, 115
        self.draw_txt(raw['Nome'].upper(), px, py, color=RED_SEAL)
        self.draw_txt(f"AI Match: {int(res['Confidenza_ML'] * 100)}%", px, py + 30, font=self.font_small)

        # Sezione Verifica
        y_check = py + 80
        self.draw_txt("■ VALIDAZIONE DATASET:", px, y_check, font=self.font_bold_small)
        for crit in [self.rows[r], self.cols[c]]:
            y_check += 35
            mapped = self.engine.map_col(crit)
            is_ok = proc.get(mapped) == 1
            color = MINT_GREEN if is_ok else RED_SEAL
            status = "✓ VALID" if is_ok else "✗ ERROR"

            clean = crit.replace("Fac_", "").replace("Taglia_", "").replace("Haki_", "")
            self.draw_txt(f"• {clean[:12]}:", px, y_check, font=self.font_small)
            self.draw_txt(status, self.audit_panel.right - 90, y_check, font=self.font_small, color=color)

        # Sezione Dati Raw
        y_raw = y_check + 50
        pygame.draw.rect(self.screen, INK, (px, y_raw, 260, 1))
        self.draw_txt("■ INFO ORIGINALI:", px, y_raw + 15, font=self.font_bold_small)
        y_raw += 45
        for line in [f"Fac: {raw['Fazione']}", f"Frut: {raw['Tipo_Frutto']}", f"Haki: {len(raw['Haki_List'])} tipi"]:
            self.draw_txt(line, px, y_raw, font=self.font_small)
            y_raw += 25

    def draw_game(self):
        self.screen.fill(WOOD)
        pygame.draw.rect(self.screen, PARCHMENT, (30, 30, 1140, 740), border_radius=15)
        pygame.draw.rect(self.screen, INK, (30, 30, 1140, 740), 3, border_radius=15)

        self.draw_txt("📜 THE WILL OF DATA MAP", 60, 50, color=INK)

        # Labels
        for i in range(3):
            self.draw_txt(self.cols[i], 210 + i * 210 + 95, 115, True, font=self.font_small)
            self.draw_txt(self.rows[i], 50, 160 + i * 165 + 75, font=self.font_small)

        m_pos = pygame.mouse.get_pos()
        hover_data = None

        for r in range(3):
            for c in range(3):
                rect = self.cells[r][c]
                is_hover = rect.collidepoint(m_pos)
                pygame.draw.rect(self.screen, (220, 205, 180) if is_hover else PARCHMENT, rect, border_radius=8)
                pygame.draw.rect(self.screen, INK, rect, 1, border_radius=8)

                res = self.grid_results[r][c]
                if res:
                    self.draw_txt(res['Personaggio'], rect.centerx, rect.centery, True)
                    if is_hover: hover_data = (res, r, c)
                else:
                    self.draw_txt("?", rect.centerx, rect.centery, True, color=(160, 150, 140))

        if hover_data:
            self.draw_audit_log(*hover_data)
        else:
            self.draw_audit_log(None, 0, 0)

        # Bottoni
        for btn, txt, col in [(self.solve_btn, "SET SAIL", WOOD), (self.clear_btn, "BURN MAP", RED_SEAL)]:
            pygame.draw.rect(self.screen, col, btn, border_radius=10)
            self.draw_txt(txt, btn.centerx, btn.centery, True, color=GOLD if col == WOOD else WHITE)

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
    # Assicura il percorso corretto per i file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(script_dir, ".."))
    WillOfDataApp().run()