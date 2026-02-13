
import os
import re

BASE_DIR = r"c:\Users\aconi\workspease\アプリ"
SCENARIOS_DIR = os.path.join(BASE_DIR, "scenarios")
INDEX_PATH = os.path.join(SCENARIOS_DIR, "index.html")
IMG_DIR = os.path.join(SCENARIOS_DIR, "img")

# Files to ensure are in index
TARGET_FILES = [
    "snow_guardians.html",
    "auction.html",
    "volnark_ruins.html",
    "cursed_labyrinth.html",
    "chase_young_thieves.html",
    "happy_black_powder.html",
    "evil_tree_labyrinth.html",
]

def extract_meta(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_match = re.search(r'<title>(.*?) - DKPの倉庫</title>', content)
    title = title_match.group(1) if title_match else "Unknown Title"
    
    # Try to find a reasonable description. 
    # Usually first <p> in article, or maybe a specific summary div?
    # Note files usually have body content directly.
    # Let's verify commonly used patterns.
    # Often the first p that is not a class?
    # The new template puts content in <article class="...">
    
    desc = "詳細はお読みください。"
    article_match = re.search(r'<article.*?>(.*?)</article>', content, re.DOTALL)
    if article_match:
        article_content = article_match.group(1)
        # Find first paragraph
        p_match = re.search(r'<p>(.*?)</p>', article_content, re.DOTALL)
        if p_match:
            desc = p_match.group(1)
            # Strip tags
            desc = re.sub(r'<[^>]+>', '', desc)
            if len(desc) > 80:
                desc = desc[:80] + "..."
    
    return title, desc

def find_image(basename):
    # basename e.g. "snow_guardians"
    # Look in IMG_DIR for something starting with basename
    for fname in os.listdir(IMG_DIR):
        if fname.startswith(basename):
            return f"img/{fname}"
    return "img/default_card_bg.jpg" # Fallback? glassrunner uses custom img

def generate_card(filename, title, desc, img_src):
    color = "blue" # Default
    if "ダンジョン" in desc or "迷宮" in title:
        color = "red"
    elif "シティ" in desc or "街" in desc:
        color = "indigo"
    elif "探索" in desc:
        color = "emerald"
    elif "初心者" in desc:
        color = "green"

    tags = "テキスト"
    if "ダンジョン" in desc or "迷宮" in title: tags += " ダンジョン"
    if "シティ" in desc: tags += " シティ"
    if "高レベル" in desc: tags += " 高レベル帯"

    return f"""
        <!-- {title} Card -->
        <a href="{filename}" data-tags="{tags}"
            class="scenario-card flex flex-col bg-white dark:bg-slate-800 rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition transform hover:-translate-y-1 group border border-transparent dark:border-slate-700">
            <img src="{img_src}" alt="{title}" class="w-full h-48 object-cover bg-gray-100 dark:bg-slate-700">
            <div class="flex-1 p-6 flex flex-col justify-between">
                <div>
                    <p class="text-sm font-medium text-{color}-600">
                        テキストシナリオ
                    </p>
                    <h3
                        class="mt-2 text-xl font-semibold text-gray-900 dark:text-white group-hover:text-{color}-600 dark:group-hover:text-{color}-400 transition">
                        {title}
                    </h3>
                    <p class="mt-3 text-base text-gray-500 dark:text-gray-400">
                        {desc}
                    </p>
                    <div class="mt-4 flex flex-wrap gap-2">
                        <span class="px-2 py-1 bg-gray-100 dark:bg-slate-700 text-xs rounded text-gray-600 dark:text-gray-300">テキスト</span>
                    </div>
                </div>
            </div>
        </a>
"""

def main():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    new_cards = []
    
    for fname in TARGET_FILES:
        if fname in html:
            print(f"[INFO] Skipping {fname}, already in index.")
            continue
            
        fpath = os.path.join(SCENARIOS_DIR, fname)
        if not os.path.exists(fpath):
            print(f"[WARN] {fname} does not exist.")
            continue
            
        title, desc = extract_meta(fpath)
        basename = os.path.splitext(fname)[0]
        img_src = find_image(basename)
        
        # If no specific image (default_card_bg.jpg likely doesn't exist), try to copy one or use a placeholder
        # For now, let's just use what find_image returns.
        
        card_html = generate_card(fname, title, desc, img_src)
        new_cards.append(card_html)
        print(f"[INFO] Generated card for {title}")

    if not new_cards:
        print("No new cards to add.")
        return

    # Insert after Glassrunner card
    # Find <!-- Glassrunner Card --> ... </a>
    glassrunner_end = html.find('<!-- Glassrunner Card -->')
    if glassrunner_end == -1:
        # Fallback: Insert at beginning of grid
        # The grid likely starts after <div class="... grid ...">
        # In the provided snippet, it is <div class="py-12 ..."> ... <h1 ...> ...
        # Actually line 97 starts the cards.
        insert_pos = html.find('<!-- Glassrunner Card -->')
    else:
        # Find the closing </a> for glassrunner
        # We can just insert BEFORE glassrunner to be safe/easy, or after.
        # Let's insert BEFORE Herbs Card (Next one)
        insert_pos = html.find('<!-- Herbs Card -->')
    
    if insert_pos == -1:
         insert_pos = html.find('<!-- Silver Speer Card -->') # typo check? it was "Silver Spear"
         
    if insert_pos == -1:
        print("[ERROR] Could not find insertion point.")
        return

    final_html = html[:insert_pos] + "\n".join(new_cards) + "\n" + html[insert_pos:]
    
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"[SUCCESS] Updated index.html with {len(new_cards)} new cards.")

if __name__ == "__main__":
    main()
