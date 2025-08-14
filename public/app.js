/**
 * ===================================================================
 * メインロジック：ページの読み込みが完了したら、共通ヘッダーを読み込み、
 * ページの種類を判別して、対応するデータ取得関数を呼び出す。
 * ===================================================================
 */
document.addEventListener('DOMContentLoaded', () => {
    loadHeader();

    // ツールマップページ (landscape.html) の場合のみ、関連機能を初期化
    if (document.getElementById('main-container')) {
        fetchLandscapeData();
        initializeModal(); // ★モーダル機能の初期化をここで行う
    }
    
    // 最新ニュースページ (news.html) の場合
    if (document.getElementById('news-container')) {
        fetchNewsData();
    }
});

// バックエンドAPIの基本URL
const API_URL = 'https://ai-product-manager-backend-501254184747.asia-northeast1.run.app';

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

        const currentPagePath = window.location.pathname;
        const navLinks = headerPlaceholder.querySelectorAll('.header-nav a');
        
        navLinks.forEach(link => {
            const linkPath = link.dataset.path;
            if ((currentPagePath === '/' || currentPagePath.endsWith('/index.html')) && linkPath === '/') {
                link.classList.add('active');
            } else if (linkPath !== '/' && currentPagePath.endsWith(linkPath)) {
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

// --- ツールマップページ (landscape.html) 用 ---
async function fetchLandscapeData() {
    const mainContainer = document.getElementById('main-container');
    try {
        const response = await fetch(API_URL); 
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        
        const toolData = await response.json();
        mainContainer.innerHTML = '';

        for (const category in toolData) {
            const section = document.createElement('div');
            section.className = 'category-section';

            const categoryTitle = document.createElement('h2');
            categoryTitle.textContent = category;
            section.appendChild(categoryTitle);

            toolData[category].forEach(tool => {
                const cardElement = createToolCard(tool);
                section.appendChild(cardElement);
            });
            
            mainContainer.appendChild(section);
        }
    } catch (error) {
        mainContainer.innerHTML = '<p>ツールマップの取得に失敗しました。</p>';
        console.error('Error fetching landscape data:', error);
    }
}

function createToolCard(tool) {
    const card = document.createElement('div');
    card.className = 'tool-card';

    card.innerHTML = `
      <h3 class="tool-name"><a href="${tool.link}" target="_blank" rel="noopener noreferrer">${tool.name}</a></h3>
      <p class="section-title">概要</p>
      <p class="section-content">${tool.summary}</p>
      <p class="section-title">主な使用場面</p>
      <p class="section-content">${tool.use_case}</p>
      <div class="tool-footer"></div>
    `;

    if (tool.company) {
      const corporateBtn = document.createElement('button');
      corporateBtn.className = 'corporate-info-btn';
      corporateBtn.textContent = '企業情報';
      corporateBtn.dataset.companyName = tool.company;
      card.querySelector('.tool-footer').appendChild(corporateBtn);
    }

    return card;
}

// --- 最新ニュースページ (news.html) 用 ---
async function fetchNewsData() {
    const newsContainer = document.getElementById('news-container');
    try {
        const response = await fetch(API_URL + '/api/news');
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

/**
 * ===================================================================
 * 法人情報モーダル（ポップアップ）関連の機能
 * ===================================================================
 */

// モーダル機能の初期化（イベントリスナーの設定など）
function initializeModal() {
    const modal = document.getElementById('corporate-info-modal');
    if (!modal) return; // モーダルがHTMLに存在しないページでは何もしない

    const closeModalButton = modal.querySelector('.modal-close-button');

    // 「企業情報」ボタンが押された時のイベントを監視
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('corporate-info-btn')) {
            const companyName = event.target.dataset.companyName;
            openModal(companyName);
        }
    });

    // 閉じるボタンが押された時の処理
    closeModalButton.addEventListener('click', closeModal);
    // モーダルの外側がクリックされた時の処理
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
}

// モーダルを開く
function openModal(companyName) {
    const modal = document.getElementById('corporate-info-modal');
    if (!modal) return;
    
    modal.style.display = 'flex';
    const modalHeader = modal.querySelector('#modal-company-name');
    if (modalHeader) modalHeader.textContent = '法人情報';
    
    const modalBody = modal.querySelector('#modal-body-content');
    if (modalBody) modalBody.innerHTML = '<div class="loader"></div>';

    fetchCorporateInfo(companyName);
}

// モーダルを閉じる
function closeModal() {
    const modal = document.getElementById('corporate-info-modal');
    if (modal) modal.style.display = 'none';
}

// バックエンドAPIを叩いて法人情報を取得・表示する
async function fetchCorporateInfo(companyName) {
    const modal = document.getElementById('corporate-info-modal');
    if (!modal) return;

    const modalHeader = modal.querySelector('#modal-company-name');
    if (modalHeader) modalHeader.textContent = `「${companyName}」の法人情報`;
  
    const modalBody = modal.querySelector('#modal-body-content');
    if (!modalBody) return;

    try {
        const response = await fetch(`${API_URL}/api/corporate_info?name=${encodeURIComponent(companyName)}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '情報を取得できませんでした。');
        }
        
        const data = await response.json();
        
        modalBody.innerHTML = `
            <p><strong>法人名:</strong> ${data.name}</p>
            <p><strong>法人番号:</strong> ${data.corporate_number}</p>
            <p><strong>所在地:</strong> 〒${data.full_address}</p>
            <p><strong>最終更新日:</strong> ${data.update_date}</p>
        `;
        
    } catch (error) {
        console.error('Fetch corporate info error:', error);
        modalBody.innerHTML = `<p style="color: red;">エラー: ${error.message}</p>`;
    }
}