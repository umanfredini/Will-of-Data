import pandas as pd
import joblib
import os


class WillOfDataEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.proc_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')
        self.raw_path = os.path.join(base_dir, 'data', 'will_of_data_raw.csv')
        models_dir = os.path.join(base_dir, 'models')

        if not os.path.exists(self.proc_path):
            raise FileNotFoundError(f"❌ File non trovato: {self.proc_path}")

        self.df_proc = pd.read_csv(self.proc_path)
        self.df_raw = pd.read_csv(self.raw_path)

        # Caricamento Modelli
        self.model_fac = joblib.load(os.path.join(models_dir, 'model_fazione.pkl'))
        self.model_fruit = joblib.load(os.path.join(models_dir, 'model_frutto.pkl'))
        self.features = joblib.load(os.path.join(models_dir, 'features.pkl'))

        self.fac_classes = self.model_fac.classes_.tolist()

    def get_best_match(self, row_val, col_val, top_n=3):
        row_key = f"Fac_{row_val}" if f"Fac_{row_val}" in self.df_proc.columns else row_val
        col_key = f"Fruit_{col_val}" if f"Fruit_{col_val}" in self.df_proc.columns else col_val

        if col_val in self.df_proc.columns: col_key = col_val

        if row_key not in self.df_proc.columns or col_key not in self.df_proc.columns:
            return []

        X = self.df_proc[self.features]

        if row_key in self.fac_classes:
            idx = self.fac_classes.index(row_key)
            prob_scores = self.model_fac.predict_proba(X)[:, idx]
        else:
            prob_scores = self.df_proc[row_key].values

        match_mask = (self.df_proc[row_key] == 1) & (self.df_proc[col_key] == 1)
        rarity_weight = 1 / (match_mask.sum() + 1)

        results = []
        for i, row in self.df_proc.iterrows():
            real_match = 1 if (row[row_key] == 1 and row[col_key] == 1) else 0
            importance = self.df_raw.iloc[i]['Grado_Importanza']
            score = (prob_scores[i] + real_match) * rarity_weight * importance

            if score > 0:
                results.append({
                    'Personaggio': row['Nome'],
                    'Score': round(float(score), 4),
                    'Confidenza_ML': round(float(prob_scores[i]), 2)
                })

        return sorted(results, key=lambda x: x['Score'], reverse=True)[:top_n]