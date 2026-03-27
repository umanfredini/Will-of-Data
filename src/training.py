import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler


def train():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')
    models_dir = os.path.join(base_dir, 'models')
    if not os.path.exists(models_dir): os.makedirs(models_dir)

    df = pd.read_csv(data_path)

    # 1. Identificazione dei gruppi di target
    target_configs = {
        'fazione': [c for c in df.columns if c.startswith('Fac_')],
        'frutto': [c for c in df.columns if c.startswith('Fruit_')],
        'potenza': [c for c in df.columns if c.startswith('Taglia_')]
    }

    # 2. Creazione della matrice X (Features)
    # Fondamentale: Droppiamo TUTTI i target possibili per evitare data leakage
    all_targets = []
    for cols in target_configs.values():
        all_targets.extend(cols)

    # Rimuoviamo Nome e tutte le colonne target da X
    X = df.drop(['Nome'] + all_targets, axis=1).select_dtypes(include=['number'])

    # 3. Ciclo di addestramento per ogni modello
    for category, cols in target_configs.items():
        print(f"🌀 Addestramento modello: {category}...")

        # Trasformiamo le colonne dummy in una singola etichetta per il training
        y = df[cols].idxmax(axis=1)

        # Bilanciamento delle classi (importante per categorie rare come 'Elite')
        rus = RandomUnderSampler(random_state=42)
        X_res, y_res = rus.fit_resample(X, y)

        # Training del Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_res, y_res)

        # Salvataggio del modello specifico
        joblib.dump(model, os.path.join(models_dir, f'model_{category}.pkl'))
        # Salviamo anche le classi per sapere l'ordine delle probabilità nell'engine
        joblib.dump(model.classes_.tolist(), os.path.join(models_dir, f'classes_{category}.pkl'))

    # Salvataggio della lista delle features per l'Engine
    joblib.dump(X.columns.tolist(), os.path.join(models_dir, 'features.pkl'))
    print("✅ Tutti i modelli (Fazione, Frutto, Potenza) sono stati addestrati e salvati.")


if __name__ == "__main__":
    train()