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
    "gradient": "radial-gradient(circle at 80% 30%, rgba(239, 68, 68, 0.28) 0%, transparent 55%), radial-gradient(circle at 20% 70%, rgba(59, 130, 246, 0.3) 0%, transparent 55%), linear-gradient(135deg, #070b14 0%, #0f172a 50%, #1a101f 100%)",
    "tags": ["DEMOCRATIC DONKEY (BLUE)", "REPUBLICAN ELEPHANT (RED)", "47 PRESIDENTS", "PARTY REALIGNMENT", "ELECTORAL COLLEGE"],
    "icon_svg": """<svg width="340" height="260" viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="demGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#60a5fa" />
          <stop offset="100%" stop-color="#2563eb" />
        </linearGradient>
        <linearGradient id="gopGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f87171" />
          <stop offset="100%" stop-color="#dc2626" />
        </linearGradient>
        <filter id="glowDem" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#3b82f6" flood-opacity="0.4"/>
        </filter>
        <filter id="glowGop" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#ef4444" flood-opacity="0.4"/>
        </filter>
      </defs>

      <!-- Center Dynamic Dividing Ring -->
      <circle cx="170" cy="130" r="115" stroke="rgba(255,255,255,0.08)" stroke-width="2" stroke-dasharray="4 6"/>
      <circle cx="170" cy="130" r="95" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>

      <!-- Center VS Badge -->
      <g transform="translate(170, 130)">
        <polygon points="0,-22 6,-6 22,-6 10,4 14,20 0,10 -14,20 -10,4 -22,-6 -6,-6" fill="#f8fafc" opacity="0.9"/>
        <line x1="0" y1="-70" x2="0" y2="-32" stroke="rgba(255,255,255,0.3)" stroke-width="2" stroke-dasharray="3 3"/>
        <line x1="0" y1="32" x2="0" y2="70" stroke="rgba(255,255,255,0.3)" stroke-width="2" stroke-dasharray="3 3"/>
      </g>

      <!-- DEMOCRATIC DONKEY (Left Side - Blue) -->
      <g id="donkey" filter="url(#glowDem)">
        <!-- Donkey Silhouette Path Facing Right -->
        <path d="M 60 70 
                 C 55 58, 62 42, 68 32 
                 C 70 28, 74 30, 73 36 
                 C 71 45, 74 50, 78 40 
                 C 81 33, 85 35, 84 42 
                 C 82 52, 85 58, 98 62 
                 C 106 64, 114 70, 110 78 
                 C 104 84, 95 82, 88 80 
                 C 86 86, 92 98, 95 110 
                 C 108 114, 122 115, 134 122 
                 C 142 128, 140 136, 132 140 
                 L 132 186 C 132 192, 124 192, 122 186 L 122 152 
                 L 110 152 L 108 186 C 108 192, 100 192, 98 186 L 100 148 
                 C 90 148, 80 146, 70 142 
                 L 66 186 C 66 192, 58 192, 56 186 L 60 140 
                 C 50 138, 44 130, 42 122 
                 C 40 114, 44 106, 38 100 
                 C 34 96, 32 102, 30 112 
                 C 28 120, 24 122, 22 118 
                 C 22 110, 28 92, 36 84 
                 C 44 76, 52 74, 60 70 Z" 
              fill="url(#demGrad)" stroke="#93c5fd" stroke-width="2.5" stroke-linejoin="round"/>
        <!-- Donkey White Stars (Classic Emblem) -->
        <polygon points="76,104 78,110 84,110 79,114 81,120 76,116 71,120 73,114 68,110 74,110" fill="#ffffff"/>
        <polygon points="94,114 96,120 102,120 97,124 99,130 94,126 89,130 91,124 86,120 92,120" fill="#ffffff"/>
        <polygon points="112,124 114,130 120,130 115,134 117,140 112,136 107,140 109,134 104,130 110,130" fill="#ffffff"/>
        <!-- Democratic Party Text Pill -->
        <rect x="36" y="204" width="90" height="22" rx="11" fill="rgba(37,99,235,0.25)" stroke="#60a5fa" stroke-width="1.5"/>
        <text x="81" y="219" fill="#93c5fd" font-size="11" font-weight="700" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1.5">DEMOCRAT</text>
      </g>

      <!-- REPUBLICAN ELEPHANT (Right Side - Red) -->
      <g id="elephant" filter="url(#glowGop)">
        <!-- Elephant Silhouette Path Facing Left -->
        <path d="M 280 72 
                 C 272 62, 258 60, 246 64 
                 C 236 68, 228 76, 222 84 
                 C 214 94, 210 108, 206 122 
                 C 202 134, 196 142, 190 144 
                 C 184 146, 180 140, 182 132 
                 C 184 122, 192 118, 194 110 
                 C 196 104, 190 104, 186 110 
                 C 180 120, 172 134, 174 146 
                 C 176 156, 184 162, 194 160 
                 C 204 158, 212 148, 216 138 
                 L 218 186 C 218 192, 226 192, 228 186 L 230 152 
                 L 242 152 L 244 186 C 244 192, 252 192, 254 186 L 256 148 
                 C 264 148, 274 146, 282 142 
                 L 286 186 C 286 192, 294 192, 296 186 L 294 138 
                 C 304 132, 312 120, 310 106 
                 C 308 92, 298 78, 280 72 Z" 
              fill="url(#gopGrad)" stroke="#fca5a5" stroke-width="2.5" stroke-linejoin="round"/>
        <!-- Elephant Ear Line & Tusk Accent -->
        <path d="M 252 82 C 242 88, 238 104, 244 118 C 248 126, 256 130, 264 128" 
              stroke="rgba(255,255,255,0.6)" stroke-width="2" fill="none" stroke-linecap="round"/>
        <path d="M 212 132 C 206 136, 198 138, 192 136" 
              stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
        <!-- Republican White Stars (Classic Emblem) -->
        <polygon points="238,76 240,82 246,82 241,86 243,92 238,88 233,92 235,86 230,82 236,82" fill="#ffffff"/>
        <polygon points="256,86 258,92 264,92 259,96 261,102 256,98 251,102 253,96 248,92 254,92" fill="#ffffff"/>
        <polygon points="274,96 276,102 282,102 277,106 279,112 274,108 269,112 271,106 266,102 272,102" fill="#ffffff"/>
        <!-- Republican Party Text Pill -->
        <rect x="214" y="204" width="90" height="22" rx="11" fill="rgba(220,38,38,0.25)" stroke="#f87171" stroke-width="1.5"/>
        <text x="259" y="219" fill="#fca5a5" font-size="11" font-weight="700" text-anchor="middle" font-family="'Segoe UI', Roboto, sans-serif" letter-spacing="1.5">REPUBLICAN</text>
      </g>
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
    background: rgba(15, 23, 42, 0.76);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.14);
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
    font-size: 46px;
    font-weight: 800;
    line-height: 1.18;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #93c5fd 100%);
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
    width: 360px;
    height: 280px;
    position: relative;
    filter: drop-shadow(0 0 30px rgba(96, 165, 250, 0.35));
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
