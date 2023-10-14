import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess


class ProfessorSpider(scrapy.Spider):
    name = 'professors'
    allowed_domains = ['cis.um.edu.mo']
    start_urls = ['https://www.cis.um.edu.mo/acadstaff.html']

    def parse(self, response):
        professors = response.xpath("//table[@id='stafflist']//td")

        profData = []
        for professor in professors:
            name = professor.xpath(".//a[@class='staffname']/text()").get()
            title = professor.xpath(".//span[@class='stafftitle']/text()").get()
            email = professor.xpath(".//span[@class='tel']/preceding-sibling::text()[contains(., 'Email')]").get()
            tel = professor.xpath(".//span[@class='tel']/text()[contains(.,'Tel')]").get()
            location = professor.xpath(".//span[@class='location']/text()").get()
            research_interests = professor.xpath(".//div[@class='research']/text()").get()

            if name:
                name = name.strip()
                print("Name:", name)
            if title:
                title = title.strip()
                print("Title:", title)
            if email:
                email = email.strip()
                email = email + '@um.edu.mo'
                print(email)    # The text itself contains "Email"
            if tel:
                tel = tel.strip()
                print(tel)
            if location:
                location = location.strip()
                print("Location:", location)
            if research_interests:
                research_interests = research_interests.strip()
                print("Research Interests:", research_interests)
                print('\n')

            if name:
                profData.append(
                    {
                        "name": name,
                        "title": title,
                        "email": email,
                        "tel": tel,
                        "location": location,
                        "research_interests": research_interests
                    }
                )

        df = pd.DataFrame(profData)
        df.to_excel("Professors.xlsx",index = False);


# Present result
process = CrawlerProcess()
process.crawl(ProfessorSpider)
process.start()  # Start Crawler
