import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://api.midtrans.com.freexxx.xhamster.biz.id/?page=1&wildcard=&conf', 
        'https://api.midtrans.com.freexxx.xhamster.biz.id/?page=2&wildcard=&conf',
        'https://api.midtrans.com.freexxx.xhamster.biz.id/?page=3&wildcard=&conf'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 使用集合来存储IP地址，自动去重
unique_ips = set()

for url in urls:
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 根据网站的不同结构找到包含IP地址的元素
    if url == 'https://api.midtrans.com.freexxx.xhamster.biz.id/?page=1&wildcard=&conf':
        elements = soup.find_all('tr')
    elif url == 'https://api.midtrans.com.freexxx.xhamster.biz.id/?page=2&wildcard=&conf':
        elements = soup.find_all('tr')
    elif url == 'https://api.midtrans.com.freexxx.xhamster.biz.id/?page=3&wildcard=&conf':
        elements = soup.find_all('tr')
    else:
        elements = soup.find_all('li')
    
    # 遍历所有元素,查找IP地址
    for element in elements:
        element_text = element.get_text()
        ip_matches = re.findall(ip_pattern, element_text)
        
        # 将找到的IP地址添加到集合中（自动去重）
        unique_ips.update(ip_matches)

# 将去重后的IP地址写入文件
with open('ip.txt', 'w') as file:
    for ip in unique_ips:
        file.write(ip + '\n')

print(f'共找到 {len(unique_ips)} 个唯一IP地址，已保存到ip.txt文件中。')
