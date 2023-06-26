DATA_FILE: str = 'data/data.xlsx'

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
BRANDS: dict[str:str] = {
    'PARTKOM': {
        'Mann': 'MANN'
    },
    'ROSSKO': {
        'Mann': 'Mann'
    }
}
