import time

from parser import VintedParser
from db_manager import VintedDBManager
from models import Item


marketplaces = ('vinted', 'depop', 'ebay', 'mercari', 'grailed')

marketplace_to_dbmanager = {
    'vinted': VintedDBManager,
    # 'depop': DepopDBManager,
    # 'ebay': EbayDBManager,
    # 'mercari': MercariDBManager,
    # 'grailed': GrailedDBManager
}
marketplace_to_parser = {
    'vinted': VintedParser,
    # 'depop': DepopParser,
    # 'ebay': EbayParser,
    # 'mercari': MercariParser,
    # 'grailed': GrailedParser
}


def main():
    from tqdm import tqdm
    marketplace = get_marketplace()
    category = input('Enter category: ')
    # db_m = marketplace_to_dbmanager[marketplace]()
    parser = marketplace_to_parser[marketplace]()
    items = parser.get(category)
    for item in tqdm(items,
                     desc='Inserting items into database',
                     colour='green',
                     unit='items',
                     total=len(items)):
        print(parser.get_details(item))
        time.sleep(1)


def get_marketplace():
    marketplace = input('Enter marketplace: ')
    match marketplace:
        case 'vinted':
            return marketplace
        case 'exit':
            exit()
        case _:
            print('Marketplace not supported')

    get_marketplace()


def get_item_details(item: Item) -> Item:
    marketplace = get_marketplace()
    parser = marketplace_to_parser[marketplace]()
    return parser.get_details(item)


if __name__ == '__main__':
    # print(get_item_details(
    #     'https://www.vinted.pl/'
    #     'mezczyzni/akcesoria-dodatki/'
    #     'kapelusze-i-czapki/'
    #     'zimowe-czapki/2697590571-czapka'))
    main()
