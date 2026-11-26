import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

spec = {
    "filename": "tesla-fsd-v15-reality-view-guide.jpg",
    "badge": "TESLA FSD v15 · GENERATIVE AI VISUALIZATION",
    "badge_color": "#ef4444",
    "title": "Tesla FSD v15 Reality View",
    "subtitle": "Generative 36fps AI Street View · Universal Vision Encoder (UVE) · 1B Diffusion Model on AI4 TRIP Accelerator",
    "glow_color": "rgba(239, 68, 68, 0.42)",
    "gradient": "radial-gradient(circle at 80% 25%, rgba(239, 68, 68, 0.28) 0%, transparent 58%), radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.28) 0%, transparent 55%), linear-gradient(135deg, #09090b 0%, #121520 50%, #1a0d12 100%)",
    "tags": ["FSD v15", "REALITY VIEW", "UVE ENCODER", "1B DIFFUSION", "36 FPS", "AI4 TRIP"],
    "icon_svg": """<svg width="340" height="260" viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="roadGrad" x1="50%" y1="0%" x2="50%" y2="100%">
          <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.65"/>
        </linearGradient>
        <linearGradient id="pathGlow" x1="50%" y1="0%" x2="50%" y2="100%">
          <stop offset="0%" stop-color="#60a5fa"/>
          <stop offset="100%" stop-color="#2563eb"/>
        </linearGradient>
        <linearGradient id="carBody" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="100%" stop-color="#94a3b8"/>
        </linearGradient>
        <filter id="neonRed" x="-25%" y="-25%" width="150%" height="150%">
          <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#3b82f6" flood-opacity="0.7"/>
        </filter>
      </defs>

      <!-- Display Screen Frame -->
      <rect x="20" y="20" width="300" height="220" rx="16" fill="rgba(10, 14, 24, 0.92)" stroke="rgba(255,255,255,0.16)" stroke-width="1.5"/>

      <!-- Cityscape Horizon Buildings (Photorealistic Silhouette Layer) -->
      <g opacity="0.55">
        <rect x="35" y="45" width="32" height="65" rx="2" fill="#1e293b" stroke="#38bdf8" stroke-width="0.8"/>
        <rect x="72" y="60" width="24" height="50" rx="2" fill="#1e293b" stroke="#38bdf8" stroke-width="0.8"/>
        <rect x="242" y="50" width="28" height="60" rx="2" fill="#1e293b" stroke="#38bdf8" stroke-width="0.8"/>
        <rect x="275" y="38" width="30" height="72" rx="2" fill="#1e293b" stroke="#ef4444" stroke-width="0.8"/>
      </g>

      <!-- Perspective Street Surface -->
      <polygon points="135,105 205,105 295,225 45,225" fill="url(#roadGrad)" stroke="rgba(96,165,250,0.4)" stroke-width="1"/>
      
      <!-- Lane Lines -->
      <line x1="158" y1="105" x2="115" y2="225" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="6 6"/>
      <line x1="182" y1="105" x2="225" y2="225" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="6 6"/>

      <!-- AI FSD Intent Path (Glowing Blue Trajectory Ribbon) -->
      <path d="M 170 195 Q 170 150, 175 112" stroke="url(#pathGlow)" stroke-width="14" stroke-linecap="round" opacity="0.85" filter="url(#neonRed)"/>
      <!-- Intent Turn Arrow -->
      <polygon points="175,98 164,116 186,116" fill="#93c5fd" filter="url(#neonRed)"/>

      <!-- Ego Vehicle (Top-Down Chase View) -->
      <g transform="translate(152, 168)">
        <rect x="0" y="0" width="36" height="54" rx="10" fill="url(#carBody)" stroke="#ef4444" stroke-width="1.5"/>
        <!-- Windshield & Glass Roof -->
        <rect x="5" y="12" width="26" height="28" rx="5" fill="#0f172a"/>
        <!-- Taillights -->
        <rect x="4" y="48" width="10" height="3" rx="1" fill="#ef4444"/>
        <rect x="22" y="48" width="10" height="3" rx="1" fill="#ef4444"/>
      </g>

      <!-- Generative Vision Scan Rings -->
      <ellipse cx="170" cy="185" rx="75" ry="22" stroke="rgba(56,189,248,0.45)" stroke-width="1.2" stroke-dasharray="4 4"/>
      <ellipse cx="170" cy="185" rx="115" ry="34" stroke="rgba(239,68,68,0.35)" stroke-width="1" stroke-dasharray="6 6"/>

      <!-- HUD Overlay Pill -->
      <rect x="34" y="30" width="112" height="20" rx="6" fill="rgba(15,23,42,0.85)" stroke="#38bdf8" stroke-width="1"/>
      <text x="90" y="43" font-family="'Consolas', monospace" font-size="9" fill="#38bdf8" text-anchor="middle" font-weight="bold">REALITY VIEW 36FPS</text>

      <rect x="224" y="30" width="82" height="20" rx="6" fill="rgba(15,23,42,0.85)" stroke="#ef4444" stroke-width="1"/>
      <text x="265" y="43" font-family="'Consolas', monospace" font-size="9" fill="#f87171" text-anchor="middle" font-weight="bold">UVE · AI4</text>
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
    background: rgba(15, 23, 42, 0.78);
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
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid {spec['badge_color']};
    color: #f87171;
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
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 55%, #f87171 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
  }}
  .subtitle {{
    font-size: 18px;
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
    filter: drop-shadow(0 0 30px rgba(239, 68, 68, 0.35));
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

    temp_html = os.path.abspath("temp_fsd15_banner.html")
    temp_png = os.path.abspath("temp_fsd15_banner.png")
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

