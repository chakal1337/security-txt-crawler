import sys
import requests
import threading
import time
import random
import string

debug = 0

urlsfound = []

with open("top10000.txt", "rb") as file:
 url_list = file.read().decode().splitlines()

def crawl():
 global url_list, urlsfound
 while 1:
  try:
   with threading.Lock(): url = url_list.pop(0)
   url = url+"/.well-known/security.txt"
   #print("Testing: {}".format(url))
   headers = {
    "User-Agent":"SecCheck +(Security Research Crawler)"
   }
   r = requests.get(url=url, headers=headers, timeout=5, allow_redirects=False)
   if r.status_code == 200:
    if "Contact:" in r.text: 
     print(url)
     with threading.Lock(): urlsfound.append(url)
  except Exception as error:
   if debug == 1: print(error)

def main():
 threads = []
 for i in range(200):
  t=threading.Thread(target=crawl)
  t.start()
  threads.append(t)
 for t in threads:
  t.join()

if __name__ == '__main__':
 main()
 with open("outputs.txt", "wb") as file:
  file.write("".join(urlsfound).encode())
  file.close()