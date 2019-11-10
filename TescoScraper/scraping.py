import scrapy
import html2text

class TescoGenreSpider(scrapy.Spider):
    name = "tesco_scraper"
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/fresh-food/all']
    product_list_class_name = 'list-page-1'

    def parse(self, response):
        LIST_SELECTOR = '.' + self.product_list_class_name
        html_response = response.css(LIST_SELECTOR)
        NAME_SELECTOR = 'img ::attr(alt)'
        PRICE_SELECTOR = 'span ::text'

        prices_list = html_response.css(PRICE_SELECTOR).extract()
        names_list = html_response.css(NAME_SELECTOR).extract()

        prices = []
        for element in range(len(prices_list)):
            is_sterling = prices_list[element]
            if is_sterling == '£':
                is_empty = prices_list[element + 1]
                if is_empty == ' ':
                    prices.append(prices_list[element + 2])

        i = 0
        product_prices = { }
        for product in names_list:
            product_prices[product] = prices[i]
            i += 1

        yield product_prices
        # Error: Pulling in correct prices for the products, but is pulling
        # additional products using the per kilo price from different products
