import re
import requests
from bs4 import BeautifulSoup

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
        
        # 精确的IP:端口正则表达式
        ip_port_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(?:[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b'
        
        matches = re.findall(ip_port_pattern, text)
        return list(set(matches))  # 去重
        
    except Exception as e:
        print(f"抓取 {url} 时出错: {str(e)}")
        return []

def save_to_file(ip_list, filename='ip.txt'):
    """保存结果到文件"""
    with open(filename, 'w') as f:
        for ip in ip_list:
            f.write(f"{ip}\n")
    print(f"已保存 {len(ip_list)} 个IP地址到 {filename}")

if __name__ == "__main__":
    # 在这里填写你的目标网址列表
    target_urls = [
        "https://api.midtrans.com.freexxx.xhamster.biz.id/?page=1&wildcard=&configType=tls&search=JP",
        "https://api.midtrans.com.freexxx.xhamster.biz.id/?page=2&wildcard=&configType=tls&search=JP",
        "https://api.midtrans.com.freexxx.xhamster.biz.id/?page=3&wildcard=&configType=tls&search=JP"
        # 添加更多具体网址...
    ]
    
    all_ip_ports = []
    
    for url in target_urls:
        print(f"正在处理: {url}")
        ip_ports = extract_ip_port(url)
        if ip_ports:
            print(f"找到 {len(ip_ports)} 个IP:端口")
            all_ip_ports.extend(ip_ports)
    
    if all_ip_ports:
        # 最终去重
        unique_ip_ports = list(set(all_ip_ports))
        print("\n找到的所有唯一IP地址和端口:")
        for item in unique_ip_ports:
            print(item)
        
        save_to_file(unique_ip_ports)
    else:
        print("未找到任何IP:端口信息")
