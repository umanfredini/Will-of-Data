import pandas as pd
import ast
import os


def preprocess():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'will_of_data_raw.csv')
    proc_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')

    if not os.path.exists(raw_path):
        print("❌ Errore: File raw non trovato.")
        return

    df = pd.read_csv(raw_path)

    # 1. Gestione Haki
    # Trasforma la stringa "[...]" in una lista Python vera e propria
    df['Haki_List'] = df['Haki_List'].apply(ast.literal_eval)
    for t in ['Armatura', 'Percezione', 'Imperatore']:
        df[f'Haki_{t}'] = df['Haki_List'].apply(lambda x: 1 if t in x else 0)

    # Criterio: Senza Haki
    df['Senza_Haki'] = df['Haki_List'].apply(lambda x: 1 if len(x) == 0 else 0)

    # 2. Gestione Bounty (Taglie) con fasce complete
    df['Bounty'] = df['Bounty'].replace('Incerto', -1).astype(float)
    df['Taglia_Senza_Taglia'] = (df['Bounty'] == 0).astype(int)
    df['Taglia_Rookie'] = ((df['Bounty'] > 0) & (df['Bounty'] < 100000000)).astype(int)
    df['Taglia_Veterano'] = ((df['Bounty'] >= 100000000) & (df['Bounty'] < 1000000000)).astype(int)
    df['Taglia_Elite'] = (df['Bounty'] >= 1000000000).astype(int)

    # 3. Gestione Frutti
    # Forza 'Nessuno' per chi non ha frutti (genererà Fruit_Nessuno nel dummy encoding)
    df.loc[df['Ha_Frutto'] == False, 'Tipo_Frutto'] = 'Nessuno'

    # TRASFORMAZIONE CRUCIALE: Converte Ha_Frutto da Booleano a Intero (0/1)
    df['Ha_Frutto'] = df['Ha_Frutto'].astype(int)

    # 4. Dummy Encoding per Fazione e Tipo_Frutto
    df_final = pd.get_dummies(df, columns=['Fazione', 'Tipo_Frutto'], prefix=['Fac', 'Fruit'])

    # 5. Pulizia finale
    # Eliminiamo Haki_List (non numerica) e Grado_Importanza (non più richiesto come criterio)
    df_final = df_final.drop(['Haki_List', 'Grado_Importanza'], axis=1)

    # Salvataggio
    df_final.to_csv(proc_path, index=False)
    print(f"✅ Preprocessing completato correttamente.")


if __name__ == "__main__":
    preprocess()