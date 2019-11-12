import scrapy
from bs4 import BeautifulSoup


PRODUCT_WRAPPER_TAG = 'li'
PRODUCT_WRAPPER_NAME = 'product-list--list-item'
html_identifier = PRODUCT_WRAPPER_TAG + '.' + PRODUCT_WRAPPER_NAME


class TescoGenreSpider(scrapy.Spider):
    name = "tesco_scraper"
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/fresh-food/all']

    def next_page_link(self, response):
        first_tag = '//nav[@class="pagination--page-selector-wrapper"]'
        second_tag = '/ul/li[last()]'
        third_tag = '/a/@href'

        xml_path = first_tag + second_tag + third_tag

        link = response.xpath(xml_path).extract_first()

        return link

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

            print(span_soup)

            result_set = span_soup.find_all('span', {'class': 'value'})

            try:
                result_set = result_set[0]
            except IndexError:
                continue

            yield {
                'price': result_set.text
            }

        next_link = self.next_page_link(response)
        if next_link:
            yield scrapy.Request(
                response.urljoin(next_link),
                callback=self.parse
            )
