import scrapy
from bs4 import BeautifulSoup


PRODUCT_WRAPPER_TAG = 'li'
PRODUCT_WRAPPER_NAME = 'product-list--list-item'
html_identifier = PRODUCT_WRAPPER_TAG + '.' + PRODUCT_WRAPPER_NAME


class TescoGenreSpider(scrapy.Spider):
    name = "tesco_scraper"
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/fresh-food/all']

    def parse(self, response):
        PRODUCT_SELECTOR = response.css(html_identifier)

        xml_path_prices = '//li[@class="' + PRODUCT_WRAPPER_NAME + '"]'
        page_products = response.xpath(xml_path_prices).extract()

        xml_path_titles = '//a[@data-auto="product-tile--title"]/text()'
        titles = response.xpath(xml_path_titles).extract()
        titles = titles[1:len(titles)]

        prices = []
        for product in page_products:
            soup = BeautifulSoup(product, 'html.parser')
            spans = soup.find_all('span')

            price_span = None

            for span in spans:
                if span.get('class') == None:
                    continue
                else:
                    if span.get('class')[0] == 'value':
                        price_span = span
                        break

            span = str(span)
            span_soup = BeautifulSoup(span, 'html.parser')

            result_set = span_soup.find_all('span', {'class': 'value'})
            for result in result_set:
                prices.append(result.text)

        for i in range(len(prices)):
            yield {
                titles[i]: prices[i]
            }
