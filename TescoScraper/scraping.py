import scrapy
import pickle

from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


PRODUCT_WRAPPER_TAG = 'li'
PRODUCT_WRAPPER_NAME = 'product-list--list-item'
PRODUCT_TILE_CLASS = 'product-tile--title'
NEXT_PAGE_CLASS = 'pagination--page-selector-wrapper'
html_identifier = PRODUCT_WRAPPER_TAG + '.' + PRODUCT_WRAPPER_NAME

PAGE_LINK_1 = 'https://www.tesco.com/groceries/en-GB/shop/'
PAGE_LINK_2 = '/all'
CATEGORIES = ['fresh-food',
    'bakery',
    'frozen-food',
    'food-cupboard',
    'drinks',
    'baby',
    'health-and-beauty',
    'pets',
    'household',
    'home-and-ents']


class TescoGenreSpider(scrapy.Spider):
    name = "tesco_scraper"
    start_urls = []
    for category in CATEGORIES:
        url = PAGE_LINK_1 + category + PAGE_LINK_2
        start_urls.append(url)
    all_fresh_food = { }

    def pickle_results(self):
        pickle.dump(self.all_fresh_food, open(self.category + ".pkl", "wb"))

        return None

    def next_page_link(self, response):
        first_tag = '//nav[@class="' + NEXT_PAGE_CLASS + '"]'
        second_tag = '/ul/li[last()]'
        third_tag = '/a/@href'

        xml_path = first_tag + second_tag + third_tag

        link = response.xpath(xml_path).extract_first()

        return link

    def parse(self, response):
        PRODUCT_SELECTOR = response.css(html_identifier)

        xml_path_prices = '//li[@class="' + PRODUCT_WRAPPER_NAME + '"]'
        page_products = response.xpath(xml_path_prices).extract()

        xml_path_titles = '//a[@data-auto="' + PRODUCT_TILE_CLASS + '"]/text()'
        titles = response.xpath(xml_path_titles).extract()
        titles = titles[1:len(titles)]

        for i in range(len(page_products)):
            product = page_products[i]
            product_title = titles[i]

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

            try:
                result_set = result_set[0]
            except IndexError:
                continue

            self.all_fresh_food[product_title] = result_set.text

        next_link = self.next_page_link(response)
        if next_link:
            yield scrapy.Request(
                response.urljoin(next_link),
                callback=self.parse
            )

        self.pickle_results()



if __name__ == "__main__":
    pass
