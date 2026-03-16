import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
import os

def train():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')
    models_dir = os.path.join(base_dir, 'models')

    if not os.path.exists(proc_path):
        print(f"❌ Errore: Esegui prima preprocessor.py. File non trovato: {proc_path}")
        return

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    df = pd.read_csv(proc_path)

    fac_cols = [c for c in df.columns if c.startswith('Fac_')]
    fruit_cols = [c for c in df.columns if c.startswith('Fruit_')]
    all_targets = fac_cols + fruit_cols

    X = df.drop(['Nome'] + all_targets, axis=1)
    X = X.select_dtypes(include=['number'])

    target_groups = {'fazione': fac_cols, 'frutto': fruit_cols}

    for category, cols in target_groups.items():
        print(f"🌀 Addestramento modello {category}...")
        y = df[cols].idxmax(axis=1)

        rus = RandomUnderSampler(random_state=42)
        X_res, y_res = rus.fit_resample(X, y)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_res, y_res)
        joblib.dump(model, os.path.join(models_dir, f'model_{category}.pkl'))

    joblib.dump(X.columns.tolist(), os.path.join(models_dir, 'features.pkl'))
    print(f"✅ Training completato. Modelli salvati in: {models_dir}")

if __name__ == "__main__":
    train()