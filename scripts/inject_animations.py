import re

css_code = """
    /* ==============================================================
       ANIMATION 1: The 270 Battleground Bar Styles
       ============================================================== */
    .battle-arena-widget {
      background: var(--bg-alt);
      border: 1.5px solid var(--border);
      border-radius: 16px;
      padding: 1.8rem;
      margin: 2.5rem 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .widget-title {
      font-size: 1.35rem;
      font-weight: 800;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .widget-desc {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-bottom: 1.2rem;
    }
    .battle-year-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
    }
    .year-chip {
      padding: 0.4rem 0.85rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .year-chip:hover {
      border-color: #3b82f6;
      color: var(--text);
      transform: translateY(-1px);
    }
    .year-chip.active {
      background: #2563eb;
      color: #fff;
      border-color: #2563eb;
      box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    }
    .battle-contestants {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.8rem;
    }
    .contestant {
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }
    .contestant-avatar {
      font-size: 2.4rem;
      line-height: 1;
      filter: drop-shadow(0 2px 8px rgba(0,0,0,0.15));
      transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .contestant.winner .contestant-avatar {
      transform: scale(1.3) translateY(-4px);
    }
    .contestant-name {
      font-size: 1.2rem;
      font-weight: 800;
    }
    .contestant-party {
      font-size: 0.82rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .party-blue-text { color: #2563eb; }
    .dark-mode .party-blue-text { color: #60a5fa; }
    .party-red-text { color: #dc2626; }
    .dark-mode .party-red-text { color: #f87171; }
    .contestant-score {
      font-family: "Fira Code", monospace;
      font-size: 1.8rem;
      font-weight: 800;
    }
    .battle-bar-outer {
      position: relative;
      height: 44px;
      border-radius: 22px;
      background: #e2e8f0;
      overflow: hidden;
      display: flex;
      box-shadow: inset 0 2px 6px rgba(0,0,0,0.12);
      border: 2px solid var(--border);
    }
    .dark-mode .battle-bar-outer {
      background: #1e293b;
    }
    .bar-segment-dem {
      height: 100%;
      background: linear-gradient(90deg, #1d4ed8, #3b82f6);
      transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      justify-content: flex-start;
      padding-left: 1rem;
      color: #fff;
      font-weight: 800;
      font-size: 0.95rem;
      white-space: nowrap;
      position: relative;
      overflow: hidden;
    }
    .bar-segment-gop {
      height: 100%;
      background: linear-gradient(90deg, #ef4444, #b91c1c);
      transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 1rem;
      color: #fff;
      font-weight: 800;
      font-size: 0.95rem;
      white-space: nowrap;
      position: relative;
      overflow: hidden;
    }
    .bar-threshold-marker {
      position: absolute;
      left: 50.18%; /* 270 / 538 */
      top: 0;
      bottom: 0;
      width: 4px;
      background: #fbbf24;
      box-shadow: 0 0 12px #fbbf24, 0 0 24px rgba(251, 191, 36, 0.8);
      z-index: 5;
      transform: translateX(-50%);
    }
    .threshold-badge {
      position: absolute;
      top: -26px;
      left: 50.18%;
      transform: translateX(-50%);
      background: #fbbf24;
      color: #78350f;
      font-size: 0.75rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      z-index: 6;
      white-space: nowrap;
    }
    .battle-result-card {
      margin-top: 1.4rem;
      padding: 1.1rem 1.4rem;
      border-radius: 10px;
      background: var(--bg);
      border: 1px solid var(--border);
      font-size: 0.95rem;
      line-height: 1.6;
    }
    .battle-result-card strong {
      color: var(--text);
    }

    /* ==============================================================
       ANIMATION 2: The Great Reversal Compass Styles
       ============================================================== */
    .compass-widget {
      background: var(--bg-alt);
      border: 1.5px solid var(--border);
      border-radius: 16px;
      padding: 1.8rem;
      margin: 2.5rem 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .compass-controls {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 1.2rem;
      margin-bottom: 1.2rem;
    }
    .compass-btn {
      padding: 0.5rem 1.2rem;
      border-radius: 9999px;
      border: 1.5px solid var(--border);
      background: var(--bg);
      color: var(--text);
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }
    .compass-btn:hover {
      border-color: #3b82f6;
      color: #2563eb;
    }
    .compass-slider-wrap {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 0.8rem;
      min-width: 250px;
    }
    .compass-slider {
      flex: 1;
      height: 6px;
      border-radius: 3px;
      accent-color: #2563eb;
      cursor: pointer;
    }
    .compass-canvas-wrap {
      position: relative;
      width: 100%;
      height: 400px;
      background: var(--bg);
      border: 1.5px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 1.2rem;
    }
    #compassCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }
    .compass-narrative {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.2rem;
      line-height: 1.65;
      font-size: 0.95rem;
    }
    .compass-narrative h4 {
      font-size: 1.15rem;
      font-weight: 800;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* ==============================================================
       ANIMATION 3: Mascot Duel & Quote Terminal Styles
       ============================================================== */
    .mascot-duel-widget {
      background: var(--bg-alt);
      border: 1.5px solid var(--border);
      border-radius: 16px;
      padding: 1.8rem;
      margin: 2.5rem 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .mascot-ring {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin: 1.5rem 0;
    }
    @media (max-width: 768px) {
      .mascot-ring { grid-template-columns: 1fr; }
    }
    .mascot-clickable-card {
      background: var(--bg);
      border: 2px solid var(--border);
      border-radius: 14px;
      padding: 1.6rem;
      text-align: center;
      cursor: pointer;
      user-select: none;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .mascot-clickable-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(0,0,0,0.08);
    }
    .mascot-clickable-card.dem:hover {
      border-color: #3b82f6;
    }
    .mascot-clickable-card.gop:hover {
      border-color: #ef4444;
    }
    .mascot-big-icon {
      font-size: 4.5rem;
      line-height: 1;
      margin-bottom: 0.8rem;
      display: inline-block;
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .mascot-title {
      font-size: 1.3rem;
      font-weight: 800;
      margin-bottom: 0.3rem;
    }
    .mascot-subtitle {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 0.8rem;
    }
    .click-prompt {
      display: inline-block;
      font-size: 0.8rem;
      font-weight: 700;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      letter-spacing: 1px;
      text-transform: uppercase;
    }
    .prompt-dem {
      background: rgba(37,99,235,0.12);
      color: #2563eb;
      border: 1px solid rgba(37,99,235,0.3);
    }
    .prompt-gop {
      background: rgba(220,38,38,0.12);
      color: #dc2626;
      border: 1px solid rgba(220,38,38,0.3);
    }

    /* Mascot Action Animations */
    .donkey-kick {
      animation: donkeyKickAnim 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes donkeyKickAnim {
      0% { transform: rotate(0deg) scale(1); }
      25% { transform: rotate(-25deg) scale(1.15) translateX(-8px); }
      50% { transform: rotate(35deg) scale(1.3) translateY(-14px) translateX(12px); }
      75% { transform: rotate(-10deg) scale(1.05); }
      100% { transform: rotate(0deg) scale(1); }
    }

    .elephant-trumpet {
      animation: elephantTrumpetAnim 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes elephantTrumpetAnim {
      0% { transform: scale(1) translateY(0); }
      25% { transform: scale(1.2) translateY(-16px) rotate(-12deg); }
      45% { transform: scale(1.35) translateY(-22px) rotate(8deg); }
      70% { transform: scale(1.1) translateY(-6px); }
      100% { transform: scale(1) translateY(0); }
    }

    /* Star Confetti Explosion Particles */
    .star-sparkle {
      position: absolute;
      pointer-events: none;
      font-size: 1.4rem;
      animation: starFloatAnim 0.8s ease-out forwards;
      z-index: 10;
    }
    @keyframes starFloatAnim {
      0% { opacity: 1; transform: translate(0, 0) scale(0.6); }
      100% { opacity: 0; transform: translate(var(--tx), var(--ty)) scale(1.4); }
    }

    /* Quote Terminal Box */
    .duel-terminal-box {
      border-radius: 12px;
      background: #090d16;
      border: 1px solid #1e293b;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(0,0,0,0.35);
      margin-top: 1rem;
    }
    .terminal-bar {
      background: #111827;
      padding: 0.6rem 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      border-bottom: 1px solid #1f2937;
    }
    .terminal-circle {
      width: 11px;
      height: 11px;
      border-radius: 50%;
    }
    .c-red { background: #ef4444; }
    .c-yellow { background: #f59e0b; }
    .c-green { background: #10b981; }
    .terminal-title-text {
      color: #94a3b8;
      font-size: 0.82rem;
      font-family: "Fira Code", monospace;
      margin-left: 0.4rem;
    }
    .terminal-content {
      padding: 1.4rem 1.6rem;
      color: #e2e8f0;
      font-family: "Fira Code", monospace;
      min-height: 115px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .terminal-speaker {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.9rem;
      color: #38bdf8;
      margin-bottom: 0.5rem;
    }
    .terminal-quote-text {
      font-size: 1.12rem;
      line-height: 1.6;
      color: #ffffff;
      font-weight: 600;
    }
    .cursor-blink {
      display: inline-block;
      width: 8px;
      height: 1.1em;
      background: #38bdf8;
      vertical-align: -2px;
      margin-left: 4px;
      animation: blink 0.9s infinite;
    }
    @keyframes blink {
      0%, 50% { opacity: 1; }
      51%, 100% { opacity: 0; }
    }
"""

html_animation_1 = """
        <!-- ANIMATION 1: The 270 Battleground Bar -->
        <div class="battle-arena-widget" id="battleground-arena">
          <div class="widget-title">🗳️ 歷屆白宮爭霸：270 票選舉人團動態拉鋸戰 (Road to 270)</div>
          <p class="widget-desc">點擊不同歷史重大轉折選舉，體驗民主黨（藍）與共和黨（紅）如何跨越 270 票黃金當選門檻！</p>
          
          <div class="battle-year-chips" id="battle-year-chips">
            <button class="year-chip" data-year="1860">1860 林肯危機</button>
            <button class="year-chip" data-year="1932">1932 羅斯福新政</button>
            <button class="year-chip" data-year="1964">1964 詹森民權勝選</button>
            <button class="year-chip" data-year="1980">1980 雷根革命</button>
            <button class="year-chip" data-year="1984">1984 雷根49州橫掃</button>
            <button class="year-chip" data-year="2000">2000 佛州極限爭議</button>
            <button class="year-chip" data-year="2008">2008 歐巴馬藍潮</button>
            <button class="year-chip" data-year="2016">2016 川普藍牆翻紅</button>
            <button class="year-chip" data-year="2020">2020 拜登勝選</button>
            <button class="year-chip active" data-year="2024">2024 川普逆轉橫掃</button>
          </div>

          <div class="battle-contestants">
            <div class="contestant" id="contestant-dem">
              <div class="contestant-avatar">🫏</div>
              <div>
                <div class="contestant-name" id="name-dem">賀錦麗</div>
                <div class="contestant-party party-blue-text">民主黨 (Dem)</div>
              </div>
            </div>
            <div style="text-align: center;">
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); letter-spacing: 1.5px;">ELECTORAL VOTES</span>
              <div style="font-family: monospace; font-size: 1.05rem; color: #fbbf24; font-weight: 800;">門檻 270 / 總計 538</div>
            </div>
            <div class="contestant" id="contestant-gop" style="flex-direction: row-reverse; text-align: right;">
              <div class="contestant-avatar winner">🐘</div>
              <div>
                <div class="contestant-name" id="name-gop">唐納·川普</div>
                <div class="contestant-party party-red-text">共和黨 (GOP)</div>
              </div>
            </div>
          </div>

          <div class="battle-bar-outer">
            <div class="threshold-badge">★ 270 當選門檻 ★</div>
            <div class="bar-threshold-marker"></div>
            <div class="bar-segment-dem" id="bar-dem" style="width: 42%;">
              <span id="score-dem">226 票</span>
            </div>
            <div class="bar-segment-gop" id="bar-gop" style="width: 58%;">
              <span id="score-gop">312 票</span>
            </div>
          </div>

          <div class="battle-result-card" id="battle-summary">
            <strong>2024 年大選回顧：</strong>唐納·川普（Donald Trump）橫掃全部 7 個關鍵搖擺州（賓州、喬治亞、北卡、密西根、威斯康辛、內華達、亞利桑那），奪下 312 張選舉人票，以絕對優勢突破 270 票門檻，擊敗賀錦麗（Kamala Harris，226 票），完成相隔 132 年後罕見的非連續隔屆重返白宮奇蹟。
          </div>
        </div>
"""

html_animation_2 = """
        <!-- ANIMATION 2: The Great Reversal Compass -->
        <div class="compass-widget" id="reversal-compass">
          <div class="widget-title">🔀 兩黨百年「意識形態大逆轉」動態政治光譜儀 (The Great Ideological Reversal)</div>
          <p class="widget-desc">點擊「▶ 自動播放軌跡」或拖曳歷史滑桿，親眼見證兩黨如何在 150 年間從經濟、種族到聯邦權限完成世紀「大交換」！</p>

          <div class="compass-controls">
            <button class="compass-btn" id="compass-play-btn">▶ 自動播放軌跡</button>
            <div class="compass-slider-wrap">
              <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-muted);">歷史時期：</span>
              <input type="range" min="0" max="4" value="0" class="compass-slider" id="compass-slider" />
              <strong id="slider-era-label" style="min-width: 140px; font-size: 0.95rem; color: #2563eb;">1854 內戰建黨</strong>
            </div>
          </div>

          <div class="compass-canvas-wrap">
            <canvas id="compassCanvas" width="800" height="400"></canvas>
          </div>

          <div class="compass-narrative" id="compass-narrative">
            <h4 id="narrative-title">🏛️ 1854–1865 創黨與內戰：聯邦至上 vs 南方州權</h4>
            <p id="narrative-body">共和黨誕生於反奴隸制擴張運動，堅決維護聯邦統一、主張北方工業發展與聯邦關稅；當時的民主黨由南方蓄奴種族主義白人主導，狂熱捍衛各州自主（States' Rights）與農業經濟。</p>
          </div>
        </div>
"""

html_animation_3 = """
        <!-- ANIMATION 3: Mascot Duel & Quote Terminal -->
        <div class="mascot-duel-widget">
          <div class="widget-title">🫏🐘 驢象榮耀對決：點擊吉祥物觸發戰鬥動態與經典金句</div>
          <p class="widget-desc">點擊左側民主黨「藍色戰驢」或右側共和黨「紅色戰象」，觸發踢蹄/鳴鼻戰鬥動畫，並由歷史終端機為你輸出歷任總統劃時代名言！</p>

          <div class="mascot-ring">
            <div class="mascot-clickable-card dem" id="mascot-dem-card">
              <div class="mascot-big-icon" id="donkey-icon">🫏</div>
              <div class="mascot-title party-blue-text">民主黨戰驢 (The Donkey)</div>
              <div class="mascot-subtitle">堅毅、平民普選、社會福利與民權捍衛</div>
              <span class="click-prompt prompt-dem">點擊發動踢蹄戰鬥 ✦</span>
            </div>

            <div class="mascot-clickable-card gop" id="mascot-gop-card">
              <div class="mascot-big-icon" id="elephant-icon">🐘</div>
              <div class="mascot-title party-red-text">共和黨戰象 (The Elephant)</div>
              <div class="mascot-subtitle">穩健、雄厚力量、自由市場與主權保守</div>
              <span class="click-prompt prompt-gop">點擊發動象鼻長鳴 ★</span>
            </div>
          </div>

          <!-- Quote Terminal Box -->
          <div class="duel-terminal-box">
            <div class="terminal-bar">
              <span class="terminal-circle c-red"></span>
              <span class="terminal-circle c-yellow"></span>
              <span class="terminal-circle c-green"></span>
              <span class="terminal-title-text">whitehouse-historical-quotes.sh — bash — 80x24</span>
            </div>
            <div class="terminal-content">
              <div class="terminal-speaker" id="quote-speaker">💡 點擊上方驢子或大象吉祥物，召喚跨時代總統歷史金句！</div>
              <div class="terminal-quote-text">
                <span id="quote-text">"Talk is cheap. Show me the code... and the vote."</span>
                <span class="cursor-blink"></span>
              </div>
            </div>
          </div>
        </div>
"""

js_code = """
    /* ==============================================================
       JAVASCRIPT: 3 NEW DYNAMIC ANIMATIONS LOGIC
       ============================================================== */
    
    // --- 1. Battleground 270 Bar Data & Logic ---
    const electionsData = {
      "1860": {
        dem: { name: "史蒂芬·道格拉斯 / 民主分裂", score: 84 },
        gop: { name: "亞伯拉罕·林肯 (勝)", score: 180 },
        total: 303,
        threshold: 152,
        winner: "gop",
        summary: "<strong>1860 年南北內戰危機：</strong>共和黨候選人林肯在普選票僅獲 39.8% 的情況下，包攬北部所有自由州，在 303 張選舉人票中斬獲 180 票成功過半（當時門檻 152 票）。民主黨因南北蓄奴爭議分裂出三組候選人慘敗，直接引爆南方 11 州脫離聯邦與南北戰爭。"
      },
      "1932": {
        dem: { name: "富蘭克林·D·羅斯福 (勝)", score: 472 },
        gop: { name: "赫伯特·胡佛", score: 59 },
        total: 531,
        threshold: 266,
        winner: "dem",
        summary: "<strong>1932 年大蕭條新政海嘯：</strong>富蘭克林·羅斯福以推行「新政（New Deal）」對抗經濟崩盤為號召，橫掃 42 個州奪下 472 張選舉人票，將現任共和黨總統胡佛（僅 59 票）擊潰，開創了長達三十餘年的民主黨新政聯盟統治時代。"
      },
      "1964": {
        dem: { name: "林登·B·詹森 (勝)", score: 486 },
        gop: { name: "貝利·高華德", score: 52 },
        total: 538,
        threshold: 270,
        winner: "dem",
        summary: "<strong>1964 年民權時代壓倒性大勝：</strong>甘迺迪遇刺後，林登·詹森簽署 1964《民權法案》並以 486 票狂勝強硬保守派高華德（52 票）。然而高華德奪得南方深南五州，敲響了傳統南方白人民主黨「堅固南方」崩解轉向共和黨的歷史前奏。"
      },
      "1980": {
        dem: { name: "吉米·卡特", score: 49 },
        gop: { name: "隆納·雷根 (勝)", score: 489 },
        total: 538,
        threshold: 270,
        winner: "gop",
        summary: "<strong>1980 年雷根保守主義革命：</strong>面對停滯性通膨與伊朗人質危機，雷根以「供給面減稅與強大國防」橫掃 44 州狂攬 489 票，擊敗現任總統卡特（僅 49 票），正式確立了現代美國保守主義共和黨的主導地位。"
      },
      "1984": {
        dem: { name: "沃爾特·蒙代爾", score: 13 },
        gop: { name: "隆納·雷根 (勝)", score: 525 },
        total: 538,
        threshold: 270,
        winner: "gop",
        summary: "<strong>1984 年雷根 49 州史詩級橫掃：</strong>雷根創下美國歷史上第二高的選舉人票紀錄（525 票，奪下 49 個州），民主黨蒙代爾僅拿下家鄉明尼蘇達州與華盛頓特區（13 票），成為現代總統選舉中最懸殊的勝利之一。"
      },
      "2000": {
        dem: { name: "艾爾·高爾", score: 266 },
        gop: { name: "喬治·W·布希 (勝)", score: 271 },
        total: 538,
        threshold: 270,
        winner: "gop",
        summary: "<strong>2000 年佛羅里達 537 票世紀大戰：</strong>高爾雖在全國普選票領先 54 萬票，但佛州選情陷入 537 票極限撕裂。歷經 36 天重新計票與最高法院判決（Bush v. Gore），小布希以 271 票（僅超門檻 1 票）險勝高爾的 266 票入主白宮。"
      },
      "2008": {
        dem: { name: "巴拉克·歐巴馬 (勝)", score: 365 },
        gop: { name: "約翰·麥肯", score: 173 },
        total: 538,
        threshold: 270,
        winner: "dem",
        summary: "<strong>2008 年首位非裔總統誕生：</strong>歐巴馬乘著「改變（Hope & Change）」與反對次貸金融海嘯之勢，翻轉維吉尼亞、佛州、俄亥俄與印第安納等紅州，以 365 票對 173 票大勝麥肯，締造歷史性藍潮。"
      },
      "2016": {
        dem: { name: "希拉蕊·柯林頓", score: 227 },
        gop: { name: "唐納·川普 (勝)", score: 304 },
        total: 538,
        threshold: 270,
        winner: "gop",
        summary: "<strong>2016 年川普撕裂「鐵鏽帶藍牆」：</strong>川普主打「美國優先（America First）」與反全球化關稅，以些微差距擊穿民主黨數十年鐵壁賓州、密西根與威斯康辛，以 304 票突破 270 門檻戰勝希拉蕊（227 票），震驚全球政壇。"
      },
      "2020": {
        dem: { name: "喬·拜登 (勝)", score: 306 },
        gop: { name: "唐納·川普", score: 232 },
        total: 538,
        threshold: 270,
        winner: "dem",
        summary: "<strong>2020 年歷史最高投票率對決：</strong>在疫情與郵寄選票浪潮下，拜登奪得創紀錄的 8128 萬普選票，並重新奪回鐵鏽帶三州以及歷史性翻轉喬治亞與亞利桑那，以 306 票對 232 票擊敗川普。"
      },
      "2024": {
        dem: { name: "賀錦麗", score: 226 },
        gop: { name: "唐納·川普 (勝)", score: 312 },
        total: 538,
        threshold: 270,
        winner: "gop",
        summary: "<strong>2024 年川普逆轉橫掃七大戰場州：</strong>川普囊括全部 7 個關鍵搖擺州（賓州、喬治亞、北卡、密西根、威斯康辛、內華達、亞利桑那），並一舉拿下全國普選票多數，奪下 312 張選舉人票大勝賀錦麗（226 票），成為 132 年來首位隔屆重返白宮之總統。"
      }
    };

    function updateBattleground(year) {
      const data = electionsData[year];
      if (!data) return;

      document.getElementById("name-dem").textContent = data.dem.name;
      document.getElementById("name-gop").textContent = data.gop.name;
      document.getElementById("score-dem").textContent = `${data.dem.score} 票`;
      document.getElementById("score-gop").textContent = `${data.gop.score} 票`;

      const demPct = Math.round((data.dem.score / data.total) * 100);
      const gopPct = 100 - demPct;

      document.getElementById("bar-dem").style.width = demPct + "%";
      document.getElementById("bar-gop").style.width = gopPct + "%";

      const cDem = document.getElementById("contestant-dem");
      const cGop = document.getElementById("contestant-gop");
      if (data.winner === "dem") {
        cDem.classList.add("winner");
        cGop.classList.remove("winner");
      } else {
        cGop.classList.add("winner");
        cDem.classList.remove("winner");
      }

      document.getElementById("battle-summary").innerHTML = data.summary;
    }

    document.querySelectorAll("#battle-year-chips .year-chip").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("#battle-year-chips .year-chip").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        updateBattleground(btn.getAttribute("data-year"));
      });
    });

    // --- 2. Ideological Reversal Compass Canvas Animation ---
    const compassEras = [
      {
        year: "1854",
        label: "1854 內戰建黨",
        title: "🏛️ 1854–1865 創黨與內戰：聯邦至上 vs 南方州權",
        body: "共和黨誕生於反奴隸制擴張運動，堅決維護聯邦統一、主張北方工業發展與聯邦關稅；當時的民主黨由南方蓄奴種族主義白人主導，狂熱捍衛各州自主（States' Rights）與農業經濟。",
        dem: { x: -0.2, y: -0.7 },
        gop: { x: 0.35, y: 0.75 }
      },
      {
        year: "1896",
        label: "1896 鍍金進步時代",
        title: "🏭 1896–1920 鍍金時代與進步浪潮：工商業資本 vs 庶民平民黨",
        body: "麥金利與老羅斯福時期的共和黨成為現代自由市場、企業資本與金本位代表；民主黨吸納平民黨人（William Jennings Bryan），開始主張反壟斷與農民勞工平民權益。",
        dem: { x: -0.45, y: -0.2 },
        gop: { x: 0.75, y: 0.25 }
      },
      {
        year: "1932",
        label: "1932 羅斯福新政",
        title: "🌊 1932–1945 大蕭條新政大位移：福利國家凱因斯主義誕生",
        body: "小羅斯福推動龐大『新政（New Deal）』，民主黨大步跨入大政府集權與社會福利網，形成現代自由派大本營；共和黨退守捍衛自由放任市場原則，反對聯邦過度干預。",
        dem: { x: -0.75, y: 0.65 },
        gop: { x: 0.75, y: -0.15 }
      },
      {
        year: "1964",
        label: "1964 民權與南方策略",
        title: "⚖️ 1964–1980 民權法案與雷根革命：政黨版圖徹底翻轉",
        body: "詹森簽署《民權法案》，民主黨正式成為少數族裔平權先驅，南方保守白人出走；尼克森以南方策略整合，雷根推行小政府低稅與基督教保守主義，兩黨位置徹底互換！",
        dem: { x: -0.7, y: 0.7 },
        gop: { x: 0.7, y: -0.55 }
      },
      {
        year: "2025",
        label: "2025 現代民粹文化戰",
        title: "🌐 2016–2025 現代極化格局：進步多元文化 vs 美國優先勞工民粹",
        body: "民主黨由沿海都會、大學學歷與多元文化進步派主導，強調全球氣候與社會正義；共和黨演變為鐵鏽帶藍領、鄉村選民與反建制愛國保守民粹（MAGA），兩黨大交換完全確立。",
        dem: { x: -0.85, y: 0.75 },
        gop: { x: 0.65, y: -0.75 }
      }
    ];

    let currentCompassIndex = 0;
    let animCompassProgress = 0;
    let isPlayingCompass = false;
    let compassTimer = null;

    const compassCanvas = document.getElementById("compassCanvas");
    const ctx = compassCanvas ? compassCanvas.getContext("2d") : null;

    function renderCompass(index, progress) {
      if (!ctx || !compassCanvas) return;
      const w = compassCanvas.width;
      const h = compassCanvas.height;
      const isDark = document.documentElement.classList.contains("dark-mode");

      ctx.clearRect(0, 0, w, h);

      const cx = w / 2;
      const cy = h / 2;

      // Background Grid
      ctx.strokeStyle = isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)";
      ctx.lineWidth = 1;
      const step = 40;
      for (let x = 0; x < w; x += step) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
      }
      for (let y = 0; y < h; y += step) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
      }

      // Main Axes
      ctx.strokeStyle = isDark ? "rgba(255,255,255,0.3)" : "rgba(0,0,0,0.3)";
      ctx.lineWidth = 2;
      // X Axis
      ctx.beginPath(); ctx.moveTo(40, cy); ctx.lineTo(w - 40, cy); ctx.stroke();
      // Y Axis
      ctx.beginPath(); ctx.moveTo(cx, 30); ctx.lineTo(cx, h - 30); ctx.stroke();

      // Axis Labels
      ctx.fillStyle = isDark ? "#94a3b8" : "#64748b";
      ctx.font = "bold 12px -apple-system, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("▲ 強大聯邦統一管轄 (Strong Federal Power)", cx, 20);
      ctx.fillText("▼ 地方州權至上 / 分權 (States' Rights / Decentralization)", cx, h - 10);

      ctx.textAlign = "left";
      ctx.fillText("◀ 大政府福利 / 經濟干預 (Liberal / Welfare)", 45, cy - 10);
      ctx.textAlign = "right";
      ctx.fillText("自由放任 / 小政府低稅 (Free Market / Laissez-faire) ▶", w - 45, cy - 10);

      // Interpolate coordinates
      const fromEra = compassEras[index];
      const toEra = compassEras[Math.min(index + 1, compassEras.length - 1)];

      const t = progress;
      const curDem = {
        x: fromEra.dem.x + (toEra.dem.x - fromEra.dem.x) * t,
        y: fromEra.dem.y + (toEra.dem.y - fromEra.dem.y) * t
      };
      const curGop = {
        x: fromEra.gop.x + (toEra.gop.x - fromEra.gop.x) * t,
        y: fromEra.gop.y + (toEra.gop.y - fromEra.gop.y) * t
      };

      const scaleX = (w - 120) / 2;
      const scaleY = (h - 90) / 2;

      // Draw Trails
      function drawTrail(color, key, upToIndex) {
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        for (let i = 0; i <= upToIndex; i++) {
          const pt = compassEras[i][key];
          const px = cx + pt.x * scaleX;
          const py = cy - pt.y * scaleY;
          if (i === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.setLineDash([]);
      }

      drawTrail("rgba(59, 130, 246, 0.4)", "dem", index);
      drawTrail("rgba(239, 68, 68, 0.4)", "gop", index);

      // Draw Historical Milestone Dots
      for (let i = 0; i < compassEras.length; i++) {
        const dPt = compassEras[i].dem;
        const gPt = compassEras[i].gop;
        const dx = cx + dPt.x * scaleX;
        const dy = cy - dPt.y * scaleY;
        const gx = cx + gPt.x * scaleX;
        const gy = cy - gPt.y * scaleY;

        ctx.fillStyle = i <= index ? "#2563eb" : "rgba(37, 99, 235, 0.25)";
        ctx.beginPath(); ctx.arc(dx, dy, 4, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = i <= index ? "#dc2626" : "rgba(220, 38, 38, 0.25)";
        ctx.beginPath(); ctx.arc(gx, gy, 4, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = isDark ? "#94a3b8" : "#64748b";
        ctx.font = "10px monospace";
        ctx.fillText(compassEras[i].year, dx, dy + 15);
        ctx.fillText(compassEras[i].year, gx, gy + 15);
      }

      // Draw Current Glowing Orbs
      const curDemX = cx + curDem.x * scaleX;
      const curDemY = cy - curDem.y * scaleY;
      const curGopX = cx + curGop.x * scaleX;
      const curGopY = cy - curGop.y * scaleY;

      // Dem Orb
      ctx.shadowColor = "#3b82f6";
      ctx.shadowBlur = 18;
      ctx.fillStyle = "#2563eb";
      ctx.beginPath(); ctx.arc(curDemX, curDemY, 14, 0, Math.PI * 2); ctx.fill();
      ctx.shadowBlur = 0;
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 14px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("🫏", curDemX, curDemY);

      // Gop Orb
      ctx.shadowColor = "#ef4444";
      ctx.shadowBlur = 18;
      ctx.fillStyle = "#dc2626";
      ctx.beginPath(); ctx.arc(curGopX, curGopY, 14, 0, Math.PI * 2); ctx.fill();
      ctx.shadowBlur = 0;
      ctx.fillStyle = "#ffffff";
      ctx.fillText("🐘", curGopX, curGopY);
    }

    function setCompassEra(index) {
      currentCompassIndex = index;
      renderCompass(index, 0);
      const era = compassEras[index];
      document.getElementById("slider-era-label").textContent = era.label;
      document.getElementById("narrative-title").textContent = era.title;
      document.getElementById("narrative-body").textContent = era.body;
      const slider = document.getElementById("compass-slider");
      if (slider) slider.value = index;
    }

    const sliderEl = document.getElementById("compass-slider");
    if (sliderEl) {
      sliderEl.addEventListener("input", (e) => {
        setCompassEra(parseInt(e.target.value));
      });
    }

    const playBtnEl = document.getElementById("compass-play-btn");
    if (playBtnEl) {
      playBtnEl.addEventListener("click", () => {
        if (isPlayingCompass) {
          isPlayingCompass = false;
          playBtnEl.textContent = "▶ 自動播放軌跡";
          cancelAnimationFrame(compassTimer);
        } else {
          isPlayingCompass = true;
          playBtnEl.textContent = "⏸ 暫停播放";
          animateCompass();
        }
      });
    }

    function animateCompass() {
      if (!isPlayingCompass) return;
      animCompassProgress += 0.015;
      if (animCompassProgress >= 1) {
        animCompassProgress = 0;
        currentCompassIndex++;
        if (currentCompassIndex >= compassEras.length - 1) {
          currentCompassIndex = 0;
        }
        setCompassEra(currentCompassIndex);
      } else {
        renderCompass(currentCompassIndex, animCompassProgress);
      }
      compassTimer = requestAnimationFrame(animateCompass);
    }

    // Initialize compass
    renderCompass(0, 0);

    // --- 3. Mascot Duel & Typewriter Logic ---
    const quotesLibrary = {
      dem: [
        { speaker: "富蘭克林·D·羅斯福 (第 32 任總統 · 1933)", text: "我們唯一要恐懼的就是恐懼本身。— The only thing we have to fear is fear itself." },
        { speaker: "約翰·F·甘迺迪 (第 35 任總統 · 1961)", text: "不要問國家能為你做什麼，問你能為國家做什麼。— Ask not what your country can do for you, ask what you can do for your country." },
        { speaker: "林登·B·詹森 (第 36 任總統 · 1965)", text: "我們必將戰勝偏見。一個偉大的國家不該忽視它的人民。— We shall overcome." },
        { speaker: "巴拉克·歐巴馬 (第 44 任總統 · 2008)", text: "改變不會在等待中發生，我們就是我們一直在等待的改變！— Yes We Can." }
      ],
      gop: [
        { speaker: "亞伯拉罕·林肯 (第 16 任總統 · 1863)", text: "民有、民治、民享之政府，當免於在地球上凋零。— Government of the people, by the people, for the people, shall not perish from the earth." },
        { speaker: "狄奧多·羅斯福 (第 26 任總統 · 1901)", text: "溫言在口，巨棒在手，你必能走得深遠。— Speak softly and carry a big stick; you will go far." },
        { speaker: "隆納·雷根 (第 40 任總統 · 1987)", text: "戈巴契夫先生，推倒這座牆吧！— Mr. Gorbachev, tear down this wall!" },
        { speaker: "唐納·川普 (第 45 & 47 任總統 · 2016)", text: "讓美國再次偉大！我們將建造、創造並贏得勝利。— Make America Great Again." }
      ]
    };

    let demQuoteIndex = 0;
    let gopQuoteIndex = 0;
    let typewriterTimer = null;

    function typeWriter(speaker, text) {
      const spEl = document.getElementById("quote-speaker");
      const txtEl = document.getElementById("quote-text");
      if (!spEl || !txtEl) return;

      clearTimeout(typewriterTimer);
      spEl.textContent = `🎙️ ${speaker}`;
      txtEl.textContent = "";

      let charIndex = 0;
      function addChar() {
        if (charIndex < text.length) {
          txtEl.textContent += text.charAt(charIndex);
          charIndex++;
          typewriterTimer = setTimeout(addChar, 25);
        }
      }
      addChar();
    }

    function createSparkles(card, isDem) {
      const symbols = isDem ? ["✦", "★", "🫏", "🔹"] : ["★", "✦", "🐘", "🔺"];
      for (let i = 0; i < 7; i++) {
        const star = document.createElement("span");
        star.className = "star-sparkle";
        star.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        star.style.left = `${50 + (Math.random() - 0.5) * 40}%`;
        star.style.top = `${40 + (Math.random() - 0.5) * 30}%`;
        star.style.setProperty("--tx", `${(Math.random() - 0.5) * 160}px`);
        star.style.setProperty("--ty", `${-60 - Math.random() * 80}px`);
        star.style.color = isDem ? "#60a5fa" : "#f87171";
        card.appendChild(star);
        setTimeout(() => star.remove(), 800);
      }
    }

    const donkeyCard = document.getElementById("mascot-dem-card");
    const donkeyIcon = document.getElementById("donkey-icon");
    if (donkeyCard && donkeyIcon) {
      donkeyCard.addEventListener("click", () => {
        donkeyIcon.classList.remove("donkey-kick");
        void donkeyIcon.offsetWidth;
        donkeyIcon.classList.add("donkey-kick");
        createSparkles(donkeyCard, true);

        const q = quotesLibrary.dem[demQuoteIndex];
        demQuoteIndex = (demQuoteIndex + 1) % quotesLibrary.dem.length;
        typeWriter(q.speaker, q.text);
      });
    }

    const elephantCard = document.getElementById("mascot-gop-card");
    const elephantIcon = document.getElementById("elephant-icon");
    if (elephantCard && elephantIcon) {
      elephantCard.addEventListener("click", () => {
        elephantIcon.classList.remove("elephant-trumpet");
        void elephantIcon.offsetWidth;
        elephantIcon.classList.add("elephant-trumpet");
        createSparkles(elephantCard, false);

        const q = quotesLibrary.gop[gopQuoteIndex];
        gopQuoteIndex = (gopQuoteIndex + 1) % quotesLibrary.gop.length;
        typeWriter(q.speaker, q.text);
      });
    }
"""

with open("us-political-parties-presidents-guide.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject CSS before </style>
if "ANIMATION 1: The 270 Battleground Bar Styles" not in content:
    content = content.replace("  </style>", css_code + "\n  </style>")

# 2. Inject Animation 1 (270 Bar) right after Electoral College bullet point
if 'id="battleground-arena"' not in content:
    content = re.sub(
        r"(全州贏者通吃制。第三黨即使在全國拿下.*?<\/li>\s*<\/ul>)",
        r"\1\n" + html_animation_1,
        content,
        flags=re.DOTALL
    )

# 3. Inject Animation 2 (Reversal Compass) right before Section 4
if 'id="reversal-compass"' not in content:
    target_s4 = "<!-- Section 4 -->"
    content = content.replace(target_s4, html_animation_2 + "\n\n        " + target_s4)

# 4. Inject Animation 3 (Mascot Duel & Quote Terminal) right before Section 5
if 'class="mascot-duel-widget"' not in content:
    content = re.sub(
        r"(<!-- Section 5 -->)",
        html_animation_3 + "\n\n        \\1",
        content
    )

# 5. Inject JS logic before </script> at the end
if "JAVASCRIPT: 3 NEW DYNAMIC ANIMATIONS LOGIC" not in content:
    content = content.replace("    });\n  </script>", "    });\n" + js_code + "\n  </script>")

with open("us-political-parties-presidents-guide.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected all 3 animations successfully!")
