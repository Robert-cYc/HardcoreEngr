<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html>
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> — RSS Feed</title>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #0f1117;
            color: #e6e6e6;
            line-height: 1.7;
            font-size: 1.1rem;
          }
          .container { max-width: 720px; margin: 0 auto; padding: 3rem 1.5rem; }
          h1 {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #fff;
          }
          .description { color: #888; margin-bottom: 1.5rem; font-size: 1rem; }
          .meta { color: #666; font-size: 0.85rem; margin-bottom: 2rem; }
          .meta a { color: #888; text-decoration: none; }
          .meta a:hover { text-decoration: underline; }
          h2 {
            font-size: 1.2rem;
            font-weight: 600;
            margin: 1.5rem 0 0.5rem;
          }
          h2 a {
            color: #fff;
            text-decoration: none;
            display: block;
          }
          h2 a:hover { text-decoration: underline; }
          .item-description {
            color: #aaa;
            margin-bottom: 0.3rem;
          }
          .item-meta {
            display: flex;
            gap: 0.75rem;
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 1.5rem;
          }
          .item-meta a { color: #888; text-decoration: none; }
          .item-meta a:hover { text-decoration: underline; }
          .footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #2a2d3a;
            color: #555;
            font-size: 0.85rem;
            text-align: center;
          }
          .rss-icon {
            display: inline-block;
            width: 24px;
            height: 24px;
            border: 2px solid #e6e6e6;
            border-radius: 50%;
            margin-right: 0.5rem;
            vertical-align: middle;
          }
          .rss-icon::after {
            content: "";
            position: absolute;
            width: 12px;
            height: 12px;
            border: 2px solid #e6e6e6;
            border-radius: 50%;
            margin: 4px 0 0 4px;
          }
        </style>
        <link rel="icon" href="data:,🎯"/>
      </head>
      <body>
        <div class="container">
          <h1><span class="rss-icon"></span><xsl:value-of select="/rss/channel/title"/></h1>
          <p class="description"><xsl:value-of select="/rss/channel/description"/></p>
          <div class="meta">
            <xsl:if test="/rss/channel/link">
              Website: <a href="{/rss/channel/link}"><xsl:value-of select="/rss/channel/link"/></a>
            </xsl:if>
            <xsl:if test="/rss/channel/language">
              · Language: <xsl:value-of select="/rss/channel/language"/>
            </xsl:if>
          </div>

          <xsl:for-each select="/rss/channel/item">
            <div>
              <h2>
                <a href="{link}"><xsl:value-of select="title"/></a>
              </h2>
              <p class="item-description"><xsl:value-of select="description"/></p>
              <div class="item-meta">
                <span><xsl:value-of select="pubDate"/></span>
                <span>·</span>
                <a href="{link}">閱讀文章 →</a>
              </div>
            </div>
          </xsl:for-each>

          <div class="footer">
            © 2026 "&quot;AI&quot;" 硬核工程師 · Talk is cheap. Show me the code.
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
