import scrapy
from functools import partial

BASE_URL = "https://www.bhhsamb.com"
HEADERS = {
    'Referer': 'https://www.bhhsamb.com/roster/agents'
}

def agent_detail_link(l):
    return BASE_URL + l


class BhhSambSpider(scrapy.Spider):
    name = "bhhsamb"
    start_urls = ["https://www.bhhsamb.com/CMS/CmsRoster/RosterSection?layoutID=963&pageSize=10&pageNumber=1&sortBy=firstname-desc"]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=HEADERS)

    def parse(self, response, page_no=None):
        agents = response.css('a[class="site-roster-card-image-link"]::attr(href)').extract()
        agents_links = list(map(agent_detail_link, agents))

        for url in agents_links:
            yield scrapy.Request(url, callback=self.parse_agent)

        page_no = (page_no or 1) + 1
        next_page = "https://www.bhhsamb.com/CMS/CmsRoster/RosterSection?layoutID=963&pageSize=10&pageNumber=%s&sortBy=firstname-desc" % (page_no)
        callback = partial(self.parse, page_no=page_no)
        yield scrapy.Request(next_page, callback=callback, headers=HEADERS)
    
    def parse_agent(self, response):
        """
        To parse agent details
        """
        name = response.css('p[class="rng-agent-profile-contact-name"]::text').get().strip()
        job_title = response.css('span[class="rng-agent-profile-contact-title"]::text').get()
        image_url = response.css('img[class="rng-agent-profile-photo"]::attr(src)').get()
        address = "".join(response.xpath('//li[@class="rng-agent-profile-contact-address"]//text()[normalize-space()]').extract()).strip()
        phone_number = response.css('li[class="rng-agent-profile-contact-phone"] a::text').extract_first(default='').strip()
        offices = []
        languages = []
        description = response.css('article[class="rng-agent-profile-content"] span::text').get()
        facebook =  response.css('li[class="social-facebook"] a::attr(href)').get()
        twitter =  response.css('li[class="social-twitter"] a::attr(href)').get()
        instagram = response.css('li[class="social-instagram"] a::attr(href)').get()
        youtube = response.css('li[class="social-youtube"] a::attr(href)').get()
        pinterest = response.css('li[class="social-pinterest"] a::attr(href)').get()
        linkedin = response.css('li[class="social-linkedin"] a::attr(href)').get() 
        
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
                'facebook': facebook or '',
                'twitter': twitter or '',
                'linkedin': linkedin or '',
                'youtube': youtube or '',
                'pinterest': pinterest or '',
                'instagram': instagram or ''
            }
        }
