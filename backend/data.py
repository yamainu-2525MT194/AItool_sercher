# ai-news-app/backend/data.py

TOOL_LANDSCAPE_DATA = {
    "LLM (大規模言語モデル)": [
        {"name": "OpenAI (ChatGPT)", "company": "OpenAI", "summary": "対話型AIのパイオニアであり、汎用性が最も高いモデル。文章生成、アイデア出し、要約、翻訳、コーディング支援など、あらゆるタスクに対応可能。", "use_case": "新商品のキャッチコピー案を10個作ってもらう、複雑なメールの返信文を作成する、Pythonコードのデバッグを手伝ってもらうなど。", "link": "https://chat.openai.com/"},
        {"name": "Anthropic (Claude)", "company": "Anthropic", "summary": "安全性と長文読解能力に強みを持つモデル。「憲法AI」という独自の倫理基準を持ち、より信頼性の高い回答を生成することを目指している。", "use_case": "数万字に及ぶ論文や契約書をアップロードし、その内容を要約・分析させる。企業の倫理規定に関する壁打ち相手として使うなど。", "link": "https://claude.ai/"},
        {"name": "Google (Gemini)", "company": "Google", "summary": "Googleが開発したマルチモーダルAI。テキストだけでなく、画像や音声、動画を統合的に理解する能力が非常に高い。", "use_case": "商品の写真を見せて、それを使ったマーケティングプランを立案させる。ホワイトボードの図を読み取ってコードを生成するなど。", "link": "https://gemini.google.com/"}
    ],
    "AI開発": [
        {"name": "Hugging Face", "company": "Hugging Face", "summary": "AIコミュニティの中心的なプラットフォーム。最新のAIモデル、データセット、ライブラリが集約されており、AI開発者はここを拠点に多くの開発を行う。", "use_case": "`transformers`ライブラリを使って特定のタスク（感情分析など）のモデルを数行のコードで実装する。他の研究者が公開したモデルをダウンロードしてファインチューニングする。", "link": "https://huggingface.co/"},
        {"name": "LangChain", "company": "LangChain", "summary": "大規模言語モデル（LLM）を使ったアプリケーション開発を効率化するフレームワーク。複雑な処理（RAGなど）をコンポーネントの組み合わせで実現できる。", "use_case": "社内ドキュメントを読み込ませ、それに基づいて回答するチャットボットを構築する。複数のAPIやツールを連携させる自律型AIエージェントを作成する。", "link": "https://www.langchain.com/"},
        {"name": "Weights & Biases", "company": "Weights & Biases", "summary": "機械学習プロジェクトの実験管理プラットフォーム。モデルの学習過程（ハイパーパラメータ、メトリクスなど）を自動で記録・可視化し、再現性を高める。", "use_case": "複数の条件でモデルを学習させ、どのパラメータが最も性能が良いかをダッシュボードで比較・検討する。チームで実験結果を共有し、プロジェクトの進捗を管理する。", "link": "https://wandb.ai/"}
    ],
    "AIエージェント": [
        {"name": "Manus (Cognition)", "company": "Cognition AI", "summary": "自律的にソフトウェア開発タスクをこなすAIエンジニア。大まかな指示を与えるだけで、自身で計画を立て、コーディング、デバッグ、テストまで行う。", "use_case": "「ユーザーログイン機能を追加して」といった曖昧な指示から、必要なコードを全て実装させる。バグ報告を渡して修正を任せるなど。", "link": "https://www.cognition-labs.com/"},
        {"name": "n8n", "company": "n8n", "summary": "オープンソースで柔軟なカスタマイズが可能なワークフロー自動化ツール。視覚的なインターフェースで様々なアプリやAPIを連携できる。", "use_case": "Webサイトのフォームに問い合わせが来たら、その内容をSlackに通知し、顧客リスト（Google Sheets）に自動で追加する、といった連携処理を構築する。", "link": "https://n8n.io/"},
        {"name": "Zapier", "company": "Zapier", "summary": "ノーコードで数千種類以上のアプリを連携できる、ワークフロー自動化の代表的サービス。プログラミング知識がなくても利用可能。", "use_case": "Gmailに特定のキーワードを含むメールが届いたら、その添付ファイルを自動でDropboxに保存する、といった日常業務を自動化する。", "link": "https://zapier.com/"}
    ],
    "画像・動画生成": [
        {"name": "Midjourney", "company": "Midjourney", "summary": "非常に高品質で芸術的な画像を生成することに特化したAI。特に独創的で美しいビジュアル表現に定評がある。", "use_case": "ゲームや映画のコンセプトアート、ウェブサイトのヒーローイメージなど、プロ品質のオリジナル画像を生成する。", "link": "https://www.midjourney.com/"},
        {"name": "Runway", "company": "Runway", "summary": "動画の生成、編集、エフェクト追加など、AIを活用した高度な動画制作機能を提供するプラットフォーム。", "use_case": "短いテキスト指示から動画クリップを生成したり、既存の動画から特定の部分だけを動かしたり（シネマグラフ）する。", "link": "https://runwayml.com/"},
        {"name": "Pika", "company": "Pika", "summary": "テキストや画像から短い動画を手軽に生成できるツール。特にアニメーションやキャラクターを動かすことに優れている。", "use_case": "SNS投稿用に、一枚のイラストを動かして短いアニメーション動画を作成する。", "link": "https://pika.art/"}
    ],
    "AIスライド": [
        {"name": "Gamma", "company": "Gamma", "summary": "テキスト入力からプレゼンテーション、ドキュメント、Webページを瞬時に生成するAIツール。デザインをAIに任せて内容に集中できる。", "use_case": "箇条書きのメモを貼り付けて、AIにデザインやレイアウトを自動生成させ、10分でプレゼンの初稿を作成する。", "link": "https://gamma.app/"},
        {"name": "Tome", "company": "Tome", "summary": "物語を語るような、ナラティブでインタラクティブなプレゼンテーション作成を得意とするAIツール。", "use_case": "製品のビジョンやストーリーを伝えるための、視覚的に豊かで引き込まれるようなピッチ資料を作成する。", "link": "https://tome.app/"},
        {"name": "Canva", "company": "Canva", "summary": "デザインプラットフォームのCanvaに搭載されたAI機能群。豊富なテンプレートや素材とAIを組み合わせて、あらゆるデザイン作成を効率化できる。", "use_case": "プレゼン資料のデザインに迷った際に、AIにレイアウト案を提案させたり、資料に合う画像をAIで生成したりする。", "link": "https://www.canva.com/"}
    ],
    "AIセキュリティ": [
        {"name": "CrowdStrike", "company": "CrowdStrike", "summary": "クラウドネイティブのエンドポイント保護プラットフォーム。AIを活用して、未知の脅威や高度な攻撃をリアルタイムで検知・防御する。", "use_case": "企業の全デバイス（PC、サーバー）を保護し、ランサムウェアやサイバー攻撃の兆候をAIが自動で分析・対処する。", "link": "https://www.crowdstrike.com/"},
        {"name": "SentinelOne", "company": "SentinelOne", "summary": "自律的な検知と対応を特徴とするAIセキュリティプラットフォーム。攻撃の検知から修復までを自動で行う。", "use_case": "セキュリティ担当者が不在の夜間でも、AIが不審な挙動を検知し、ネットワークから隔離、脅威を無力化する。", "link": "https://www.sentinelone.com/"},
        {"name": "Wiz", "company": "Wiz", "summary": "クラウド環境全体のリスクを可視化するAIセキュリティツール。設定ミスや脆弱性をグラフで示し、優先順位を付けて対策を促す。", "use_case": "複雑なクラウドインフラ（AWS, Azureなど）のどこにセキュリティ上の穴があるかをAIにスキャンさせ、攻撃経路を特定する。", "link": "https://www.wiz.io/"}
    ]
}