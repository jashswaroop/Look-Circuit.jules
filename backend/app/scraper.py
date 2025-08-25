from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_myntra(query):
    """
    Scrapes Myntra for a given search query using Playwright to handle JavaScript rendering.
    """
    search_query = query.replace(' ', '-')
    url = f"https://www.myntra.com/{search_query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            # Wait for the product grid to be visible
            page.wait_for_selector('ul.results-base', timeout=10000)
            html_content = page.content()
        except Exception as e:
            print(f"Error with Playwright navigation or waiting: {e}")
            browser.close()
            return []
        finally:
            browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []
    product_list = soup.select('li.product-base')

    for item in product_list[:5]:
        product = {}
        try:
            brand = item.select_one('h3.product-brand')
            name = item.select_one('h4.product-product')
            price_info = item.select_one('div.product-price')
            link_tag = item.find('a')
            img_tag = item.select_one('picture.img-responsive img')

            if all([brand, name, price_info, link_tag, img_tag]):
                product['brand'] = brand.get_text(strip=True)
                product['name'] = name.get_text(strip=True)

                price_span = price_info.select_one('span.product-discountedPrice')
                if not price_span:
                    price_span = price_info.find('span')

                product['price'] = price_span.get_text(strip=True) if price_span else "N/A"

                href = link_tag.get('href')
                product['link'] = f"https://www.myntra.com/{href}" if href and not href.startswith('http') else href

                product['image_url'] = img_tag.get('src')
                products.append(product)
        except Exception as e:
            print(f"Error parsing a Myntra product item: {e}")
            continue

    return products

def scrape_snitch(query):
    """
    Scrapes Snitch for a given search query using Playwright.
    """
    search_query = query.replace(' ', '+')
    url = f"https://www.snitch.co.in/search?q={search_query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_selector('div.product-card', timeout=10000)
            html_content = page.content()
        except Exception as e:
            print(f"Error with Playwright navigation for Snitch: {e}")
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
            name_tag = item.select_one('.product-card__title')
            price_tag = item.select_one('.price-item--regular')
            link_tag = item.select_one('a.product-card-link')
            img_tag = item.select_one('img.product-card-image')

            if all([name_tag, price_tag, link_tag, img_tag]):
                product['brand'] = "Snitch"
                product['name'] = name_tag.get_text(strip=True)
                product['price'] = price_tag.get_text(strip=True)

                href = link_tag.get('href')
                product['link'] = f"https://www.snitch.co.in{href}" if href and href.startswith('/') else href

                # Handle potential different image src attributes
                img_src = img_tag.get('src') or img_tag.get('data-src')
                product['image_url'] = f"https:{img_src}" if img_src and img_src.startswith('//') else img_src
                products.append(product)
        except Exception as e:
            print(f"Error parsing a Snitch product item: {e}")
            continue

    return products

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
    Scrapes Ajio for a given search query using Playwright.
    """
    search_query = query.replace(' ', '%20')
    url = f"https://www.ajio.com/search/?text={search_query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            # Ajio has a specific product grid container
            page.wait_for_selector('.products-list', timeout=10000)
            html_content = page.content()
        except Exception as e:
            print(f"Error with Playwright navigation for Ajio: {e}")
            browser.close()
            return []
        finally:
            browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')

    products = []
    # Selector based on inspection of Ajio's structure
    product_list = soup.select('div.item.product-card')

    for item in product_list[:5]:
        product = {}
        try:
            brand = item.select_one('div.brand')
            name = item.select_one('div.nameCls')
            price_info = item.select_one('span.price')
            link_tag = item.find('a')
            img_tag = item.select_one('img.ril-lazy-img-loaded')

            if all([brand, name, price_info, link_tag, img_tag]):
                product['brand'] = brand.get_text(strip=True)
                product['name'] = name.get_text(strip=True)
                product['price'] = price_info.get_text(strip=True)

                href = link_tag.get('href')
                product['link'] = f"https://www.ajio.com{href}" if href and href.startswith('/') else href

                product['image_url'] = img_tag.get('src')
                products.append(product)
        except Exception as e:
            print(f"Error parsing an Ajio product item: {e}")
            continue

    return products
