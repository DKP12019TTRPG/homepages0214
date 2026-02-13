
import re
import os

INDEX_PATH = r"c:\Users\aconi\workspease\アプリ\scenarios\index.html"

# Colors for tags
TAG_COLORS = {
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
}

def generate_tag_html(tag_text):
    color = "slate"
    for key, c in TAG_COLORS.items():
        if key in tag_text:
            color = c
            break
            
    # Conditional logic for dark mode opacity if needed, sticking to reference logic
    # Reference: bg-{color}-100 text-{color}-600 dark:bg-{color}-900/30 dark:text-{color}-400
    
    return f'<span class="px-2 py-0.5 text-xs font-medium text-{color}-600 bg-{color}-100 rounded dark:bg-{color}-900/30 dark:text-{color}-400">{tag_text}</span>'

def main():
    if not os.path.exists(INDEX_PATH):
        print("Index file not found.")
        return

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find existing cards
    # We look for <a href="..." data-tags="..."> ... </a>
    # Note: Content inside might be messed up due to previous edits, but the wrapper is consistent.
    
    card_pattern = re.compile(
        r'<a href="([^"]+)" data-tags="([^"]+)"\s*class="scenario-card[^"]*">(.*?)</a>',
        re.DOTALL
    )

    def replacement(match):
        href = match.group(1)
        data_tags = match.group(2)
        inner_html = match.group(3)
        
        # Extract Image
        img_match = re.search(r'<img src="([^"]+)" alt="([^"]+)"', inner_html)
        if img_match:
            img_src = img_match.group(1)
            img_alt = img_match.group(2)
        else:
            # Fallback if image not found (shouldn't happen based on previous steps)
            img_src = "img/default_card_bg.jpg"
            img_alt = "Scenario"

        # Extract Title (h3 text)
        title_match = re.search(r'<h3[^>]*>(.*?)</h3>', inner_html, re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = "Unknown Scenario"

        # Process Tags
        tags = data_tags.split()
        tag_htmls = []
        for t in tags:
            if "テキスト" in t: continue # Skip "Text" tag
            if t.startswith("#"): continue # Skip hashtags if any? user didn't specify but maybe clean
            tag_htmls.append(generate_tag_html(t))
            
        tags_block = ""
        if tag_htmls:
            tags_block = f'<div class="flex flex-wrap gap-2 mb-3">{" ".join(tag_htmls)}</div>'

        # New Card Template
        new_card = f"""<a href="{href}" data-tags="{data_tags}"
            class="scenario-card group flex flex-col bg-white dark:bg-slate-800 rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border border-transparent dark:border-slate-700">
            
            <div class="relative w-full h-48 overflow-hidden">
                <img src="{img_src}" alt="{img_alt}"
                    class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
            </div>

            <div class="flex-1 p-5 flex flex-col">
                {tags_block}
                <h3 class="text-lg font-bold text-slate-800 dark:text-slate-100 leading-tight mb-2 group-hover:text-primary-600 transition-colors">
                    {title}
                </h3>
            </div>
        </a>"""
        
        return new_card

    new_content = card_pattern.sub(replacement, content)
    
    # Also clean up the grid container if needed? It's id="scenario-grid"?
    # The snippet didn't change the grid, just the card.

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Applied fancy card design.")

if __name__ == "__main__":
    main()
