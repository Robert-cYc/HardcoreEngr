import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

spec = {
    "filename": "ai-and-harness-engineering-guide.jpg",
    "badge": "AUTONOMOUS AGENT HARNESS SYSTEMS",
    "badge_color": "#a855f7",
    "title": "Hermes & OpenClaw Agent Harness",
    "subtitle": "Model-Native Tool Calling · Gateway-First Architecture · AST Sandboxing & Multi-Channel Egress",
    "glow_color": "rgba(168, 85, 247, 0.45)",
    "gradient": "radial-gradient(circle at 80% 30%, rgba(168, 85, 247, 0.28) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.25) 0%, transparent 55%), linear-gradient(135deg, #090614 0%, #110d24 50%, #08182b 100%)",
    "tags": ["NOUS HERMES 3", "OPENCLAW 2.0", "AGENT HARNESS", "AST SECURITY", "MCP PROTOCOL"],
    "icon_svg": """<svg width="340" height="260" viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="hermesGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#c084fc" />
          <stop offset="100%" stop-color="#a855f7" />
        </linearGradient>
        <linearGradient id="clawGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8" />
          <stop offset="100%" stop-color="#3b82f6" />
        </linearGradient>
        <filter id="glowHarness" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="12" flood-color="#a855f7" flood-opacity="0.5"/>
        </filter>
      </defs>

      <!-- Background Network Grid / Bus Lines -->
      <path d="M 20 45 L 90 45 L 130 85 L 210 85 L 250 45 L 320 45" stroke="rgba(255,255,255,0.08)" stroke-width="2" stroke-dasharray="4 6"/>
      <path d="M 20 215 L 90 215 L 130 175 L 210 175 L 250 215 L 320 215" stroke="rgba(255,255,255,0.08)" stroke-width="2" stroke-dasharray="4 6"/>

      <!-- Central Hexagonal Harness Shield -->
      <polygon points="170,35 255,85 255,175 170,225 85,175 85,85" 
               fill="rgba(15, 23, 42, 0.85)" stroke="url(#hermesGrad)" stroke-width="3" filter="url(#glowHarness)"/>

      <!-- Inner Rotating Circuit Loop -->
      <polygon points="170,55 235,95 235,165 170,205 105,165 105,95" 
               fill="none" stroke="url(#clawGrad)" stroke-width="1.8" stroke-dasharray="8 6"/>

      <!-- Left Core: Hermes Winged Symbol -->
      <g transform="translate(132, 95)">
        <!-- Wing Left -->
        <path d="M 8 20 C -12 10, -22 35, 4 48 C -6 32, 2 24, 8 20 Z" fill="#c084fc" opacity="0.9"/>
        <!-- Wing Right -->
        <path d="M 30 20 C 50 10, 60 35, 34 48 C 44 32, 36 24, 30 20 Z" fill="#c084fc" opacity="0.9"/>
        <!-- Central Caduceus / Thought Orb -->
        <circle cx="19" cy="34" r="12" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
        <path d="M 19 12 L 19 56" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="19" cy="10" r="4" fill="#38bdf8"/>
      </g>

      <!-- Right Core: Robotic Claw Harness Gripper -->
      <g transform="translate(148, 142)">
        <path d="M 22 18 Q 42 12, 48 30 Q 38 32, 26 24" fill="#38bdf8" opacity="0.9"/>
        <path d="M 22 26 Q 42 34, 46 48 Q 36 44, 26 32" fill="#38bdf8" opacity="0.9"/>
      </g>

      <!-- Connection Bus Nodes -->
      <circle cx="85" cy="130" r="6" fill="#38bdf8"/>
      <circle cx="85" cy="130" r="10" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2 2"/>
      
      <circle cx="255" cy="130" r="6" fill="#a855f7"/>
      <circle cx="255" cy="130" r="10" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="2 2"/>

      <line x1="30" y1="130" x2="85" y2="130" stroke="#38bdf8" stroke-width="2.5"/>
      <line x1="255" y1="130" x2="310" y2="130" stroke="#a855f7" stroke-width="2.5"/>

      <!-- Status Indicators -->
      <rect x="135" y="192" width="70" height="18" rx="4" fill="#030712" stroke="#10b981" stroke-width="1.5"/>
      <text x="170" y="204" font-family="'Consolas', monospace" font-size="9" fill="#10b981" text-anchor="middle" font-weight="bold">HARNESS PASS</text>
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
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #c084fc 100%);
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
    filter: drop-shadow(0 0 30px rgba(168, 85, 247, 0.35));
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

    temp_html = os.path.abspath("temp_hermes_banner.html")
    temp_png = os.path.abspath("temp_hermes_banner.png")
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
