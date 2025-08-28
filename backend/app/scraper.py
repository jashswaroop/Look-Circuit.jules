from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_myntra(query):
    """
    NOTE: Myntra has advanced bot detection that prevents scraping in this environment.
    This function is disabled and will return no results.
    """
    print("Myntra scraper is currently disabled due to advanced anti-bot measures.")
    return []

def scrape_snitch(query):
    """
    NOTE: This scraper is disabled due to anti-bot measures.
    """
    print("Snitch scraper is currently disabled.")
    return []

def scrape_thesouledstore(query):
    """
    Scrapes The Souled Store for a given search query using Playwright.
    """
    search_query = query.replace(' ', '+')
    url = f"https://www.thesouledstore.com/search?q={search_query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_selector('div.product-card', timeout=10000)
            html_content = page.content()
        except Exception as e:
            print(f"Error with Playwright navigation for The Souled Store: {e}")
            browser.close()
            return []
        finally:
            browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []
    product_list = soup.select('div.product-card')

    for item in product_list[:5]:
        product = {}
        try:
            name_tag = item.select_one('h4.product-card__title')
            price_tag = item.select_one('span.product-card__price')
            link_tag = item.find('a')
            img_tag = item.select_one('img.product-card__image')

            if all([name_tag, price_tag, link_tag, img_tag]):
                product['brand'] = "The Souled Store"
                product['name'] = name_tag.get_text(strip=True)
                product['price'] = price_tag.get_text(strip=True)

                href = link_tag.get('href')
                product['link'] = f"https://www.thesouledstore.com{href}" if href and href.startswith('/') else href

                img_src = img_tag.get('src') or img_tag.get('data-src')
                product['image_url'] = f"https:{img_src}" if img_src and img_src.startswith('//') else img_src
                products.append(product)
        except Exception as e:
            print(f"Error parsing a The Souled Store product item: {e}")
            continue

    return products

def scrape_comicsense(query):
    """
    Scrapes Comicsense for a given search query using Playwright.
    """
    search_query = query.replace(' ', '+')
    # URL structure is a guess
    url = f"https://comicsense.in/search?q={search_query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_selector('div.product-item', timeout=10000) # Common selector pattern
            html_content = page.content()
        except Exception as e:
            print(f"Error with Playwright navigation for Comicsense: {e}")
            browser.close()
            return []
        finally:
            browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []
    product_list = soup.select('div.product-item')

    for item in product_list[:5]:
        product = {}
        try:
            name_tag = item.select_one('h3.product-title')
            price_tag = item.select_one('.price')
            link_tag = item.find('a')
            img_tag = item.select_one('img.product-image')

            if all([name_tag, price_tag, link_tag, img_tag]):
                product['brand'] = "Comicsense"
                product['name'] = name_tag.get_text(strip=True)
                product['price'] = price_tag.get_text(strip=True)

                href = link_tag.get('href')
                product['link'] = f"https://comicsense.in{href}" if href and href.startswith('/') else href

                img_src = img_tag.get('src') or img_tag.get('data-src')
                product['image_url'] = f"https:{img_src}" if img_src and img_src.startswith('//') else img_src
                products.append(product)
        except Exception as e:
            print(f"Error parsing a Comicsense product item: {e}")
            continue

    return products

def scrape_xenpachi(query):
    """
    Scrapes Xenpachi for a given search query using Playwright.
    """
    search_query = query.replace(' ', '+')
    url = f"https://www.xenpachi.in/search?q={search_query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_selector('div.product-grid-item', timeout=10000)
            html_content = page.content()
        except Exception as e:
            print(f"Error with Playwright navigation for Xenpachi: {e}")
            browser.close()
            return []
        finally:
            browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []
    product_list = soup.select('div.product-grid-item')

    for item in product_list[:5]:
        product = {}
        try:
            name_tag = item.select_one('h3.product-name')
            price_tag = item.select_one('span.product-price')
            link_tag = item.find('a')
            img_tag = item.select_one('img.product-image')

            if all([name_tag, price_tag, link_tag, img_tag]):
                product['brand'] = "Xenpachi"
                product['name'] = name_tag.get_text(strip=True)
                product['price'] = price_tag.get_text(strip=True)

                href = link_tag.get('href')
                product['link'] = f"https://www.xenpachi.in{href}" if href and href.startswith('/') else href

                img_src = img_tag.get('src') or img_tag.get('data-src')
                product['image_url'] = f"https:{img_src}" if img_src and img_src.startswith('//') else img_src
                products.append(product)
        except Exception as e:
            print(f"Error parsing a Xenpachi product item: {e}")
            continue

    return products

def scrape_ajio(query):
    """
    NOTE: This scraper is disabled due to anti-bot measures.
    """
    print("Ajio scraper is currently disabled.")
    return []
