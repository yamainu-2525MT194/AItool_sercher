/**
 * ===================================================================
 * メインロジック：ページの読み込みが完了したら、ヘッダーを読み込み、
 * ページの種類を判別して、対応するデータ取得関数を呼び出す。
 * ===================================================================
 */
document.addEventListener('DOMContentLoaded', () => {
    loadHeader();

    if (document.getElementById('main-container')) {
        fetchLandscapeData(); // ツールマップページ用の関数
    }
    if (document.getElementById('news-container')) {
        fetchNewsData(); // 最新ニュースページ用の関数
    }
});

const API_URL = 'https://ai-news-api-501254184747.asia-northeast1.run.app';

/**
 * ===================================================================
 * ヘッダー読み込み & ナビゲーション制御
 * ===================================================================
 */
async function loadHeader() {
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (!headerPlaceholder) return;

    try {
        const response = await fetch('header.html');
        if (!response.ok) return;
        const headerHtml = await response.text();
        
        headerPlaceholder.innerHTML = `<a href="/" class="header-title">AI PM Dashboard</a><div class="header-nav">${headerHtml}</div>`;

        // 現在表示しているページに応じて、ナビゲーションリンクのアクティブ状態を切り替える
        const currentPagePath = window.location.pathname;
        const navLinks = headerPlaceholder.querySelectorAll('.header-nav a');
        navLinks.forEach(link => {
            const linkPath = link.getAttribute('href');
            // トップページ（/ または /index.html）の場合の判定
            if ((currentPagePath === '/' || currentPagePath.endsWith('/index.html')) && linkPath === '/') {
                link.classList.add('active');
            } 
            // その他のページの場合の判定
            else if (currentPagePath.endsWith(linkPath) && linkPath !== '/') {
                link.classList.add('active');
            }
        });
    } catch (error) {
        console.error('ヘッダーの読み込みに失敗しました:', error);
    }
}

/**
 * ===================================================================
 * ページ別データ取得 & 表示ロジック
 * ===================================================================
 */

// --- 静的なツールマップページ用 ---
async function fetchLandscapeData() {
    const mainContainer = document.getElementById('main-container');
    try {
        const response = await fetch(API_URL); // バックエンドのルートURL (/) を呼び出す
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        
        const toolData = await response.json();
        mainContainer.innerHTML = ''; // ローディング表示をクリア

        for (const category in toolData) {
            const section = document.createElement('div');
            section.className = 'category-section';
            let toolsHtml = `<h2>${category}</h2>`;
            toolData[category].forEach(tool => {
                toolsHtml += `
                    <div class="tool-card">
                        <h3 class="tool-name"><a href="${tool.link}" target="_blank" rel="noopener noreferrer">${tool.name}</a></h3>
                        <p class="section-title">概要</p><p class="section-content">${tool.summary}</p>
                        <p class="section-title">主な使用場面</p><p class="section-content">${tool.use_case}</p>
                    </div>`;
            });
            section.innerHTML = toolsHtml;
            mainContainer.appendChild(section);
        }
    } catch (error) {
        mainContainer.innerHTML = '<p>ツールマップの取得に失敗しました。</p>';
        console.error('Error fetching landscape data:', error);
    }
}

// --- 動的な最新ニュースページ用 ---
async function fetchNewsData() {
    const newsContainer = document.getElementById('news-container');
    try {
        const response = await fetch(API_URL + '/api/news'); // /api/news エンドポイントを呼び出す
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        
        const data = await response.json();
        renderNews(data.news);
        renderFilterButtons(data.news);
    } catch (error) {
        newsContainer.innerHTML = '<p>ニュースの取得に失敗しました。</p>';
        console.error('Error fetching news:', error);
    }
}

function renderNews(newsData) {
    const newsContainer = document.getElementById('news-container');
    newsContainer.innerHTML = '';
    if (!Array.isArray(newsData) || newsData.length === 0) {
        newsContainer.innerHTML = '<p>表示するニュースがありません。</p>';
        return;
    }
    newsData.forEach(news => {
        const card = document.createElement('div');
        card.className = 'news-card';
        card.dataset.category = news.category;
        card.innerHTML = `<div class="card-header"><span class="source-tag">${news.source || '不明'}</span><span class="category-tag">${news.category || '一般'}</span></div><h3 class="card-title">${news.title}</h3><p class="card-summary-title">【PM視点の分析】</p><p class="card-summary">${news.summary || '分析結果はありません。'}</p><a href="${news.link}" target="_blank" rel="noopener noreferrer" class="card-link">原文を読む →</a>`;
        newsContainer.appendChild(card);
    });
}

function renderFilterButtons(newsData) {
    const buttonContainer = document.getElementById('filter-buttons');
    if (!buttonContainer || !Array.isArray(newsData)) return;
    const categories = ['すべて', ...new Set(newsData.map(news => news.category).filter(c => c))];
    buttonContainer.innerHTML = '';
    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.textContent = category;
        if (category === 'すべて') button.classList.add('active');
        button.addEventListener('click', () => filterByCategory(category));
        buttonContainer.appendChild(button);
    });
}

function filterByCategory(category) {
    document.querySelectorAll('.news-card').forEach(card => {
        card.style.display = (category === 'すべて' || card.dataset.category === category) ? 'block' : 'none';
    });
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent === category);
    });
}