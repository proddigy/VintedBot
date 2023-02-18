import os


def category_url(requested_category: str) -> str:
    result = f'{os.environ["VINTED_URL"]}vetements?search_text=' \
             f'{requested_category.strip().replace(" ", "+")}' \
             f'&order=newest_first'
    return result
