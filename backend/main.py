import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
import feedparser
import requests
import google.generativeai as genai
from datetime import datetime, timezone
from itertools import chain
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# data.pyからツールマップのデータを読み込みます
from data import TOOL_LANDSCAPE_DATA

app = Flask(__name__)
CORS(app)

# --- Part 1: 静的データ（AIツール市場マップ）---
@app.route("/")
def get_tool_landscape_handler():
    """トップページ用の静的なツールマップデータを返す"""
    return jsonify(TOOL_LANDSCAPE_DATA)

# --- Part 2: 動的データ（最新AIニュース）---
def categorize_news(title, content):
    title_lower = title.lower(); content_lower = content.lower()
    if any(k in title_lower for k in ["funding", "raised", "investment"]): return "資金調達"
    if any(k in title_lower for k in ["launches", "releases", "model", "paper"]): return "新技術・リリース"
    if any(k in content_lower for k in ["google", "openai", "meta", "anthropic", "microsoft"]): return "企業動向"
    return "一般ニュース"

def get_news_from_feed(url, source_name):
    items = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # ★★★ ここを修正しました ★★★
        # 不要な socket_timeout 引数を削除
        feed = feedparser.parse(url, request_headers=headers)
        
        for entry in feed.entries:
            soup = BeautifulSoup(entry.summary, 'html.parser')
            clean_content = soup.get_text(separator=' ', strip=True)[:1500]
            dt = datetime.now(timezone.utc)
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc)
            category = categorize_news(entry.title, clean_content)
            items.append({"source": source_name, "title": entry.title, "link": entry.link, "content": clean_content, "published_date": dt, "category": category})
    except Exception as e:
        print(f"{source_name}の取得に失敗: {e}")
    return items

def analyze_for_pm(news_item, gemini_model):
    if not news_item or not news_item.get('content'): return news_item
    time.sleep(1)
    try:
        prompt = f"以下のAI関連ニュースの重要性を、AIプロダクトマネージャーの視点で150字程度の日本語で分析してください。\n---\nタイトル: {news_item['title']}\n概要: {news_item['content']}"
        response = gemini_model.generate_content(prompt)
        news_item['summary'] = response.text.strip().replace('\n', ' ')
    except Exception as e:
        print(f"Gemini API Error for '{news_item.get('title')}': {e}")
        news_item['summary'] = "AIによる分析中にエラーが発生しました。"
    return news_item

@app.route("/api/news")
def get_ai_news_handler():
    """最新ニュースを取得・分析して返す"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key: return jsonify({"error": "APIキーが設定されていません。"}), 500
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return jsonify({"error": f"APIの初期化に失敗しました: {e}"}), 500
    
    fetch_functions = [
        get_news_from_feed("https://www.producthunt.com/topics/ai.rss", "Product Hunt"),
        get_news_from_feed("https://www.bensbites.co/feed", "Ben's Bites"),
        get_news_from_feed("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch"),
    ]
    with ThreadPoolExecutor(max_workers=len(fetch_functions)) as executor:
        list_of_lists = executor.map(lambda f: f, fetch_functions)
        all_news_items = list(chain.from_iterable(list_of_lists))

    all_news_items.sort(key=lambda x: x.get('published_date', datetime.now(timezone.utc)), reverse=True)
    top_5_news = all_news_items[:5]
    analyzed_news = [analyze_for_pm(item, model) for item in top_5_news]
    
    return jsonify({"news": analyzed_news})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))