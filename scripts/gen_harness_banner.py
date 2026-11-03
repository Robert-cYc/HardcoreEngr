import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

spec = {
    "filename": "ai-and-harness-engineering-guide.jpg",
    "badge": "PHYSICAL & AGENTIC HARNESS SYSTEMS",
    "badge_color": "#10b981",
    "title": "AI & Harness Engineering",
    "subtitle": "Smart Wire Harness Topological Routing · 48V Zonal Architecture · AI Agent Eval & Safety Testbed Harness",
    "glow_color": "rgba(16, 185, 129, 0.45)",
    "gradient": "radial-gradient(circle at 80% 30%, rgba(16, 185, 129, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.2) 0%, transparent 55%), linear-gradient(135deg, #05100c 0%, #0c1c16 50%, #0d222e 100%)",
    "tags": ["WIRING HARNESS (EWIS)", "TESLA 48V ZONAL", "AI EVAL HARNESS", "AGENT SANDBOXING", "DETERMINISTIC TESTBED"],
    "icon_svg": """<svg width="340" height="260" viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="wireGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#10b981" />
          <stop offset="100%" stop-color="#3b82f6" />
        </linearGradient>
        <linearGradient id="wireGrad2" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#38bdf8" />
          <stop offset="100%" stop-color="#a855f7" />
        </linearGradient>
        <filter id="glowHarness" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="10" flood-color="#10b981" flood-opacity="0.4"/>
        </filter>
      </defs>

      <!-- Background Network Grid / Circuit Traces -->
      <path d="M 20 50 L 100 50 L 140 90 L 220 90 L 260 50 L 320 50" stroke="rgba(255,255,255,0.08)" stroke-width="2" stroke-dasharray="4 6"/>
      <path d="M 20 210 L 100 210 L 140 170 L 220 170 L 260 210 L 320 210" stroke="rgba(255,255,255,0.08)" stroke-width="2" stroke-dasharray="4 6"/>

      <!-- Central Multi-core Cable Harness Bundle (Conduit & Splices) -->
      <g filter="url(#glowHarness)">
        <!-- Braided Wire Bundle Outer Sleeve -->
        <path d="M 30 130 C 90 90, 130 170, 200 130 C 250 100, 280 150, 310 130" 
              stroke="rgba(16, 185, 129, 0.25)" stroke-width="22" stroke-linecap="round" fill="none"/>

        <!-- Multi-Core Color Wires Inside Harness -->
        <!-- Wire 1: Emerald/Cyan Signal Bus -->
        <path d="M 30 124 C 90 84, 130 164, 200 124 C 250 94, 280 144, 310 124" 
              stroke="#10b981" stroke-width="3.5" stroke-linecap="round" fill="none"/>
        <!-- Wire 2: Electric Blue Power Rail -->
        <path d="M 30 130 C 90 90, 130 170, 200 130 C 250 100, 280 150, 310 130" 
              stroke="#38bdf8" stroke-width="3" stroke-linecap="round" fill="none"/>
        <!-- Wire 3: Purple High-Speed CAN/Ethernet -->
        <path d="M 30 136 C 90 96, 130 176, 200 136 C 250 106, 280 156, 310 136" 
              stroke="#a855f7" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <!-- Wire 4: Amber Ground Rail -->
        <path d="M 30 142 C 90 102, 130 182, 200 142 C 250 112, 280 162, 310 142" 
              stroke="#f59e0b" stroke-width="2" stroke-linecap="round" fill="none"/>

        <!-- Connectors / Terminal Blocks (Left & Right) -->
        <rect x="20" y="115" width="22" height="36" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
        <line x1="26" y1="123" x2="34" y2="123" stroke="#34d399" stroke-width="2"/>
        <line x1="26" y1="130" x2="34" y2="130" stroke="#38bdf8" stroke-width="2"/>
        <line x1="26" y1="137" x2="34" y2="137" stroke="#a855f7" stroke-width="2"/>
        <line x1="26" y1="144" x2="34" y2="144" stroke="#f59e0b" stroke-width="2"/>

        <rect x="298" y="115" width="22" height="36" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
        <line x1="304" y1="123" x2="312" y2="123" stroke="#34d399" stroke-width="2"/>
        <line x1="304" y1="130" x2="312" y2="130" stroke="#38bdf8" stroke-width="2"/>
        <line x1="304" y1="137" x2="312" y2="137" stroke="#a855f7" stroke-width="2"/>
        <line x1="304" y1="144" x2="312" y2="144" stroke="#f59e0b" stroke-width="2"/>

        <!-- Central Smart Microcontroller / Zonal Compute Node / Testbed Sandbox Shield -->
        <circle cx="170" cy="130" r="38" fill="rgba(15, 23, 42, 0.9)" stroke="#10b981" stroke-width="2.5"/>
        <circle cx="170" cy="130" r="28" fill="rgba(16, 185, 129, 0.15)" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="3 3"/>
        
        <!-- AI Core Neural / CPU / Harness Node Glyph -->
        <rect x="159" y="119" width="22" height="22" rx="4" fill="#10b981" fill-opacity="0.3" stroke="#34d399" stroke-width="1.5"/>
        <circle cx="170" cy="130" r="4" fill="#ffffff"/>
        
        <!-- Pins sticking out of Zonal Node -->
        <line x1="154" y1="125" x2="159" y2="125" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="154" y1="135" x2="159" y2="135" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="181" y1="125" x2="186" y2="125" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="181" y1="135" x2="186" y2="135" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="165" y1="114" x2="165" y2="119" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="175" y1="114" x2="175" y2="119" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="165" y1="141" x2="165" y2="146" stroke="#38bdf8" stroke-width="1.5"/>
        <line x1="175" y1="141" x2="175" y2="146" stroke="#38bdf8" stroke-width="1.5"/>
      </g>

      <!-- Branching Harness Drops (Sensors & Actuators & Agent Tool Calls) -->
      <path d="M 100 110 Q 110 65, 140 50" stroke="#10b981" stroke-width="2" stroke-linecap="round" fill="none"/>
      <circle cx="140" cy="50" r="4" fill="#34d399"/>
      
      <path d="M 230 120 Q 240 75, 270 60" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" fill="none"/>
      <circle cx="270" cy="60" r="4" fill="#38bdf8"/>

      <path d="M 120 160 Q 110 200, 80 220" stroke="#a855f7" stroke-width="2" stroke-linecap="round" fill="none"/>
      <circle cx="80" cy="220" r="4" fill="#c084fc"/>

      <path d="M 220 150 Q 230 195, 250 215" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" fill="none"/>
      <circle cx="250" cy="215" r="4" fill="#fbbf24"/>
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
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #6ee7b7 100%);
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
    filter: drop-shadow(0 0 30px rgba(16, 185, 129, 0.35));
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

    temp_html = os.path.abspath("temp_harness_banner.html")
    temp_png = os.path.abspath("temp_harness_banner.png")
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
