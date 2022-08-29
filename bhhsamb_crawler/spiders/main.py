import scrapy

BASE_URL = "https://www.bhhsamb.com"
HEADERS = {
    'Referer': 'https://www.bhhsamb.com/roster/agents'
}

def agent_detail_link(l):
    return BASE_URL + l


class BhhSambSpider(scrapy.Spider):
    name = "bhhsamb"
    start_urls = ["https://www.bhhsamb.com/CMS/CmsRoster/RosterSection?layoutID=963&pageSize=10&pageNumber=1&sortBy=firstname-asc"]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=HEADERS)

    def parse(self, response, **kwargs):
        agents = response.css('a[class="site-roster-card-image-link"]::attr(href)').extract()
        agents_links = list(map(agent_detail_link, agents))

        for url in agents_links:
            yield scrapy.Request(url, callback=self.parse_agent)
        return super().parse(response, **kwargs)
    
    def parse_agent(self, response):
        """
        To parse agent details
        """
        name = response.css('p[class="rng-agent-profile-contact-name"]::text').get().strip()
        job_title = response.css('span[class="rng-agent-profile-contact-title"]::text').get()
        image_url = response.css('img[class="rng-agent-profile-photo"]::attr(src)').get()
        address = " ".join(response.css('li[class="rng-agent-profile-contact-address"] strong').get().split()).replace('<strong>', '')
        phone_number = response.css('li[class="rng-agent-profile-contact-phone"] a::text').extract_first(default='')
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
            'contact_details': {
                'Office': "",
                'Fax': "",
                'Cell': phone_number
            },
            'offices': offices,
            'languages': languages,
            'description': description,
            'social_accounts': {
                'facebook': facebook or '',
                'twitter': twitter or '',
                'linkedin': linkedin or '',
                'youtube': youtube or '',
                'pinterest': pinterest or '',
                'instagram': instagram or ''
            }
        }
