BOT_NAME = "price_manager_scraper"

SPIDER_MODULES = [
  "price_manager.scraper.spiders",
]

NEWSPIDER_MODULE = "price_manager.scraper.spiders"

ROBOTSTXT_OBEY = False

USER_AGENT = (
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
  "AppleWebKit/537.36 (KHTML, like Gecko) "
  "Chrome/120.0.0.0 Safari/537.36"
)

DEFAULT_REQUEST_HEADERS = {
  "Accept": (
    "text/html,application/xhtml+xml,application/xml;"
    "q=0.9,image/avif,image/webp,*/*;q=0.8"
  ),
  "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
  "Cache-Control": "no-cache",
  "Pragma": "no-cache",
  "Referer": "https://www.google.com/",
}

ITEM_PIPELINES = {
  "price_manager.scraper.pipelines.StarComputacionPipeline": 300,
}

DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 20

RETRY_ENABLED = True
RETRY_TIMES = 2

HTTPERROR_ALLOWED_CODES = [403, 404]

LOG_LEVEL = "INFO"
