
# WebScour: A Distributed Web Crawler and Search Engine
PROBLEM STATEMENT :
With the rapid growth of the internet, a huge amount of information is spread across millions of web pages. Manually searching, collecting and organizing this information is inefficient and time-consuming.
There is a need for a lightweight, efficient and scalable web crawling system that can automatically traverse web pages, extract relevant links and content, and store the collected data for further processing and search operations.
The challenge is to design and implement a Python-based web crawler that:
	Starts from a given seed URL
	Crawls web pages systematically
	Avoids duplicate and irrelevant pages
	Works within defined limits(domain and page count)
	Can be extended into a distributed crawler and search engine
Finally this project, WebScour aims to address this problem by developing a modular and extensible web crawling system that forms the foundation for a distributed search engine. 

# KEY CONCEPTS USED IN THE PROJECT :
1.	WEB CRAWLER : A web crawler is a software program that automatically visits web pages starting from a given URL, downloads their content, and follows the links found on those pages.
In this project, the crawler systematically navigates through websites, collects page data, and avoids revisiting the same URLs.
2.	WEB SCRAPING : Web scraping is the process of extracting useful information from web pages such as text, links or metadata.
In this project,the scraping is used to extract page content and hyperlinks using Python libraries like BeautifulSoup.
3.	SEARCH ENGINE : A search engine is a system that collects web data, indexes it, and allows users to search for relevant information efficiently.
In this project,the crawler acts as the foundation for building a search engine in future milestones.
4.	WEB SCOUR : Webscour is a Python -based web crawling system designed to automatically crawl websites, extract links and content, and store the collected data.
It is designed to be modular, scalable and extendable into a distributed crawler and search engine.
5.	DISTRIBUTED : distributed means that the web crawling and data processing work is divided across multiple systems or processes instead of being handled by a single program or machine.
INDUSTRY USE CASE :
Why webscour is relevant for companies ?
WebScour is useful for businesses since it offers an automated, scalable, and customized way to gather web data according to particular business requirements. Businesses may control what data is collected, how frequently it is collected, and from which sources by using systems like WebScour instead of depending on third-party applications or manual data collecting.
How companies use webscour ?
Companies use WebScour to:
•	crawl particular websites or domains that are pertinent to their company.
•	Extract structured data, including news, employment listings, product details, text, and links.
•	Keep an eye on competitor data, trends, and website upgrades.
•	Save gathered information for reporting, analytics, and search systems.
•	Construct internal or external search engines
Example Companies Using Similar Systems :
•	Google & Bing - use large-scale crawlers to index web content for search results
•	Amazon & Flipkart - collect and analyze product and pricing data
•	LinkedIn & Indeed - aggregate job postings and public profile data
•	MakeMyTrip & Booking.com - gather travel and availability information
•	Media & Research companies - collect articles, blogs, and reports from multiple sources
HIGH LEVEL ARCHITECTURE FOR WEB SCOUR :
 
Seed URLs :- Seed URLs act as the entry point for the crawler.
Crawler :- The crawler automatically visits web pages and collects their content and links.
Page Storage :- Page storage saves the crawled content for future processing.
Indexer :- The indexer converts raw web pages into searchable data.
Search Engine :- The search engine helps users find relevant information from the crawled data.
WHY PYTHON FITS CRAWLING WELL ?
Python supports these data structures with simple syntax and strong library support, allowing efficient URL management, duplicate handling, and data storage with minimal code.
1.	Functions : Functions are reusable blocks of code that perform a specific task.
In our project, functions are used to separate crawling tasks such as fetching a page, extracting links, and storing content. This makes the crawler modular, readable, and easy to maintain.
2.	Lists : Lists are ordered collections used to store multiple values.
Lists are used to maintain the queue of URLs that need to be crawled. URLs are added when discovered and removed once processed.
3.	Sets : Sets store unique values and automatically remove duplicates.
Sets are used to keep track of visited URLs, ensuring the crawler does not revisit the same page multiple times.
4.	Dictionaries : Dictionaries store data in key–value pairs.
Dictionaries can be used to store metadata such as page ID and URL, page content mapping, or crawl status information.
