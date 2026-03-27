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
        mapping = {
            'Senza_Frutto': 'Fruit_Nessuno', 'Senza_Haki': 'Senza_Haki',
            'Ha_Frutto': 'Ha_Frutto', 'Nessuno': 'Fruit_Nessuno'
        }
        if c in mapping: return mapping[c]
        for p in ['Fac_', 'Fruit_', 'Haki_', 'Taglia_']:
            if p + c in self.df_proc.columns: return p + c
        return c if c in self.df_proc.columns else None

    def get_best_match(self, c1, c2, top_n=30):
        """
        Calcola il miglior match applicando una penalità ai falsi positivi
        per bilanciare l'intuizione del ML con la coerenza del dataset.
        """
        k1 = self.map_col(c1)
        k2 = self.map_col(c2)

        if not k1 or not k2:
            return []

        X = self.df_proc[self.features]

        # 1. Recupero delle probabilità dai modelli specialistici
        def get_prob(key):
            # Controlla se la chiave appartiene a uno dei target dei modelli
            for category in ['fazione', 'frutto', 'potenza']:
                if key in self.classes[category]:
                    idx = self.classes[category].index(key)
                    return self.models[category].predict_proba(X)[:, idx]
            # Se è un flag binario non gestito dai modelli (es. Ha_Frutto),
            # usiamo il valore della colonna stessa
            return self.df_proc[key].values.astype(float)

        prob1 = get_prob(k1)
        prob2 = get_prob(k2)

        # 2. Calcolo della rarità globale della combinazione
        # Serve a dare più punti a chi risolve celle difficili
        match_mask = (self.df_proc[k1] == 1) & (self.df_proc[k2] == 1)
        match_count = match_mask.sum()
        rarity_weight = 1 / (match_count + 1)

        results = []
        for i, row in self.df_proc.iterrows():
            # DETERMINAZIONE DEI FILTRI RIGIDI
            # Se uno dei criteri è una Fazione, il personaggio DEVE appartenervi (Filtro Hard)
            is_faction_crit_1 = k1.startswith('Fac_')
            is_faction_crit_2 = k2.startswith('Fac_')

            fazione_ok = True
            if is_faction_crit_1 and row[k1] == 0: fazione_ok = False
            if is_faction_crit_2 and row[k2] == 0: fazione_ok = False

            # Se la fazione è sbagliata, lo score è 0. Fine dei giochi per Doflamingo-Marine.
            if not fazione_ok:
                continue

            # Se la fazione è corretta, usiamo le probabilità ML per trovare il "miglior match"
            # Ad esempio: tra tutti i Marine, chi ha il profilo più simile a un "Veterano"?
            score = (prob1[i] * prob2[i]) * rarity_weight

            if score > 0.001:
                results.append({
                    'Personaggio': row['Nome'],
                    'Score': float(score),
                    'Confidenza_ML': float(prob1[i] * prob2[i])
                })

        # Ordinamento per score decrescente
        return sorted(results, key=lambda x: x['Score'], reverse=True)[:top_n]

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