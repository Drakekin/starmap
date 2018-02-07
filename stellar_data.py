import csv
import json
import random
from collections import defaultdict

from stellar_obj import Star, Planet
from util import unique

SPECIAL_NAMES = {71681: "Alpha Centauri A", 71683: "Alpha Centauri B",
                 54035: "Lalande 21185", 16537: "Epsilon Eridani", 114046: "Lacaille 9352",
                 91772: "Struve 2398 A", 104214: "61 Cygni A", 104217: "61 Cygni B",
                 91768: "Struve 2398 B", 110893: "Kruger 60", 106440: "Gliese 832",
                 88601: "70 Ophiuchi", 677: 'Alpheratz', 746: 'Caph', 1067: 'Algenib',
                 2081: 'Ankaa', 2920: 'Fulu', 3179: 'Schedar', 3419: 'Diphda',
                 3821: 'Achird', 4422: 'Castula', 5447: 'MIRACH', 5348: 'Wurren',
                 5737: 'Revati', 6411: 'Adhil', 6686: 'Ruchbah', 11767: 'Polaris',
                 7097: 'Alpherg', 7513: 'Titawin', 7607: 'Nembus', 7588: 'Achernar',
                 8198: 'Torcular', 8645: 'Baten Kaitos', 8886: 'Segin', 8796: 'Mothallah',
                 8832: 'Mesarthim', 8903: 'Sheratan', 9487: 'Alrescha', 9640: 'Almach',
                 9884: 'Hamal', 10826: 'Mira', 12706: 'Kaffaljidhma', 13061: 'Lilii Borea',
                 13268: 'Miram', 13209: 'Bharani', 13288: 'Angetenar', 13701: 'Azha',
                 13879: 'Gorgonea Secunda', 13847: 'Acamar', 14135: 'Menkar',
                 14354: 'Gorgonea Tertia', 14576: 'Algol', 14668: 'Misam',
                 14817: 'Gorgonea Quarta', 14838: 'Botein', 15197: 'Zibal', 15863: 'Mirfak',
                 17448: 'Atik', 17378: 'Rana', 17489: 'Celaeno', 17499: 'Electra',
                 17531: 'Taygeta', 17573: 'Maia', 17579: 'Asterope', 17608: 'Merope',
                 17702: 'Alcyone', 17847: 'Atlas', 17851: 'Pleione', 18614: 'Menkhib',
                 18543: 'Zaurak', 19587: 'Beid', 19849: 'Keid', 20205: 'Prima Hyadum',
                 20455: 'Secunda Hyadum', 20535: 'Beemim', 20889: 'Ain', 20894: 'Chamukuy',
                 21421: 'Aldebaran', 21393: 'Theemin', 21594: 'Sceptrum', 22449: 'Tabit',
                 23015: 'Hassaleh', 23416: 'Almaaz', 23453: 'Saclateni', 23767: 'Haedus',
                 23875: 'Cursa', 24186: 'Kapteyn', 24608: 'Capella', 24436: 'Rigel',
                 25336: 'Bellatrix', 25428: 'Elnath', 25606: 'Nihal', 25930: 'Mintaka',
                 25985: 'Arneb', 26207: 'Meissa', 26241: 'Hatysa', 26311: 'Alnilam',
                 26451: 'Tianguan', 26727: 'Alnitak', 26634: 'Phact', 27366: 'Saiph',
                 27628: 'Wazn', 27989: 'Betelgeuse', 28041: "Gore's Nova",
                 28360: 'Menkalinan', 28380: 'Mahasim', 29655: 'Propus', 30122: 'Furud',
                 30343: 'Tejat', 30324: 'Mirzam', 30438: 'Canopus', 31681: 'Alhena',
                 31685: 'Kaimana', 32246: 'Mebsuta', 32362: 'Alzirr', 32349: 'Sirius',
                 32768: 'Altaleban', 33579: 'Adhara', 33856: 'Unurgunite', 34088: 'Mekbuda',
                 34045: 'Muliphein', 34444: 'Wezen', 35264: 'Ahadi', 35550: 'Wasat',
                 35904: 'Aludra', 36188: 'Gomeisa', 36369: 'Eskimo', 36377: 'Hadir',
                 36850: 'Castor', 37265: 'Jishui', 37279: 'Procyon', 37229: 'Markeb',
                 37826: 'Pollux', 38170: 'Asmidiske', 39429: 'Naos', 39757: 'Tureis',
                 40167: 'Tegmine', 39953: 'Regor', 40526: 'Altarf', 41075: 'Alsciaukat',
                 41037: 'Avior', 41704: 'Muscida', 42402: 'Minchir', 42556: 'Meleph',
                 42806: 'Asellus Borealis', 42911: 'Asellus Australis', 43587: 'Copernicus',
                 44127: 'Talitha', 44066: 'Acubens', 44471: 'Alkaphrah', 44816: 'Suhail',
                 45238: 'Miaplacidus', 45556: 'Aspidiske', 46471: 'Intercrus',
                 46390: 'Alphard', 46750: 'Alterf', 47508: 'Subra', 48356: 'Zhang',
                 48455: 'Rasalas', 49669: 'Regulus', 50372: 'Tania Borealis',
                 50335: 'Adhafera', 50583: 'Algieba', 50801: 'Tania Australis',
                 53229: 'Praecipua', 53721: 'Chalawan', 53740: 'Alkes', 53910: 'Merak',
                 54061: 'Dubhe', 54872: 'Zosma', 54879: 'Chertan', 55219: 'Alula Borealis',
                 56211: 'Giausar', 56709: "Przybylski's Star", 57399: 'Alkafzah',
                 57632: 'Denebola', 57757: 'Zavijava', 58001: 'Phecda', 58952: 'Tonatiuh',
                 59199: 'Alchiba', 59316: 'Minkar', 59774: 'Megrez', 59803: 'Gienah Corvi',
                 60129: 'Zaniah', 60260: 'Ginan', 60965: 'Algorab', 61084: 'Gacrux',
                 61317: 'Chara', 61359: 'Kraz', 61941: 'Porrima', 62223: 'La Superba',
                 62434: 'Mimosa', 62423: 'Tianyi', 62956: 'Alioth', 63090: 'Minelauva',
                 63125: 'Cor Caroli', 63076: 'Taiyi', 63608: 'Vindemiatrix',
                 64241: 'Diadem', 65378: 'Mizar', 65474: 'Spica', 65477: 'Alcor',
                 66249: 'Heze', 67301: 'Alkaid', 67927: 'Muphrid', 68702: 'Agena',
                 68933: 'Menkent', 68756: 'Thuban', 69427: 'Kang', 69701: 'Syrma',
                 69673: 'Arcturus', 69732: 'Xuange', 69974: 'Khambalia',
                 70553: "Preston's Star", 71075: 'Seginus', 72105: 'Izar',
                 72622: 'Zubenelgenubi', 72487: 'Merga', 72607: 'Kochab', 73555: 'Nekkar',
                 73714: 'Brachium', 74785: 'Zubeneschamali', 74793: 'Pherkad Minor',
                 75411: 'Alkalurops', 75097: 'Pherkad', 75458: 'Edasich', 75695: 'Nusakan',
                 76333: 'Zubenelhakrabi', 76267: 'Alphecca', 77070: 'Unukalhai',
                 77233: 'Chow', 78104: 'Iklil', 78265: 'Fang', 78401: 'Dschubba',
                 79374: 'Jabbah', 79593: 'Yed Prior', 79882: 'Yed Posterior',
                 80112: 'Alniyat', 80463: 'Cujam', 80331: 'Athebyne', 80763: 'Antares',
                 80816: 'Kornephoros', 80883: 'Marfik', 80838: 'Ogma', 82273: 'Atria',
                 82396: 'Larawag', 82514: 'Xamidimura', 82545: 'Pipirima', 83608: 'Alrakis',
                 84012: 'Sabik', 83895: 'Aldhibah', 84345: 'Rasalgethi', 84379: 'Sarin',
                 86284: 'MU OPH GROUP}', 86598: 'BPMG} member', 89769: 'Anon WR 113}',
                 92316: 'Nova Aquila No 3', 95947: 'Albereo', 85696: 'Lesath',
                 85693: 'Maasym', 85927: 'Shaula', 85670: 'Rastaban', 86228: 'Sargas',
                 86032: 'Rasalhague', 86796: 'Cervantes', 86742: 'Cebalrai', 87261: 'Fuyue',
                 86614: 'Dziban', 87585: 'Grumium', 87833: 'Etamin', 88635: 'Alnasl',
                 85822: 'Yildun', 89341: 'Polis', 89931: 'Kaus Media',
                 90185: 'Kaus Australis', 90191: 'Alathfar', 90496: 'Kaus Borealis',
                 90344: 'Fafnir', 91262: 'Vega', 92420: 'Sheliak', 92761: 'Ainalrami',
                 92855: 'Nunki', 93194: 'Sulafat', 93506: 'Ascella', 93427: 'Perky',
                 104382: 'Polaris Australis', 94114: 'Meridiana', 94141: 'Albaldah',
                 94481: 'Aladfar', 94376: 'Altais', 95241: 'Arkab Prior',
                 95294: 'Arkab Posterior', 95347: 'Rukbat', 95771: 'Anser', 96100: 'Alsafi',
                 96757: 'Sham', 97278: 'Tarazed', 97649: 'Altair', 97433: 'Tyl',
                 97938: 'Libertas', 98066: 'Terebellum', 98036: 'Alshain',
                 100027: 'Prima Giedi', 100064: 'Secunda Giedi', 100310: 'Alshat',
                 100325: 'Dabih Minor', 100345: 'Dabih Major', 100751: 'Peacock',
                 100453: 'SADR', 101421: 'Aldulfin', 101260: 'V73 Dra', 101769: 'Rotanev',
                 101958: 'Svalocin', 102098: 'Deneb', 102626: 'Speedy Mic',
                 102488: 'Aljanah', 102618: 'Albali', 103527: 'Musica', 104987: 'Kitalpha',
                 105090: 'Lacaille 8760', 105199: 'Alderamin', 106278: 'Sadalsuud',
                 106032: 'Alfirk', 106786: 'Bunda', 106985: 'Nashira', 107136: 'Azelfafage',
                 107315: 'Enif', 107556: 'Deneb Algedi', 108085: 'Al Dhanab',
                 109074: 'Sadalmelik', 108917: 'Kurhah', 109268: 'Alnair', 109427: 'Biham',
                 110003: 'Ancha', 110395: 'Sadachbia', 111710: 'Situla', 112029: 'Homam',
                 112122: 'Tiaki', 112158: 'Matar', 112748: 'Sadalbari', 113136: 'Skat',
                 113357: 'Helvetios', 113881: 'Scheat', 113963: 'Markab', 115250: 'Salm',
                 115623: 'Alkarab', 116076: 'Veritate', 116727: 'Errai', }


with open("starcatalogue.json") as json_catalogue:
    RAW_STARMAP = json.load(json_catalogue)["Stars"]

with open("starnames.csv") as csv_names:
    STARNAMES = [name.lower() for name, mag, ra, dec in csv.reader(csv_names)]
    STARNAME_MARKOV = defaultdict(lambda: [])
    for name in STARNAMES:
        for n, char in enumerate(name):
            STARNAME_MARKOV[name[max(0, n - 3):n]].append(char)
        STARNAME_MARKOV[name[-3:]].append(None)

with open("spectypes.json") as json_spec:
    STAR_CLASS = json.load(json_spec)

USED_STARNAMES = set()


@unique(USED_STARNAMES, limit=1000)
def get_star_name():
    name = ""
    while True:
        char = random.choice(STARNAME_MARKOV[name[max(0, len(name) - 3):]])
        if char is None:
            if len(name) < 3:
                continue
            return name.title()
        name += char


SOL = Star(0, 0, 0, 0, name="Sol", stellar_class="G8")
SOL._planets = [Planet(SOL, 0.72, 1e9, "Venus", 0), Planet(SOL, 1, 5e9, "Earth", 0), Planet(SOL, 1.6, 3e9, "Mars", 100),
                Planet(SOL, 2.5, 2e9, "Belt", 100),
                Planet(SOL, 5.2, 4e9, "Jupiter", 125), Planet(SOL, 9.5, 2e9, "Saturn", 130)]
STARMAP = [SOL]

for star in RAW_STARMAP:
    if abs(star["distance"]) > 750 or str(star["HIP"]) not in STAR_CLASS:
        continue
    s = Star(name=SPECIAL_NAMES.get(star['HIP']), stellar_class=STAR_CLASS[str(star["HIP"])], **star)
    x, y, z = s.position
    STARMAP.append(s)
