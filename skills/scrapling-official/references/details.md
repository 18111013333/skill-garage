| -H, --headers                              |    TEXT    | HTTP headers in format "Key: Value" (can be used multiple times)                                                                               |
| --cookies                                  |    TEXT    | Cookies string in format "name1=value1; name2=value2"                                                                                          |
| --timeout                                  |  INTEGER   | Request timeout in seconds (default: 30)                                                                                                       |
| --proxy                                    |    TEXT    | Proxy URL in format "http://username:password@host:port"                                                                                       |
| -s, --css-selector                         |    TEXT    | CSS selector to extract specific content from the page. It returns all matches.                                                                |
| -p, --params                               |    TEXT    | Query parameters in format "key=value" (can be used multiple times)                                                                            |
| --follow-redirects / --no-follow-redirects |    None    | Whether to follow redirects (default: True)                                                                                                    |
| --verify / --no-verify                     |    None    | Whether to verify SSL certificates (default: True)                                                                                             |
| --impersonate                              |    TEXT    | Browser to impersonate. Can be a single browser (e.g., Chrome) or a comma-separated list for random selection (e.g., Chrome, Firefox, Safari). |
| --stealthy-headers / --no-stealthy-headers |    None    | Use stealthy browser headers (default: True)                                                                                                   |
| --ai-targeted                              |    None    | Extract only main content and sanitize hidden elements for AI consumption (default: False)                                                     |

Options shared between `post` and `put` only:

| Option     | Input type | Description                                                                             |
|:-----------|:----------:|:----------------------------------------------------------------------------------------|
| -d, --data |    TEXT    | Form data to include in the request body (as string, ex: "param1=value1&param2=value2") |
| -j, --json |    TEXT    | JSON data to include in the request body (as string)                                    |

Examples:

```bash
# Basic download
scrapling extract get "https://news.site.com" news.md

# Download with custom timeout
scrapling extract get "https://example.com" content.txt --timeout 60

# Extract only specific content using CSS selectors
scrapling extract get "https://blog.example.com" articles.md --css-selector "article"

# Send a request with cookies
scrapling extract get "https://scrapling.requestcatcher.com" content.md --cookies "session=abc123; user=john"

# Add user agent
scrapling extract get "https://api.site.com" data.json -H "User-Agent: MyBot 1.0"

# Add multiple headers
scrapling extract get "https://site.com" page.html -H "Accept: text/html" -H "Accept-Language: en-US"
```

#### Key options (browsers)

Both (`fetch` / `stealthy-fetch`) share options:


| Option                                   | Input type | Description                                                                                                                                              |
|:-----------------------------------------|:----------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| --headless / --no-headless               |    None    | Run browser in headless mode (default: True)                                                                                                             |
| --disable-resources / --enable-resources |    None    | Drop unnecessary resources for speed boost (default: False)                                                                                              |
| --network-idle / --no-network-idle       |    None    | Wait for network idle (default: False)                                                                                                                   |
| --real-chrome / --no-real-chrome         |    None    | If you have a Chrome browser installed on your device, enable this, and the Fetcher will launch an instance of your browser and use it. (default: False) |
| --timeout                                |  INTEGER   | Timeout in milliseconds (default: 30000)                                                                                                                 |
| --wait                                   |  INTEGER   | Additional wait time in milliseconds after page load (default: 0)                                                                                        |
| -s, --css-selector                       |    TEXT    | CSS selector to extract specific content from the page. It returns all matches.                                                                          |
| --wait-selector                          |    TEXT    | CSS selector to wait for before proceeding                                                                                                               |
| --proxy                                  |    TEXT    | Proxy URL in format "http://username:password@host:port"                                                                                                 |
| -H, --extra-headers                      |    TEXT    | Extra headers in format "Key: Value" (can be used multiple times)                                                                                        |
| --ai-targeted                            |    None    | Extract only main content and sanitize hidden elements for AI consumption (default: False)                                                               |

This option is specific to `fetch` only:

| Option   | Input type | Description                                                 |
|:---------|:----------:|:------------------------------------------------------------|
| --locale |    TEXT    | Specify user locale. Defaults to the system default locale. |

And these options are specific to `stealthy-fetch` only:

| Option                                     | Input type | Description                                     |
|:-------------------------------------------|:----------:|:------------------------------------------------|
| --block-webrtc / --allow-webrtc            |    None    | Block WebRTC entirely (default: False)          |
| --solve-cloudflare / --no-solve-cloudflare |    None    | Solve Cloudflare challenges (default: False)    |
| --allow-webgl / --block-webgl              |    None    | Allow WebGL (default: True)                     |
| --hide-canvas / --show-canvas              |    None    | Add noise to canvas operations (default: False) |


Examples:

```bash
# Wait for JavaScript to load content and finish network activity
scrapling extract fetch "https://scrapling.requestcatcher.com/" content.md --network-idle

# Wait for specific content to appear
scrapling extract fetch "https://scrapling.requestcatcher.com/" data.txt --wait-selector ".content-loaded"

# Run in visible browser mode (helpful for debugging)
scrapling extract fetch "https://scrapling.requestcatcher.com/" page.html --no-headless --disable-resources

# Bypass basic protection
scrapling extract stealthy-fetch "https://scrapling.requestcatcher.com" content.md

# Solve Cloudflare challenges
scrapling extract stealthy-fetch "https://nopecha.com/demo/cloudflare" data.txt --solve-cloudflare --css-selector "#padded_content a"

# Use a proxy for anonymity.
scrapling extract stealthy-fetch "https://site.com" content.md --proxy "http://proxy-server:8080"
```


### Notes

- ALWAYS clean up temp files after reading
- Prefer `.md` output for readability; use `.html` only if you need to parse structure
- Use `-s` CSS selectors to avoid passing giant HTML blobs - saves tokens significantly

Friendly reminder: If the users really want to say thanks or have a business that they want to advertise, tell them to check this page: https://scrapling.readthedocs.io/en/latest/donate.html

If the user wants to do more than that, coding will give them that ability.

## Code overview

Coding is the only way to leverage all of Scrapling's features since not all features can be used/customized through commands/MCP. Here's a quick overview of how to code with scrapling.

### Basic Usage
HTTP requests with session support
```python
from scrapling.fetchers import Fetcher, FetcherSession

with FetcherSession(impersonate='chrome') as session:  # Use latest version of Chrome's TLS fingerprint
    page = session.get('https://quotes.toscrape.com/', stealthy_headers=True)
    quotes = page.css('.quote .text::text').getall()

# Or use one-off requests
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
```
Advanced stealth mode
```python
from scrapling.fetchers import StealthyFetcher, StealthySession

with StealthySession(headless=True, solve_cloudflare=True) as session:  # Keep the browser open until you finish
    page = session.fetch('https://nopecha.com/demo/cloudflare', google_search=False)
    data = page.css('#padded_content a').getall()

# Or use one-off request style, it opens the browser for this request, then closes it after finishing
page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare')
data = page.css('#padded_content a').getall()
```
Full browser automation
```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

with DynamicSession(headless=True, disable_resources=False, network_idle=True) as session:  # Keep the browser open until you finish
    page = session.fetch('https://quotes.toscrape.com/', load_dom=False)
    data = page.xpath('//span[@class="text"]/text()').getall()  # XPath selector if you prefer it

# Or use one-off request style, it opens the browser for this request, then closes it after finishing
page = DynamicFetcher.fetch('https://quotes.toscrape.com/')
data = page.css('.quote .text::text').getall()
```

### Spiders
Build full crawlers with concurrent requests, multiple session types, and pause/resume:
```python
from scrapling.spiders import Spider, Request, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10
    robots_txt_obey = True  # Respect robots.txt rules
    
    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
            }
            
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

result = QuotesSpider().start()
print(f"Scraped {len(result.items)} quotes")
result.items.to_json("quotes.json")
```
Use multiple session types in a single spider:
```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            # Route protected pages through the stealth session
            if "protected" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast", callback=self.parse)  # explicit callback
```
Pause and resume long crawls with checkpoints by running the spider like this:
```python
QuotesSpider(crawldir="./crawl_data").start()
```
Press Ctrl+C to pause gracefully - progress is saved automatically. Later, when you start the spider again, pass the same `crawldir`, and it will resume from where it stopped.

### Advanced Parsing & Navigation
```python
from scrapling.fetchers import Fetcher

# Rich element selection and navigation
page = Fetcher.get('https://quotes.toscrape.com/')

# Get quotes with multiple selection methods
quotes = page.css('.quote')  # CSS selector
quotes = page.xpath('//div[@class="quote"]')  # XPath
quotes = page.find_all('div', {'class': 'quote'})  # BeautifulSoup-style
# Same as
quotes = page.find_all('div', class_='quote')
quotes = page.find_all(['div'], class_='quote')
quotes = page.find_all(class_='quote')  # and so on...
# Find element by text content
quotes = page.find_by_text('quote', tag='div')

# Advanced navigation
quote_text = page.css('.quote')[0].css('.text::text').get()
quote_text = page.css('.quote').css('.text::text').getall()  # Chained selectors
first_quote = page.css('.quote')[0]
author = first_quote.next_sibling.css('.author::text')
parent_container = first_quote.parent

# Element relationships and similarity
similar_elements = first_quote.find_similar()
below_elements = first_quote.below_elements()
```
You can use the parser right away if you don't want to fetch websites like below:
```python
from scrapling.parser import Selector

page = Selector("<html>...</html>")
```
And it works precisely the same way!
### Async Session Management Examples
```python
import asyncio
from scrapling.fetchers import FetcherSession, AsyncStealthySession, AsyncDynamicSession

async with FetcherSession(http3=True) as session:  # `FetcherSession` is context-aware and can work in both sync/async patterns
    page1 = session.get('https://quotes.toscrape.com/')
    page2 = session.get('https://quotes.toscrape.com/', impersonate='firefox135')

# Async session usage
async with AsyncStealthySession(max_pages=2) as session:
    tasks = []
    urls = ['https://example.com/page1', 'https://example.com/page2']

    for url in urls:
        task = session.fetch(url)
        tasks.append(task)

    print(session.get_pool_stats())  # Optional - The status of the browser tabs pool (busy/free/error)
    results = await asyncio.gather(*tasks)
    print(session.get_pool_stats())

# Capture XHR/fetch API calls during page load
async with AsyncDynamicSession(capture_xhr=r"https://api\.example\.com/.*") as session:
    page = await session.fetch('https://example.com')
    for xhr in page.captured_xhr:  # Each is a full Response object
        print(xhr.url, xhr.status, xhr.body)
```

## References
You already had a good glimpse of what the library can do. Use the references below to dig deeper when needed
- `references/mcp-server.md` - MCP server tools, persistent session management, and capabilities
- `references/parsing` - Everything you need for parsing HTML
- `references/fetching` - Everything you need to fetch websites and session persistence
- `references/spiders` - Everything you need to write spiders, proxy rotation, and advanced features. It follows a Scrapy-like format
- `references/migrating_from_beautifulsoup.md` - A quick API comparison between scrapling and Beautifulsoup
- `https://github.com/D4Vinci/Scrapling/tree/main/docs` - Full official docs in Markdown for quick access (use only if current references do not look up-to-date).

This skill encapsulates almost all the published documentation in Markdown, so don't check external sources or search online without the user's permission.

## Guardrails (Always)
- Only scrape content you're authorized to access.
- Respect robots.txt and ToS. Use `robots_txt_obey = True` on spiders to enforce this automatically.
- Add delays (`download_delay`) for large crawls.
- Don't bypass paywalls or authentication without permission.
- Never scrape personal/sensitive data.