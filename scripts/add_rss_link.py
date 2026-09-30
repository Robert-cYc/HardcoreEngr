"""Add RSS feed link to all HTML pages that don't already have it."""
import glob

RSS_TAG = '  <link rel="alternate" type="application/rss+xml" title="AI 硬核工程師 RSS" href="https://ai-hardcore-engineer.com/feed.xml">\n'

pages = glob.glob('*.html')
count = 0
for f in pages:
    content = open(f, encoding='utf-8').read()
    if 'feed.xml' in content:
        continue
    insert_at = content.find('<link rel="preconnect"')
    if insert_at == -1:
        insert_at = content.find('</head>')
    if insert_at == -1:
        continue
    new_content = content[:insert_at] + RSS_TAG + content[insert_at:]
    open(f, 'w', encoding='utf-8').write(new_content)
    count += 1

import sys
sys.stdout.buffer.write(f'Added RSS link to {count} pages\n'.encode('utf-8'))
