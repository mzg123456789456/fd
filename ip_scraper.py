import re
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def extract_ip_port(url):
    """从单个页面提取IP:端口"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        
        ip_port_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(?:[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b'
        
        matches = re.findall(ip_port_pattern, text)
        return list(set(matches))
        
    except Exception as e:
        print(f"抓取 {url} 时出错: {str(e)}")
        return []

def save_to_file(ip_list, filename='ip.txt'):
    """保存结果到文件"""
    with open(filename, 'w') as f:
        f.write(f"# 最后更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for ip in ip_list:
            f.write(f"{ip}\n")

if __name__ == "__main__":
    # 从环境变量读取目标URL，或使用默认值
    target_urls = os.getenv('TARGET_URLS', '').split(',')
    if not target_urls or target_urls == ['']:
        target_urls = [
            "https://api.midtrans.com.freexxx.xhamster.biz.id/?page=1&wildcard=&configType=tls&search=JP",
            "https://api.midtrans.com.freexxx.xhamster.biz.id/?page=2&wildcard=&configType=tls&search=JP",
            "https://api.midtrans.com.freexxx.xhamster.biz.id/?page=3&wildcard=&configType=tls&search=JP"
        ]
    
    print(f"开始抓取 {len(target_urls)} 个目标URL...")
    
    all_ip_ports = []
    for url in target_urls:
        url = url.strip()
        if not url:
            continue
            
        print(f"\n正在处理: {url}")
        ip_ports = extract_ip_port(url)
        if ip_ports:
            print(f"找到 {len(ip_ports)} 个IP:端口")
            all_ip_ports.extend(ip_ports)
    
    if all_ip_ports:
        unique_ip_ports = sorted(list(set(all_ip_ports)))
        print(f"\n找到 {len(unique_ip_ports)} 个唯一IP:端口")
        save_to_file(unique_ip_ports)
    else:
        print("未找到任何IP:端口信息")
