# Will of Data: One Piece Grid Logic & Rarity Predictor 🏴‍☠️📊

## 🎯 Obiettivo
Sviluppo di un sistema di Machine Learning in grado di risolvere una griglia di attributi (One Piece Grid Game) ottimizzando la scelta del personaggio in base a criteri di pertinenza, rarità statistica e importanza narrativa.

## 🛠️ Pipeline di ML
1. **Data Engineering**: Gestione missing values ("Incerto") e feature encoding.
2. **Preprocessing**: Bilanciamento tramite Undersampling per preservare l'autenticità dei dati.
3. **Modeling**: Confronto tra classificatori (Random Forest vs XGBoost) per la predizione degli attributi.
4. **Scoring Engine**: Algoritmo di ranking basato su Distanza Probabilistica e Grado di Importanza.

## 📂 Dataset
Il dataset comprende personaggi del mondo di One Piece caratterizzati da fazioni, poteri (Frutti), Haki e taglie.
