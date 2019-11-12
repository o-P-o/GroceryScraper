import scrapy
from bs4 import BeautifulSoup


PRODUCT_WRAPPER_TAG = 'li'
PRODUCT_WRAPPER_NAME = 'product-list--list-item'
html_identifier = PRODUCT_WRAPPER_TAG + '.' + PRODUCT_WRAPPER_NAME


class TescoGenreSpider(scrapy.Spider):
    name = "tesco_scraper"
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/fresh-food/all']

    def check_page_number(self, link, prev_page):
        is_next_page = False
        idx = link.find('page=')
        sub_string = link[idx:][len('page='):]
        if prev_page == int(sub_string):
            return True

        prev_page += 1

        return is_next_page, prev_page

    page = 1
    def parse(self, response):
        PRODUCT_SELECTOR = response.css(html_identifier)

        xml_path_prices = '//li[@class="' + PRODUCT_WRAPPER_NAME + '"]'
        page_products = response.xpath(xml_path_prices).extract()

        xml_path_titles = '//a[@data-auto="product-tile--title"]/text()'
        titles = response.xpath(xml_path_titles).extract()
        titles = titles[1:len(titles)]

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

            result_set = span_soup.find_all('span', {'class': 'value'})[0]

            yield {
                'price': result_set.text
            }

        xml_path_next_page = '.pagination-btn-holder ::attr(href)'
        next_page_link = response.css(xml_path_next_page).extract_first()

        is_next_page = check_page_number(next_page_link, self.page)[0]
        new_page = check_page_number(next_page_link, self.page)[1]

        
