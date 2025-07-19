import scrapy

class OLXSpider(scrapy.Spider):
    name = "olx_manaus"
    allowed_domains = ["olx.com.br"]
    start_urls = [
        "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-am/regiao-de-manaus/manaus"
    ]

    def start_requests(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }

        cookies = {
            'visitor-id': '3959586728832538000V10',
            'UID': '6dc096c22cae19a2dddca8b882eaa3ca',

        }

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=headers,
                cookies=cookies,
                callback=self.parse
            )

    def parse(self, response):
        for ad in response.css("section.olx-adcard"):
            yield {
                "titulo": ad.css("a.olx-adcard_link::attr(title)").get(),
                "link": ad.css("a.olx-adcard_link::attr(href)").get(),
                "preco": ad.css("h2::text").get(),
                "quilometragem": ad.css("div.olx-adcard_detail::attr(aria-label)").get(),
                "aceita_troca": ad.css("span[aria-label*='Aceita trocas']::text").get(),
            }

        next_page = response.css("a[title='Próxima página']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, headers=response.request.headers)
