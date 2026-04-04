import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler


def train():
    # Setup percorsi
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')
    models_dir = os.path.join(base_dir, 'models')
    if not os.path.exists(models_dir): os.makedirs(models_dir)

    # Caricamento dataset processato
    if not os.path.exists(data_path):
        print(f"❌ Errore: File {data_path} non trovato. Lancia prima il preprocessor!")
        return

    df = pd.read_csv(data_path)

    # 1. Configurazione dei Target (Cosa vogliamo che l'IA indovini)
    target_configs = {
        'fazione': [c for c in df.columns if c.startswith('Fac_')],
        'frutto': [c for c in df.columns if c.startswith('Fruit_')],
        'potenza': [c for c in df.columns if c.startswith('Taglia_')]
    }

    # 2. Creazione della matrice X (Features predittive)
    # Raccogliamo tutti i target per escluderli da X (Evita Data Leakage)
    all_targets = []
    for cols in target_configs.values():
        all_targets.extend(cols)

    # COLONNE DA ESCLUDERE:
    # - Nome: identificativo unico (inutile per la statistica)
    # - Bounty: rimosso per evitare che il modello 'potenza' bari leggendo il numero esatto
    # - All Targets: l'IA non può guardare la risposta mentre studia!
    drop_cols = ['Nome', 'Bounty'] + all_targets

    # Selezioniamo solo le colonne numeriche (Haki, Role_..., Race_..., Possiede_la_D, Ha_Frutto)
    X = df.drop(columns=[c for c in drop_cols if c in df.columns], axis=1).select_dtypes(include=['number'])

    print(f"🚀 Features identificate ({len(X.columns)}): {', '.join(X.columns.tolist()[:5])}...")

    # 3. Ciclo di addestramento
    for category, cols in target_configs.items():
        print(f"🌀 Addestramento modello: {category.upper()}...")

        # Trasformiamo le colonne dummy in etichette (Label Encoding al volo)
        y = df[cols].idxmax(axis=1)

        # Bilanciamento delle classi
        # Con 180+ personaggi, usiamo il campionamento per non ignorare i rari (es. Rivoluzionari)
        try:
            rus = RandomUnderSampler(random_state=42)
            X_res, y_res = rus.fit_resample(X, y)
        except ValueError:
            # Se una classe è troppo rara (es. 1 solo elemento), procediamo senza undersampling
            X_res, y_res = X, y

        # Random Forest: Aumentiamo la complessità per gestire Ruoli e Razze
        model = RandomForestClassifier(
            n_estimators=150,  # Più alberi per gestire la nuova complessità
            random_state=42,
            max_depth=12,  # Leggermente più profondo per le correlazioni 'D' / 'Ruolo'
            class_weight='balanced'  # Ulteriore aiuto per le classi sbilanciate
        )

        model.fit(X_res, y_res)

        # Salvataggio modello e classi
        joblib.dump(model, os.path.join(models_dir, f'model_{category}.pkl'))
        joblib.dump(model.classes_.tolist(), os.path.join(models_dir, f'classes_{category}.pkl'))

    # Salvataggio definitivo delle features per l'Engine
    joblib.dump(X.columns.tolist(), os.path.join(models_dir, 'features.pkl'))
    print(f"✅ Training completato. L'IA ora riconosce {len(X.columns)} attributi per ogni PG.")


if __name__ == "__main__":
    train()