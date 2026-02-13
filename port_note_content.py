
import os
import re
import shutil
import html

# Configuration
BASE_DIR = r"c:\Users\aconi\workspease\アプリ"
SCENARIOS_DIR = os.path.join(BASE_DIR, "scenarios")
IMG_DIR = os.path.join(SCENARIOS_DIR, "img")

# Mapping of Source Note HTML -> Target Website HTML
MAPPING = {
    "ソードワールド2.5　シナリオ「雪原の守護者たち」｜DKP.html": "snow_guardians.html",
    "ソード・ワールド2.5シナリオ「オークションへようこそ！」｜DKP.html": "auction.html",
    "ソード・ワールド2.5シナリオ「ヴォルナークの研究所跡」｜DKP.html": "volnark_ruins.html",
    "ソード・ワールド2.5シナリオ「呪われた屍霊の迷宮」｜DKP.html": "cursed_labyrinth.html",
    "ソード・ワールド2.5シナリオ「少年窃盗団を追え！」｜DKP.html": "chase_young_thieves.html",
    "ソード・ワールド2.5シナリオ「幸せの黒い粉」｜DKP.html": "happy_black_powder.html",
    "ソード・ワールド2.5シナリオ「悪しき樹木と迷霧の迷宮」｜DKP.html": "evil_tree_labyrinth.html",
    "【sw25シナリオ】メリアの島へようこそ！【無料】｜DKP.html": "melia_island.html",
    "【sw25シナリオ】樹海のトビウオ漁【#ウルシラの迷い道】｜DKP.html": "flying_fish.html",
    "【無料】Sw2.5シナリオ「海辺の蟹戦争」｜DKP.html": "crab_war.html",
    "ソードワールド2.5　シナリオ「ペガサスとキメラ」｜DKP.html": "pegasus.html",
    "ソードワールド2.5シナリオ「薬草探し」｜DKP.html": "herbs.html",
    "ソード・ワールド2.5 シナリオ「狐憑き」｜DKP.html": "fox.html",
    "ソード・ワールド2.5　シナリオ「奈落の魂喰らい」｜DKP.html": "soul_eater.html",
    "ソード・ワールド2.5「奴隷生活からの脱走」ver2.0｜DKP.html": "escape_slave.html",
    "ソードワールド2.5 シナリオ 「グラスランナーの後始末」｜DKP.html": "glassrunner.html",
    "ソードワールド2.5　シナリオ「白銀の槍」｜DKP.html": "silver_spear.html",
}

# Template: Double curly braces for literal '{' and '}'
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="ja" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob:; connect-src 'self'; base-uri 'none'; form-action 'none';">
    <title>{TITLE} - DKPの倉庫</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
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
        body {{
            font-family: 'Noto Sans JP', sans-serif;
        }}

        .scenario-body h2 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #0369a1;
            border-left: 4px solid #0ea5e9;
            padding-left: 1rem;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
        }}

        .dark .scenario-body h2 {{
            color: #38bdf8;
            border-left-color: #0ea5e9;
        }}

        .scenario-body h3 {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: #4b5563;
        }}

        .dark .scenario-body h3 {{
            color: #9ca3af;
        }}

        .scenario-body p {{
            margin-bottom: 1rem;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        
        /* Note specific cleanups */
        .scenario-body figure {{
            margin: 2rem 0;
        }}
        .scenario-body img {{
            border-radius: 0.5rem;
            max-width: 100%;
            height: auto;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>

<body class="bg-gray-50 dark:bg-slate-900 text-gray-800 dark:text-gray-100 transition-colors duration-300 flex flex-col min-h-screen">

    <!-- Header -->
    <header class="sticky top-0 z-50 bg-white/80 dark:bg-slate-850/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <a href="../index.html" class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 hover:opacity-80 transition">
                        DKPの倉庫
                    </a>
                </div>
                <nav class="hidden md:flex space-x-8">
                    <a href="../index.html" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition">ホーム</a>
                    <a href="../tools/index.html" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition">ツール</a>
                    <a href="../scenarios/index.html" class="text-blue-600 dark:text-blue-400 font-bold transition">シナリオ</a>
                    <a href="../materials/index.html#doujinshi" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition">同人誌</a>
                    <a href="../materials/index.html" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition">配布物</a>
                    <a href="../about.html" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition">規約・連絡先</a>
                </nav>
                <div class="flex items-center gap-4">
                    <button id="theme-toggle" class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-slate-700 transition">
                        <svg id="sun-icon" class="w-5 h-5 hidden text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                        </svg>
                        <svg id="moon-icon" class="w-5 h-5 hidden text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                        </svg>
                    </button>
                    <button id="menu-toggle" class="md:hidden p-2 rounded hover:bg-gray-100 dark:hover:bg-slate-700 transition">
                        <svg class="w-6 h-6 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div id="mobile-menu" class="hidden md:hidden bg-white dark:bg-slate-800 border-t border-gray-100 dark:border-gray-700">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <a href="../index.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200">ホーム</a>
                <a href="../tools/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200">ツール</a>
                <a href="../scenarios/index.html" class="block px-3 py-2 rounded-md text-base font-bold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20">シナリオ</a>
                <a href="../materials/index.html#doujinshi" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200">同人誌</a>
                <a href="../materials/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200">配布物</a>
                <a href="../about.html" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200">規約・連絡先</a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="py-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <div class="mb-6">
            <a href="../index.html#scenarios" class="text-sm text-primary-600 dark:text-primary-400 hover:underline">&larr; シナリオ一覧に戻る</a>
        </div>

        <section class="mb-10">
            <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-4">{TITLE}</h1>
        </section>

        <article class="prose dark:prose-invert max-w-none scenario-body bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-slate-700">
            {CONTENT}
        </article>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 dark:bg-slate-950 text-white mt-auto">
        <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
            <div class="text-center text-sm text-gray-400">
                &copy; 2026 SW2.5 Unofficial Fan Site. All rights reserved.
            </div>
        </div>
    </footer>

    <script>
        const themeToggle = document.getElementById('theme-toggle');
        const sunIcon = document.getElementById('sun-icon');
        const moonIcon = document.getElementById('moon-icon');
        const menuToggle = document.getElementById('menu-toggle');
        const mobileMenu = document.getElementById('mobile-menu');

        // Theme Sync
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
            sunIcon.classList.remove('hidden');
        }} else {{
            moonIcon.classList.remove('hidden');
        }}

        themeToggle.addEventListener('click', () => {{
            if (document.documentElement.classList.contains('dark')) {{
                document.documentElement.classList.remove('dark');
                localStorage.theme = 'light';
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            }} else {{
                document.documentElement.classList.add('dark');
                localStorage.theme = 'dark';
                sunIcon.classList.remove('hidden');
                moonIcon.classList.add('hidden');
            }}
        }});

        menuToggle.addEventListener('click', () => {{
            mobileMenu.classList.toggle('hidden');
        }});
    </script>
</body>
</html>
"""

def clean_filename(fname):
    return re.sub(r'[^\w\.-]', '_', fname)

def extract_body(content, file_path):
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).replace('｜DKP', '').strip() if title_match else "Unknown Title"
    
    start_marker = 'class="note-common-styles__textnote-body'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print(f"[WARN] Could not find content body in {file_path}")
        return title, None

    tag_open_end = content.find('>', start_idx)
    
    current_pos = tag_open_end + 1
    div_count = 1
    extracted_body = ""
    
    while div_count > 0 and current_pos < len(content):
        next_tag_start = content.find('<', current_pos)
        if next_tag_start == -1: break
        
        extracted_body += content[current_pos:next_tag_start]
        
        if content.startswith('</div>', next_tag_start):
            div_count -= 1
            extracted_body += '</div>'
            current_pos = next_tag_start + 6
        elif content.startswith('<div', next_tag_start):
            div_count += 1
            tag_end = content.find('>', next_tag_start)
            extracted_body += content[next_tag_start:tag_end+1]
            current_pos = tag_end + 1
        else:
            tag_end = content.find('>', next_tag_start)
            extracted_body += content[next_tag_start:tag_end+1]
            current_pos = tag_end + 1
            
    if extracted_body.endswith('</div>'):
        extracted_body = extracted_body[:-6]
        
    return title, extracted_body

def process_images(content, source_html_path, target_html_filename):
    source_dir = os.path.dirname(source_html_path)
    source_files_dir_name = os.path.splitext(os.path.basename(source_html_path))[0] + "_files"
    source_files_path = os.path.join(source_dir, source_files_dir_name)
    
    if not os.path.exists(source_files_path):
        return content

    def replacer(match):
        img_src = match.group(1)
        if "_files" not in img_src and "/" in img_src:
            return match.group(0)
            
        img_filename = os.path.basename(img_src)
        from urllib.parse import unquote
        img_filename = unquote(img_filename)
        
        src_img_full = os.path.join(source_files_path, img_filename)
        
        if os.path.exists(src_img_full):
            target_base = os.path.splitext(target_html_filename)[0]
            new_img_name = f"{target_base}_{img_filename}"
            new_img_name = clean_filename(new_img_name)
            
            dest_img_full = os.path.join(IMG_DIR, new_img_name)
            
            shutil.copy2(src_img_full, dest_img_full)
            return f'src="img/{new_img_name}"'
        else:
            return match.group(0)

    content = re.sub(r'data-src="([^"]+)"', replacer, content)
    content = re.sub(r'src="([^"]+)"', replacer, content)
    return content

def clean_html(content):
    content = re.sub(r'\sclass="[^"]*"', '', content)
    content = re.sub(r'\sstyle="[^"]*"', '', content)
    content = re.sub(r'\swidth="[^"]*"', '', content)
    content = re.sub(r'\sheight="[^"]*"', '', content)
    return content

def main():
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)

    for src_file, target_file in MAPPING.items():
        src_path = os.path.join(BASE_DIR, src_file)
        target_path = os.path.join(SCENARIOS_DIR, target_file)
        
        print(f"Processing {src_file} -> {target_file}")
        
        if not os.path.exists(src_path):
            print(f"[ERROR] Source file not found: {src_path}")
            continue

        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
        except Exception as e:
            print(f"[ERROR] Reading {src_file}: {e}")
            continue

        title, body = extract_body(raw_content, src_path)
        if not body:
            continue

        body = clean_html(body)
        body = process_images(body, src_path, target_file)
        
        full_html = TEMPLATE_HTML.format(TITLE=title, CONTENT=body)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
            
        print(f"[SUCCESS] Wrote to {target_path}")

if __name__ == "__main__":
    main()
