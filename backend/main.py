import os
import requests
import feedparser
import google.generativeai as genai
import json # <-- 【重要】この一行を追加しました
# === ここから法人番号APIの機能をコメントアウト ===
# import xml.etree.ElementTree as ET
# from urllib.parse import quote
# === ここまで ===
from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import secretmanager

# backend/data.py からツールデータをインポート
from data import TOOL_LANDSCAPE_DATA

app = Flask(__name__)
CORS(app)  # クロスオリジンリクエストを許可する

# --- Secret ManagerからAPIキーを取得する関数 ---
def get_secret(secret_id, version_id="latest"):
    """
    Secret Managerからシークレットの値を取得する
    """
    project_id = os.environ.get("GCP_PROJECT")
    if not project_id:
        # ローカル環境などでGCP_PROJECTが設定されていない場合のフォールバック
        # 実際のプロジェクトIDに置き換えてください
        project_id = "my-ai-news-app-final" 

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret: {e}")
        return None

# --- エンドポイント定義 ---

# ツールマップのデータを返すエンドポイント
@app.route('/')
def index():
    return jsonify(TOOL_LANDSCAPE_DATA)

# 最新AIニュースを返すエンドポイント
@app.route('/api/news')
def get_news():
    # (ニュース機能のコードは変更なし)
    rss_feeds = {
        "Google AI Blog": "https://ai.googleblog.com/feeds/posts/default",
        "OpenAI Blog": "https://openai.com/blog/rss.xml",
        "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    }
    
    all_articles = []
    for source, url in rss_feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]: # 各フィードから最新5件を取得
                all_articles.append({
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                })
        except Exception as e:
            print(f"Error fetching RSS feed from {url}: {e}")

    if not all_articles:
        return jsonify({"error": "Failed to fetch news articles"}), 500

    gemini_api_key = get_secret("GEMINI_API_KEY")
    if not gemini_api_key:
        return jsonify({"error": "Gemini API key not found"}), 500
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

    formatted_articles = "\n".join([f"- {a['title']}" for a in all_articles])
    prompt = f"""
    以下のAI関連ニュース記事のリストから、AIプロダクトマネージャーにとって最も重要だと考えられるトップ5の記事を選び、その選定理由とPM視点での簡単な分析を日本語で加えてください。

    出力形式は以下のJSON形式のリストのみとしてください。他のテキストは含めないでください。
    [
      {{
        "title": "記事のタイトル",
        "category": "カテゴリ（例：大規模言語モデル, AI倫理, スタートアップ動向など）",
        "summary": "PM視点での分析と重要性の解説（100文字程度）"
      }},
      ...
    ]

    ニュース記事リスト:
    {formatted_articles}
    """

    try:
        response = model.generate_content(prompt)
        # レスポンスからJSON部分を抽出
        json_response_text = response.text.strip().lstrip("```json").rstrip("```")
        analyzed_news_list = json.loads(json_response_text)
        
        # 元の記事情報とマージ
        final_news_list = []
        for analyzed_news in analyzed_news_list:
            original_article = next((a for a in all_articles if a["title"] == analyzed_news["title"]), None)
            if original_article:
                original_article.update(analyzed_news)
                final_news_list.append(original_article)

        return jsonify({"news": final_news_list})
    except Exception as e:
        print(f"Error analyzing news with Gemini: {e}")
        return jsonify({"error": "Failed to analyze news"}), 500

# === ここから法人番号APIの機能をコメントアウト ===
# @app.route('/api/corporate_info')
# def corporate_info():
#     """
#     企業名から国税庁APIを使って法人情報を取得するエンドポイント
#     """
#     company_name = request.args.get('name')
#     if not company_name:
#         return jsonify({"error": "Company name is required"}), 400

#     try:
#         api_key = get_secret('CORPORATE_API_KEY')
#         if not api_key:
#              return jsonify({"error": "API key not configured"}), 500

#         api_url = "https://api.houjin-bangou.nta.go.jp/4/name"
#         params = {
#             'id': api_key,
#             'name': quote(company_name),
#             'type': '12',
#             'history': '0'
#         }
        
#         response = requests.get(api_url, params=params)
#         response.raise_for_status()

#         root = ET.fromstring(response.content)
#         ns = {'nta': 'http://www.houjin-bangou.nta.go.jp/core'}
#         corporation = root.find('nta:corporation', ns)
        
#         if corporation is None:
#             return jsonify({"error": "Corporation not found"}), 404
            
#         full_address = "{}{}{}".format(
#             corporation.findtext('nta:prefectureName', '', ns),
#             corporation.findtext('nta:cityName', '', ns),
#             corporation.findtext('nta:streetNumber', '', ns)
#         )

#         info = {
#             "corporate_number": corporation.findtext('nta:corporateNumber', '', ns),
#             "name": corporation.findtext('nta:name', '', ns),
#             "prefecture_name": corporation.findtext('nta:prefectureName', '', ns),
#             "city_name": corporation.findtext('nta:cityName', '', ns),
#             "street_number": corporation.findtext('nta:streetNumber', '', ns),
#             "full_address": full_address,
#             "update_date": corporation.findtext('nta:updateDate', '', ns),
#         }
        
#         return jsonify(info)

#     except requests.exceptions.RequestException as e:
#         print(f"Error calling corporate API: {e}")
#         return jsonify({"error": "Failed to call external API"}), 502
#     except ET.ParseError as e:
#         print(f"Error parsing XML: {e}")
#         return jsonify({"error": "Failed to parse API response"}), 500
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return jsonify({"error": "An internal server error occurred"}), 500
# === ここまで ===


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))