import scrapy

class MercadoLivrePerfumesSpider(scrapy.Spider):
    name = "scraper_merc_livre"
    start_urls = [
        "https://lista.mercadolivre.com.br/perfume#D[A:perfume]"
    ]

    def parse(self, response):
        for produto in response.css("div.poly-card__content"):
            yield {
                "nome": produto.css("a.poly-component__title::text").get(),
                #"link": produto.css("a.poly-component__title::attr(href)").get(),
                "vendedor": produto.css("span.poly-component__seller::text").get(),
                "avaliacao": produto.css("span.poly-reviews_rating::text").get(),
                #"total_avaliacoes": produto.css("span.poly-reviews_total::text").get(),
                "preco_reais": produto.css("div.poly-price__current span.andes-money-amount__fraction::text").get(),
                "preco_centavos": produto.css("div.poly-price__current span.andes-money-amount__cents::text").get(),
            }

        # Paginação
        next_page = response.css('a.andes-pagination__link[title="Seguinte"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
