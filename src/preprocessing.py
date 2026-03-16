import pandas as pd
import ast
import os

def preprocess():
    # Trova la root e i percorsi
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'will_of_data_raw.csv')
    proc_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')

    if not os.path.exists(raw_path):
        print(f"❌ Errore: File non trovato in {raw_path}")
        return

    df = pd.read_csv(raw_path)

    # TRASFORMAZIONE LISTE
    df['Haki_List'] = df['Haki_List'].apply(ast.literal_eval)
    types = ['Armatura', 'Percezione', 'Imperatore', 'Incerto']
    for t in types:
        df[f'Haki_{t}'] = df['Haki_List'].apply(lambda x: 1 if t in x else 0)

    df = df.drop('Haki_List', axis=1)
    df['Bounty'] = df['Bounty'].replace('Incerto', -1).astype(float)

    df.loc[df['Ha_Frutto'] == False, 'Tipo_Frutto'] = 'Nessuno'
    df_final = pd.get_dummies(df, columns=['Fazione', 'Tipo_Frutto'], prefix=['Fac', 'Fruit'])

    df_final.to_csv(proc_path, index=False)
    print(f"✅ Preprocessing completato in: {proc_path}")

if __name__ == "__main__":
    preprocess()