import re

def extract_urls(paragraph):
    # Regular expression pattern for matching URLs
    url_pattern = r'https?://\S+|www\.\S+'
    # Find all URLs in the paragraph
    urls = re.findall(url_pattern, paragraph)
    return urls



def categorize_urls(paragraph):
    url_list = extract_urls(paragraph)
    image_urls = []
    website_urls = []
    map_urls = []

    # Define patterns for image URLs, website URLs, and map URLs
    # image_pattern = r'\.(jpg|jpeg|png|gif|bmp|svg|webp)$'
    image_pattern =r'google\.com/search.*[?&]q=.*(image|images|imager|imagers)'
    map_pattern = r'google\.com/maps|maps\.google\.com|maps\.app\.goo\.gl'

    for url in url_list:
        # Check if the URL matches the image pattern
        if re.search(image_pattern, url, re.IGNORECASE):
            image_urls.append(url)
        # Check if the URL matches the map pattern
        elif re.search(map_pattern, url, re.IGNORECASE):
            map_urls.append(url)
        # Check if the URL is a general website URL
        elif url.startswith(('http://', 'https://')):
            website_urls.append(url)

    return image_urls, website_urls, map_urls