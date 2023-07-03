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

BRANDS: dict[str:str] = {
    'PARTKOM': {
        'Mann': 'MANN',
        'Sakura': 'SAKURA',
        'BIG FILTER': 'BIGFILTER'
    },
    'ROSSKO': {
        'Mann': 'Mann',
        'Sakura': 'Sakura',
        'BIG FILTER': 'BIG Filter'
    },
    'TTS': {
        'Mann': 'MANN-FILTER',
        'Sakura': 'Sakura',
        'BIG FILTER': 'BIG FILTER'
    },
    "MOSKVORECHIE": {
        'Mann': "Mann-filter",
        'BIG FILTER': 'BIG FILTER'
    }
}
