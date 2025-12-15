import requests
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#initialization
seed_url="https://www.w3schools.com/"
seed_domain="w3schools.com"
queue=[seed_url]
visited=set()
page_id=1
MAX_PAGES=10

unique_urls=set()
duplicate_count=0

#creating folder 
if not os.path.exists("pages"):
	os.makedirs("pages")

#fetch page
def fetch_page(url):
	retries=3    #try maximum 3 times
	delay=2      #wait for 2 sec between retries
	for attempt in range(1,retries+1):
		try:
			response = requests.get(url,timeout=5,headers={"User-Agent": "WebScourCrawler/1.0"})
			if response.status_code == 200:
				print(f"[FETCHED] {url}")
				return response.text
			else:
				print(f"[ERROR] Failed ({response.status_code})->{url}")
				return None
		except Exception as e:
			print(f"[RETRY {attempt}/{retries}] Error fetching -> {url}")
			if attempt==retries:
				print(f"[FAILED] Giving up on {url}")
				return None
			time.sleep(delay) #wait for next retry
	
#extract links
def extract_links(html,base_url):
	soup=BeautifulSoup(html,"html.parser")
	links=set()

	for tag in soup.find_all("a",href=True):
		href=tag["href"].strip()

		#filtering useless links
		if href.startswith(("mailto:","javascript:","tel:","#")):
			continue

		#crawling the pages from the same domain
		#absolute URL
		if href.startswith("http"):
			if seed_domain in href:
				links.add(href)

		#relative URL
		elif href.startswith("/"):
			links.add(urljoin(base_url,href))
	return links

#start crawling
start_time=time.time()

#while queue is not empty and pages crawled < MAX_PAGES
while queue and page_id<=MAX_PAGES:
	url=queue.pop(0)
	if url in visited:
		duplicate_count +=1
		continue   #skipped because alredy visited
	print(f"Crawling {url}")
	
	#fetchpage html
	html=fetch_page(url)
	if html is None:
		continue
	#save html content into file
	savefile=f"pages/page_{page_id}.html"
	with open(savefile,"w",encoding="utf-8") as sf:
		sf.write(html)

	print(f"[SAVED] {savefile}")
	
	#extract links
	found_links=extract_links(html,seed_url)
	#add links to queue
	for link in found_links:

		if seed_domain not in link:
			print(f"[SKIPPED] Different domain -> {link}")
			continue
		if link not in visited and link not in queue:
			queue.append(link)
			unique_urls.add(link)
		else:
			duplicate_count+=1

	visited.add(url) #add visited url
	page_id+=1	 #increment the page_id
	time.sleep(0.5)  #sleep for a short term

end_time=time.time()
time_taken=round(end_time-start_time,2)

#save visited urls to visited.txt
with open("visited.txt","w",encoding="utf-8") as vt:
	for url in visited:
		vt.write(url+"\n")

#print total pages
print("\n ======= SUMMARY =======\n")
print(f"Total pages crawled: {page_id-1}")
print(f"Total unique URLs found: {len(unique_urls)}")
print(f"Total duplicate URLs seen: {duplicate_count}")
print(f"Time taken: {time_taken} seconds")
print("Visited URLs saved to visited.txt")