#!/usr/bin/env python3
"""Convert tweet.md into a static HTML preview that looks like X/Twitter."""

import re
from pathlib import Path
from typing import Optional

TRUNCATE_AT = 280

def parse_tweets(md_content: str) -> list:
    """Parse tweet.md into a list of tweet dicts."""
    tweets = []
    sections = re.split(r'^## Tweet \d+.*$', md_content, flags=re.MULTILINE)
    headers = re.findall(r'^## (Tweet \d+.*?)$', md_content, flags=re.MULTILINE)

    for i, section in enumerate(sections[1:], 0):
        # Remove TODO comments and HTML video/img tags
        lines = []
        in_video = False
        for line in section.strip().split('\n'):
            if line.strip().startswith('*TODO'):
                continue
            if '<video' in line or '<img' in line:
                in_video = True
            if in_video:
                if '</video>' in line or ('/>' in line and '<img' in line) or ('>' in line and '<img' in line):
                    in_video = False
                continue
            if line.strip() == '---':
                continue
            lines.append(line)

        # Extract media
        media = []
        video_src_match = re.search(r'<source src="([^"]+)"', section)
        video_aria_match = re.search(r'<video[^>]+aria-label="([^"]+)"', section)
        img_match = re.search(r'<img src="([^"]+)"(?:[^>]*alt="([^"]*)")?', section)
        if video_src_match:
            alt = video_aria_match.group(1) if video_aria_match else ''
            media.append(('video', video_src_match.group(1), alt))
        if img_match:
            alt = img_match.group(2) or ''
            media.append(('image', img_match.group(1), alt))

        content = '\n'.join(lines).strip()
        # Remove trailing (N/10)
        content = re.sub(r'\n*\(\d+/\d+\)\s*$', '', content)

        tweets.append({
            'header': headers[i] if i < len(headers) else f'Tweet {i+1}',
            'content': content,
            'media': media,
        })

    return tweets


def format_tweet_content(content: str) -> tuple:
    """Convert markdown to HTML and split at truncation point."""

    def to_html(text):
        """Convert markdown to HTML using <br> for all line breaks (no block elements)."""
        html = text
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'(https?://[^\s]+)', r'<a href="\1" class="link">\1</a>', html)
        html = re.sub(r'@(\w+)', r'<a href="https://x.com/\1" class="mention">@\1</a>', html)
        # Use <br><br> for paragraph breaks to keep everything inline
        html = html.replace('\n\n', '<br><br>').replace('\n', '<br>')
        return html

    # Calculate character count (URLs = 23 chars, newlines don't count)
    def char_count(text):
        t = re.sub(r'https?://[^\s]+', 'x' * 23, text)
        t = re.sub(r'[\r\n]', '', t)
        return len(t)

    if char_count(content) <= TRUNCATE_AT:
        return to_html(content), None

    # Find truncation point
    count = 0
    truncate_idx = 0
    i = 0
    while i < len(content) and count < TRUNCATE_AT:
        if content[i] in '\r\n':
            i += 1
            continue
        url_match = re.match(r'https?://[^\s]+', content[i:])
        if url_match:
            count += 23
            i += len(url_match.group(0))
        else:
            count += 1
            i += 1
    truncate_idx = i

    # Find a good break point (space or newline)
    for j in range(truncate_idx, max(0, truncate_idx - 50), -1):
        if content[j] in ' \n':
            truncate_idx = j
            break

    visible_content = content[:truncate_idx]
    hidden_content = content[truncate_idx:]

    return to_html(visible_content), to_html(hidden_content)


def generate_html(tweets: list) -> str:
    """Generate the full HTML page."""
    tweet_html = []

    for i, tweet in enumerate(tweets):
        visible, hidden = format_tweet_content(tweet['content'])

        media_html = ''
        for media_type, src, alt in tweet['media']:
            if media_type == 'video':
                aria = f' aria-label="{alt}"' if alt else ''
                media_html += f'<video controls class="media"{aria}><source src="{src}" type="video/mp4"></video>'
                if alt:
                    media_html += f'<p class="media-alt">{alt}</p>'
            else:
                media_html += f'<img src="{src}" alt="{alt}" class="media">'
                if alt:
                    media_html += f'<p class="media-alt">{alt}</p>'

        show_more = ''
        if hidden:
            tweet_id = f'tweet-{i}'
            show_more = f'''<span class="hidden-content" id="{tweet_id}-hidden" style="display:none">{hidden}</span>
                <button class="show-more" onclick="document.getElementById('{tweet_id}-hidden').style.display='inline'; this.style.display='none';">Show more</button>'''

        connector = '<div class="connector"></div>' if i < len(tweets) - 1 else ''

        tweet_html.append(f'''
        <div class="tweet">
            <div class="tweet-left">
                <div class="avatar"></div>
                {connector}
            </div>
            <div class="tweet-right">
                <div class="tweet-header">
                    <span class="name">TiPToP</span>
                    <span class="handle">@tiptop_robot</span>
                    <span class="dot">·</span>
                    <span class="time">1m</span>
                </div>
                <div class="tweet-content">
                    {visible}{show_more}
                </div>
                {media_html}
                <div class="tweet-actions">
                    <span class="action">💬</span>
                    <span class="action">🔁</span>
                    <span class="action">❤️</span>
                    <span class="action">📊</span>
                    <span class="action">🔖</span>
                    <span class="action">↗️</span>
                </div>
            </div>
        </div>
        ''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TiPToP Thread Preview</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #000;
            color: #e7e9ea;
            line-height: 1.4;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            border-left: 1px solid #2f3336;
            border-right: 1px solid #2f3336;
            min-height: 100vh;
        }}
        .header {{
            padding: 16px;
            border-bottom: 1px solid #2f3336;
            font-size: 20px;
            font-weight: bold;
            position: sticky;
            top: 0;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
        }}
        .tweet {{
            display: flex;
            padding: 12px 16px;
            border-bottom: 1px solid #2f3336;
        }}
        .tweet-left {{
            margin-right: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #1d9bf0, #1a8cd8);
            flex-shrink: 0;
        }}
        .connector {{
            width: 2px;
            flex-grow: 1;
            background: #333639;
            margin-top: 4px;
        }}
        .tweet-right {{
            flex: 1;
            min-width: 0;
        }}
        .tweet-header {{
            display: flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 4px;
        }}
        .name {{
            font-weight: bold;
        }}
        .handle, .dot, .time {{
            color: #71767b;
        }}
        .tweet-content {{
            word-wrap: break-word;
            line-height: 1.5;
        }}
        .link {{
            color: #1d9bf0;
            text-decoration: none;
        }}
        .link:hover {{
            text-decoration: underline;
        }}
        .mention {{
            color: #1d9bf0;
            text-decoration: none;
        }}
        .show-more {{
            background: none;
            border: none;
            color: #1d9bf0;
            cursor: pointer;
            font-size: 15px;
            padding: 0;
            margin-top: 4px;
            display: block;
        }}
        .show-more:hover {{
            text-decoration: underline;
        }}
        .media {{
            margin-top: 8px;
            border-radius: 16px;
            max-width: 100%;
            border: 1px solid #2f3336;
        }}
        .media-alt {{
            font-size: 13px;
            color: #71767b;
            margin-top: 6px;
            font-style: italic;
        }}
        .tweet-actions {{
            display: flex;
            justify-content: space-between;
            margin-top: 12px;
            max-width: 400px;
            color: #71767b;
        }}
        .action {{
            cursor: pointer;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Thread Preview</div>
        {''.join(tweet_html)}
    </div>
</body>
</html>
'''


def main():
    md_path = Path(__file__).parent / 'tweet.md'
    html_path = Path(__file__).parent / 'tweet.html'

    md_content = md_path.read_text()
    tweets = parse_tweets(md_content)
    html = generate_html(tweets)
    html_path.write_text(html)
    print(f'Generated {html_path} with {len(tweets)} tweets')


if __name__ == '__main__':
    main()
