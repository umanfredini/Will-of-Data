import pandas as pd
import os

def create_directory():
    # Risale di un livello da src/ per trovare la root Will-of-Data/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def generate_dataset():
    data_dir = create_directory()
    path = os.path.join(data_dir, "will_of_data_raw.csv")

    characters = [
        # --- STRAW HAT CREW (Completata) ---
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

        # --- BLACKBEARD PIRATES (Titanic Captains aggiunti) ---
        ["Blackbeard", "Pirata", True, "Logia", ["Armatura", "Percezione"], "3996000000", 10],
        ["Shiryu", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 8],
        ["Van Augur", "Pirata", True, "Paramecia", ["Percezione"], "Incerto", 7],
        ["Burgess", "Pirata", True, "Paramecia", ["Armatura"], "Incerto", 7],
        ["Laffitte", "Pirata", True, "Incerto", ["Percezione"], "Incerto", 7],
        ["Kuzan", "Pirata", True, "Logia", ["Armatura", "Percezione"], "Incerto", 9],
        ["Doc Q.", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 7],
        ["Catarina Devon", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "Incerto", 7],
        ["Vasco Shot", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 7],
        ["Sanjuan Wolf", "Pirata", True, "Paramecia", [], "Incerto", 6],
        ["Avalo Pizarro", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 7],

        # --- CROSS GUILD ---
        ["Buggy", "Pirata", True, "Paramecia", [], "3189000000", 10],
        ["Crocodile", "Pirata", True, "Logia", ["Armatura", "Percezione"], "1965000000", 9],
        ["Mihawk", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "3590000000", 10],
        ["Alvida", "Pirata", True, "Paramecia", [], "5000000", 4],

        # --- ROGER PIRATES & OLD GENERATION ---
        ["Gol D. Roger", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "5564800000", 10],
        ["Rayleigh", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "Incerto", 10],
        ["Scopper Gaban", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "Incerto", 7],
        ["Shanks", "Pirata", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "4048900000", 10],
        ["Benn Beckman", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "Incerto", 9],

        # --- WHITEBEARD PIRATES ---
        ["Whitebeard", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "5046000000", 10],
        ["Marco", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "1374000000", 9],
        ["Ace", "Pirata", True, "Logia", ["Armatura", "Percezione"], "550000000", 9],
        ["Jozu", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 8],
        ["Vista", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "Incerto", 8],

        # --- BEAST PIRATES (KAIDO) ---
        ["Kaido", "Pirata", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "4611100000", 10],
        ["King", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "1390000000", 8],
        ["Queen", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "1320000000", 8],
        ["Jack", "Pirata", True, "Zoan", ["Armatura", "Percezione"], "1000000000", 7],
        ["Yamato", "Pirata", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "Incerto", 9],

        # --- BIG MOM PIRATES ---
        ["Big Mom", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "4388000000", 10],
        ["Katakuri", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "1057000000", 9],
        ["Smoothie", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "932000000", 8],
        ["Cracker", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "860000000", 8],
        ["Perospero", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "700000000", 7],

        # --- MARINE & WORLD GOVERNMENT (Espanso) ---
        ["Akainu", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Kizaru", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Fujitora", "Marine", True, "Paramecia", ["Armatura", "Percezione"], "0", 10],
        ["Aramaki", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Sengoku", "Marine", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "0", 10],
        ["Garp", "Marine", False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "0", 10],
        ["Tsuru", "Marine", True, "Paramecia", ["Armatura", "Percezione"], "0", 8],
        ["Koby", "Marine", False, "Nessuno", ["Percezione", "Armatura"], "0", 7],
        ["Helmeppo", "Marine", False, "Nessuno", ["Percezione", "Armatura"], "0", 5],
        ["Smoker", "Marine", True, "Logia", ["Armatura", "Percezione"], "0", 8],
        ["Tashigi", "Marine", False, "Nessuno", ["Armatura", "Percezione"], "0", 7],
        ["Imu", "Governo Mondiale", True, "Incerto", ["Imperatore"], "0", 10],
        ["Saturn", "Governo Mondiale", True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Mars", "Governo Mondiale", True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Warcury", "Governo Mondiale", True, "Incerto", ["Armatura", "Percezione", "Imperatore"], "0", 10],
        ["Nusjuro", "Governo Mondiale", True, "Incerto", ["Armatura", "Percezione"], "0", 10],
        ["Ju Peter", "Governo Mondiale", True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Garling", "Governo Mondiale", False, "Nessuno", ["Armatura", "Percezione"], "0", 9],
        ["Rob Lucci", "Governo Mondiale", True, "Zoan", ["Armatura", "Percezione"], "0", 9],
        ["Kaku", "Governo Mondiale", True, "Zoan", ["Armatura", "Percezione"], "0", 7],

        # --- REVOLUTIONARY ARMY (Bilanciato) ---
        ["Dragon", "Rivoluzionario", True, "Incerto", ["Incerto"], "Incerto", 10],
        ["Sabo", "Rivoluzionario", True, "Logia", ["Armatura", "Percezione"], "602000000", 9],
        ["Ivankov", "Rivoluzionario", True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 8],
        ["Inazuma", "Rivoluzionario", True, "Paramecia", [], "Incerto", 6],
        ["Karasu", "Rivoluzionario", True, "Logia", ["Armatura", "Percezione"], "400000000", 7],
        ["Morley", "Rivoluzionario", True, "Paramecia", ["Armatura"], "293000000", 4],
        ["Belo Betty", "Rivoluzionario", True, "Paramecia", ["Percezione"], "457000000", 7],
        ["Lindbergh", "Rivoluzionario", False, "Nessuno", ["Percezione"], "316000000", 7],
        ["Koala", "Rivoluzionario", False, "Nessuno", ["Armatura"], "Incerto", 6],

        # --- ALTRI PROTAGONISTI / RIVALI ---
        ["Law", "Pirata", True, "Paramecia", ["Armatura", "Percezione"], "3000000000", 10],
        ["Bepo", "Pirata", False, "Nessuno", ["Armatura"], "500", 6],
        ["Kid", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "3000000000", 9],
        ["Killer", "Pirata", False, "Nessuno", ["Armatura", "Percezione"], "484000000", 8],
        ["Hancock", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "1659000000", 9],
        ["Doflamingo", "Pirata", True, "Paramecia", ["Armatura", "Percezione", "Imperatore"], "340000000", 9],
        ["Moria", "Pirata", True, "Paramecia", [], "320000000", 8],
        ["Vegapunk", "Civile", True, "Paramecia", [], "0", 10],
        ["Vivi", "Civile", False, "Nessuno", [], "0", 9],
        ["Loki", "Civile", True, "Zoan", ["Armatura", "Percezione", "Imperatore"], "2600000000", 10],
    ]

    columns = ["Nome", "Fazione", "Ha_Frutto", "Tipo_Frutto", "Haki_List", "Bounty", "Grado_Importanza"]
    df = pd.DataFrame(characters, columns=columns)

    df.to_csv(path, index=False)
    print(f"✅ Dataset creato in: {path}")

if __name__ == "__main__":
    generate_dataset()