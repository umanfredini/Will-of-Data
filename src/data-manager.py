import pandas as pd
import os

def create_directory():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)
    return data_dir

def generate_dataset():
    data_dir = create_directory()
    path = os.path.join(data_dir, "will_of_data_raw.csv")

    # [Nome, Fazione, Razza, Ruolo, Possiede_la_D, Ha_Frutto, Tipo_Frutto, Haki_List, Bounty, Grado_Importanza]
    characters = [
        # --- STRAW HAT CREW (Mugiwara) ---
        ["Luffy", "Pirata", "Umano", "Capitano", True, True, "Zoan", ["Armatura", "Percezione", "Imperatore"],
         "3000000000", 10],
        ["Zoro", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"],
         "1100100000", 10],
        ["Nami", "Pirata", "Umano", "Navigatore", False, False, "Nessuno", ["Percezione"], "366000000", 10],
        ["Usopp", "Pirata", "Umano", "Cecchino", False, False, "Nessuno", ["Percezione"], "500000000", 10],
        ["Sanji", "Pirata", "Umano", "Cuoco", False, False, "Nessuno", ["Armatura", "Percezione"], "1032000000", 10],
        ["Chopper", "Pirata", "Animale", "Medico", False, True, "Zoan", [], "1000", 10],
        ["Robin", "Pirata", "Umano", "Archeologo", False, True, "Paramecia", [], "930000000", 10],
        ["Franky", "Pirata", "Cyborg", "Carpentiere", False, False, "Nessuno", [], "394000000", 10],
        ["Brook", "Pirata", "Non-morto", "Musicista", False, True, "Paramecia", [], "383000000", 10],
        ["Jinbe", "Pirata", "Uomo-Pesce", "Timoniere", False, False, "Nessuno", ["Armatura", "Percezione"],
         "1100000000", 10],

        # --- RED HAIR PIRATES (Haki Masters) ---
        ["Shanks", "Pirata", "Umano", "Capitano", False, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"],
         "4048900000", 10],
        ["Benn Beckman", "Pirata", "Umano", "Primo Ufficiale", False, False, "Nessuno", ["Armatura", "Percezione"],
         "Incerto", 9],
        ["Yasopp", "Pirata", "Umano", "Cecchino", False, False, "Nessuno", ["Percezione"], "Incerto", 8],
        ["Lucky Roux", "Pirata", "Umano", "Cuoco", False, False, "Nessuno", ["Armatura"], "Incerto", 8],
        ["Limejuice", "Pirata", "Umano", "Ufficiale", False, False, "Nessuno", ["Armatura", "Percezione"], "Incerto",
         7],
        ["Bonk Punch", "Pirata", "Umano", "Musicista", False, False, "Nessuno", ["Armatura"], "Incerto", 7],
        ["Monster", "Pirata", "Animale", "Musicista", False, False, "Nessuno", [], "Incerto", 6],
        ["Building Snake", "Pirata", "Umano", "Navigatore", False, False, "Nessuno", ["Armatura", "Percezione"],
         "Incerto", 7],
        ["Hongo", "Pirata", "Umano", "Medico", False, False, "Nessuno", ["Percezione"], "Incerto", 7],
        ["Howling Gab", "Pirata", "Umano", "Ufficiale", False, False, "Nessuno", ["Armatura"], "Incerto", 7],

        # --- BLACKBEARD PIRATES (Titanic Captains) ---
        ["Blackbeard", "Pirata", "Umano", "Capitano", True, True, "Logia", ["Armatura", "Percezione"], "3996000000",
         10],
        ["Shiryu", "Pirata", "Umano", "Spadaccino", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 8],
        ["Van Augur", "Pirata", "Umano", "Cecchino", False, True, "Paramecia", ["Percezione"], "Incerto", 7],
        ["Burgess", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", ["Armatura"], "Incerto", 7],
        ["Laffitte", "Pirata", "Umano", "Navigatore", False, True, "Incerto", ["Percezione"], "Incerto", 7],
        ["Kuzan", "Pirata", "Umano", "Ufficiale", False, True, "Logia", ["Armatura", "Percezione"], "Incerto", 9],
        ["Doc Q.", "Pirata", "Umano", "Medico", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 7],
        ["Catarina Devon", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "Incerto",
         7],
        ["Vasco Shot", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto",
         7],
        ["Sanjuan Wolf", "Pirata", "Gigante", "Ufficiale", False, True, "Paramecia", [], "Incerto", 6],
        ["Avalo Pizarro", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"],
         "Incerto", 7],

        # --- WHITEBEARD PIRATES ---
        ["Whitebeard", "Pirata", "Umano", "Capitano", False, True, "Paramecia",
         ["Armatura", "Percezione", "Imperatore"], "5046000000", 10],
        ["Marco", "Pirata", "Umano", "Medico", False, True, "Zoan", ["Armatura", "Percezione"], "1374000000", 9],
        ["Ace", "Pirata", "Umano", "Comandante", True, True, "Logia", ["Armatura", "Percezione", "Imperatore"],
         "550000000", 9],
        ["Jozu", "Pirata", "Umano", "Comandante", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 8],
        ["Vista", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"], "Incerto", 8],
        ["Thatch", "Pirata", "Umano", "Cuoco", False, False, "Nessuno", ["Armatura"], "Incerto", 7],
        ["Haruta", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Percezione"], "Incerto", 7],
        ["Atmos", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura"], "Incerto", 7],
        ["Namur", "Pirata", "Uomo-Pesce", "Ufficiale", False, False, "Nessuno", ["Armatura"], "Incerto", 7],
        ["Blenheim", "Pirata", "Umano", "Ufficiale", False, False, "Nessuno", ["Armatura"], "Incerto", 7],

        # --- BEAST PIRATES (Kaido) ---
        ["Kaido", "Pirata", "Umano", "Capitano", False, True, "Zoan", ["Armatura", "Percezione", "Imperatore"],
         "4611100000", 10],
        ["King", "Pirata", "Lunaria", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "1390000000", 8],
        ["Queen", "Pirata", "Cyborg", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "1320000000", 8],
        ["Jack", "Pirata", "Uomo-Pesce", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "1000000000", 7],
        ["Yamato", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione", "Imperatore"],
         "Incerto", 9],
        ["Who's-Who", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "546000000", 8],
        ["Black Maria", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "480000000",
         8],
        ["Sasaki", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "472000000", 8],
        ["Ulti", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "400000000", 8],
        ["Page One", "Pirata", "Umano", "Ufficiale", False, True, "Zoan", ["Armatura", "Percezione"], "290000000", 7],

        # --- BIG MOM PIRATES ---
        ["Big Mom", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione", "Imperatore"],
         "4388000000", 10],
        ["Katakuri", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione", "Imperatore"],
         "1057000000", 9],
        ["Smoothie", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"], "932000000",
         8],
        ["Cracker", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"], "860000000",
         8],
        ["Perospero", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"], "700000000",
         7],
        ["Oven", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", ["Armatura", "Percezione"], "300000000", 8],
        ["Daifuku", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", ["Armatura", "Percezione"], "300000000",
         8],
        ["Mont-d'Or", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", [], "120000000", 7],

        # --- DONQUIXOTE FAMILY (Dressrosa) ---
        ["Doflamingo", "Pirata", "Umano", "Capitano", False, True, "Paramecia",
         ["Armatura", "Percezione", "Imperatore"], "340000000", 9],
        ["Trebol", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 7],
        ["Diamante", "Pirata", "Umano", "Spadaccino", False, True, "Paramecia", ["Armatura", "Percezione"], "99000000",
         7],
        ["Pica", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", ["Armatura", "Percezione"], "99000000", 7],
        ["Sugar", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", [], "Incerto", 8],
        ["Lao G", "Pirata", "Umano", "Lottatore", False, False, "Nessuno", [], "Incerto", 7],
        ["Senor Pink", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", [], "Incerto", 7],
        ["Dellinger", "Pirata", "Uomo-Pesce", "Lottatore", False, False, "Nessuno", [], "Incerto", 6],
        ["Giolla", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", [], "Incerto", 6],
        ["Machvise", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", [], "Incerto", 6],

        # --- CROSS GUILD & WARLORDS ---
        ["Buggy", "Pirata", "Umano", "Capitano", False, True, "Paramecia", [], "3189000000", 10],
        ["Crocodile", "Pirata", "Umano", "Capitano", False, True, "Logia", ["Armatura", "Percezione"], "1965000000", 9],
        ["Mihawk", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"], "3590000000",
         10],
        ["Hancock", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione", "Imperatore"],
         "1659000000", 9],
        ["Moria", "Pirata", "Umano", "Capitano", False, True, "Paramecia", [], "320000000", 8],

        # --- WORST GENERATION & ALLIES ---
        ["Law", "Pirata", "Umano", "Capitano", True, True, "Paramecia", ["Armatura", "Percezione"], "3000000000", 10],
        ["Kid", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione", "Imperatore"],
         "3000000000", 9],
        ["Killer", "Pirata", "Umano", "Combattente", False, False, "Nessuno", ["Armatura", "Percezione"], "484000000",
         8],
        ["Jewelry Bonney", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione"],
         "320000000", 9],
        ["X Drake", "Marine", "Umano", "Vice-Ammiraglio", False, True, "Zoan", ["Armatura", "Percezione"], "222000000",
         8],
        ["Capone Bege", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione"],
         "350000000", 8],
        ["Basil Hawkins", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione"],
         "320000000", 8],
        ["Scratchmen Apoo", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura", "Percezione"],
         "350000000", 8],
        ["Urouge", "Pirata", "Umano", "Capitano", False, True, "Paramecia", ["Armatura"], "108000000", 8],
        ["Bepo", "Pirata", "Animale", "Navigatore", False, False, "Nessuno", ["Armatura"], "500", 6],

        # --- WANO SAMURAI (The Nine Red Scabbards) ---
        ["Oden", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"],
         "3500000000", 10],
        ["Kin'emon", "Pirata", "Umano", "Spadaccino", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto",
         8],
        ["Denjiro", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"], "Incerto", 8],
        ["Raizo", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto", 7],
        ["Ashura Doji", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"], "Incerto",
         8],
        ["Okiku", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"], "Incerto", 8],
        ["Kawamatsu", "Pirata", "Uomo-Pesce", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"],
         "Incerto", 7],
        ["Hyougorou", "Civile", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura"], "0", 7],
        ["Shinobu", "Civile", "Umano", "Ufficiale", False, True, "Paramecia", [], "0", 7],
        ["Kanjuro", "Pirata", "Umano", "Spadaccino", False, True, "Paramecia", ["Armatura", "Percezione"], "Incerto",
         8],
        ["Momonosuke", "Civile", "Umano", "Capitano", False, True, "Zoan", ["Percezione"], "0", 9],

        # --- REVOLUTIONARY ARMY ---
        ["Dragon", "Rivoluzionario", "Umano", "Capitano", True, True, "Incerto", ["Incerto"], "Incerto", 10],
        ["Sabo", "Rivoluzionario", "Umano", "Capo di Stato Maggiore", False, True, "Logia", ["Armatura", "Percezione"],
         "602000000", 9],
        ["Ivankov", "Rivoluzionario", "Umano", "Comandante", False, True, "Paramecia", ["Armatura", "Percezione"],
         "Incerto", 8],
        ["Inazuma", "Rivoluzionario", "Umano", "Ufficiale", False, True, "Paramecia", [], "Incerto", 6],
        ["Karasu", "Rivoluzionario", "Umano", "Comandante", False, True, "Logia", ["Armatura", "Percezione"],
         "400000000", 7],
        ["Morley", "Rivoluzionario", "Gigante", "Comandante", False, True, "Paramecia", ["Armatura"], "293000000", 4],
        ["Belo Betty", "Rivoluzionario", "Umano", "Comandante", False, True, "Paramecia", ["Percezione"], "457000000",
         7],
        ["Lindbergh", "Rivoluzionario", "Animale", "Comandante", False, False, "Nessuno", ["Percezione"], "316000000",
         7],
        ["Koala", "Rivoluzionario", "Umano", "Ufficiale", False, False, "Nessuno", ["Armatura"], "Incerto", 6],
        ["Hack", "Rivoluzionario", "Uomo-Pesce", "Ufficiale", False, False, "Nessuno", ["Armatura"], "Incerto", 6],

        # --- MARINE ---
        ["Akainu", "Marine", "Umano", "Ammiraglio della Flotta", False, True, "Logia", ["Armatura", "Percezione"], "0",
         10],
        ["Kizaru", "Marine", "Umano", "Ammiraglio", False, True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Fujitora", "Marine", "Umano", "Ammiraglio", False, True, "Paramecia", ["Armatura", "Percezione"], "0", 10],
        ["Aramaki", "Marine", "Umano", "Ammiraglio", False, True, "Logia", ["Armatura", "Percezione"], "0", 10],
        ["Sengoku", "Marine", "Umano", "Ex-Ammiraglio della Flotta", False, True, "Zoan",
         ["Armatura", "Percezione", "Imperatore"], "0", 10],
        ["Garp", "Marine", "Umano", "Vice-Ammiraglio", True, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"],
         "0", 10],
        ["Tsuru", "Marine", "Umano", "Vice-Ammiraglio", False, True, "Paramecia", ["Armatura", "Percezione"], "0", 8],
        ["Momonga", "Marine", "Umano", "Vice-Ammiraglio", False, False, "Nessuno", ["Armatura", "Percezione"], "0", 7],
        ["Onigumo", "Marine", "Umano", "Vice-Ammiraglio", False, True, "Zoan", ["Armatura", "Percezione"], "0", 7],
        ["Smoker", "Marine", "Umano", "Vice-Ammiraglio", False, True, "Logia", ["Armatura", "Percezione"], "0", 8],
        ["Tashigi", "Marine", "Umano", "Ufficiale", False, False, "Nessuno", ["Armatura", "Percezione"], "0", 7],
        ["Koby", "Marine", "Umano", "Capitano", False, False, "Nessuno", ["Percezione", "Armatura"], "0", 7],
        ["Helmeppo", "Marine", "Umano", "Capitano", False, False, "Nessuno", ["Percezione", "Armatura"], "0", 5],
        ["Sentomaru", "Marine", "Umano", "Lottatore", False, False, "Nessuno", ["Armatura"], "0", 7],
        ["Vergo", "Marine", "Umano", "Ufficiale", False, False, "Nessuno", ["Armatura", "Percezione"], "0", 8],
        ["T-Bone", "Marine", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura"], "0", 6],
        ["Rosinante", "Marine", "Umano", "Ufficiale", False, True, "Paramecia", [], "0", 8],

        # --- WORLD GOVERNMENT & CP ---
        ["Imu", "Governo Mondiale", "Incerto", "Sovrano", False, True, "Incerto", ["Imperatore"], "0", 10],
        ["Saturn", "Governo Mondiale", "Demone", "Gosei", False, True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Mars", "Governo Mondiale", "Demone", "Gosei", False, True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Warcury", "Governo Mondiale", "Demone", "Gosei", False, True, "Incerto",
         ["Armatura", "Percezione", "Imperatore"], "0", 10],
        ["Nusjuro", "Governo Mondiale", "Demone", "Gosei", False, True, "Incerto", ["Armatura", "Percezione"], "0", 10],
        ["Ju Peter", "Governo Mondiale", "Demone", "Gosei", False, True, "Incerto", ["Armatura", "Percezione"], "0", 9],
        ["Garling", "Governo Mondiale", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione"],
         "0", 9],
        ["Rob Lucci", "Governo Mondiale", "Umano", "Agente CP0", False, True, "Zoan", ["Armatura", "Percezione"], "0",
         9],
        ["Kaku", "Governo Mondiale", "Umano", "Agente CP0", False, True, "Zoan", ["Armatura", "Percezione"], "0", 7],
        ["Stussy", "Governo Mondiale", "Cyborg", "Agente CP0", False, True, "Paramecia", ["Armatura", "Percezione"],
         "0", 8],
        ["Magellan", "Governo Mondiale", "Umano", "Ufficiale", False, True, "Paramecia", ["Armatura", "Percezione"],
         "0", 9],
        ["Hannyabal", "Governo Mondiale", "Umano", "Ufficiale", False, False, "Nessuno", [], "0", 7],
        ["Jabura", "Governo Mondiale", "Umano", "Agente CP9", False, True, "Zoan", ["Armatura", "Percezione"], "0", 7],
        ["Kalifa", "Governo Mondiale", "Umano", "Agente CP9", False, True, "Paramecia", ["Armatura", "Percezione"], "0",
         7],
        ["Blueno", "Governo Mondiale", "Umano", "Agente CP9", False, True, "Paramecia", ["Armatura", "Percezione"], "0",
         7],

        # --- SKYPIEA SAGA (Angeli) ---
        ["Enel", "Pirata", "Angelo", "Capitano", False, True, "Logia", ["Percezione"], "Incerto", 9],
        ["Wyper", "Civile", "Angelo", "Lottatore", False, False, "Nessuno", [], "0", 7],
        ["Gan Fall", "Civile", "Angelo", "Sovrano", False, False, "Nessuno", [], "0", 7],
        ["Braham", "Civile", "Angelo", "Cecchino", False, False, "Nessuno", [], "0", 6],
        ["Ohm", "Civile", "Angelo", "Spadaccino", False, False, "Nessuno", ["Percezione"], "0", 6],
        ["Satori", "Civile", "Angelo", "Ufficiale", False, False, "Nessuno", ["Percezione"], "0", 6],

        # --- THRILLER BARK SAGA (Gothic Horror) ---
        ["Moria", "Pirata", "Umano", "Capitano", False, True, "Paramecia", [], "320000000", 8],
        ["Perona", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", [], "Incerto", 7],
        ["Ryuma", "Pirata", "Non-morto", "Spadaccino", False, False, "Nessuno", ["Armatura"], "Incerto", 9],
        ["Dr. Hogback", "Pirata", "Umano", "Medico", False, False, "Nessuno", [], "Incerto", 6],
        ["Absalom", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", [], "Incerto", 6],
        ["Oars", "Pirata", "Gigante", "Lottatore", False, False, "Nessuno", [], "Incerto", 8],

        # --- CIVILIANS & SPECIAL LINKS ---
        ["Vegapunk", "Civile", "Umano", "Scienziato", False, True, "Paramecia", [], "0", 10],
        ["Vivi", "Civile", "Umano", "Principessa", False, False, "Nessuno", [], "0", 9],
        ["Makino", "Civile", "Umano", "Barista", False, False, "Nessuno", [], "0", 3],
        ["Dadan", "Civile", "Umano", "Bandito", False, False, "Nessuno", [], "Incerto", 4],
        ["Iceburg", "Civile", "Umano", "Sindaco", False, False, "Nessuno", [], "0", 6],
        ["Tom", "Civile", "Uomo-Pesce", "Carpentiere", False, False, "Nessuno", [], "0", 7],
        ["Zeff", "Civile", "Umano", "Cuoco", False, False, "Nessuno", [], "Incerto", 7],
        ["Dr. Kureha", "Civile", "Umano", "Medico", False, False, "Nessuno", [], "0", 6],
        ["Dr. Hiriluk", "Civile", "Umano", "Medico", False, False, "Nessuno", [], "0", 5],
        ["Jaguar D. Saul", "Civile", "Gigante", "Ex-Marine", True, False, "Nessuno", [], "Incerto", 6],
        ["Olvia", "Civile", "Umano", "Archeologo", False, False, "Nessuno", [], "79000000", 6],
        ["Claud D. Clover", "Civile", "Umano", "Archeologo", True, False, "Nessuno", [], "0", 6],
        ["Belle-mere", "Civile", "Umano", "Ufficiale", False, False, "Nessuno", [], "0", 5],
        ["Kuina", "Civile", "Umano", "Spadaccino", False, False, "Nessuno", [], "0", 4],
        ["Toki", "Civile", "Umano", "Navigatore", False, True, "Paramecia", [], "0", 7],

        # --- BAROQUE WORKS & OTHERS ---
        ["Bentham", "Pirata", "Umano", "Lottatore", False, True, "Paramecia", [], "32000000", 8],
        ["Daz Bonez", "Pirata", "Umano", "Spadaccino", False, True, "Paramecia", ["Armatura"], "75000000", 7],
        ["Galdino", "Pirata", "Umano", "Ufficiale", False, True, "Paramecia", [], "24000000", 7],

        # --- GIANTS & TONTATTA (Mink/Nan/Gig) ---
        ["Dorry", "Pirata", "Gigante", "Capitano", False, False, "Nessuno", ["Armatura"], "100000000", 8],
        ["Brogy", "Pirata", "Gigante", "Capitano", False, False, "Nessuno", ["Armatura"], "100000000", 8],
        ["Hajrudin", "Pirata", "Gigante", "Capitano", False, False, "Nessuno", ["Armatura"], "Incerto", 7],
        ["Leo", "Pirata", "Nano", "Capitano", False, True, "Paramecia", ["Armatura"], "Incerto", 7],
        ["Mansherry", "Civile", "Nano", "Medico", False, True, "Paramecia", [], "0", 7],

        # --- LEGENDS & "D." FAMILY ---
        ["Gol D. Roger", "Pirata", "Umano", "Capitano", True, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "5564800000", 10],
        ["Rocks D. Xebec", "Pirata", "Umano", "Capitano", True, True, "Incerto", ["Armatura", "Percezione", "Imperatore"], "Incerto", 10],
        ["Silvers Rayleigh", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "Incerto", 10],
        ["Scopper Gaban", "Pirata", "Umano", "Spadaccino", False, False, "Nessuno", ["Armatura", "Percezione", "Imperatore"], "Incerto", 9],
        ["Nefertari D. Cobra", "Civile", "Umano", "Sovrano", True, False, "Nessuno", [], "0", 7],
        ["Portgas D. Rouge", "Civile", "Umano", "Medico", True, False, "Nessuno", [], "0", 5],
        ["Trafalgar D. Lami", "Civile", "Umano", "Medico", True, False, "Nessuno", [], "0", 4],
    ]


    columns = ["Nome", "Fazione", "Razza", "Ruolo", "Possiede_la_D", "Ha_Frutto", "Tipo_Frutto", "Haki_List", "Bounty", "Grado_Importanza"]
    df = pd.DataFrame(characters, columns=columns)
    df.to_csv(path, index=False)
    print(f"✅ Dataset Completo ({len(characters)} personaggi) creato in: {path}")

if __name__ == "__main__": generate_dataset()