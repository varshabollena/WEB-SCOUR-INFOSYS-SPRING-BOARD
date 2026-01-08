import requests
import time
import os
import multiprocessing
import pika
from bs4 import BeautifulSoup
from urllib.parse import urljoin

Rabbitmq_host="localhost"
Queue_name="url_queue"
Max_pages=10
os.makedirs("pages",exist_ok=True)

#------------fetch page-----------
def fetch_page(url):
	try:
		response = requests.get(url,timeout=5,headers={"User-Agent": "WebScourCrawler/1.0"})
		if response.status_code == 200:
			return response.text
	except Exception:
		pass
	return None
			
#------------extract links----------
def extract_links(html,base_url):
	soup=BeautifulSoup(html,"html.parser")
	links=set()
	for tag in soup.find_all("a",href=True):		
		absolute_url=urljoin(base_url,tag["href"])
		links.add(absolute_url)
	return links
	
#--------SAVE HTML---------
def save_html(page_id,html):
	filename=f"pages/{page_id}.html"
	with open(filename,"w",encoding="utf-8") as file:
		file.write(html)
	print(f"[SAVED] {filename}")

#-------------WORKER FUNCTION-----------
def worker(worker_id,page_counter):
	visited=set()

	#task 8:prevent duplicates flooding and stores urls sent back to rabbitmq
	sent_urls=set()

	def callback(ch,method,properties,body):
		url=body.decode()
		print(f"\n[WORKER-{worker_id}] Crawling => {url}")

		if url in visited:
			ch.basic_ack(delivery_tag=method.delivery_tag)
			print(f"[WORKER-{worker_id}] SKIPPED (visited)")
			return
		
    	#fetch page
		html=fetch_page(url)
		if html is None:
			ch.basic_ack(delivery_tag=method.delivery_tag)
			print(f"[WORKER-{worker_id}] FETCH FAILED")
			return
		
		with page_counter.get_lock():
			if page_counter.value>=Max_pages:
				ch.basic_ack(delivery_tag=method.delivery_tag)
				print(f"[WORKER-{worker_id}] MAX_PAGES reached.So stopping the workers")
				ch.stop_consuming()
				return
			page_counter.value+=1
			page_id=page_counter.value
		
    	#save html
		save_html(page_id,html)
	
		#Extract links
		links=extract_links(html,url)

		#task 8 conditions:
		#Send new links back to RabbitMQ
		for link in links:
			if link.startswith("http") and link not in sent_urls:
				ch.basic_publish(
					exchange="",
					routing_key=Queue_name,
					body=link
				)
				sent_urls.add(link)

		visited.add(url)
			
		ch.basic_ack(delivery_tag=method.delivery_tag)
		print(f"[WORKER-{worker_id}] ACK => {url}")

	#----------RABBITMQ setup--------
	connection=pika.BlockingConnection(
		pika.ConnectionParameters(host=Rabbitmq_host)
	)
	channel=connection.channel()

	channel.queue_declare(queue=Queue_name,durable=True)

	#Task 9:Workers process different URLs
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(queue=Queue_name,on_message_callback=callback)

	print(f"[WORKER-{worker_id}] Waiting for URLs...")
	channel.start_consuming()


if __name__=="__main__":
	#task 10:record time taken
	start_time=time.time()

	#Task 9:multiple worker process
	num_workers=3

	#Task 10:shared counter for total pages crawled
	page_counter=multiprocessing.Value('i',0)
	processes=[]
	

	for i in range(num_workers):
		p=multiprocessing.Process(
			target=worker,
			args=(i+1,page_counter)
		)
		p.start()
		processes.append(p)

	for p in processes:
		p.join()

	#SUMMARY
	end_time=time.time()
	total_time=end_time - start_time

	print("===============SUMMARY================")
	print(f"Number of workers used   : {num_workers}")
	print(f"Total pages crawled      : {page_counter.value}")
	print(f"Total time taken (sec)   : {total_time:.2f}")
	print("======================================")
