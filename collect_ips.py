import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://api.midtrans.com.freexxx.xhamster.biz.id/?page=1&wildcard=&configType=tls&search=JP'
        ]

# 正则表达式用于匹配IP:端口
ip_port_pattern = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::(?:[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 使用集合来存储IP:端口，自动去重
unique_ip_ports = set()

for url in urls:
    try:
        # 发送HTTP请求获取网页内容
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.midtrans.com.freexxx.xhamster.biz.id/?page=1&wildcard=&configType=tls&search=JP':
            # 特殊处理cloudflare.html的表格结构
            for tr in soup.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:  # 确保有足够的列
                    ip_port = f"{tds[0].get_text(strip=True)}:{tds[1].get_text(strip=True)}"
                    if re.fullmatch(ip_port_pattern, ip_port):
                        unique_ip_ports.add(ip_port)
        else:
            # 其他网站的处理方式
            text = soup.get_text()
            matches = re.findall(ip_port_pattern, text)
            unique_ip_ports.update(matches)
            
    except Exception as e:
        print(f"处理 {url} 时出错: {str(e)}")
        continue

# 将去重后的IP:端口写入文件
with open('ip.txt', 'w') as file:
    for ip_port in sorted(unique_ip_ports):
        file.write(ip_port + '\n')

print(f'共找到 {len(unique_ip_ports)} 个唯一IP:端口组合，已保存到ip.txt文件中。')
