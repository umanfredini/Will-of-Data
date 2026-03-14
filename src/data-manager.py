import pandas as pd
import os


def create_directory():
    if not os.path.exists('data'):
        os.makedirs('data')


def generate_dataset():
    # Struttura: Nome, Fazione, Ha_Frutto, Tipo_Frutto, Haki_List, Bounty, Grado_Imp
    # Nota: Bounty "0" = Valore reale nullo | "Incerto" = Valore esistente ma ignoto
    characters = [
        # --- a. CIURMA DI CAPPELLO DI PAGLIA ---
        ["Luffy", "Pirata", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "3000000000", 10],
        ["Zoro", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "1100100000", 10],
        ["Nami", "Pirata", False, "Nessuno", [], "366000000", 10],
        ["Usopp", "Pirata", False, "Nessuno", ["Percezione"], "500000000", 10],
        ["Sanji", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "1032000000", 10],
        ["Chopper", "Pirata", True, "Zoan", [], "1000", 10],
        ["Robin", "Pirata", True, "Paramecia", [], "930000000", 10],
        ["Franky", "Pirata", False, "Nessuno", [], "394000000", 10],
        ["Brook", "Pirata", True, "Paramecia", [], "383000000", 10],
        ["Jinbe", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "1100000000", 10],

        # --- b. CIURMA DI BARBANERA ---
        ["Blackbeard", "Pirata", True, "Logia", ["Armatura", "Percezione"], "3996000000", 10],
        ["Shiryu", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 8],
        ["Van Augur", "Pirata", True, "Paramecia", ["Percezione"], "Incerto", 7],
        ["Burgess", "Pirata", True, "Paramecia", ["Armatura"], "Incerto", 7],
        ["Laffitte", "Pirata", True, "Incerto", ["Percezione"], "Incerto", 7],
        ["Kuzan", "Pirata", True, "Logia", ["Armatura", "Percezione"], "Incerto", 9],
        ["Doc Q.", "Pirata", True, "Logia", ["Armatura", "Percezione"], "Incerto", 9],

        # --- c. CIURMA DI BUGGY (CROSS GUILD) ---
        ["Buggy", "Pirata", True, "Paramecia", [], "3189000000", 10],
        ["Crocodile", "Pirata", True, "Logia", ["Armatura", "Percezione"], "1965000000", 9],
        ["Mihawk", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "3590000000", 10],
        ["Alvida", "Pirata", True, "Paramecia", [], "5000000", 4],

        # --- d, e, f. EAST BLUE & MARINES ---
        ["Jango", "Marine", False, "Nessuno", [], "0", 4],
        ["Smoker", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 8],
        ["Tashigi", "Marine", False, "Nessuno", ["Armatura", "Percezione"], "0", 7],
        ["Kuro", "Pirata", False, "Nessuno", [], "16000000", 5],
        ["Kaya", "Civile", False, "Nessuno", [], "0", 3],
        ["Merry", "Civile", False, "Nessuno", [], "0", 2],

        # --- g. CIURMA DI ROGER ---
        ["Gol D. Roger", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "5564800000", 10],
        ["Rayleigh", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "Incerto", 10],
        ["Scopper Gaban", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "Incerto", 7],

        # --- h, i. REGNI ---
        ["Cobra", "Civile", False, "Nessuno", [], "0", 7],
        ["Vivi", "Civile", False, "Nessuno", [], "0", 9],
        ["Pell", "Civile", True, "Zoan", [], "0", 5],
        ["Wapol", "Civile", True, "Paramecia", [], "0", 6],
        ["Hiriluk", "Civile", False, "Nessuno", [], "0", 5],
        ["Dr. Kureka", "Civile", False, "Nessuno", [], "0", 4],

        # --- j, l. FLOTTA DEI SETTE & BAROQUE WORKS ---
        ["Hancock", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "1659000000", 9],
        ["Doflamingo", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "340000000", 9],
        ["Moria", "Pirata", True, "Paramecia", [], "320000000", 8],
        ["Bon Kurei", "Pirata", True, "Paramecia", [], "32000000", 7],
        ["Galdino", "Pirata", True, "Paramecia", [], "24000000", 7],

        # --- k. KOBI & HELMEPPO ---
        ["Koby", "Marine", False, "Nessuno", ["Percezione", "Armatura", "Imperatore"], "0", 7],
        ["Helmeppo", "Marine", False, "Nessuno", ["Percezione", "Armatura"], "0", 5],

        # --- m, n. SHANKS & GIGANTI ---
        ["Shanks", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "4048900000", 10],
        ["Benn Beckman", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "Incerto", 9],
        ["Loki", "Civile", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "2600000000", 10],
        ["Dory", "Pirata", False, "Nessuno", [], "100000000", 7],
        ["Brogy", "Pirata", False, "Nessuno", [], "100000000", 7],

        # --- o, y. GOVERNO MONDIALE, ASTRI & CAVALIERI ---
        ["Imu", "Governo Mondiale", True, "Incerto", ["Imperatore"], "0", 10],
        ["Saturn", "Governo Mondiale", True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Garling", "Governo Mondiale", False, "Nessuno", ["Armatura", "Percezione"], "0", 9],

        # --- p, q. GEN. PEGGIORE & VEGAPUNK ---
        ["Law", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "3000000000", 10],
        ["Kid", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "3000000000", 9],
        ["Vegapunk", "Civile", True, "Paramecia", [], "0", 10],
        ["Lilith", "Civile", False, "Nessuno", [], "0", 8],

        # --- r. CP9 & CP0 ---
        ["Rob Lucci", "Governo Mondiale", True, "Zoan", ["Armatura", "Percezione"], "0", 9],
        ["Kaku", "Governo Mondiale", True, "Zoan", ["Armatura", "Percezione"], "0", 7],
        ["Guernica", "Governo Mondiale", False, "Nessuno", ["Armatura", "Percezione"], "0", 3],

        # --- s, t, u. IMPERATORI ---
        ["Whitebeard", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "5046000000", 10],
        ["Marco", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "1374000000", 9],
        ["Kaido", "Pirata", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "4611100000", 10],
        ["King", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "1390000000", 8],
        ["Big Mom", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "4388000000", 10],
        ["Katakuri", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "1057000000", 9],

        # --- v, w, x. GRANDE FLOTTA & AMAZZONI ---
        ["Leo", "Pirata", True, "Paramecia", ["Armatura"], "66000000", 6],
        ["Bartolomeo", "Pirata", True, "Paramecia", [], "200000000", 7],
        ["Sandersonia", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "40000000", 4],

        # --- z. MARINES & AMMIRAGLI ---
        ["Akainu", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Kizaru", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Fujitora", "Marine", True, "Paramecia", ["Armatura", "Percezione"], "0", 10],
        ["Sengoku", "Marine", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "0", 10],
        ["Garp", "Marine", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "0", 10],
    ]

    columns = ["Nome", "Fazione", "Ha_Frutto", "Tipo_Frutto", "Haki_List", "Bounty", "Grado_Importanza"]
    df = pd.DataFrame(characters, columns=columns)

    create_directory()
    df.to_csv("data/will_of_data_raw.csv", index=False)
    print(f"✅ Dataset creato con {len(df)} personaggi.")


if __name__ == "__main__":
    generate_dataset()