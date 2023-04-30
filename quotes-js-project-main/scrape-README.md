Creating a project: 
    scrapy startproject tutorial

How to run spider
    scrapy crawl <spider-name>

To access scrapy shell
    scrapy shell 'https://quotes.toscrape.com/page/1/'

### Settings
    https://docs.scrapy.org/en/latest/topics/settings.html

    => scrapy crawl myspider -s DOWNLOAD_HANDLERS = {"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler","https":"scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",}  (or)  change in settings.py


### To get dynamic web content install scrapy-playwright
    https://docs.scrapy.org/en/latest/topics/dynamic-content.html
    https://github.com/scrapy-plugins/scrapy-playwright

### Installations
    https://github.com/python-scrapy-playbook/quotes-js-project
    pip3 install Scrapy
    pip3 install scrapy-playwright
    playwright install firefox chromium
    pip3 install pyyaml