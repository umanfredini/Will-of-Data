import pandas as pd
import ast
import os

def preprocess():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'will_of_data_raw.csv')
    proc_path = os.path.join(base_dir, 'data', 'will_of_data_processed.csv')

    if not os.path.exists(raw_path): return

    df = pd.read_csv(raw_path)

    # 1. Gestione Haki
    df['Haki_List'] = df['Haki_List'].apply(ast.literal_eval)
    for t in ['Armatura', 'Percezione', 'Imperatore']:
        df[f'Haki_{t}'] = df['Haki_List'].apply(lambda x: 1 if t in x else 0)
    df['Senza_Haki'] = df['Haki_List'].apply(lambda x: 1 if len(x) == 0 else 0)

    # 2. Gestione Bounty
    df['Bounty'] = df['Bounty'].replace('Incerto', -1).astype(float)
    df['Taglia_Senza_Taglia'] = (df['Bounty'] == 0).astype(int)
    df['Taglia_Rookie'] = ((df['Bounty'] > 0) & (df['Bounty'] < 100000000)).astype(int)
    df['Taglia_Veterano'] = ((df['Bounty'] >= 100000000) & (df['Bounty'] < 1000000000)).astype(int)
    df['Taglia_Elite'] = (df['Bounty'] >= 1000000000).astype(int)

    # 3. Gestione Booleani e Categorie
    df['Ha_Frutto'] = df['Ha_Frutto'].astype(int)
    df['Possiede_la_D'] = df['Possiede_la_D'].astype(int)

    # 4. Dummy Encoding (One-Hot) per le nuove feature
    categorical_cols = ['Fazione', 'Tipo_Frutto', 'Razza', 'Ruolo']
    df_final = pd.get_dummies(df, columns=categorical_cols, prefix=['Fac', 'Fruit', 'Race', 'Role'], dtype=int)

    # 5. Pulizia
    df_final = df_final.drop(['Haki_List', 'Grado_Importanza'], axis=1)
    df_final.to_csv(proc_path, index=False)
    print(f"✅ Preprocessing completato: {df_final.shape[1]} feature generate.")

if __name__ == "__main__": preprocess()