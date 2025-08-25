import requests
from bs4 import BeautifulSoup

def scrape_myntra(query):
    """
    Scrapes Myntra for a given search query.

    Args:
        query (str): The search term.

    Returns:
        list: A list of dictionaries, where each dictionary represents a product.
    """
    search_query = query.replace(' ', '-')
    url = f"https://www.myntra.com/{search_query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Myntra page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    # NOTE: These selectors are based on Myntra's structure as of a certain date.
    # They are highly likely to break and will need maintenance.
    product_list = soup.find_all('li', class_='product-base')

    for item in product_list[:5]: # Limit to first 5 results for the PoC
        product = {}
        try:
            brand = item.find('h3', class_='product-brand')
            name = item.find('h4', class_='product-product')
            price_info = item.find('div', class_='product-price')
            link_tag = item.find('a')

            if all([brand, name, price_info, link_tag]):
                product['brand'] = brand.get_text(strip=True)
                product['name'] = name.get_text(strip=True)

                # Extract price, handling discounted and original prices
                price_span = price_info.find('span', class_='product-discountedPrice')
                if not price_span:
                    price_span = price_info.find('span') # Fallback for non-discounted

                product['price'] = price_span.get_text(strip=True) if price_span else "N/A"

                # Construct absolute URL if the link is relative
                href = link_tag.get('href')
                product['link'] = f"https://www.myntra.com/{href}" if href and not href.startswith('http') else href

                # Image URL often requires special handling (lazy loading, etc.)
                # This is a simplified selector
                img_tag = item.find('img', class_='img-responsive')
                product['image_url'] = img_tag.get('src') if img_tag else "No Image"

                products.append(product)
        except Exception as e:
            print(f"Error parsing a product item: {e}")
            continue

    return products

def scrape_snitch(query):
    """
    Scrapes Snitch for a given search query.
    """
    search_query = query.replace(' ', '+')
    url = f"https://www.snitch.co.in/search?q={search_query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Snitch page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    # NOTE: These selectors are best-guess.
    product_list = soup.find_all('div', class_='product-card') # Common class name

    for item in product_list[:5]:
        product = {}
        try:
            # Best-guess selectors
            product['brand'] = "Snitch" # Typically brand is not listed separately on own-brand sites
            name_tag = item.find('h3', class_='product-card-title')
            price_tag = item.find('span', class_='price-item--regular')
            link_tag = item.find('a', class_='product-card-link')
            img_tag = item.find('img', class_='product-card-image')

            if all([name_tag, price_tag, link_tag, img_tag]):
                product['name'] = name_tag.get_text(strip=True)
                product['price'] = price_tag.get_text(strip=True)

                href = link_tag.get('href')
                product['link'] = f"https://www.snitch.co.in{href}" if href and href.startswith('/') else href

                product['image_url'] = img_tag.get('src')
                products.append(product)
        except Exception as e:
            print(f"Error parsing a Snitch product item: {e}")
            continue

    return products

def scrape_thesouledstore(query):
    print(f"Scraping The Souled Store for: {query}")
    return []

def scrape_comicsense(query):
    print(f"Scraping Comicsense for: {query}")
    return []

def scrape_xenpachi(query):
    print(f"Scraping Xenpachi for: {query}")
    return []

def scrape_ajio(query):
    """
    Scrapes Ajio for a given search query.
    """
    search_query = query.replace(' ', '%20')
    url = f"https://www.ajio.com/search/?text={search_query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Ajio page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    # NOTE: These selectors are best-guess based on common structures, as direct inspection is blocked.
    # This will likely need refinement.
    product_list = soup.find_all('div', class_='item-grid')

    for item in product_list[:5]:
        product = {}
        try:
            brand = item.find('div', class_='brand')
            name = item.find('div', class_='name')
            price_info = item.find('span', class_='price')
            link_tag = item.find('a')
            img_tag = item.find('img')

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
