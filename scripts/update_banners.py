import os
import re
import json
import bs4

ARTICLE_BANNER_MAP = {
    "ai-algorithms.html": "ai-algorithms-guide.jpg",
    "ai-automation-tools-guide.html": "workflow-automation-guide.jpg",
    "ai-models.html": "frontier-llms-guide.jpg",
    "antigravity-2-vs-ide-vs-cli-vs-sdk.html": "antigravity-2-vs-ide-vs-cli-vs-sdk-guide.jpg",
    "antigravity-desktop-vs-ide-vs-agy.html": "antigravity-desktop-vs-ide-vs-agy-guide.jpg",
    "anythingllm-guide.html": "anythingllm-guide.jpg",
    "apache-vs-tomcat.html": "apache-tomcat-guide.jpg",
    "api-architecture-guide.html": "api-architecture-guide.jpg",
    "apple-services-ecosystem.html": "apple-ecosystem.jpg",
    "bluetooth-technology-guide.html": "bluetooth-technology-guide.jpg",
    "btop-monitor-guide.html": "btop-monitor-guide.jpg",
    "canva-tutorial.html": "canva-design-guide.jpg",
    "chip-wars-intel-amd-nvidia-asic.html": "chip-wars-guide.jpg",
    "claude-code-commands.html": "claude-code-guide.jpg",
    "claude-code-hooks-guide.html": "claude-code-guide.jpg",
    "claude-code-mcp-skill-guide.html": "claude-code-guide.jpg",
    "claude-model-families.html": "claude-model-guide.jpg",
    "claude-skill-mcp-plugin-deep.html": "claude-code-guide.jpg",
    "cloudflare-guide.html": "cloudflare-network-guide.jpg",
    "deepseek-ai-guide.html": "deepseek-ai-guide.jpg",
    "docker-compose-guide.html": "docker-guide.jpg",
    "docker-container-guide.html": "docker-guide.jpg",
    "gemini-model-guide.html": "gemini-model-guide.jpg",
    "git-commands.html": "git-commands-guide.jpg",
    "github-actions-guide.html": "github-actions.jpg",
    "google-antigravity-ide-guide.html": "google-antigravity-guide.jpg",
    "google-colab-guide.html": "google-colab-guide.jpg",
    "google-services-ecosystem.html": "google-ecosystem.jpg",
    "gpt-5-model-guide.html": "gpt5-model-guide.jpg",
    "grok-model-guide.html": "grok-model-guide.jpg",
    "hermes-agent-guide.html": "hermes-agent-guide.jpg",
    "hermes-desktop-vs-hermes-one.html": "hermes-agent-guide.jpg",
    "industrial-protocols-guide.html": "industrial-protocols-guide.jpg",
    "influxdb-guide.html": "influxdb-timeseries-guide.jpg",
    "java-nodejs-npm-guide.html": "nodejs-javascript-guide.jpg",
    "json-architecture-guide.html": "json-architecture-guide.jpg",
    "kubernetes-beginner-guide.html": "kubernetes-guide.jpg",
    "libre-hardware-monitor-guide.html": "libre-hardware-monitor-guide.jpg",
    "linux-commands.html": "linux-terminal-guide.jpg",
    "llama-cpp-gguf.html": "local-llm-inference-guide.jpg",
    "llm-naming-quantization-guide.html": "llm-quantization-guide.jpg",
    "lm-studio-local-llm.html": "local-llm-inference-guide.jpg",
    "mac-commands.html": "linux-terminal-guide.jpg",
    "microsoft-services-ecosystem.html": "microsoft-ecosystem.jpg",
    "n8n-workflow-automation.html": "workflow-automation-guide.jpg",
    "nas-storage-comparison.html": "nas-storage-guide.jpg",
    "node-js-commands.html": "nodejs-javascript-guide.jpg",
    "notion-guide.html": "notion-workspace-guide.jpg",
    "nvidia-gpu-cuda-architecture-guide.html": "nvidia-gpu-cuda-architecture-guide.jpg",
    "obsidian-guide.html": "obsidian-pkm-guide.jpg",
    "ollama-local-llm.html": "ollama-guide.jpg",
    "open-source-licenses.html": "open-source-licenses-guide.jpg",
    "openclaw-ai-assistant.html": "openclaw-agent-guide.jpg",
    "os-architecture-comparison.html": "os-diagram.jpg",
    "prompt-engineering-guide.html": "prompt-engineering-guide.jpg",
    "pyinstaller-python-packaging-guide.html": "pyinstaller-guide.jpg",
    "rag-technology-guide.html": "rag-guide.jpg",
    "react-introduction.html": "react-framework-guide.jpg",
    "rtx-spark-vs-dgx-spark-guide.html": "rtx-spark-vs-dgx-spark-guide.jpg",
    "slm-small-language-models-guide.html": "slm-guide.jpg",
    "spacex-aerospace-engineering-guide.html": "spacex-aerospace-guide.jpg",
    "storage-spec-performance-comparison.html": "storage-spec-performance-guide.jpg",
    "tesla-model-lineup-guide.html": "tesla_car_hero.jpg",
    "tesla-roadster-performance-thrust-rocket-guide.html": "tesla-roadster-trinity.jpg",
    "tmux-terminal-guide.html": "tmux-terminal-guide.jpg",
    "top-5-llms-2026.html": "frontier-llms-guide.jpg",
    "usb-history-evolution-guide.html": "usb-evolution-guide.jpg",
    "us-political-parties-presidents-guide.html": "us-political-parties-presidents-guide.jpg",
    "uv-guide.html": "python-uv-guide.jpg",
    "video-cable-display-interfaces-guide.html": "video-interfaces-guide.jpg",
    "virtual-machine-comparison.html": "virtual-machine-guide.jpg",
    "wireshark-network-analysis.html": "wireshark-packet-guide.jpg",
    "wsl-guide.html": "wsl-content.jpg",
    "zapier-make-n8n-comparison.html": "workflow-automation-guide.jpg",
}

def update_articles():
    print("Updating individual article HTML files...")
    updated_count = 0
    for filename, banner in ARTICLE_BANNER_MAP.items():
        if not os.path.exists(filename):
            continue
        
        banner_path = f"./images/{banner}"
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        soup = bs4.BeautifulSoup(content, "html.parser")
        changed = False

        # Update og:image
        og_img = soup.find("meta", property="og:image")
        if og_img and og_img.get("content") != banner_path:
            og_img["content"] = banner_path
            changed = True
        elif not og_img and soup.head:
            new_tag = soup.new_tag("meta", property="og:image", content=banner_path)
            soup.head.append(new_tag)
            changed = True

        # Update twitter:image
        tw_img = soup.find("meta", attrs={"name": "twitter:image"})
        if tw_img and tw_img.get("content") != banner_path:
            tw_img["content"] = banner_path
            changed = True
        elif not tw_img and soup.head:
            new_tag = soup.new_tag("meta", attrs={"name": "twitter:image", "content": banner_path})
            soup.head.append(new_tag)
            changed = True

        # Update hero image
        hero_wrap = soup.find("div", class_="hero-image-wrap")
        if hero_wrap:
            img = hero_wrap.find("img")
            if img and img.get("src") != banner_path:
                img["src"] = banner_path
                changed = True
        else:
            hero_sec = soup.find("section", class_="article-hero")
            if hero_sec:
                img = hero_sec.find("img")
                if img and img.get("src") != banner_path:
                    img["src"] = banner_path
                    changed = True

        # Update any remaining picsum images inside article body or sidebar
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if "picsum.photos" in src:
                # If it's a small sidebar link to another article
                parent_a = img.find_parent("a", href=True)
                if parent_a:
                    target_href = parent_a["href"].replace("./", "")
                    if target_href in ARTICLE_BANNER_MAP:
                        img["src"] = f"./images/{ARTICLE_BANNER_MAP[target_href]}"
                        changed = True
                        continue
                img["src"] = banner_path
                changed = True

        if changed:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(soup))
            updated_count += 1

    print(f"Updated {updated_count} article files.")

def update_articles_html():
    print("Updating articles.html cards...")
    if not os.path.exists("articles.html"):
        return
    with open("articles.html", "r", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f.read(), "html.parser")

    cards = soup.find_all("article", class_="article-card")
    updated = 0
    for card in cards:
        link = card.find("a", href=True)
        img = card.find("img")
        if link and img:
            href = link["href"].replace("./", "")
            if href in ARTICLE_BANNER_MAP:
                expected = f"./images/{ARTICLE_BANNER_MAP[href]}"
                if img.get("src") != expected:
                    img["src"] = expected
                    updated += 1

    with open("articles.html", "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Updated {updated} cards in articles.html")

def update_index_html():
    print("Updating index.html...")
    if not os.path.exists("index.html"):
        return
    with open("index.html", "r", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f.read(), "html.parser")

    cards = soup.find_all("article", class_="article-card")
    updated = 0
    for card in cards:
        link = card.find("a", href=True)
        img = card.find("img")
        if link and img:
            href = link["href"].replace("./", "")
            if href in ARTICLE_BANNER_MAP:
                expected = f"./images/{ARTICLE_BANNER_MAP[href]}"
                if img.get("src") != expected:
                    img["src"] = expected
                    updated += 1

    # Also update any other featured article links with images
    for a in soup.find_all("a", href=True):
        href = a["href"].replace("./", "")
        img = a.find("img")
        if href in ARTICLE_BANNER_MAP and img:
            expected = f"./images/{ARTICLE_BANNER_MAP[href]}"
            if img.get("src") != expected:
                img["src"] = expected
                updated += 1

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Updated {updated} image references in index.html")

def update_about_html():
    print("Updating about.html...")
    if not os.path.exists("about.html"):
        return
    with open("about.html", "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("https://picsum.photos/seed/megan-ai/150/150", "./images/megan.png")
    with open("about.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated about.html profile pic.")

def update_js_files():
    print("Updating js/script.js and js/enhancements.js...")
    map_str = json.dumps(ARTICLE_BANNER_MAP)

    # Update script.js
    if os.path.exists("js/script.js"):
        with open("js/script.js", "r", encoding="utf-8") as f:
            js = f.read()
        js = re.sub(r'const heroImage = \{[^}]*\};', f'const heroImage = {map_str};', js)
        with open("js/script.js", "w", encoding="utf-8") as f:
            f.write(js)
        print("Updated js/script.js")

    # Update enhancements.js
    if os.path.exists("js/enhancements.js"):
        with open("js/enhancements.js", "r", encoding="utf-8") as f:
            js = f.read()
        js = re.sub(r'var heroImageMap = \{[^}]*\};', f'var heroImageMap = {map_str};', js)
        with open("js/enhancements.js", "w", encoding="utf-8") as f:
            f.write(js)
        print("Updated js/enhancements.js")

def update_search_index():
    print("Updating search-index.json...")
    if not os.path.exists("search-index.json"):
        return
    with open("search-index.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for item in data:
        url = item.get("url", "").replace("./", "")
        if url in ARTICLE_BANNER_MAP:
            expected = f"./images/{ARTICLE_BANNER_MAP[url]}"
            if item.get("image") != expected:
                item["image"] = expected
                updated += 1

    with open("search-index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated} entries in search-index.json")

def main():
    update_articles()
    update_articles_html()
    update_index_html()
    update_about_html()
    update_js_files()
    update_search_index()
    print("Banner update complete!")

if __name__ == "__main__":
    main()
