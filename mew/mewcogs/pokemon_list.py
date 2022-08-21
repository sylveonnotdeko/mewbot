import inspect
import aiohttp
import ujson
import subprocess
import discord
from mewcogs.json_files import FORMS
import re

# NATURES, BERRIES, & ITEMS, NOT POKEMON ---------------------------------------------
natlist = [
    "Lonely",
    "Brave",
    "Adamant",
    "Naughty",
    "Bold",
    "Relaxed",
    "Impish",
    "Lax",
    "Timid",
    "Hasty",
    "Jolly",
    "Naive",
    "Modest",
    "Mild",
    "Quiet",
    "Rash",
    "Calm",
    "Gentle",
    "Sassy",
    "Careful",
    "Bashful",
    "Quirky",
    "Serious",
    "Docile",
    "Hardy",
]

berryList = {
    "berry",
    "aguav-berry",
    "figy-berry",
    "iapapa-berry",
    "mago-berry",
    "wiki-berry",
    "sitrus-berry",
    "apicot-berry",
    "ganlon-berry",
    "lansat-berry",
    "liechi-berry",
    "micle-berry",
    "petaya-berry",
    "salac-berry",
    "starf-berry",
    "aspear-berry",
    "cheri-berry",
    "chesto-berry",
    "lum-berry",
    "pecha-berry",
    "persim-berry",
    "rawst-berry",
}

activeItemList = (
    "tart-apple",
    "sweet-apple",
    "sun-stone",
    "dusk-stone",
    "thunder-stone",
    "fire-stone",
    "ice-stone",
    "water-stone",
    "dawn-stone",
    "leaf-stone",
    "moon-stone",
    "shiny-stone",
    "evo-stone",
    "cracked-pot",
    "chipped-pot",
    "meltan-candy",
    "galarica-wreath",
    "galarica-cuff",
    "black-augurite",
    "peat-block",
)

# POKEMON THAT CAN SPAWN FROM FISHING AT DIFFERENT RARITIES --------------------------
common_water = [
    "Psyduck",
    "Poliwag",
    "Poliwhirl",
    "Tentacool",
    "Tentacruel",
    "Slowpoke",
    "Slowbro",
    "Seel",
    "Dewgong",
    "Shellder",
    "Krabby",
    "Kingler",
    "Horsea",
    "Goldeen",
    "Staryu",
    "Magikarp",
    "Chinchou",
    "Marill",
    "Wooper",
    "Qwilfish",
    "Remoraid",
    "Lotad",
    "Lombre",
    "Wingull",
    "Azurill",
    "Carvanha",
    "Wailmer",
    "Barboach",
    "Whiscash",
    "Corphish",
    "Crawdaunt",
    "Spheal",
    "Sealeo",
    "Clamperl",
    "Luvdisc",
    "Buizel",
    "Shellos",
    "Gastrodon",
    "Finneon",
    "Lumineon",
    "Mantyke",
    "Panpour",
    "Tympole",
    "Palpitoad",
    "Basculin",
    "Ducklett",
    "Frillish",
    "Binacle",
    "Barbaracle",
    "Skrelp",
    "Clauncher",
    "Clawitzer",
    "Wishiwashi",
    "Dewpider",
    "Araquanid",
    "Wimpod",
    "Pyukumuku",
    "Bruxish",
    "Chewtle",
    "Drednaw",
    "Arrokuda",
    "Barraskewda",
    "Qwilfish-hisui",
]

uncommon_water = [
    "Golduck",
    "Poliwrath",
    "Cloyster",
    "Seadra",
    "Seaking",
    "Starmie",
    "Omanyte",
    "Omastar",
    "Kabuto",
    "Kabutops",
    "Lanturn",
    "Azumarill",
    "Politoed",
    "Quagsire",
    "Corsola",
    "Octillery",
    "Mantine",
    "Ludicolo",
    "Pelipper",
    "Sharpedo",
    "Wailord",
    "Feebas",
    "Walrein",
    "Huntail",
    "Gorebyss",
    "Relicanth",
    "Floatzel",
    "Simipour",
    "Seismitoad",
    "Tirtouga",
    "Carracosta",
    "Swanna",
    "Jellicent",
    "Alomomola",
    "Dragalge",
    "Mareanie",
    "Toxapex",
    "Golisopod",
    "Cramorant",
    "Dracovish",
    "Arctovish",
    "Overqwil",
    "Basculegion",
]

rare_water = [
    "Squirtle",
    "Wartortle",
    "Dratini",
    "Dragonair",
    "Totodile",
    "Croconaw",
    "Slowking",
    "Kingdra",
    "Mudkip",
    "Marshtomp",
    "Milotic",
    "Piplup",
    "Prinplup",
    "Oshawott",
    "Dewott",
    "Froakie",
    "Frogadier",
    "Popplio",
    "Brionne",
    "Sobble",
    "Drizzile",
]

extremely_rare_water = [
    "Blastoise",
    "Gyarados",
    "Lapras",
    "Dragonite",
    "Feraligatr",
    "Swampert",
    "Empoleon",
    "Samurott",
    "Greninja",
    "Primarina",
    "Inteleon",
    "Samurott-hisui",
]

ultra_rare_water = [
    "Suicune",
    "Kyogre",
    "Palkia",
    "Phione",
    "Manaphy",
    "Keldeo",
    "Volcanion",
    "Tapu-fini",
]

# ALL REGIONAL FORMS -----------------------------------------------------------------
alolans = [
    "Rattata-alola",
    "Raticate-alola",
    "Raichu-alola",
    "Sandshrew-alola",
    "Sandslash-alola",
    "Vulpix-alola",
    "Ninetales-alola",
    "Diglett-alola",
    "Dugtrio-alola",
    "Meowth-alola",
    "Persian-alola",
    "Geodude-alola",
    "Graveler-alola",
    "Golem-alola",
    "Grimer-alola",
    "Muk-alola",
    "Exeggutor-alola",
    "Marowak-alola",
]

galarians = [
    "Meowth-galar",
    "Ponyta-galar",
    "Rapidash-galar",
    "Slowpoke-galar",
    "Farfetchd-galar",
    "Mr-mime-galar",
    "Corsola-galar",
    "Weezing-galar",
    "Zigzagoon-galar",
    "Linoone-galar",
    "Darumaka-galar",
    "Darmanitan-galar",
    "Yamask-galar",
    "Stunfisk-galar",
    "Slowking-galar",
    "Slowbro-galar",
]

hisuians = [
    "Arcanine-hisui",
    "Avalugg-hisui",
    "Braviary-hisui",
    "Decidueye-hisui",
    "Electrode-hisui",
    "Goodra-hisui",
    "Growlithe-hisui",
    "Lilligant-hisui",
    "Qwilfish-hisui",
    "Samurott-hisui",
    "Sliggoo-hisui",
    "Sneasel-hisui",
    "Syphlosion-hisui",
    "Typhlosion-hisui",
    "Voltorb-hisui",
    "Zoroark-hisui",
    "Zorua-hisui",
]

# ALL POKEMON SHOULD BE IN EXACTLY ONE OF THE FOLLOWING LISTS ------------------------
# basic pokemon that are not one of the other categories
pList = [
    "Skwovet",
    "Greedent",
    "Rookidee",
    "Corvisquire",
    "Corviknight",
    "Blipbug",
    "Dottler",
    "Orbeetle",
    "Nickit",
    "Thievul",
    "Gossifleur",
    "Eldegoss",
    "Wooloo",
    "Dubwool",
    "Chewtle",
    "Drednaw",
    "Yamper",
    "Boltund",
    "Rolycoly",
    "Carkol",
    "Coalossal",
    "Applin",
    "Flapple",
    "Appletun",
    "Silicobra",
    "Sandaconda",
    "Cramorant",
    "Arrokuda",
    "Barraskewda",
    "Toxel",
    "Toxtricity",
    "Toxtricity",
    "Sizzlipede",
    "Centiskorch",
    "Clobbopus",
    "Grapploct",
    "Sinistea",
    "Polteageist",
    "Hatenna",
    "Hattrem",
    "Hatterene",
    "Impidimp",
    "Morgrem",
    "Grimmsnarl",
    "Obstagoon",
    "Perrserker",
    "Cursola",
    "Sirfetchd",
    "Mr-rime",
    "Runerigus",
    "Milcery",
    "Alcremie",
    "Falinks",
    "Pincurchin",
    "Snom",
    "Frosmoth",
    "Stonjourner",
    "Eiscue",
    "Eiscue",
    "Indeedee",
    "Indeedee",
    "Morpeko",
    "Cufant",
    "Copperajah",
    "Dracozolt",
    "Arctozolt",
    "Dracovish",
    "Arctovish",
    "Duraludon",
    "Skwovet",
    "Greedent",
    "Rookidee",
    "Corvisquire",
    "Corviknight",
    "Blipbug",
    "Dottler",
    "Orbeetle",
    "Nickit",
    "Thievul",
    "Gossifleur",
    "Eldegoss",
    "Wooloo",
    "Dubwool",
    "Chewtle",
    "Drednaw",
    "Yamper",
    "Boltund",
    "Rolycoly",
    "Carkol",
    "Coalossal",
    "Applin",
    "Flapple",
    "Appletun",
    "Silicobra",
    "Sandaconda",
    "Cramorant",
    "Arrokuda",
    "Barraskewda",
    "Toxel",
    "Toxtricity",
    "Toxtricity",
    "Sizzlipede",
    "Centiskorch",
    "Clobbopus",
    "Grapploct",
    "Sinistea",
    "Polteageist",
    "Hatenna",
    "Hattrem",
    "Hatterene",
    "Impidimp",
    "Morgrem",
    "Grimmsnarl",
    "Obstagoon",
    "Perrserker",
    "Cursola",
    "Sirfetchd",
    "Mr-rime",
    "Runerigus",
    "Milcery",
    "Alcremie",
    "Falinks",
    "Pincurchin",
    "Snom",
    "Frosmoth",
    "Stonjourner",
    "Eiscue",
    "Eiscue",
    "Indeedee",
    "Indeedee",
    "Morpeko",
    "Cufant",
    "Copperajah",
    "Dracozolt",
    "Arctozolt",
    "Dracovish",
    "Arctovish",
    "Duraludon",
    "Caterpie",
    "Metapod",
    "Butterfree",
    "Weedle",
    "Kakuna",
    "Beedrill",
    "Pidgey",
    "Pidgeotto",
    "Pidgeot",
    "Rattata",
    "Rattata-alola",
    "Raticate",
    "Raticate-alola",
    "Spearow",
    "Fearow",
    "Ekans",
    "Arbok",
    "Pikachu",
    "Raichu",
    "Raichu-alola",
    "Sandshrew",
    "Sandshrew-alola",
    "Sandslash",
    "Sandslash-alola",
    "Nidoran-f",
    "Nidorina",
    "Nidoqueen",
    "Nidoran-m",
    "Nidorino",
    "Nidoking",
    "Clefairy",
    "Clefable",
    "Vulpix",
    "Vulpix-alola",
    "Ninetales",
    "Ninetales-alola",
    "Jigglypuff",
    "Wigglytuff",
    "Zubat",
    "Golbat",
    "Oddish",
    "Gloom",
    "Vileplume",
    "Paras",
    "Parasect",
    "Venonat",
    "Venomoth",
    "Diglett",
    "Diglett-alola",
    "Dugtrio",
    "Dugtrio-alola",
    "Meowth",
    "Meowth-alola",
    "Meowth-galar",
    "Persian",
    "Persian-alola",
    "Psyduck",
    "Golduck",
    "Mankey",
    "Primeape",
    "Growlithe",
    "Arcanine",
    "Poliwag",
    "Poliwhirl",
    "Poliwrath",
    "Abra",
    "Kadabra",
    "Alakazam",
    "Machop",
    "Machoke",
    "Machamp",
    "Bellsprout",
    "Weepinbell",
    "Victreebel",
    "Tentacool",
    "Tentacruel",
    "Geodude",
    "Geodude-alola",
    "Graveler",
    "Graveler-alola",
    "Golem",
    "Golem-alola",
    "Ponyta",
    "Ponyta-galar",
    "Rapidash",
    "Rapidash-galar",
    "Slowpoke",
    "Slowpoke-galar",
    "Slowbro",
    "Slowbro-galar",
    "Magnemite",
    "Magneton",
    "Farfetchd",
    "Farfetchd-galar",
    "Doduo",
    "Dodrio",
    "Seel",
    "Dewgong",
    "Grimer",
    "Grimer-alola",
    "Muk",
    "Muk-alola",
    "Shellder",
    "Cloyster",
    "Gastly",
    "Haunter",
    "Gengar",
    "Onix",
    "Drowzee",
    "Hypno",
    "Krabby",
    "Kingler",
    "Voltorb",
    "Electrode",
    "Exeggcute",
    "Exeggutor",
    "Exeggutor-alola",
    "Cubone",
    "Marowak",
    "Marowak-alola",
    "Hitmonlee",
    "Hitmonchan",
    "Lickitung",
    "Koffing",
    "Weezing",
    "Weezing-galar",
    "Rhyhorn",
    "Rhydon",
    "Chansey",
    "Tangela",
    "Kangaskhan",
    "Horsea",
    "Seadra",
    "Goldeen",
    "Seaking",
    "Staryu",
    "Starmie",
    "Mr-mime",
    "Mr-mime-galar",
    "Scyther",
    "Jynx",
    "Electabuzz",
    "Magmar",
    "Pinsir",
    "Tauros",
    "Magikarp",
    "Ditto",
    "Vaporeon",
    "Jolteon",
    "Flareon",
    "Porygon",
    "Omanyte",
    "Omastar",
    "Kabuto",
    "Kabutops",
    "Sentret",
    "Furret",
    "Hoothoot",
    "Noctowl",
    "Ledyba",
    "Ledian",
    "Spinarak",
    "Ariados",
    "Crobat",
    "Chinchou",
    "Lanturn",
    "Pichu",
    "Cleffa",
    "Igglybuff",
    "Togepi",
    "Togetic",
    "Natu",
    "Xatu",
    "Mareep",
    "Flaaffy",
    "Ampharos",
    "Bellossom",
    "Marill",
    "Azumarill",
    "Sudowoodo",
    "Politoed",
    "Hoppip",
    "Skiploom",
    "Jumpluff",
    "Aipom",
    "Sunkern",
    "Sunflora",
    "Yanma",
    "Wooper",
    "Quagsire",
    "Espeon",
    "Umbreon",
    "Murkrow",
    "Slowking",
    "Slowking-galar",
    "Misdreavus",
    "Unown",
    "Wobbuffet",
    "Girafarig",
    "Pineco",
    "Forretress",
    "Dunsparce",
    "Gligar",
    "Steelix",
    "Snubbull",
    "Granbull",
    "Qwilfish",
    "Scizor",
    "Shuckle",
    "Heracross",
    "Sneasel",
    "Teddiursa",
    "Ursaring",
    "Slugma",
    "Magcargo",
    "Swinub",
    "Piloswine",
    "Corsola",
    "Corsola-galar",
    "Remoraid",
    "Octillery",
    "Delibird",
    "Mantine",
    "Skarmory",
    "Houndour",
    "Houndoom",
    "Kingdra",
    "Phanpy",
    "Donphan",
    "Porygon2",
    "Stantler",
    "Smeargle",
    "Tyrogue",
    "Hitmontop",
    "Smoochum",
    "Elekid",
    "Magby",
    "Miltank",
    "Blissey",
    "Poochyena",
    "Mightyena",
    "Zigzagoon",
    "Zigzagoon-galar",
    "Linoone",
    "Linoone-galar",
    "Wurmple",
    "Silcoon",
    "Beautifly",
    "Cascoon",
    "Dustox",
    "Lotad",
    "Lombre",
    "Ludicolo",
    "Seedot",
    "Nuzleaf",
    "Shiftry",
    "Taillow",
    "Swellow",
    "Wingull",
    "Pelipper",
    "Ralts",
    "Kirlia",
    "Gardevoir",
    "Surskit",
    "Masquerain",
    "Shroomish",
    "Breloom",
    "Slakoth",
    "Vigoroth",
    "Slaking",
    "Nincada",
    "Ninjask",
    "Shedinja",
    "Whismur",
    "Loudred",
    "Exploud",
    "Makuhita",
    "Hariyama",
    "Azurill",
    "Nosepass",
    "Skitty",
    "Delcatty",
    "Sableye",
    "Mawile",
    "Aron",
    "Lairon",
    "Aggron",
    "Meditite",
    "Medicham",
    "Electrike",
    "Manectric",
    "Plusle",
    "Minun",
    "Volbeat",
    "Illumise",
    "Roselia",
    "Gulpin",
    "Swalot",
    "Carvanha",
    "Sharpedo",
    "Wailmer",
    "Wailord",
    "Numel",
    "Camerupt",
    "Torkoal",
    "Spoink",
    "Grumpig",
    "Spinda",
    "Trapinch",
    "Vibrava",
    "Flygon",
    "Cacnea",
    "Cacturne",
    "Swablu",
    "Altaria",
    "Zangoose",
    "Seviper",
    "Lunatone",
    "Solrock",
    "Barboach",
    "Whiscash",
    "Corphish",
    "Crawdaunt",
    "Baltoy",
    "Claydol",
    "Lileep",
    "Cradily",
    "Anorith",
    "Armaldo",
    "Feebas",
    "Milotic",
    "Castform",
    "Kecleon",
    "Shuppet",
    "Banette",
    "Duskull",
    "Dusclops",
    "Tropius",
    "Chimecho",
    "Absol",
    "Wynaut",
    "Snorunt",
    "Glalie",
    "Spheal",
    "Sealeo",
    "Walrein",
    "Clamperl",
    "Huntail",
    "Gorebyss",
    "Relicanth",
    "Luvdisc",
    "Starly",
    "Staravia",
    "Staraptor",
    "Bidoof",
    "Bibarel",
    "Kricketot",
    "Kricketune",
    "Shinx",
    "Luxio",
    "Luxray",
    "Budew",
    "Roserade",
    "Cranidos",
    "Rampardos",
    "Shieldon",
    "Bastiodon",
    "Burmy",
    "Wormadam",
    "Mothim",
    "Combee",
    "Vespiquen",
    "Pachirisu",
    "Buizel",
    "Floatzel",
    "Cherubi",
    "Cherrim",
    "Shellos",
    "Gastrodon",
    "Ambipom",
    "Drifloon",
    "Drifblim",
    "Buneary",
    "Lopunny",
    "Mismagius",
    "Honchkrow",
    "Glameow",
    "Purugly",
    "Chingling",
    "Stunky",
    "Skuntank",
    "Bronzor",
    "Bronzong",
    "Bonsly",
    "Mime-jr",
    "Happiny",
    "Chatot",
    "Spiritomb",
    "Hippopotas",
    "Hippowdon",
    "Skorupi",
    "Drapion",
    "Croagunk",
    "Toxicroak",
    "Carnivine",
    "Finneon",
    "Lumineon",
    "Mantyke",
    "Snover",
    "Abomasnow",
    "Weavile",
    "Magnezone",
    "Lickilicky",
    "Rhyperior",
    "Tangrowth",
    "Electivire",
    "Magmortar",
    "Togekiss",
    "Yanmega",
    "Leafeon",
    "Glaceon",
    "Gliscor",
    "Mamoswine",
    "Porygon-Z",
    "Gallade",
    "Probopass",
    "Dusknoir",
    "Froslass",
    "Patrat",
    "Watchog",
    "Lillipup",
    "Herdier",
    "Stoutland",
    "Purrloin",
    "Liepard",
    "Pansage",
    "Simisage",
    "Pansear",
    "Simisear",
    "Panpour",
    "Simipour",
    "Munna",
    "Musharna",
    "Pidove",
    "Tranquill",
    "Unfezant",
    "Blitzle",
    "Zebstrika",
    "Roggenrola",
    "Boldore",
    "Gigalith",
    "Woobat",
    "Swoobat",
    "Drilbur",
    "Excadrill",
    "Audino",
    "Timburr",
    "Gurdurr",
    "Conkeldurr",
    "Tympole",
    "Palpitoad",
    "Seismitoad",
    "Throh",
    "Sawk",
    "Sewaddle",
    "Swadloon",
    "Leavanny",
    "Venipede",
    "Whirlipede",
    "Scolipede",
    "Cottonee",
    "Whimsicott",
    "Petilil",
    "Lilligant",
    "Basculin",
    "Sandile",
    "Krokorok",
    "Krookodile",
    "Darumaka",
    "Darumaka-galar",
    "Darmanitan",
    "Darmanitan-galar",
    "Maractus",
    "Dwebble",
    "Crustle",
    "Scraggy",
    "Scrafty",
    "Sigilyph",
    "Yamask",
    "Yamask-galar",
    "Cofagrigus",
    "Tirtouga",
    "Carracosta",
    "Archen",
    "Archeops",
    "Trubbish",
    "Garbodor",
    "Zorua",
    "Minccino",
    "Cinccino",
    "Gothita",
    "Gothorita",
    "Gothitelle",
    "Solosis",
    "Duosion",
    "Reuniclus",
    "Ducklett",
    "Swanna",
    "Vanillite",
    "Vanillish",
    "Vanilluxe",
    "Deerling",
    "Sawsbuck",
    "Emolga",
    "Karrablast",
    "Escavalier",
    "Foongus",
    "Amoonguss",
    "Frillish",
    "Jellicent",
    "Alomomola",
    "Joltik",
    "Galvantula",
    "Ferroseed",
    "Ferrothorn",
    "Klink",
    "Klang",
    "Klinklang",
    "Tynamo",
    "Eelektrik",
    "Eelektross",
    "Elgyem",
    "Beheeyem",
    "Litwick",
    "Lampent",
    "Chandelure",
    "Axew",
    "Fraxure",
    "Haxorus",
    "Cubchoo",
    "Beartic",
    "Cryogonal",
    "Shelmet",
    "Accelgor",
    "Stunfisk",
    "Stunfisk-galar",
    "Mienfoo",
    "Mienshao",
    "Druddigon",
    "Golett",
    "Golurk",
    "Pawniard",
    "Bisharp",
    "Bouffalant",
    "Rufflet",
    "Braviary",
    "Vullaby",
    "Mandibuzz",
    "Heatmor",
    "Durant",
    "Bunnelby",
    "Diggersby",
    "Fletchling",
    "Fletchinder",
    "Talonflame",
    "Scatterbug",
    "Spewpa",
    "Vivillon",
    "Litleo",
    "Pyroar",
    "Flabebe",
    "Floette",
    "Florges",
    "Skiddo",
    "Gogoat",
    "Pancham",
    "Pangoro",
    "Furfrou",
    "Espurr",
    "Meowstic",
    "Honedge",
    "Doublade",
    "Aegislash",
    "Spritzee",
    "Aromatisse",
    "Swirlix",
    "Slurpuff",
    "Inkay",
    "Malamar",
    "Binacle",
    "Barbaracle",
    "Skrelp",
    "Dragalge",
    "Clauncher",
    "Clawitzer",
    "Helioptile",
    "Heliolisk",
    "Tyrunt",
    "Tyrantrum",
    "Amaura",
    "Aurorus",
    "Sylveon",
    "Hawlucha",
    "Dedenne",
    "Carbink",
    "Klefki",
    "Phantump",
    "Trevenant",
    "Pumpkaboo",
    "Gourgeist",
    "Bergmite",
    "Avalugg",
    "Noibat",
    "Noivern",
    "Pikipek",
    "Trumbeak",
    "Toucannon",
    "Yungoos",
    "Gumshoos",
    "Grubbin",
    "Charjabug",
    "Vikavolt",
    "Crabrawler",
    "Crabominable",
    "Oricorio",
    "Cutiefly",
    "Ribombee",
    "Rockruff",
    "Lycanroc",
    "Wishiwashi",
    "Mareanie",
    "Toxapex",
    "Mudbray",
    "Mudsdale",
    "Dewpider",
    "Araquanid",
    "Fomantis",
    "Lurantis",
    "Morelull",
    "Shiinotic",
    "Salandit",
    "Salazzle",
    "Stufful",
    "Bewear",
    "Bounsweet",
    "Steenee",
    "Tsareena",
    "Comfey",
    "Oranguru",
    "Passimian",
    "Wimpod",
    "Golisopod",
    "Sandygast",
    "Palossand",
    "Pyukumuku",
    "Minior",
    "Komala",
    "Turtonator",
    "Togedemaru",
    "Mimikyu",
    "Bruxish",
    "Drampa",
    "Dhelmise",
    "Gyarados",
    "Munchlax",
    "Snorlax",
    "Aerodactyl",
    "Larvesta",
    "Volcarona",
    "Zoroark",
    "Lapras",
    "Wyrdeer",
    "Ursaluna",
    "Sneasler",
    "Arcanine-hisui",
    "Avalugg-hisui",
    "Braviary-hisui",
    "Electrode-hisui",
    "Growlithe-hisui",
    "Lilligant-hisui",
    "Qwilfish-hisui",
    "Sneasel-hisui",
    "Voltorb-hisui",
    "Zoroark-hisui",
    "Zorua-hisui",
    "Kleavor",
    "Overqwil",
    "Basculegion",
]

# pseudo legendary pokemon
pseudoList = [
    "Deino",
    "Goodra-hisui",
    "Sliggoo-hisui",
    "Zweilous",
    "Hydreigon",
    "Larvitar",
    "Pupitar",
    "Tyranitar",
    "Bagon",
    "Shelgon",
    "Salamence",
    "Beldum",
    "Metang",
    "Metagross",
    "Gible",
    "Gabite",
    "Garchomp",
    "Riolu",
    "Lucario",
    "Jangmo-o",
    "Hakamo-o",
    "Kommo-o",
    "Deino",
    "Zweilous",
    "Hydreigon",
    "Goomy",
    "Sliggoo",
    "Goodra",
    "Dragapult",
    "Dreepy",
    "Drakloak",
    "Dratini",
    "Dragonair",
    "Dragonite",
]

# starter pokemon
starterList = [
    "Grookey",
    "Decidueye-hisui",
    "Typhlosion-hisui",
    "Samurott-hisui",
    "Thwackey",
    "Rillaboom",
    "Scorbunny",
    "Raboot",
    "Cinderace",
    "Sobble",
    "Drizzile",
    "Inteleon",
    "Turtwig",
    "Grotle",
    "Torterra",
    "Chimchar",
    "Monferno",
    "Infernape",
    "Piplup",
    "Prinplup",
    "Empoleon",
    "Bulbasaur",
    "Ivysaur",
    "Venusaur",
    "Charmander",
    "Charmeleon",
    "Charizard",
    "Squirtle",
    "Wartortle",
    "Blastoise",
    "Rowlet",
    "Dartrix",
    "Decidueye",
    "Litten",
    "Torracat",
    "Incineroar",
    "Snivy",
    "Servine",
    "Serperior",
    "Tepig",
    "Pignite",
    "Emboar",
    "Oshawott",
    "Dewott",
    "Samurott",
    "Popplio",
    "Brionne",
    "Primarina",
    "Chikorita",
    "Bayleef",
    "Meganium",
    "Cyndaquil",
    "Quilava",
    "Typhlosion",
    "Totodile",
    "Croconaw",
    "Feraligatr",
    "Treecko",
    "Grovyle",
    "Sceptile",
    "Torchic",
    "Combusken",
    "Blaziken",
    "Mudkip",
    "Marshtomp",
    "Swampert",
    "Eevee",
    "Chespin",
    "Quilladin",
    "Chesnaught",
    "Fennekin",
    "Braixen",
    "Delphox",
    "Froakie",
    "Frogadier",
    "Greninja",
]

# legendary pokemon
LegendList = [
    "Enamorus",
    "Tapu-koko",
    "Tapu-lele",
    "Tapu-bulu",
    "Tapu-fini",
    "Cosmog",
    "Cosmoem",
    "Solgaleo",
    "Lunala",
    "Necrozma",
    "Magearna",
    "Marshadow",
    "Zeraora",
    "Cobalion",
    "Terrakion",
    "Virizion",
    "Tornadus",
    "Thundurus",
    "Reshiram",
    "Zekrom",
    "Landorus",
    "Kyurem",
    "Keldeo",
    "Meloetta",
    "Genesect",
    "Articuno",
    "Zapdos",
    "Moltres",
    "Mewtwo",
    "Mew",
    "Raikou",
    "Entei",
    "Suicune",
    "Lugia",
    "Ho-oh",
    "Celebi",
    "Rotom",
    "Uxie",
    "Mesprit",
    "Azelf",
    "Dialga",
    "Palkia",
    "Heatran",
    "Regigigas",
    "Giratina",
    "Cresselia",
    "Phione",
    "Manaphy",
    "Darkrai",
    "Shaymin",
    "Arceus",
    "Victini",
    "Regirock",
    "Regice",
    "Registeel",
    "Latias",
    "Latios",
    "Kyogre",
    "Groudon",
    "Rayquaza",
    "Jirachi",
    "Deoxys",
    "Xerneas",
    "Yveltal",
    "Zygarde",
    "Diancie",
    "Hoopa",
    "Volcanion",
    "Xerneas",
    "Yveltal",
    "Zygarde",
    "Diancie",
    "Hoopa",
    "Volcanion",
    "Type-null",
    "Silvally",
    "Meltan",
    "Melmetal",
    "Zamazenta",
    "Eternatus",
    "Zacian",
    "Zarude",
    "Kubfu",
    "Urshifu",
    "Regieleki",
    "Regidrago",
    "Glastrier",
    "Spectrier",
    "Calyrex",
    "Moltres-galar",
    "Zapdos-galar",
    "Articuno-galar",
]

# ultra beast pokemon
ubList = [
    "Nihilego",
    "Buzzwole",
    "Pheromosa",
    "Xurkitree",
    "Celesteela",
    "Kartana",
    "Guzzlord",
    "Poipole",
    "Naganadel",
    "Stakataka",
    "Blacephalon",
]

# TOTAL LIST SHOULD CONTAIN EACH POKEMON ONCE
totalList = pList + pseudoList + LegendList + ubList + starterList

emotes = [
    "<a:mimi:773455788105662464>",
    "<a:slowload:773456536290459668>",
    "<a:shinxload:773456592657973288>",
    "<a:zorload:773330544078749697>",
    "<a:slugload:773456373064138752>",
    "<a:tfpika:773455912933261342>",
    "<a:soloload:773330576891314261>",
    "<a:rollyloady:773455814119522334>",
    "<a:ratload:773456329950887946>",
    "<a:genload:773314339591553045>",
    "<a:duskload:773330708332150834>",
    "<a:dittoload:773330665604382731>",
    "<a:ballload:773314416455450675>",
    "<a:ballload:773314416455450675>",
    "<a:azuload:773455959694901278>",
    "<a:charmload:773456683049549824>",
    "<a:bulbaload:773315942628982794>",
    "<a:chanduload:773314380720766986>",
]

def is_formed(name):
    if any(
        name.endswith(suffix)
        for suffix in [
            "-bug",
            "-summer",
            "-marine",
            "-elegant",
            "-poison",
            "-average",
            "-altered",
            "-winter",
            "-trash",
            "-incarnate",
            "-baile",
            "-rainy",
            "-steel",
            "-star",
            "-ash",
            "-diamond",
            "-pop-star",
            "-fan",
            "-school",
            "-therian",
            "-pau",
            "-river",
            "-poke-ball",
            "-kabuki",
            "-electric",
            "-heat",
            "-unbound",
            "-chill",
            "-archipelago",
            "-zen",
            "-normal",
            "-mega-y",
            "-resolute",
            "-blade",
            "-speed",
            "-indigo",
            "-dusk",
            "-sky",
            "-west",
            "-sun",
            "-dandy",
            "-solo",
            "-high-plains",
            "-la-reine",
            "-50",
            "-unova-cap",
            "-burn",
            "-mega-x",
            "-monsoon",
            "-primal",
            "-mother",
            "-red-striped",
            "-blue-striped",
            "-white-striped",
            "-ground",
            "-super",
            "-yellow",
            "-polar",
            "-cosplay",
            "-ultra",
            "-heart",
            "-snowy",
            "-sensu",
            "-eternal",
            "-douse",
            "-defense",
            "-sunshine",
            "-psychic",
            "-modern",
            "-natural",
            "-tundra",
            "-flying",
            "-pharaoh",
            "-libre",
            "-sunny",
            "-autumn",
            "-10",
            "-orange",
            "-standard",
            "-land",
            "-partner",
            "-dragon",
            "-plant",
            "-pirouette",
            "-male",
            "-hoenn-cap",
            "-violet",
            "-spring",
            "-fighting",
            "-sandstorm",
            "-original-cap",
            "-neutral",
            "-fire",
            "-fairy",
            "-attack",
            "-black",
            "-shock",
            "-shield",
            "-shadow",
            "-grass",
            "-continental",
            "-overcast",
            "-disguised",
            "-exclamation",
            "-origin",
            "-garden",
            "-blue",
            "-matron",
            "-red-meteor",
            "-small",
            "-rock-star",
            "-belle",
            "-alola-cap",
            "-green",
            "-active",
            "-red",
            "-mow",
            "-icy-snow",
            "-debutante",
            "-east",
            "-midday",
            "-jungle",
            "-frost",
            "-midnight",
            "-rock",
            "-fancy",
            "-busted",
            "-ordinary",
            "-water",
            "-phd",
            "-ice",
            "-spiky-eared",
            "-savanna",
            "-original",
            "-ghost",
            "-meadow",
            "-dawn",
            "-question",
            "-pom-pom",
            "-female",
            "-kalos-cap",
            "-confined",
            "-sinnoh-cap",
            "-aria",
            "-dark",
            "-ocean",
            "-wash",
            "-white",
            "-mega",
            "-sandy",
            "-complete",
            "-large",
            "-skylarr",
            "-misfit",
            "-doomed",
            "-crowned",
            "-raspberry",
            "-djspree",
            "-yuno",
            "-darkbritual",
            "-asa",
            "-speedy",
            "-curtis",
            "-savvy",
            "-brad",
            "-neuro",
            "-ice-rider",
            "-shadow-rider",
            "-pepe",
            "-zen-galar",
            "-rapid-strike",
            "-noice",
            "-hangry",
            "-gorging",
            "-gulping",
        ]
    ):
        return True
    if name.lower().startswith("unown") and any(
        name.endswith(suffix)
        for suffix in [
            "-a",
            "-b",
            "-c",
            "-d",
            "-e",
            "-f",
            "-g",
            "-h",
            "-i",
            "-j",
            "-k",
            "-l",
            "-m",
            "-n",
            "-o",
            "-p",
            "-q",
            "-r",
            "-s",
            "-t",
            "-u",
            "-v",
            "-w",
            "-x",
            "-y",
            "-z",
        ]
    ):
        return True
    return False

# OLD TRANSLATION CODE - NOT FUNCTIONING BUT INTEGRATED IN THE BOT SOMEWHAT STILL TO THE POINT THAT REMOVING IT BREAKS TOO MUCH SHIT
def parse(string):
    return f"`{string}`"

async def tr(text: str, variables):
    first_text = text
    language = "en"
    if text in emotes:
        return text
    ctx = variables["ctx"] if "ctx" in variables else variables["self"]
    # await add_text(ctx, text.lower())
    try:
        guild = variables["ctx" if "ctx" in variables else "message"]
    except:
        await ctx.bot.owner.send(text)

    # await ctx.bot.load_languages()
    # async with ctx.bot.db[0].acquire() as pconn:
    #    language = await pconn.fetchval(
    #        "SELECT language FROM servers WHERE serverid = $1", guild.guild.id
    #    )
    language = "en"
    if language == "en":
        ...
    else:
        # await ctx.send(parse(text))
        # text = ctx.bot.language_strings.get(language).get(text)
        try:
            text = (
                discord.utils.find(
                    lambda entry: entry.get("en").lower() == first_text.lower(),
                    ctx.bot.language_strings,
                )
            ).get(language, None)
        except:
            text = None
        if not text:
            entry = discord.utils.find(
                lambda entry: entry.get("en").lower() == first_text.lower(),
                ctx.bot.language_strings,
            )
            if not entry:
                await ctx.bot.owner.send(f"Appending {first_text} For language - {language}")
                ctx.bot.language_strings.append({"en": first_text, language: "None"})
            elif entry and not language in entry:
                new_entry = entry
                new_entry[language] = "None"
                ctx.bot.language_strings[ctx.bot.language_strings.index(entry)] = new_entry
            elif entry and language in entry:
                text = entry.get(language)
            try:
                await ctx.bot.translations_collection.replace_one(
                    {"_id": ctx.bot.language_strings_id},
                    {"translations": ctx.bot.language_strings},
                )
            except:
                await ctx.bot.owner.send(parse(language))
                await ctx.bot.owner.send(parse(first_text))
            ctx.bot.language_strings = (await ctx.bot.translations_collection.find_one())[
                "translations"
            ]
            text = first_text
            await ctx.bot.owner.send(f"{first_text}\nNeeds to be translated")
        else:
            text = text.replace(") }", ")}")
    # text = text.replace('{prefix}', )
    text = re.sub("await pre\((.*?)\)", "prefix", text)
    variables["prefix"] = ctx.prefix
    try:
        text = text.format(**variables)
    except Exception as e:
        await ctx.send(text)
        raise e
    if language in ctx.bot.pokemon_names:
        for word in text.split():
            if word.capitalize() in totalList:
                if is_formed(word):
                    id = [
                        i["pokemon_id"]
                        for i in FORMS
                        if i["identifier"] == word.split("-")[0].lower()
                    ][0]
                    text = (
                        text.replace(word, ctx.bot.pokemon_names.get(language)[id - 1])
                        + word.split("-")[1:]
                    )
                else:
                    id = [i["pokemon_id"] for i in FORMS if i["identifier"] == word.lower()][0]
                    text = text.replace(word, ctx.bot.pokemon_names.get(language)[id - 1])
    return text


async def _(arg):
    if type(arg) == str:
        frame = inspect.currentframe()
        try:
            variables = frame.f_back.f_locals
        finally:
            del frame
        return await tr(arg, variables)
    elif type(arg) == discord.embeds.Embed:
        embed = arg
        frame = inspect.currentframe()
        try:
            variables = frame.f_back.f_locals
        finally:
            del frame
        e = discord.Embed()
        field_names = []
        field_values = []
        if not embed.description is discord.Embed.Empty:
            description = await tr(embed.description, variables)
            e.description = description
        else:
            description = ""

        if not embed.title is discord.Embed.Empty:
            title = await tr(embed.title, variables)
            e.title = title

        for field in embed.fields:
            field_names.append(await tr(field.name, variables))
            field_values.append(await tr(field.value, variables))

        for idx, field in enumerate(field_names):
            e.add_field(name=field, value=field_values[idx], inline=False)

        if not embed.footer.text is discord.Embed.Empty:
            foot = await tr(embed.footer.text, variables)
            e.set_footer(text=foot)

        if not embed.thumbnail.url is discord.Embed.Empty:
            e.set_thumbnail(url=embed.thumbnail.url)

        if embed.image.url is discord.Embed.Empty:
            pass
        else:
            e.set_image(url=embed.image.url)
        e.color = embed.color
        return e


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)