
import re
import os

INDEX_PATH = r"c:\Users\aconi\workspease\アプリ\scenarios\index.html"

def main():
    if not os.path.exists(INDEX_PATH):
        print("Index file not found.")
        return

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Description Paragraphs
    # Pattern: <p class="mt-3 text-base text-gray-500 dark:text-gray-400">...</p>
    # Note: Using DOTALL to handle multiline content within <p> if any
    content = re.sub(
        r'<p class="mt-3 text-base text-gray-500 dark:text-gray-400">.*?</p>',
        '',
        content,
        flags=re.DOTALL
    )

    # 2. Remove Tag Divs
    # Pattern: <div class="mt-4 flex flex-wrap gap-2">...</div>
    content = re.sub(
        r'<div class="mt-4 flex flex-wrap gap-2">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # 3. Handle Category Labels
    # First, simply remove "テキストシナリオ" lines entirely.
    # Pattern needs to cover the surrounding <p> tag.
    # <p class="text-sm font-medium text-XXXX-600">\s*テキストシナリオ\s*</p>
    content = re.sub(
        r'<p class="text-sm font-medium [^"]+">\s*テキストシナリオ\s*</p>',
        '',
        content,
        flags=re.DOTALL
    )

    # Next, replace any "XXXXシナリオ" with "シナリオ"
    # Capture the class attribute to preserve color.
    # We want to replace the text content strictly.
    def replace_scenario_label(match):
        full_tag = match.group(0)
        # Check if it contains "シナリオ" inside content
        # If it's pure "テキストシナリオ" it should be gone already, but just in case.
        # We target "サンプルシナリオ", "スローライフシナリオ", etc.
        # Check content part
        if re.search(r'>\s*[^<]*シナリオ\s*<', full_tag):
            return re.sub(r'(>\s*)[^<]*シナリオ(\s*<)', r'\1シナリオ\2', full_tag)
        return full_tag

    # Use a broader pattern to catch the P tag and then process
    content = re.sub(
        r'<p class="text-sm font-medium [^"]+">.*?</p>',
        replace_scenario_label,
        content,
        flags=re.DOTALL
    )

    # Cleanup empty lines that might have resulted from removals
    # Removing <p>...</p> leaves empty lines.
    # Regex for multiple newlines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Updated index.html")

if __name__ == "__main__":
    main()
