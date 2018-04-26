# stock
usage:
1, docker run -p 8050:8050 scrapinghub/splash
2, scrapy crawl eastmoney

scrapy shell 'http://localhost:8050/render.html?url=http://domain.com/page-with-javascript.html&timeout=10&wait=0.5'
