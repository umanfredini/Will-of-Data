import pandas as pd
import joblib
import os


class WillOfDataEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.df_proc = pd.read_csv(os.path.join(base_dir, 'data', 'will_of_data_processed.csv'))
        self.df_raw = pd.read_csv(os.path.join(base_dir, 'data', 'will_of_data_raw.csv'))

        # CARICAMENTO DI TUTTI I MODELLI E LE CLASSI
        self.models = {
            'fazione': joblib.load(os.path.join(base_dir, 'models', 'model_fazione.pkl')),
            'frutto': joblib.load(os.path.join(base_dir, 'models', 'model_frutto.pkl')),
            'potenza': joblib.load(os.path.join(base_dir, 'models', 'model_potenza.pkl'))
        }

        self.classes = {
            'fazione': joblib.load(os.path.join(base_dir, 'models', 'classes_fazione.pkl')),
            'frutto': joblib.load(os.path.join(base_dir, 'models', 'classes_frutto.pkl')),
            'potenza': joblib.load(os.path.join(base_dir, 'models', 'classes_potenza.pkl'))
        }

        self.features = joblib.load(os.path.join(base_dir, 'models', 'features.pkl'))

    def map_col(self, c):
        # Mappature dirette per nomi che non seguono lo standard One-Hot
        direct_mapping = {
            'Senza_Frutto': 'Fruit_Nessuno',
            'Senza_Haki': 'Senza_Haki',
            'Ha_Frutto': 'Ha_Frutto',
            'Possiede_la_D': 'Possiede_la_D'
        }
        if c in direct_mapping: return direct_mapping[c]

        # Cerca tra i prefissi generati dal preprocessor
        for prefix in ['Fac_', 'Fruit_', 'Haki_', 'Taglia_', 'Race_', 'Role_']:
            if prefix + c in self.df_proc.columns:
                return prefix + c

        # Fallback se il criterio è già il nome esatto della colonna
        return c if c in self.df_proc.columns else None

    def get_best_match(self, c1, c2, top_n=30, rarity_boost_weight=0.6):
        k1 = self.map_col(c1)
        k2 = self.map_col(c2)

        if not k1 or not k2: return []

        X = self.df_proc[self.features]

        # Recupero probabilità dai modelli
        def get_prob(key):
            for category in ['fazione', 'frutto', 'potenza']:
                if key in self.classes[category]:
                    idx = self.classes[category].index(key)
                    return self.models[category].predict_proba(X)[:, idx]
            if key in self.df_proc.columns:
                return self.df_proc[key].values.astype(float)
            return np.zeros(len(self.df_proc))

        prob1 = get_prob(k1)
        prob2 = get_prob(k2)

        # Rarità della cella
        match_mask = (self.df_proc[k1] == 1) & (self.df_proc[k2] == 1)
        match_count = match_mask.sum()
        global_rarity = 1 / (match_count + 1)

        results = []
        for i, row in self.df_proc.iterrows():
            # --- HARD CONSTRAINT (INAMOVIBILE) ---
            fazione_ok = True
            if k1.startswith('Fac_') and row[k1] == 0: fazione_ok = False
            if k2.startswith('Fac_') and row[k2] == 0: fazione_ok = False

            # Se non rispetta i criteri, il personaggio viene eliminato subito
            if not fazione_ok:
                continue

            ml_confidence = float(prob1[i] * prob2[i])

            # Se l'IA non vede alcuna connessione, scartiamo (Soglia minima di decenza)
            if ml_confidence <= 0:
                continue

            char_raw = self.df_raw[self.df_raw['Nome'] == row['Nome']].iloc[0]
            char_rarity_factor = (11 - char_raw['Grado_Importanza']) / 10
            total_score = ml_confidence * (1 + rarity_boost_weight * char_rarity_factor) * global_rarity

            results.append({
                'Personaggio': row['Nome'],
                'Score': total_score,
                'Confidenza_ML': ml_confidence,
                'Rarity_Level': char_rarity_factor
            })

        results.sort(key=lambda x: x['Score'], reverse=True)
        return results[:top_n]

    def get_character_info_full(self, name):
        """Restituisce sia i dati RAW che quelli PROCESSATI per un controllo incrociato."""
        raw_row = self.df_raw[self.df_raw['Nome'] == name]
        proc_row = self.df_proc[self.df_proc['Nome'] == name]

        if raw_row.empty or proc_row.empty:
            return None

        import ast
        info_raw = raw_row.iloc[0].to_dict()
        try:
            # Se è già una lista non fare nulla, altrimenti eval
            if isinstance(info_raw['Haki_List'], str):
                info_raw['Haki_List'] = ast.literal_eval(info_raw['Haki_List'])
        except:
            info_raw['Haki_List'] = []

        return {
            'raw': info_raw,
            'proc': proc_row.iloc[0].to_dict()
        }