from parsers.rossko import rossko
from parsers.partkom import partkom
from services.utils.excel import excel_reader, write_xls

from config.config_data import DATA_FILE


def run(filename: str, page_name: str, column: str, brand_name: str, parser):
    result_list = []
    products = excel_reader(filename, pagename=page_name, column=column)
    for i in products:
        if parser == "Rossko":
            price = rossko(i, brand_name)
            print([i, price])
            result_list.append([i, price])
        elif parser == "Part-kom":
            price = partkom(i, brand_name)
            print([i, price])
            result_list.append([i, price])

    write_xls(result_list, f"data\\{parser}_price_result_{brand_name}_min_2.xlsx")


if __name__ == '__main__':
    run(DATA_FILE, page_name='Mann', column='A', brand_name='MANN', parser="Rossko")
