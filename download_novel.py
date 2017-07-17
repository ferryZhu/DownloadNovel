#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'Ferry'


import requests
from bs4 import BeautifulSoup

# 获取小说章节URL
def get_novel_list(url):
	print("正在获取小说章节。。。")
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	title_tag = soup.find_all(class_ ="box_con")[0]
	info = title_tag.find("div", {"id":"info"})
	title = info.find("h1").get_text()
	print("小说名称：%s" % title)

	# 取出章节列表
	menu_tag = soup.find_all(class_ ="box_con")[1]

	urls = []
	for dd in menu_tag.find_all("dd"):
		url = "http://www.xs.la" +  dd.a.get('href')
		urls.append(url)

	print("开始下载")
	return (title, urls)

# 获取小说内容
def get_novel_content(url):
		response = requests.get(url)
		soup = BeautifulSoup(response.content, "html.parser")
		title_tag = soup.find_all(class_ ="bookname")[0]
		title = title_tag.find("h1")
		menu_tag = soup.find_all(class_ = "box_con")
		content = "#" + title.get_text() + "#\n" + soup.find("div", {"id":"content"}).get_text()
		content = content.replace('\xa0', '')
		content = content.replace('\u3000', '\n')
		# print("%s" %content)
		return (title.get_text(), str(content).encode("utf-8"))

# 搜索小说
def search_novel(name):	
		url = "http://zhannei.baidu.com/cse/search?s=1393206249994657467&q=%s" % name
		print("url = %s" % url)
		response = requests.get(url.encode("utf-8"))
		soup = BeautifulSoup(response.content, "html.parser")
		menu_tag = soup.find_all(class_ = "result-item result-game-item")
		result_tag = 0
		result_urls =[]
		print("搜索结果：")
		for title_tag in menu_tag:
			result_tag = result_tag + 1
			title = title_tag.h3.a.get("title")
			url = title_tag.h3.a.get("href")
			result_game_item_info_tag = title_tag.find(class_ = "result-game-item-info-tag")
			author_tag = result_game_item_info_tag.find_all("span")[1]
			author = author_tag.get_text()
			author = author.replace("\r", "")
			author = author.replace("\n", "")
			author = author.replace(" ", "")
			result_urls.append(url)
			print("%d. title = %s  作者：%s \n 下载地址：%s" % (result_tag, title, author, url))
		select_number =	int(input("请选择需要下载的小说:"))
		url = ""
		try:
			url = result_urls[select_number - 1]
			print("选择的是：%d 下载地址为：%s" % (select_number, result_urls[select_number - 1]))
		except Exception as e:
			print("序号选择错误")
		else:
			title, urls = get_novel_list(url)
			download_novel(title, urls)

# 下载小说			
def download_novel(title, urls):
	i = 0
	for url in urls:
		chapter_title,content = get_novel_content(url)
		method = 'wb'
		if i != 0 :
			method = 'ab'
		with open(title + ".txt", method) as f:
			f.write(content)
		i = i + 1
		print("%s 下载完成" % chapter_title)
	print("完毕，共下载 %d 章" % i)

if __name__ == '__main__':
	name = input("请输入你要搜索的小说：")
	search_novel(name)
	