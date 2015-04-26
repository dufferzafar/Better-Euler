import json
import scrapy

from euler.items import EulerItem


class EulerSpider(scrapy.Spider):
    name = "euler"
    allowed_domains = ["projecteuler.net"]

    start_urls = []
    # Todo: Find a way to determine the number of PE question
    for i in range(1, 502):
        start_urls.append("https://projecteuler.net/problem=%d" % i)

    def parse(self, response):
        content = response.xpath("//div[contains(@id, 'content')]")
        info = content.xpath("//div[contains(@id, 'problem_info')]/span/text()")\
            .re('Published on (.*); Solved by (\d+)')
        text = content.xpath("//div[contains(@class, 'problem_content')]/p//text()").extract()

        item = EulerItem()
        item["name"] = content.xpath("//h2/text()").extract()[0]
        item["published"] = info[0]
        item["solvers"] = int(info[1])
        item["text"] = "".join(text)

        # Dump data to disk
        # Todo: Pipeline? JSON Exporter?
        filename = response.url.split("=")[1]+".json"
        with open("data/"+filename, 'w') as fp:
            json.dump(dict(item), fp, indent=1)
