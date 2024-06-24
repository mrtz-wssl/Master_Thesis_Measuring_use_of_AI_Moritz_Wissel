from waybackmachine_crawler import waybackmachine_crawler

#  Example usage
x = waybackmachine_crawler('www.anthropic.com')
x.crawl_from_date(2013,1,1)



my_websites = ['https://web.archive.org/web/20210601005416/https://www.anthropic.com/']
#my_websites.crawl_from_date(2018,1,1)
#crawler = waybackmachine_crawler()
#crawler.set_websites(my_websites)
#crawler.start_crawling(levels = 1)