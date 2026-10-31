import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

spec = {
    "filename": "us-political-parties-presidents-guide.jpg",
    "badge": "POLITICAL SCIENCE & AMERICAN HISTORY",
    "badge_color": "#38bdf8",
    "title": "US Political Parties & Presidents",
    "subtitle": "Democratic Party vs Republican Party · Ideological Evolution · Complete Presidential Chronicle (1789-Present)",
    "glow_color": "rgba(59, 130, 246, 0.45)",
    "gradient": "radial-gradient(circle at 75% 30%, rgba(59, 130, 246, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(239, 68, 68, 0.22) 0%, transparent 50%), linear-gradient(135deg, #090e1a 0%, #111827 50%, #1c1424 100%)",
    "tags": ["DEMOCRATIC PARTY (BLUE)", "REPUBLICAN PARTY (RED)", "47 PRESIDENTS", "PARTY REALIGNMENT", "ELECTORAL COLLEGE"],
    "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="1.5">
      <!-- Classical Capitol Dome / Monument Architectural Outline -->
      <path d="M12 2L4 7v2h16V7L12 2z" stroke="#60a5fa" stroke-width="1.8" fill="rgba(59, 130, 246, 0.15)"/>
      <path d="M6 9v8M9 9v8M12 9v8M15 9v8M18 9v8" stroke="#f87171" stroke-width="1.6"/>
      <path d="M3 17h18v4H3v-4z" stroke="#60a5fa" stroke-width="1.8" fill="rgba(239, 68, 68, 0.12)"/>
      <!-- Stars -->
      <circle cx="8" cy="5.5" r="0.75" fill="#f87171"/>
      <circle cx="12" cy="4.5" r="0.9" fill="#ffffff"/>
      <circle cx="16" cy="5.5" r="0.75" fill="#60a5fa"/>
      <!-- Eagle / Laurel subtle arc -->
      <path d="M2 22h20" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
    </svg>"""
}

def render():
    tags_html = " ".join([f'<span class="tag">{t}</span>' for t in spec["tags"]])
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1376px;
    height: 768px;
    background: {spec['gradient']};
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }}
  .grid {{
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(circle at 50% 50%, black 50%, transparent 85%);
  }}
  .container {{
    position: relative;
    width: 1216px;
    height: 608px;
    background: rgba(15, 23, 42, 0.72);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 28px;
    padding: 60px 70px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 50px {spec['glow_color']};
  }}
  .content {{
    max-width: 780px;
    z-index: 2;
  }}
  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 18px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid {spec['badge_color']};
    color: {spec['badge_color']};
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 24px;
    font-family: 'Consolas', monospace;
  }}
  .badge-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: {spec['badge_color']};
    box-shadow: 0 0 10px {spec['badge_color']};
  }}
  h1 {{
    font-size: 50px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }}
  .subtitle {{
    font-size: 20px;
    line-height: 1.5;
    color: #94a3b8;
    margin-bottom: 34px;
    font-weight: 400;
  }}
  .tags {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }}
  .tag {{
    padding: 6px 14px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    font-family: 'Consolas', monospace;
  }}
  .visual {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 250px;
    height: 250px;
    position: relative;
    filter: drop-shadow(0 0 25px rgba(59, 130, 246, 0.4));
  }}
</style>
</head>
<body>
  <div class="grid"></div>
  <div class="container">
    <div class="content">
      <div class="badge"><span class="badge-dot"></span>{spec['badge']}</div>
      <h1>{spec['title']}</h1>
      <p class="subtitle">{spec['subtitle']}</p>
      <div class="tags">
        {tags_html}
      </div>
    </div>
    <div class="visual">
      {spec['icon_svg']}
    </div>
  </div>
</body>
</html>"""

    temp_html = os.path.abspath("temp_party_banner.html")
    temp_png = os.path.abspath("temp_party_banner.png")
    dest_path = os.path.join(IMAGES_DIR, spec["filename"])

    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        EDGE_PATH,
        "--headless",
        f"--screenshot={temp_png}",
        "--window-size=1376,768",
        "--hide-scrollbars",
        f"file:///{temp_html}"
    ]
    subprocess.run(cmd, check=True)

    im = Image.open(temp_png).convert("RGB")
    im.save(dest_path, "JPEG", quality=95)

    if os.path.exists(temp_html):
        os.remove(temp_html)
    if os.path.exists(temp_png):
        os.remove(temp_png)

    print(f"Generated: {spec['filename']} ({os.path.getsize(dest_path)} bytes)")

if __name__ == "__main__":
    render()
