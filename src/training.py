import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


def train():
    # Setup percorsi
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')
    models_dir = os.path.join(base_dir, 'models')
    if not os.path.exists(models_dir): os.makedirs(models_dir)

    # Caricamento dataset
    if not os.path.exists(data_path):
        print(f"❌ Errore: File {data_path} non trovato.")
        return

    df = pd.read_csv(data_path)

    # 1. Configurazione dei Target
    target_configs = {
        'fazione': [c for c in df.columns if c.startswith('Fac_')],
        'frutto': [c for c in df.columns if c.startswith('Fruit_')],
        'potenza': [c for c in df.columns if c.startswith('Taglia_')]
    }

    # 2. Creazione della matrice X (Features)
    all_targets = [col for cols in target_configs.values() for col in cols]
    drop_cols = ['Nome', 'Bounty'] + all_targets
    X = df.drop(columns=[c for c in drop_cols if c in df.columns], axis=1).select_dtypes(include=['number'])

    print(f"🚀 Features identificate ({len(X.columns)}): {', '.join(X.columns.tolist()[:5])}...")

    # Dizionario per raccogliere i risultati di tutti i modelli
    evaluation_results = {}

    # 3. Ciclo di addestramento (UNICO, non annidato)
    for category, cols in target_configs.items():
        print(f"🌀 Addestramento modello: {category.upper()}...")

        # Target: idxmax trasforma le colonne One-Hot in una singola etichetta
        y = df[cols].idxmax(axis=1)

        # SPLIT: Teniamo il 20% per la validazione (Matrici di Confusione reali)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # BILANCIAMENTO: Applichiamo l'undersampling solo al set di addestramento
        try:
            rus = RandomUnderSampler(random_state=42)
            X_res, y_res = rus.fit_resample(X_train, y_train)
        except ValueError:
            X_res, y_res = X_train, y_train

        # Configurazione Random Forest
        model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            class_weight='balanced',
            random_state=42
        )
        model.fit(X_res, y_res)

        # VALUTAZIONE
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)

        # Archiviazione dati per i grafici della relazione
        evaluation_results[category] = {
            'report': report,
            'confusion_matrix': cm,
            'labels': model.classes_.tolist(),
            'importance': dict(zip(X.columns, model.feature_importances_))
        }

        # Salvataggio modelli individuali
        joblib.dump(model, os.path.join(models_dir, f'model_{category}.pkl'))
        joblib.dump(model.classes_.tolist(), os.path.join(models_dir, f'classes_{category}.pkl'))
        print(f"   ✅ Modello {category} salvato.")

    # 4. Salvataggio finale dei metadati per Engine e Validator
    joblib.dump(evaluation_results, os.path.join(models_dir, 'evaluation_report.pkl'))
    joblib.dump(X.columns.tolist(), os.path.join(models_dir, 'features.pkl'))

    print("-" * 30)
    print(f"🏆 Training completato con successo.")
    print(f"📊 Report di valutazione salvato in: {os.path.join(models_dir, 'evaluation_report.pkl')}")


if __name__ == "__main__":
    train()