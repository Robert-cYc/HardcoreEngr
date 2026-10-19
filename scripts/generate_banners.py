import os
import subprocess
from PIL import Image

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
IMAGES_DIR = os.path.abspath("images")
os.makedirs(IMAGES_DIR, exist_ok=True)

BANNERS = [
    {
        "filename": "google-antigravity-guide.jpg",
        "badge": "NEXT-GEN DEVELOPER TOOLS",
        "badge_color": "#4285F4",
        "title": "Google Antigravity IDE",
        "subtitle": "Agent-First Architecture · Autonomous Coding Agents · AI Pair Programming",
        "glow_color": "rgba(66, 133, 244, 0.5)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(66, 133, 244, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(168, 85, 247, 0.18) 0%, transparent 50%), linear-gradient(135deg, #060913 0%, #0c1427 50%, #150d22 100%)",
        "accent_end": "#818cf8",
        "tags": ["AGENTIC WORKSPACE", "AUTONOMOUS DEBUGGING", "TASK PLANNER", "MCP PROTOCOL"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#4285F4" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" stroke="#4285F4" stroke-opacity="0.3" stroke-dasharray="3 3"/>
          <circle cx="12" cy="12" r="6" stroke="#818cf8" stroke-width="2"/>
          <circle cx="12" cy="12" r="2" fill="#4285F4"/>
          <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="#a855f7" stroke-width="1.5"/>
          <path d="m4.93 4.93 2.83 2.83M16.24 16.24l2.83 2.83M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" stroke="#38bdf8" stroke-opacity="0.5"/>
        </svg>"""
    },
    {
        "filename": "claude-code-guide.jpg",
        "badge": "ANTHROPIC AGENTIC ECOSYSTEM",
        "badge_color": "#d97706",
        "title": "Claude Code CLI & MCP",
        "subtitle": "Autonomous Terminal Agent · Model Context Protocol · Lifecycle Hooks & Plugins",
        "glow_color": "rgba(217, 119, 6, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(217, 119, 6, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(245, 158, 11, 0.15) 0%, transparent 50%), linear-gradient(135deg, #09090b 0%, #181412 50%, #20130d 100%)",
        "accent_end": "#f59e0b",
        "tags": ["CLAUDE 3.7 SONNET", "NATIVE BASH TOOL", ".MCP.JSON SERVERS", "WORKFLOW HOOKS"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="1.5">
          <rect x="2" y="4" width="20" height="16" rx="4" stroke="#d97706" stroke-width="1.5" fill="rgba(217, 119, 6, 0.08)"/>
          <path d="m7 10 3 3-3 3" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
          <line x1="13" y1="16" x2="17" y2="16" stroke="#f59e0b" stroke-width="2" stroke-linecap="round"/>
          <circle cx="18" cy="7" r="1.5" fill="#f59e0b"/>
          <circle cx="14" cy="7" r="1.5" fill="#d97706"/>
          <circle cx="10" cy="7" r="1.5" fill="#78350f"/>
        </svg>"""
    },
    {
        "filename": "hermes-agent-guide.jpg",
        "badge": "AUTONOMOUS AGENTS",
        "badge_color": "#06b6d4",
        "title": "Hermes Agent Framework",
        "subtitle": "Open-Source AI Desktop · Autonomous Task Graphs · Multi-Tool Execution Pipelines",
        "glow_color": "rgba(6, 182, 212, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(6, 182, 212, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%), linear-gradient(135deg, #060d16 0%, #0c1a29 50%, #061e30 100%)",
        "accent_end": "#22d3ee",
        "tags": ["HERMES DESKTOP", "HERMES ONE", "FUNCTION CALLING", "LOCAL TELEMETRY"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="1.5">
          <path d="M12 2L2 7l10 5 10-5-10-5Z" stroke="#22d3ee" stroke-width="2" fill="rgba(6, 182, 212, 0.1)"/>
          <path d="m2 17 10 5 10-5" stroke="#06b6d4" stroke-width="1.5"/>
          <path d="m2 12 10 5 10-5" stroke="#06b6d4" stroke-width="1.5"/>
          <circle cx="12" cy="12" r="3" fill="#22d3ee"/>
        </svg>"""
    },
    {
        "filename": "openclaw-agent-guide.jpg",
        "badge": "DESKTOP AUTOMATION",
        "badge_color": "#14b8a6",
        "title": "OpenClaw 2.0 AI Assistant",
        "subtitle": "Open-Source Autonomous Desktop Assistant · Vision GUI Automation · Local First",
        "glow_color": "rgba(20, 184, 166, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(20, 184, 166, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(16, 185, 129, 0.15) 0%, transparent 50%), linear-gradient(135deg, #041011 0%, #091f21 50%, #0d282b 100%)",
        "accent_end": "#2dd4bf",
        "tags": ["GUI MULTIMODAL", "MOUSE & KEY AUTOMATION", "SCREEN OCR", "OFFLINE AGENT"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" stroke-width="1.5">
          <circle cx="12" cy="12" r="8" stroke="#2dd4bf" stroke-width="1.5" fill="rgba(20, 184, 166, 0.08)"/>
          <path d="M12 4v4M12 16v4M4 12h4M16 12h4" stroke="#14b8a6" stroke-width="2"/>
          <circle cx="12" cy="12" r="3" fill="#2dd4bf"/>
          <path d="m7 7 2.5 2.5M14.5 14.5 17 17M7 17l2.5-2.5M14.5 9.5 17 7" stroke="#5eead4" stroke-opacity="0.6"/>
        </svg>"""
    },
    {
        "filename": "local-llm-inference-guide.jpg",
        "badge": "ON-PREMISE AI INFRASTRUCTURE",
        "badge_color": "#76b900",
        "title": "Local LLM Inference Engine",
        "subtitle": "LM Studio · llama.cpp · GGUF Quantization · NVIDIA RTX VRAM Acceleration",
        "glow_color": "rgba(118, 185, 0, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(118, 185, 0, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(16, 185, 129, 0.15) 0%, transparent 50%), linear-gradient(135deg, #060e04 0%, #0e1e08 50%, #15290c 100%)",
        "accent_end": "#84cc16",
        "tags": ["VRAM OFFLOADING", "Q4_K_M / Q8_0", "CUDA / AVX-512", "ZERO-CLOUD PRIVACY"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#76b900" stroke-width="1.5">
          <rect x="4" y="4" width="16" height="16" rx="2" stroke="#84cc16" stroke-width="2" fill="rgba(118, 185, 0, 0.1)"/>
          <rect x="8" y="8" width="8" height="8" rx="1" fill="#76b900"/>
          <path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3" stroke="#84cc16" stroke-width="1.5"/>
        </svg>"""
    },
    {
        "filename": "workflow-automation-guide.jpg",
        "badge": "EVENT-DRIVEN AUTOMATION",
        "badge_color": "#ea4b71",
        "title": "Workflow Automation Hub",
        "subtitle": "n8n · Zapier · Make · Visual Node-Based Pipelines & AI Agent Workflows",
        "glow_color": "rgba(234, 75, 113, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(234, 75, 113, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(249, 115, 22, 0.15) 0%, transparent 50%), linear-gradient(135deg, #100609 0%, #1f0b12 50%, #2b0c16 100%)",
        "accent_end": "#fb7185",
        "tags": ["WEBHOOK TRIGGERS", "NODE PIPELINES", "SELF-HOSTED DOCKER", "API INTEGRATIONS"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#ea4b71" stroke-width="1.5">
          <circle cx="6" cy="6" r="3" stroke="#fb7185" stroke-width="2" fill="rgba(234, 75, 113, 0.2)"/>
          <circle cx="18" cy="6" r="3" stroke="#fb7185" stroke-width="2" fill="rgba(234, 75, 113, 0.2)"/>
          <circle cx="12" cy="18" r="3" stroke="#fb7185" stroke-width="2" fill="rgba(234, 75, 113, 0.2)"/>
          <path d="M8.5 7.5l7 0M7.5 8.5l3 7M16.5 8.5l-3 7" stroke="#ea4b71" stroke-width="1.5" stroke-dasharray="2 2"/>
        </svg>"""
    },
    {
        "filename": "python-uv-guide.jpg",
        "badge": "PYTHON MODERN TOOLING",
        "badge_color": "#6366f1",
        "title": "Astral uv: Next-Gen Python",
        "subtitle": "Rust-Powered Package Manager · 10-100x Faster · Pip, Poetry & Pyenv Replacement",
        "glow_color": "rgba(99, 102, 241, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(99, 102, 241, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(168, 85, 247, 0.15) 0%, transparent 50%), linear-gradient(135deg, #090916 0%, #13132d 50%, #1a153c 100%)",
        "accent_end": "#818cf8",
        "tags": ["RUST VELOCITY", "UV.LOCK RESOLVER", "VIRTUALENV MGR", "PYTHON TOOL RUNNER"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="1.5">
          <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" stroke="#818cf8" stroke-width="2" fill="rgba(99, 102, 241, 0.2)"/>
          <path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" stroke="#818cf8" stroke-width="2"/>
          <circle cx="15.5" cy="8.5" r="1.5" fill="#c084fc"/>
        </svg>"""
    },
    {
        "filename": "nodejs-javascript-guide.jpg",
        "badge": "RUNTIME & ECOSYSTEM",
        "badge_color": "#22c55e",
        "title": "Node.js & JavaScript Runtime",
        "subtitle": "V8 Engine · Libuv Event Loop · npm & npx · Enterprise Java Comparison",
        "glow_color": "rgba(34, 197, 94, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(34, 197, 94, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(234, 179, 8, 0.15) 0%, transparent 50%), linear-gradient(135deg, #051109 0%, #0b2213 50%, #142e1a 100%)",
        "accent_end": "#4ade80",
        "tags": ["NON-BLOCKING I/O", "EVENT DRIVEN", "NPM ECOSYSTEM", "JVM VS V8"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="1.5">
          <path d="M12 2l9 5v10l-9 5-9-5V7l9-5Z" stroke="#4ade80" stroke-width="2" fill="rgba(34, 197, 94, 0.1)"/>
          <path d="M12 22V12" stroke="#4ade80" stroke-width="1.5"/>
          <path d="M21 7l-9 5-9-5" stroke="#4ade80" stroke-width="1.5"/>
        </svg>"""
    },
    {
        "filename": "apache-tomcat-guide.jpg",
        "badge": "WEB & APP SERVER ARCHITECTURE",
        "badge_color": "#ef4444",
        "title": "Apache HTTP Server vs Tomcat",
        "subtitle": "Static Web Server vs Java Servlet Container · Reverse Proxy & mod_jk / AJP",
        "glow_color": "rgba(239, 68, 68, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(239, 68, 68, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(245, 158, 11, 0.15) 0%, transparent 50%), linear-gradient(135deg, #130707 0%, #240e0e 50%, #311311 100%)",
        "accent_end": "#f87171",
        "tags": ["STATIC FILE SPEED", "SERVLET & JSP ENGINE", "REVERSE PROXY", "LOAD BALANCING"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5">
          <rect x="2" y="3" width="20" height="7" rx="2" stroke="#f87171" stroke-width="2" fill="rgba(239, 68, 68, 0.1)"/>
          <rect x="2" y="14" width="20" height="7" rx="2" stroke="#fbbf24" stroke-width="2" fill="rgba(245, 158, 11, 0.1)"/>
          <circle cx="6" cy="6.5" r="1" fill="#f87171"/>
          <circle cx="6" cy="17.5" r="1" fill="#fbbf24"/>
          <path d="M12 10v4" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="2 2"/>
        </svg>"""
    },
    {
        "filename": "react-framework-guide.jpg",
        "badge": "MODERN FRONTEND ARCHITECTURE",
        "badge_color": "#00d8fe",
        "title": "React Architecture & Ecosystem",
        "subtitle": "Virtual DOM · Fiber Reconciler · Component Trees · Modern Hooks & Server Components",
        "glow_color": "rgba(0, 216, 254, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(0, 216, 254, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%), linear-gradient(135deg, #04101a 0%, #081d2e 50%, #0d273d 100%)",
        "accent_end": "#38bdf8",
        "tags": ["REACT 19", "FIBER ENGINE", "VIRTUAL DOM", "JSX ECOSYSTEM"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#00d8fe" stroke-width="1.5">
          <ellipse cx="12" cy="12" rx="10" ry="4" stroke="#00d8fe" stroke-width="1.5" transform="rotate(30 12 12)"/>
          <ellipse cx="12" cy="12" rx="10" ry="4" stroke="#00d8fe" stroke-width="1.5" transform="rotate(90 12 12)"/>
          <ellipse cx="12" cy="12" rx="10" ry="4" stroke="#00d8fe" stroke-width="1.5" transform="rotate(150 12 12)"/>
          <circle cx="12" cy="12" r="2" fill="#00d8fe"/>
        </svg>"""
    },
    {
        "filename": "cloudflare-network-guide.jpg",
        "badge": "EDGE INFRASTRUCTURE & SECURITY",
        "badge_color": "#f6821f",
        "title": "Cloudflare Global Edge Platform",
        "subtitle": "Anycast CDN · DNS Routing · WAF & DDoS Shield · V8 Isolate Workers · Pages",
        "glow_color": "rgba(246, 130, 31, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(246, 130, 31, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(250, 173, 63, 0.15) 0%, transparent 50%), linear-gradient(135deg, #120a05 0%, #211309 50%, #2f190a 100%)",
        "accent_end": "#fb923c",
        "tags": ["300+ ANYCAST POPS", "DDoS MITIGATION", "EDGE WORKERS", "ZERO TRUST WAF"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#f6821f" stroke-width="1.5">
          <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" stroke="#fb923c" stroke-width="2" fill="rgba(246, 130, 31, 0.15)"/>
          <path d="m10 13 4 4m0-4-4 4" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/>
        </svg>"""
    },
    {
        "filename": "wireshark-packet-guide.jpg",
        "badge": "PACKET FORENSICS & NETWORKING",
        "badge_color": "#0284c7",
        "title": "Wireshark Protocol Analysis",
        "subtitle": "Deep Packet Inspection · TCP/IP Streams · TLS 1.3 Decryption · Forensic PCAP",
        "glow_color": "rgba(2, 132, 199, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(2, 132, 199, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(14, 165, 233, 0.15) 0%, transparent 50%), linear-gradient(135deg, #040e16 0%, #091a27 50%, #0d283c 100%)",
        "accent_end": "#38bdf8",
        "tags": ["PACKET SNIFFER", "TCP STREAM RECONSTRUCTION", "DISPLAY FILTERS", "PROMISCUOUS CAPTURE"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="1.5">
          <path d="M2 12c4-4 8-6 12-4 3 1.5 5 5 8 4-3 5-8 7-12 5-3-1.5-5-3-8-5Z" stroke="#38bdf8" stroke-width="2" fill="rgba(2, 132, 199, 0.15)"/>
          <path d="M12 8l2-5 3 4" stroke="#38bdf8" stroke-width="2" stroke-linejoin="round" fill="rgba(56, 189, 248, 0.3)"/>
          <circle cx="8" cy="11" r="1.5" fill="#ffffff"/>
        </svg>"""
    },
    {
        "filename": "industrial-protocols-guide.jpg",
        "badge": "OPERATIONAL TECHNOLOGY (OT)",
        "badge_color": "#f59e0b",
        "title": "Industrial OT Protocols",
        "subtitle": "RS232/RS485 · Modbus RTU/TCP · OPC DA/UA · SCADA & Industrial Automation",
        "glow_color": "rgba(245, 158, 11, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(245, 158, 11, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(217, 119, 6, 0.15) 0%, transparent 50%), linear-gradient(135deg, #130d04 0%, #241909 50%, #34240a 100%)",
        "accent_end": "#fbbf24",
        "tags": ["MODBUS REGISTERS", "OPC UA SECURITY", "PLC TELEMETRY", "SCADA ARCHITECTURE"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="3" stroke="#fbbf24" stroke-width="2" fill="rgba(245, 158, 11, 0.1)"/>
          <circle cx="8" cy="8" r="2" fill="#fbbf24"/>
          <circle cx="16" cy="8" r="2" fill="#fbbf24"/>
          <circle cx="8" cy="16" r="2" fill="#fbbf24"/>
          <circle cx="16" cy="16" r="2" fill="#fbbf24"/>
          <path d="M8 10v4M16 10v4M10 8h4M10 16h4" stroke="#f59e0b" stroke-width="1.5"/>
        </svg>"""
    },
    {
        "filename": "influxdb-timeseries-guide.jpg",
        "badge": "TIME-SERIES DATABASE (TSDB)",
        "badge_color": "#9333ea",
        "title": "InfluxDB Time-Series Engine",
        "subtitle": "High-Throughput Ingestion · TSM & IOx Engine · Real-Time Telemetry & Monitoring",
        "glow_color": "rgba(147, 51, 234, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(147, 51, 234, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(168, 85, 247, 0.15) 0%, transparent 50%), linear-gradient(135deg, #0e0517 0%, #1c0a2e 50%, #280e41 100%)",
        "accent_end": "#c084fc",
        "tags": ["NANOSECOND TIMESTAMPS", "APACHE ARROW IOX", "METRIC TELEMETRY", "RETENTION POLICIES"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#9333ea" stroke-width="1.5">
          <path d="M3 3v18h18" stroke="#c084fc" stroke-width="2"/>
          <path d="m19 9-5 5-4-4-4 4" stroke="#e9d5ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="19" cy="9" r="2" fill="#c084fc"/>
          <circle cx="14" cy="14" r="2" fill="#c084fc"/>
          <circle cx="10" cy="10" r="2" fill="#c084fc"/>
          <circle cx="6" cy="14" r="2" fill="#c084fc"/>
        </svg>"""
    },
    {
        "filename": "notion-workspace-guide.jpg",
        "badge": "MODULAR KNOWLEDGE PLATFORM",
        "badge_color": "#ffffff",
        "title": "Notion Connected Workspace",
        "subtitle": "Relational Databases · Custom Formula 2.0 · Claude AI Integration · Enterprise Wiki",
        "glow_color": "rgba(255, 255, 255, 0.3)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(255, 255, 255, 0.12) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(148, 163, 184, 0.1) 0%, transparent 50%), linear-gradient(135deg, #09090b 0%, #18181b 50%, #27272a 100%)",
        "accent_end": "#e2e8f0",
        "tags": ["RELATIONAL DB", "ROLLUP FORMULAS", "AI SUMMARY", "PAGE NESTING"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.5">
          <rect x="4" y="3" width="16" height="18" rx="2" stroke="#e2e8f0" stroke-width="2" fill="rgba(255, 255, 255, 0.08)"/>
          <path d="M8 7h8M8 11h8M8 15h5" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
        </svg>"""
    },
    {
        "filename": "obsidian-pkm-guide.jpg",
        "badge": "PERSONAL KNOWLEDGE MANAGEMENT",
        "badge_color": "#8b5cf6",
        "title": "Obsidian Second Brain",
        "subtitle": "Local-First Markdown · Interactive 3D Knowledge Graph · Bidirectional Backlinks",
        "glow_color": "rgba(139, 92, 246, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(139, 92, 246, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(124, 58, 237, 0.15) 0%, transparent 50%), linear-gradient(135deg, #0a0618 0%, #140d2f 50%, #201347 100%)",
        "accent_end": "#a78bfa",
        "tags": ["LOCAL-FIRST VAULT", "BIDIRECTIONAL LINKS", "GRAPH CONSTELLATION", "DATAVIEW QUERIES"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="1.5">
          <polygon points="12 2 2 7 12 22 22 7" stroke="#a78bfa" stroke-width="2" fill="rgba(139, 92, 246, 0.15)"/>
          <line x1="2" y1="7" x2="22" y2="7" stroke="#c4b5fd" stroke-width="1.5"/>
          <line x1="12" y1="2" x2="12" y2="22" stroke="#c4b5fd" stroke-width="1.5"/>
        </svg>"""
    },
    {
        "filename": "canva-design-guide.jpg",
        "badge": "VISUAL CREATIVE TOOLS",
        "badge_color": "#00c4cc",
        "title": "Canva Creative Studio",
        "subtitle": "Modern Digital Design · Vector Composition · Brand Kits · AI Visual Workflow",
        "glow_color": "rgba(0, 196, 204, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(0, 196, 204, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(125, 42, 232, 0.15) 0%, transparent 50%), linear-gradient(135deg, #041014 0%, #091c24 50%, #112631 100%)",
        "accent_end": "#38bdf8",
        "tags": ["VECTOR CANVAS", "TYPOGRAPHY KITS", "AI MAGIC MEDIA", "PROTOTYPING"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#00c4cc" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" stroke="#00c4cc" stroke-width="2" fill="rgba(0, 196, 204, 0.1)"/>
          <path d="M14.5 9a3.5 3.5 0 1 0 0 6h2" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
        </svg>"""
    },
    {
        "filename": "google-colab-guide.jpg",
        "badge": "CLOUD DATA SCIENCE",
        "badge_color": "#f9ab00",
        "title": "Google Colab Workstation",
        "subtitle": "Cloud Jupyter Notebooks · Free GPU / TPU Acceleration · Python ML & Data Science",
        "glow_color": "rgba(249, 171, 0, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(249, 171, 0, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(234, 88, 12, 0.15) 0%, transparent 50%), linear-gradient(135deg, #130c04 0%, #221708 50%, #301f09 100%)",
        "accent_end": "#fbbf24",
        "tags": ["T4 & A100 GPU", "JUPYTER INTERACTIVE", "HUGGING FACE INTEGRATION", "ZERO INSTALL"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#f9ab00" stroke-width="1.5">
          <path d="M12 12c-2-3-6-3-8 0s2 6 5 4l3-4Z" stroke="#fbbf24" stroke-width="2" fill="rgba(249, 171, 0, 0.15)"/>
          <path d="M12 12c2 3 6 3 8 0s-2-6-5-4l-3 4Z" stroke="#fbbf24" stroke-width="2" fill="rgba(249, 171, 0, 0.15)"/>
        </svg>"""
    },
    {
        "filename": "prompt-engineering-guide.jpg",
        "badge": "COGNITIVE ARCHITECTURE",
        "badge_color": "#a855f7",
        "title": "Prompt Engineering Mastery",
        "subtitle": "Systematic Prompting · Few-Shot · Chain-of-Thought (CoT) · Tree of Thoughts",
        "glow_color": "rgba(168, 85, 247, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(168, 85, 247, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(236, 72, 153, 0.15) 0%, transparent 50%), linear-gradient(135deg, #0e0517 0%, #1a0b2c 50%, #280d40 100%)",
        "accent_end": "#c084fc",
        "tags": ["CHAIN-OF-THOUGHT", "FEW-SHOT IN-CONTEXT", "REASONING TOKENS", "STRUCTURED JSON"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="1.5">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="#c084fc" stroke-width="2" fill="rgba(168, 85, 247, 0.15)"/>
          <path d="M8 9h8M8 13h4" stroke="#f472b6" stroke-width="2" stroke-linecap="round"/>
        </svg>"""
    },
    {
        "filename": "ai-algorithms-guide.jpg",
        "badge": "MACHINE LEARNING FOUNDATIONS",
        "badge_color": "#10b981",
        "title": "AI & ML Algorithms Atlas",
        "subtitle": "Transformer Attention Matrices · Backpropagation · Gradient Descent · CNN & GNN",
        "glow_color": "rgba(16, 185, 129, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(16, 185, 129, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%), linear-gradient(135deg, #04120c 0%, #082418 50%, #0d3624 100%)",
        "accent_end": "#34d399",
        "tags": ["SELF-ATTENTION QKV", "LOSS LANDSCAPES", "CONVOLUTION KERNELS", "EMBEDDING VECTORS"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="1.5">
          <circle cx="5" cy="6" r="2.5" fill="#34d399"/>
          <circle cx="5" cy="18" r="2.5" fill="#34d399"/>
          <circle cx="12" cy="12" r="3" fill="#10b981"/>
          <circle cx="19" cy="6" r="2.5" fill="#34d399"/>
          <circle cx="19" cy="18" r="2.5" fill="#34d399"/>
          <line x1="7.5" y1="6" x2="9" y2="12" stroke="#10b981" stroke-width="1.5"/>
          <line x1="7.5" y1="18" x2="9" y2="12" stroke="#10b981" stroke-width="1.5"/>
          <line x1="15" y1="12" x2="16.5" y2="6" stroke="#10b981" stroke-width="1.5"/>
          <line x1="15" y1="12" x2="16.5" y2="18" stroke="#10b981" stroke-width="1.5"/>
        </svg>"""
    },
    {
        "filename": "open-source-licenses-guide.jpg",
        "badge": "LEGAL & OPEN SOURCE GOVERNANCE",
        "badge_color": "#38bdf8",
        "title": "Open Source Licenses Guide",
        "subtitle": "Permissive vs Copyleft · MIT & Apache 2.0 vs GPLv3 & AGPL · Commercial Compliance",
        "glow_color": "rgba(56, 189, 248, 0.45)",
        "gradient": "radial-gradient(circle at 75% 30%, rgba(56, 189, 248, 0.25) 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%), linear-gradient(135deg, #050f16 0%, #0b1f2e 50%, #102e43 100%)",
        "accent_end": "#7dd3fc",
        "tags": ["MIT PERMISSIVE", "APACHE 2.0 PATENTS", "GPLv3 RECIPROCAL", "DUAL LICENSING"],
        "icon_svg": """<svg width="220" height="220" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="1.5">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#7dd3fc" stroke-width="2" fill="rgba(56, 189, 248, 0.15)"/>
          <path d="m9 12 2 2 4-4" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>"""
    }
]

def render_banner(spec):
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
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 28px;
    padding: 60px 70px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 50px {spec['glow_color']};
  }}
  .content {{
    max-width: 760px;
    z-index: 2;
  }}
  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 18px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid {spec['badge_color']};
    color: {spec['badge_color']};
    font-size: 14px;
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
    font-size: 54px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 18px;
    background: linear-gradient(135deg, #ffffff 40%, {spec['accent_end']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
  }}
  p.subtitle {{
    font-size: 21px;
    line-height: 1.5;
    color: #94a3b8;
    margin-bottom: 36px;
    font-weight: 400;
  }}
  .tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }}
  .tag {{
    padding: 8px 16px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Consolas', monospace;
    letter-spacing: 0.5px;
  }}
  .visual {{
    position: relative;
    width: 280px;
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle, {spec['glow_color']} 0%, transparent 70%);
    border-radius: 50%;
    border: 1px dashed rgba(255, 255, 255, 0.15);
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

    temp_html = os.path.abspath("temp_banner.html")
    temp_png = os.path.abspath("temp_banner.png")
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

def main():
    print(f"Rendering {len(BANNERS)} cybernetic banners with Edge headless...")
    for spec in BANNERS:
        render_banner(spec)
    print("All banners generated successfully!")

if __name__ == "__main__":
    main()
