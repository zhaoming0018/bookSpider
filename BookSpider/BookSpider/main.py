from scrapy import cmdline
# cmdline.execute("scrapy crawl dangdang -o jingdong.jl -s FEED_EXPORT_ENCODING='utf-8'  -s JOBDIR=jobs/001".split())
#cmdline.execute('scrapy crawl suning'.split())
cmdline.execute('scrapy crawl dangdang'.split())
