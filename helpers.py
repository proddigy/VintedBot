from decouple import config


def category_url(requested_category: str) -> str:
    result = f'{config("VINTED_URL")}vetements?search_text=' \
             f'{requested_category.strip().replace(" ", "+")}' \
             f'&order=newest_first'
    return result
