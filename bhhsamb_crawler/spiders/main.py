import scrapy
from functools import partial

BASE_URL = "https://www.bhhsamb.com"
HEADERS = {
    'Referer': 'https://www.bhhsamb.com/roster/agents'
}

def get_agent_detail_link(l):
    return BASE_URL + l


class AgentSpider(scrapy.Spider):
    name = "agent"
    start_urls = ["https://www.bhhsamb.com/CMS/CmsRoster/RosterSection?layoutID=963&pageSize=10&pageNumber=1&sortBy=firstname-asc"]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=HEADERS)

    def parse(self, response, page_no=None):
        agents = response.css('a[class="site-roster-card-image-link"]::attr(href)').extract()
        agents_links = list(map(get_agent_detail_link, agents))

        for url in agents_links:
            yield scrapy.Request(url, callback=self.parse_agent)

        page_no = (page_no or 1) + 1
        next_page = "https://www.bhhsamb.com/CMS/CmsRoster/RosterSection?layoutID=963&pageSize=10&pageNumber=%s&sortBy=firstname-asc" % (page_no)
        callback = partial(self.parse, page_no=page_no)
        yield scrapy.Request(next_page, callback=callback, headers=HEADERS)
    
    def parse_agent(self, response):
        """
        To parse agent details
        """
        name = response.xpath('//p[@class="rng-agent-profile-contact-name"]//text()').get().strip()
        job_title = response.xpath('//span[@class="rng-agent-profile-contact-title"]//text()').extract_first(default="").strip()
        image_url = response.xpath('//img[@class="rng-agent-profile-photo"]//@src').get()
        address = "".join(response.xpath('//li[@class="rng-agent-profile-contact-address"]//text()[normalize-space()]').extract()).strip()
        phone_number = response.xpath('//li[@class="rng-agent-profile-contact-phone"]//a/text()').extract_first(default="").strip()
        offices = []
        languages = []
        description = response.xpath('//article[@class="rng-agent-profile-content"]//span/text()').extract_first(default="").strip()
        facebook =  response.xpath('//li[@class="social-facebook"]//a/@href').get()
        twitter =  response.xpath('//li[@class="social-twitter"]//a/@href').get()
        linkedin = response.xpath('//li[@class="social-linkedin"]//a/@href').get()
        youtube = response.xpath('//li[@class="social-youtube"]//a/@href').get()
        pinterest = response.xpath('//li[@class="social-pinterest"]//a/@href').get()
        instagram = response.xpath('//li[@class="social-instagram"]//a/@href').get()
        
        yield {
            'name': name,
            'job_title': job_title,
            'image_url': image_url,
            'address': address,
            'offices': offices,
            'languages': languages,
            'description': description,
            'contact_details': {
                'Office': "",
                'Fax': "",
                'Cell': phone_number
            },
            'social_accounts': {
                'facebook': facebook,
                'twitter': twitter,
                'linkedin': linkedin,
                'youtube': youtube,
                'pinterest': pinterest,
                'instagram': instagram
            }
        }
