DATA_FILE: str = 'data/sakura.xlsx'
ENV_PATH: str = '../parsers/.env'

TTS_CONF: dict[str:str] = {
    'url': 'http://id12740.public.api.abcp.ru',
}

ROSSKO_CONF: dict[str:str] = {
    'url': "http://api.rossko.ru/service/v2.1/GetSearch",
    'warehouse': '000000001',
}

PARTKOM_CONF: dict[str:str] = {
    'url': 'https://www.part-kom.ru/engine/api/v3/search/parts',
}

MOSKVORECHIE_CONF: dict[str:str] = {
    'url': 'https://portal.moskvorechie.ru/portal.api',
}

AutoEURO_CONF: dict[str:str] = {
    'url': 'https://api.autoeuro.ru/api/v2/json/search_items/',
}
BERG_CONF: dict[str:str] = {
    'url': 'https://api.berg.ru/',
    'Brands': 'brands.json',
    'price': 'get_stock.json',
    'address': '7053'
}

BRANDS: dict[str:str] = {
    'PARTKOM': {
        'MANN-FILTER': 'MANN',
        'Sakura': 'SAKURA',
        'BIG FILTER': 'BIGFILTER'
    },
    'ROSSKO': {
        'MANN-FILTER': 'Mann',
        'Sakura': 'Sakura',
        'BIG FILTER': 'BIG Filter'
    },
    'TTS': {
        'MANN-FILTER': 'MANN-FILTER',
        'Sakura': 'Sakura',
        'BIG FILTER': 'BIG FILTER'
    },
    "MOSKVORECHIE": {
        'MANN-FILTER': "Mann-filter",
        'BIG FILTER': 'BIG FILTER',
        'Sakura': 'SAKURA Automotive',
    },
    "AutoEURO": {
        'MANN-FILTER': "MANN-FILTER",
        'BIG FILTER': 'BIG FILTER',
        'Sakura': 'SAKURA',
        'Mahle/Knecht': "MAHLE"
    },
    "BERG": {
        'MANN-FILTER': "MANN",
        'BIG FILTER': 'BIG FILTER',
        'Sakura': 'Sakura',
        'Mahle/Knecht': "KNECHT/MAHLE"
    }
}
