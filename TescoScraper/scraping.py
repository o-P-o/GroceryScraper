import scrapy
from bs4 import BeautifulSoup


PRODUCT_WRAPPER_TAG = 'li'
PRODUCT_WRAPPER_NAME = 'product-list--list-item'
html_identifier = PRODUCT_WRAPPER_TAG + '.' + PRODUCT_WRAPPER_NAME


class TescoGenreSpider(scrapy.Spider):
    name = "tesco_scraper"
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/fresh-food/all']
    product_list_class_name = 'list-page-1'

    def parse(self, response):
        #LIST_SELECTOR = '.' + self.product_list_class_name
        #NAME_SELECTOR = 'img ::attr(alt)'
        #PRICE_SELECTOR = 'span ::text'

        PRODUCT_SELECTOR = response.css(html_identifier)

        xml_path = '//li[@class="' + PRODUCT_WRAPPER_NAME + '"]'
        page_products = response.xpath(xml_path).extract()

        prices = []

        for product in page_products:
            count += 1
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
                print.append(result.text)

        #example = page_products[1]

        #soup = BeautifulSoup(example, 'html.parser')
        #ex = soup.find_all('span')

        #test = None
        #print()
        #for x in ex:
        #    if x.get('class') == None:
        #        continue
        #    else:
        #        if x.get('class')[0] == 'value':
        #            test = x
        #            break
        #specific = ex[3]
        #print(specific)
        #print()

        #specific = str(specific)
        #soup2 = BeautifulSoup(specific, 'html.parser')
        #find = soup2.find_all('span', {'class': 'value'})
        #print(find)
        #print(type(find))
        #for d in find:
    #        print(d.text)

        #count = 0
        #for product in response.xpath('//div[@class="product-tile-wrapper"]//div[@class="prouct-controls--wrapper"]').extract():  #//span/span[@class="currency"]/text()').extract():
        #    count += 1
        #    print(count)
        #    yield {
        #        'name': product
        #    }


        #html_response = response.css(LIST_SELECTOR)

        #prices_list = html_response.css(PRICE_SELECTOR).extract()
        #names_list = html_response.css(NAME_SELECTOR).extract()

        #prices = []
        #for element in range(len(prices_list)):
        #    is_sterling = prices_list[element]
        #    if is_sterling == '£':
        #        is_empty = prices_list[element + 1]
        #        if is_empty == ' ':
        #            prices.append(prices_list[element + 2])

        #i = 0
        #product_prices = { }
        #for product in names_list:
        #    product_prices[product] = prices[i]
        #    i += 1

        #yield product_prices

        #print(prices_list)
        #print()
        #print(prices)

        # Error: Pulling in correct prices for the products, but is pulling
        # additional products using the per kilo price from different products
