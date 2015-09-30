#!/Users/chris/.virtualenvs/scraping/bin/python
# -*- coding: utf-8 -*-

import contextlib
import selenium.webdriver as webdriver
import bs4 as bs
import shelve
import pprint
import re

def download_from_url(url):
  phantomjs = 'phantomjs'
  with contextlib.closing(webdriver.PhantomJS(phantomjs)) as driver:
    driver.get(url)
    content = driver.page_source
    return content

def parse_cue_responses(content):
  soup = bs.BeautifulSoup(content, 'lxml')
  cr_divs = soup.find_all('div','cue-response')
  crs = {}
  for cr_div in cr_divs :
    cue = cr_div.find('span','cue').string
    response = cr_div.find('p','response').string
    crs[cleanup_response(response)] = cue
  return crs

def cleanup_response(response):
  response,_,_ = response.partition(",")
  response,_,_ = response.partition(";")
  response = response.replace("to ","")
  response = re.sub(r'\([^)]*\)', '', response)
  response = response.lower().strip()
  return response


course = 694846
url = "http://iknow.jp/courses/%d?language_code=en" % course
pp = pprint.PrettyPrinter(indent=4)

s = shelve.open('iknow-scrape-shelf.db')
try:
  if not url in s : s[url] = download_from_url(url)
  content = s[url]
  cue_responses = parse_cue_responses(content)
  pp.pprint (cue_responses)

finally:
    s.close()
