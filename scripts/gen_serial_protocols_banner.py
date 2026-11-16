import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

spec = {
    "filename": "i2c-spi-uart-rs232-rs485-guide.jpg",
    "badge": "EMBEDDED HARDWARE & SERIAL BUS ENGINEERING",
    "badge_color": "#06b6d4",
    "title": "I2C · SPI · UART · RS232 · RS485",
    "subtitle": "On-Board Bus vs Long-Distance Industrial Interfaces | Waveform Timing · Differential Physics · Full Architecture Matrix",
    "glow_color": "rgba(6, 182, 212, 0.45)",
    "gradient": "radial-gradient(circle at 80% 30%, rgba(6, 182, 212, 0.3) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(245, 158, 11, 0.25) 0%, transparent 55%), linear-gradient(135deg, #050e14 0%, #091722 50%, #1a1208 100%)",
    "tags": ["I2C (OPEN-DRAIN)", "SPI (FULL-DUPLEX)", "UART (ASYNC TTL)", "RS-232 (BIPOLAR)", "RS-485 (DIFFERENTIAL)"],
    "icon_svg": """<svg width="340" height="260" viewBox="0 0 340 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8" />
          <stop offset="100%" stop-color="#0284c7" />
        </linearGradient>
        <linearGradient id="amberGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fbbf24" />
          <stop offset="100%" stop-color="#d97706" />
        </linearGradient>
        <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#34d399" />
          <stop offset="100%" stop-color="#059669" />
        </linearGradient>
        <filter id="scopeGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="10" flood-color="#06b6d4" flood-opacity="0.45"/>
        </filter>
      </defs>

      <!-- Oscilloscope / Bus Background Frame -->
      <rect x="25" y="25" width="290" height="210" rx="14" fill="rgba(10, 20, 30, 0.9)" stroke="rgba(255,255,255,0.12)" stroke-width="1.5" filter="url(#scopeGlow)"/>

      <!-- Grid lines (Oscilloscope reticle) -->
      <line x1="25" y1="75" x2="315" y2="75" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3 3"/>
      <line x1="25" y1="130" x2="315" y2="130" stroke="rgba(255,255,255,0.08)"/>
      <line x1="25" y1="185" x2="315" y2="185" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3 3"/>
      <line x1="85" y1="25" x2="85" y2="235" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3 3"/>
      <line x1="170" y1="25" x2="170" y2="235" stroke="rgba(255,255,255,0.08)"/>
      <line x1="255" y1="25" x2="255" y2="235" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3 3"/>

      <!-- Trace 1: Clock Pulse (SCK / SCL) in Emerald Green -->
      <path d="M 40 60 L 65 60 L 65 45 L 85 45 L 85 60 L 105 60 L 105 45 L 125 45 L 125 60 L 145 60 L 145 45 L 165 45 L 165 60 L 185 60 L 185 45 L 205 45 L 205 60 L 225 60 L 225 45 L 245 45 L 245 60 L 265 60 L 265 45 L 285 45 L 285 60 L 300 60" 
            stroke="#10b981" stroke-width="2.5" fill="none" stroke-linejoin="round"/>
      <text x="35" y="48" font-family="'Consolas', monospace" font-size="8" fill="#10b981" font-weight="bold">CLK</text>

      <!-- Trace 2: Data Waveform (SDA / MOSI / TX) in Cyan Blue -->
      <path d="M 40 100 L 70 100 L 70 85 L 130 85 L 130 100 L 160 100 L 160 85 L 190 85 L 190 100 L 250 100 L 250 85 L 280 85 L 280 100 L 300 100" 
            stroke="#38bdf8" stroke-width="2.5" fill="none" stroke-linejoin="round"/>
      <text x="35" y="88" font-family="'Consolas', monospace" font-size="8" fill="#38bdf8" font-weight="bold">DATA</text>

      <!-- Trace 3: Differential A - B Waveform (RS-485 / CAN) in Amber -->
      <!-- Line A (+) -->
      <path d="M 40 140 L 95 140 L 95 152 L 150 152 L 150 140 L 210 140 L 210 152 L 270 152 L 270 140 L 300 140" 
            stroke="#fbbf24" stroke-width="2" fill="none" stroke-linejoin="round"/>
      <!-- Line B (-) Inverted -->
      <path d="M 40 155 L 95 155 L 95 143 L 150 143 L 150 155 L 210 155 L 210 143 L 270 143 L 270 155 L 300 155" 
            stroke="#f59e0b" stroke-width="2" fill="none" stroke-linejoin="round" opacity="0.8"/>
      <text x="35" y="145" font-family="'Consolas', monospace" font-size="8" fill="#fbbf24" font-weight="bold">DIFF</text>

      <!-- Lower Bus Interface Nodes (Microchip / Transceiver Package) -->
      <g transform="translate(60, 185)">
        <rect x="0" y="0" width="46" height="30" rx="4" fill="#0f172a" stroke="#06b6d4" stroke-width="1.5"/>
        <text x="23" y="18" font-family="'Consolas', monospace" font-size="9" fill="#38bdf8" text-anchor="middle" font-weight="bold">I2C</text>
        <circle cx="23" cy="5" r="2" fill="#06b6d4"/>
      </g>

      <g transform="translate(118, 185)">
        <rect x="0" y="0" width="46" height="30" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
        <text x="23" y="18" font-family="'Consolas', monospace" font-size="9" fill="#34d399" text-anchor="middle" font-weight="bold">SPI</text>
        <circle cx="23" cy="5" r="2" fill="#10b981"/>
      </g>

      <g transform="translate(176, 185)">
        <rect x="0" y="0" width="46" height="30" rx="4" fill="#0f172a" stroke="#a855f7" stroke-width="1.5"/>
        <text x="23" y="18" font-family="'Consolas', monospace" font-size="9" fill="#c084fc" text-anchor="middle" font-weight="bold">UART</text>
        <circle cx="23" cy="5" r="2" fill="#a855f7"/>
      </g>

      <g transform="translate(234, 185)">
        <rect x="0" y="0" width="46" height="30" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="23" y="18" font-family="'Consolas', monospace" font-size="8" fill="#fbbf24" text-anchor="middle" font-weight="bold">RS485</text>
        <circle cx="23" cy="5" r="2" fill="#f59e0b"/>
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
    background: rgba(6, 182, 212, 0.12);
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
    font-size: 44px;
    font-weight: 800;
    line-height: 1.18;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%);
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
    filter: drop-shadow(0 0 30px rgba(6, 182, 212, 0.35));
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

    temp_html = os.path.abspath("temp_serial_banner.html")
    temp_png = os.path.abspath("temp_serial_banner.png")
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
