from bs4 import BeautifulSoup

def _inject_base(soup: BeautifulSoup, base: str) -> str: 
    base = soup.new_tag('base', href=base)
    soup.head.insert(0, base)
    return soup

class HTMLProcessor:
    @staticmethod
    def process(html: str, target: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        return str(_inject_base(soup, target))