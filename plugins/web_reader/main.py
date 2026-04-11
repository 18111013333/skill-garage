#!/usr/bin/env python3
"""
网页读取插件
"""

import requests
from bs4 import BeautifulSoup

def tool_main(arg: dict) -> str:
    """
    读取网页内容
    
    Args:
        arg: {"url": "网页地址", "selector": "CSS选择器(可选)"}
    
    Returns:
        str: 网页内容
    """
    url = arg.get("url", "")
    selector = arg.get("selector", "")
    
    if not url:
        return "错误: 请提供 url 参数"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 移除脚本和样式
        for script in soup(["script", "style"]):
            script.decompose()
        
        if selector:
            elements = soup.select(selector)
            text = "\n".join([e.get_text(strip=True) for e in elements])
        else:
            text = soup.get_text(strip=True, separator="\n")
        
        # 限制长度
        if len(text) > 5000:
            text = text[:5000] + "\n... [内容已截断]"
        
        return text
    
    except Exception as e:
        return f"错误: {str(e)}"
