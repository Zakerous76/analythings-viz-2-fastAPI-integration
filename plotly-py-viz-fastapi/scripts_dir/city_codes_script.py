import json

# Convert city names to english
city_codes = {
    "adana": 1,
    "ADıYAMAN": 2,
    "AFYONKARAHiSAR": 3,
    "AĞRı": 4,
    "AMASYA": 5,
    "ANKARA": 6,
    "ANTALYA": 7,
    "ARTViN": 8,
    "AYDıN": 9,
    "BALıKESiR": 10,
    "BiLECiK": 11,
    "BiNGÖL": 12,
    "BiTLiS": 13,
    "BOLU": 14,
    "BURDUR": 15,
    "BURSA": 16,
    "ÇANAKKALE": 17,
    "ÇANKıRı": 18,
    "ÇORUM": 19,
    "DENiZLi": 20,
    "DiYARBAKıR": 21,
    "EDiRNE": 22,
    "ELAZıĞ": 23,
    "ERZiNCAN": 24,
    "ERZURUM": 25,
    "ESKiŞEHiR": 26,
    "GAZiANTEP": 27,
    "GiRESUN": 28,
    "GÜMÜŞHANE": 29,
    "HAKKARi": 30,
    "HATAY": 31,
    "iSPARTA": 32,
    "MERSiN": 33,
    "İÇEL": 33,
    "İSTANBUL": 34,
    "İZMiR": 35,
    "KARS": 36,
    "KASTAMONU": 37,
    "KAYSERi": 38,
    "kırklareli": 39,
    "KıRŞEHiR": 40,
    "KOCAELi": 41,
    "KONYA": 42,
    "KÜTAHYA": 43,
    "MALATYA": 44,
    "MANiSA": 45,
    "KAHRAMANMARAŞ": 46,
    "MARDiN": 47,
    "MUĞLA": 48,
    "MUŞ": 49,
    "NEVŞEHiR": 50,
    "NiĞDE": 51,
    "ORDU": 52,
    "RiZE": 53,
    "SAKARYA": 54,
    "SAMSUN": 55,
    "SiiRT": 56,
    "SiNOP": 57,
    "SiVAS": 58,
    "TEKiRDAĞ": 59,
    "TOKAT": 60,
    "TRABZON": 61,
    "TUNCELi": 62,
    "ŞANLıURFA": 63,
    "UŞAK": 64,
    "VAN": 65,
    "YOZGAT": 66,
    "ZONGULDAK": 67,
    "AKSARAY": 68,
    "BAYBURT": 69,
    "KARAMAN": 70,
    "KıRıKKALE": 71,
    "BATMAN": 72,
    "ŞıRNAK": 73,
    "BARTıN": 74,
    "ARDAHAN": 75,
    "iĞDıR": 76,
    "YALOVA": 77,
    "KARABÜK": 78,
    "KiLiS": 79,
    "OSMANiYE": 80,
    "DÜZCE": 81,
}
turkish_to_english = {
    "ç": "c",
    "ğ": "g",
    "ı": "i",
    "ö": "o",
    "ş": "s",
    "ü": "u",
    "i̇": "i",
    "Ç": "C",
    "Ğ": "G",
    "İ": "I",
    "Ö": "O",
    "Ş": "S",
    "Ü": "U",
    ".": "",
}


def replace_turkish_chars(text):
    text = text.lower()
    for turkish_char, english_char in turkish_to_english.items():
        text = text.replace(turkish_char, english_char)
    return text


def create_city_codes_json():
    city_codes_tr = {key.capitalize(): value for key, value in city_codes.items()}
    city_codes_en = {
        replace_turkish_chars(key): value for key, value in city_codes.items()
    }

    with open("../datasets/jsons/city_codes_tr.json", "w") as f:
        json.dump(city_codes_tr, f)

    with open("../datasets/jsons/city_codes_en.json", "w") as f:
        json.dump(city_codes_en, f)
