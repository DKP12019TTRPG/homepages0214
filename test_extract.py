
import os
import re
import html

def extract_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

    # simple extraction using regex because html.parser might be verbose for this
    # Finding the title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "No Title"
    title = title.replace('｜DKP', '').strip()

    # Finding the body content
    # Note content is usually in a div with class starting with 'note-common-styles__textnote-body'
    # Since it might be minified, we look for the class and the closing div
    
    # We can try to find the specific Start-of-Body marker
    # The class name might slightly vary or have extra classes
    start_marker = 'class="note-common-styles__textnote-body'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print(f"Could not find content body in {file_path}")
        return title, None

    # identifying the opening tag end
    tag_open_end = content.find('>', start_idx)
    
    # We need to extract the content inside this div. 
    # Since regex for nested divs is hard, and we don't have bs4...
    # We can try to count divs.
    
    current_pos = tag_open_end + 1
    div_count = 1
    extracted_body = ""
    
    while div_count > 0 and current_pos < len(content):
        # find next tag
        next_tag_start = content.find('<', current_pos)
        if next_tag_start == -1:
            break
            
        extracted_body += content[current_pos:next_tag_start]
        
        if content.startswith('</div>', next_tag_start):
            div_count -= 1
            extracted_body += '</div>'
            current_pos = next_tag_start + 6
        elif content.startswith('<div', next_tag_start):
            div_count += 1
            # find end of this tag definition to append it correctly
            tag_end = content.find('>', next_tag_start)
            extracted_body += content[next_tag_start:tag_end+1]
            current_pos = tag_end + 1
        else:
            # other tags, include them
            tag_end = content.find('>', next_tag_start)
            extracted_body += content[next_tag_start:tag_end+1]
            current_pos = tag_end + 1
            
    # Remove the last closing div which belongs to the container
    if extracted_body.endswith('</div>'):
        extracted_body = extracted_body[:-6]

    return title, extracted_body

target_files = [
    r"c:\Users\aconi\workspease\アプリ\ソードワールド2.5　シナリオ「白銀の槍」｜DKP.html"
]

for fp in target_files:
    t, b = extract_content(fp)
    print(f"File: {os.path.basename(fp)}")
    print(f"Title: {t}")
    if b:
        print(f"Body length: {len(b)}")
        print(f"Body snippet: {b[:200]}...")
    else:
        print("Body not found")
