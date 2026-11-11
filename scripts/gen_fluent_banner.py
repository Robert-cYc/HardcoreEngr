import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

spec = {
    "filename": "windows-fluent-design-guide.jpg",
    "badge": "MICROSOFT FLUENT DESIGN SYSTEM",
    "badge_color": "#0078d4",
    "title": "Windows Fluent Design",
    "subtitle": "Light · Depth · Motion · Material · Scale | Mica & Acrylic Architecture · WinUI 3 · Cross-Platform Web",
    "glow_color": "rgba(0, 120, 212, 0.45)",
    "gradient": "radial-gradient(circle at 80% 30%, rgba(0, 120, 212, 0.3) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.25) 0%, transparent 55%), linear-gradient(135deg, #050b14 0%, #0c1829 50%, #151128 100%)",
    "tags": ["MICA & ACRYLIC", "LIGHT & DEPTH", "WINUI 3", "WPF-UI", "FLUENT UI 2", "DESIGN TOKENS"],
    "icon_svg": """<svg width="340" height="260" viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="winBlue" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#60a5fa" />
          <stop offset="100%" stop-color="#0078d4" />
        </linearGradient>
        <linearGradient id="micaGlass" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="rgba(255, 255, 255, 0.28)" />
          <stop offset="100%" stop-color="rgba(255, 255, 255, 0.05)" />
        </linearGradient>
        <linearGradient id="acrylicGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="rgba(0, 120, 212, 0.35)" />
          <stop offset="100%" stop-color="rgba(139, 92, 246, 0.25)" />
        </linearGradient>
        <filter id="glassBlur" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#0078d4" flood-opacity="0.35"/>
        </filter>
        <filter id="revealGlow" x="-30%" y="-30%" width="160%" height="160%">
          <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#38bdf8" flood-opacity="0.6"/>
        </filter>
      </defs>

      <!-- Background Ambient Grid / Depth Layers -->
      <rect x="30" y="30" width="280" height="200" rx="16" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
      
      <!-- Windows 11 Modern Logo 4 Squares with Frosted Glass & Isometric Elevation -->
      <g filter="url(#glassBlur)">
        <!-- Layer 1: Bottom Base Window -->
        <rect x="50" y="55" width="240" height="150" rx="12" fill="url(#acrylicGrad)" stroke="rgba(255,255,255,0.18)" stroke-width="1.2"/>
        
        <!-- Acrylic Header Bar with Window Controls -->
        <path d="M 50 67 C 50 60, 55 55, 62 55 L 278 55 C 285 55, 290 60, 290 67 L 290 85 L 50 85 Z" fill="rgba(255,255,255,0.08)"/>
        <circle cx="68" cy="70" r="4" fill="#ef4444" opacity="0.8"/>
        <circle cx="80" cy="70" r="4" fill="#f59e0b" opacity="0.8"/>
        <circle cx="92" cy="70" r="4" fill="#10b981" opacity="0.8"/>
        <line x1="120" y1="70" x2="200" y2="70" stroke="rgba(255,255,255,0.2)" stroke-width="3" stroke-linecap="round"/>

        <!-- Foreground Mica Floating Card with Rounded Corners -->
        <rect x="85" y="95" width="170" height="95" rx="10" fill="url(#micaGlass)" stroke="rgba(255,255,255,0.35)" stroke-width="1.5" filter="url(#revealGlow)"/>

        <!-- 4 Windows Fluent Tiles inside floating card -->
        <rect x="105" y="112" width="28" height="28" rx="4" fill="url(#winBlue)"/>
        <rect x="139" y="112" width="28" height="28" rx="4" fill="url(#winBlue)" opacity="0.9"/>
        <rect x="105" y="146" width="28" height="28" rx="4" fill="url(#winBlue)" opacity="0.85"/>
        <rect x="139" y="146" width="28" height="28" rx="4" fill="url(#winBlue)" opacity="0.75"/>

        <!-- UI Elements: Toggle Switch, Sliders, Text Skeleton -->
        <line x1="182" y1="120" x2="235" y2="120" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" opacity="0.85"/>
        <line x1="182" y1="130" x2="215" y2="130" stroke="rgba(255,255,255,0.4)" stroke-width="2.5" stroke-linecap="round"/>
        
        <!-- Fluent Toggle Capsule -->
        <rect x="182" y="148" width="36" height="18" rx="9" fill="#0078d4"/>
        <circle cx="209" cy="157" r="6" fill="#ffffff"/>
      </g>

      <!-- Light Indicator (Reveal Highlight Vector Rays) -->
      <path d="M 230 40 L 260 70" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity="0.7"/>
      <circle cx="230" cy="40" r="3" fill="#38bdf8"/>
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
    font-family: 'Segoe UI Variable', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
      linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(circle at 50% 50%, black 50%, transparent 85%);
  }}
  .container {{
    position: relative;
    width: 1216px;
    height: 608px;
    background: rgba(15, 23, 42, 0.72);
    backdrop-filter: blur(28px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 28px;
    padding: 60px 65px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 50px {spec['glow_color']};
  }}
  .content {{
    max-width: 720px;
    z-index: 2;
  }}
  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 18px;
    border-radius: 9999px;
    background: rgba(0, 120, 212, 0.15);
    border: 1px solid {spec['badge_color']};
    color: #60a5fa;
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
    background: #60a5fa;
    box-shadow: 0 0 10px #60a5fa;
  }}
  h1 {{
    font-size: 45px;
    font-weight: 800;
    line-height: 1.18;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }}
  .subtitle {{
    font-size: 19px;
    line-height: 1.5;
    color: #94a3b8;
    margin-bottom: 32px;
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
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
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
    width: 360px;
    height: 280px;
    position: relative;
    filter: drop-shadow(0 0 35px rgba(0, 120, 212, 0.4));
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

    temp_html = os.path.abspath("temp_fluent_banner.html")
    temp_png = os.path.abspath("temp_fluent_banner.png")
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

