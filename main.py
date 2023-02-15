from parser import vinted
from tqdm import tqdm
from db_manager import VintedDBManager

if __name__ == '__main__':
    category = 'Carhartt'
    items = vinted.parse(category)
    for item in tqdm(items,
                     desc='Parsing details',
                     ncols=100,
                     nrows=100,
                     colour='blue',
                     unit='items',
                     total=len(items)):

        match item.market_place:
            case 'Vinted':
                db_manager = VintedDBManager()
            case 'Depop':
                # db_manager = DepopDBManager()
                pass
            case 'Ebay':
                # db_manager = EbayDBManager()
                pass
            case 'Mercari':
                # db_manager = MercariDBManager()
                pass
            case 'Grailed':
                # db_manager = GrailedDBManager()
                pass
        db_manager.insert_item(item)
