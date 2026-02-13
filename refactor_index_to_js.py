
import re
import os

INDEX_PATH = r"c:\Users\aconi\workspease\アプリ\scenarios\index.html"

# Tags mapping
TAG_COLORS_JS = """
const TAG_COLORS = {
    "初心者向け": "emerald",
    "探索": "teal",
    "ダンジョン": "purple",
    "シティ": "indigo",
    "和風": "orange",
    "高レベル帯": "red",
    "サンプル": "amber",
    "キャンペーン": "cyan",
    "スローライフ": "lime",
    "スカイノーツ": "sky",
    "捏造ミステリー": "rose",
};
"""

def main():
    if not os.path.exists(INDEX_PATH):
        print("Index file not found.")
        return

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    scenarios = []
    card_pattern = re.compile(
        r'<a href="([^"]+)" data-tags="([^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL
    )

    for match in card_pattern.finditer(content):
        href = match.group(1)
        data_tags = match.group(2)
        inner_html = match.group(3)

        img_match = re.search(r'<img src="([^"]+)"', inner_html)
        img_src = img_match.group(1) if img_match else "img/default_card_bg.jpg"

        title_match = re.search(r'<h3[^>]*>(.*?)</h3>', inner_html, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        
        if "テキスト" in data_tags:
            data_tags = data_tags.replace("テキスト", "").strip()
        tags_list = [t for t in data_tags.split() if t]
        
        scenarios.append({
            "title": title,
            "img": img_src,
            "url": href,
            "tags": tags_list,
            "desc": "" 
        })

    js_data = "const scenarioData = [\n"
    for s in scenarios:
        tags_js = str(s['tags']).replace("'", '"')
        js_data += f'    {{ title: "{s["title"]}", img: "{s["img"]}", url: "{s["url"]}", tags: {tags_js}, desc: "{s["desc"]}" }},\n'
    js_data += "];"

    # Robust Footer Detection
    footer_start_idx = content.find('<footer')
    if footer_start_idx != -1:
        footer_part = content[footer_start_idx:]
        script_idx = footer_part.find('<script>')
        if script_idx != -1:
            footer_part = footer_part[:script_idx]
    else:
        # Fallback Footer
        footer_part = """<footer class="bg-gray-800 dark:bg-slate-950 text-white mt-auto">
        <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
            <div class="text-center text-sm text-gray-400">
                &copy; 2026 SW2.5 Unofficial Fan Site. All rights reserved.
            </div>
        </div>
    </footer>"""

    new_html = f"""<!DOCTYPE html>
<html lang="ja" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; base-uri 'none'; form-action 'none';">
    <title>シナリオ一覧 - DKPの倉庫</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: {{ 50: '#f0f9ff', 100: '#e0f2fe', 500: '#0ea5e9', 600: '#0284c7', 700: '#0369a1', 900: '#0c4a6e' }},
                        slate: {{ 850: '#151e2e', 900: '#0f172a' }}
                    }},
                    fontFamily: {{ sans: ['"Noto Sans JP"', 'sans-serif'] }}
                }}
            }}
        }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans JP', sans-serif; }}
        .filter-btn.active {{ background-color: #0ea5e9; color: white; border-color: #0ea5e9; }}
        .dark .filter-btn.active {{ background-color: #0284c7; border-color: #0284c7; }}
    </style>
</head>
<body class="bg-stone-50 text-stone-800 transition-colors duration-300 flex flex-col min-h-screen">

    <!-- Header (Nav) -->
    <header class="sticky top-0 z-50 bg-stone-50/80 backdrop-blur-md border-b border-stone-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <div class="flex items-center">
                    <a href="../index.html" class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 hover:opacity-80 transition">DKPの倉庫</a>
                </div>
                <!-- Desktop Nav -->
                <nav class="hidden md:flex space-x-8">
                    <a href="../index.html" class="text-stone-600 hover:text-primary-600 font-medium transition">ホーム</a>
                    <a href="../about.html" class="text-stone-600 hover:text-primary-600 font-medium transition">規約・概要</a>
                    <a href="../tools/index.html" class="text-stone-600 hover:text-primary-600 font-medium transition">ツール</a>
                    <a href="#" class="text-primary-600 font-bold transition" aria-current="page">シナリオ</a>
                    <a href="../doujinshi/index.html" class="text-stone-600 hover:text-primary-600 font-medium transition">同人誌</a>
                    <a href="../materials/index.html" class="text-stone-600 hover:text-primary-600 font-medium transition">配布物</a>
                </nav>
                <!-- Mobile Menu Button -->
                <div class="flex items-center gap-4">
                    <button id="theme-toggle" class="p-2 rounded-full hover:bg-stone-200 transition hidden">
                         <svg id="sun-icon" class="w-5 h-5 hidden text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                         <svg id="moon-icon" class="w-5 h-5 hidden text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                    </button>
                    <button id="menu-toggle" class="md:hidden p-2 rounded hover:bg-stone-200 transition">
                        <svg class="w-6 h-6 text-stone-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                    </button>
                </div>
            </div>
        </div>
        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-gray-100">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <a href="../index.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700">ホーム</a>
                <a href="../tools/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700">ツール</a>
                <a href="#" class="block px-3 py-2 rounded-md text-base font-bold text-blue-600 bg-blue-50">シナリオ</a>
                <a href="../materials/index.html#doujinshi" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700">同人誌</a>
                <a href="../materials/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700">配布物</a>
                <a href="../about.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700">規約・連絡先</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <h1 class="text-3xl font-extrabold text-stone-900 mb-8 border-b-2 border-primary-500 pb-2 inline-block">シナリオ一覧</h1>
        
        <!-- Filters -->
        <div class="mb-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex flex-wrap gap-2 justify-center md:justify-start">
               <button class="filter-btn active px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="all">すべて</button>
               <button class="filter-btn px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="初心">初心者向け</button>
               <button class="filter-btn px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="ダンジョン">ダンジョン</button>
               <button class="filter-btn px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="シティ">シティ</button>
               <button class="filter-btn px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="探索">探索</button>
               <button class="filter-btn px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="サンプル">サンプル</button>
               <button class="filter-btn px-4 py-2 rounded-full border border-gray-300 dark:border-gray-600 text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-700" data-filter="スローライフ">スローライフ</button>
            </div>
            <div class="w-full md:w-auto">
                <input type="text" id="search-input" placeholder="検索..." class="w-full md:w-64 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-slate-700 focus:ring-2 focus:ring-blue-500 outline-none transition">
            </div>
        </div>
        
        <p class="mb-4 text-sm text-gray-500">表示中: <span id="result-count" class="font-bold">0</span> 件</p>

        <!-- Scenario Grid -->
        <div id="scenario-grid" class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
             <!-- JS Rendered Content -->
        </div>
    </div>

    {footer_part}

    <script>
    // 1. Data Source
    {js_data}

    {TAG_COLORS_JS}

    // 2. Rendering Function
    const grid = document.getElementById('scenario-grid');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('search-input');
    const resultCount = document.getElementById('result-count');

    let activeFilter = 'all';
    let searchQuery = '';

    function renderScenarios() {{
        grid.innerHTML = '';
        let count = 0;

        scenarioData.forEach(item => {{
            // Filter Logic
            const tagString = item.tags.join(' ');
            const matchesFilter = activeFilter === 'all' || tagString.includes(activeFilter) || item.title.includes(activeFilter); 
            const matchesSearch = item.title.toLowerCase().includes(searchQuery) || 
                                  tagString.includes(searchQuery);

            if (matchesFilter && matchesSearch) {{
                count++;
                
                // Construct Tags HTML
                let tagsHtml = '';
                item.tags.forEach(tag => {{
                    let color = 'slate';
                    for (const key in TAG_COLORS) {{
                        if (tag.includes(key)) {{
                            color = TAG_COLORS[key];
                            break;
                        }}
                    }}
                    tagsHtml += `<span class="px-2 py-0.5 text-xs font-medium text-${{color}}-600 bg-${{color}}-100 rounded dark:bg-${{color}}-900/30 dark:text-${{color}}-400">${{tag}}</span> `;
                }});
                if (tagsHtml) {{
                    tagsHtml = `<div class="flex flex-wrap gap-2 mb-3">${{tagsHtml}}</div>`;
                }}
                
                // Construct Card HTML using template literal as requested
                // Note: Using insertAdjacentHTML for better performance and cleaner code as suggested
                const cardHTML = `
                <a href="${{item.url}}" data-tags="${{item.tags.join(' ')}}" 
                   class="scenario-card group flex flex-col bg-white dark:bg-slate-800 rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border border-transparent dark:border-slate-700">
                    <div class="relative w-full h-48 overflow-hidden">
                        <img src="${{item.img}}" alt="${{item.title}}"
                            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
                    </div>
                    <div class="flex-1 p-5 flex flex-col">
                        ${{tagsHtml}}
                        <h3 class="text-lg font-bold text-slate-800 dark:text-slate-100 leading-tight mb-2 group-hover:text-primary-600 transition-colors">
                            ${{item.title}}
                        </h3>
                        ${{item.desc ? `<p class="text-sm text-slate-500 dark:text-slate-400 line-clamp-2">${{item.desc}}</p>` : ''}}
                    </div>
                </a>
                `;
                
                grid.insertAdjacentHTML('beforeend', cardHTML);
            }}
        }});
        resultCount.textContent = count;
    }}

    // Event Listeners
    filterBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeFilter = btn.getAttribute('data-filter');
            renderScenarios();
        }});
    }});

    searchInput.addEventListener('input', (e) => {{
        searchQuery = e.target.value.toLowerCase();
        renderScenarios();
    }});

    // Initial Render
    document.addEventListener('DOMContentLoaded', renderScenarios);
    
    // Header/Mobile Menu Logic
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    if(menuToggle && mobileMenu) {{
        menuToggle.addEventListener('click', () => {{
            mobileMenu.classList.toggle('hidden');
        }});
    }}
    </script>
</body>
</html>
"""

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("Successfully refactored index.html to use JS data rendering.")

if __name__ == "__main__":
    main()
