// ==UserScript==
// @name        Export Chat/Gemini/Grok conversations as Markdown
// @namespace   4e6166697a
// @version     1.0.6
// @description Export chat history from ChatGPT / Gemini / Grok sites to Markdown.
// @include     *://chatgpt.com/*
// @include     *://grok.com/*
// @include     *://gemini.google.com/*
// @run-at      document-idle
// @grant       GM_addStyle
// @noframes
// @license     MIT
// ==/UserScript==

(function () {
  'use strict';

  /* --------------------- Small helper utilities --------------------- */
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => Array.from(root.querySelectorAll(s));

  function addStyle(css) { try { GM_addStyle(css); } catch (e) { const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); } }

  function sanitizeFilename(name = '') {
    const illegal = /[\/\\\?\%\*\:\|"<>\.]/g;
    const control = /[\x00-\x1f\x80-\x9f]/g;
    name = String(name || 'chat_export').replace(illegal, '_').replace(control, '_').trim();
    if (!name) name = 'chat_export';
    // windows reserved names
    if (/^(con|prn|aux|nul|com[1-9]|lpt[1-9])$/i.test(name)) name = `file_${name}`;
    return name;
  }

  function downloadText(data, filename) {
    const blob = new Blob([data], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 500);
  }

  /* --------------------- HTML -> Markdown (minimal, robust) --------------------- */
  function htmlToMarkdown(html, platform) {
    // Use a document fragment to parse and manipulate safely
    const parser = new DOMParser();
    const doc = parser.parseFromString(`<div id="md-root">${html}</div>`, 'text/html');
    const root = doc.getElementById('md-root');

    // Remove katex visual-only nodes that can pollute export
    root.querySelectorAll('span.katex-html, mrow, annotation[encoding="application/x-tex"]').forEach(n => {
      // For TeX annotations, convert to inline/delimited latex where reasonable
      if (n.tagName.toLowerCase() === 'annotation' && n.getAttribute('encoding') === 'application/x-tex') {
        const latex = n.textContent.trim();
        const container = n.closest('.katex-display') ? `\n\n$$\n${latex}\n$$\n\n` : `$${latex}$`;
        const repl = doc.createTextNode(container);
        n.parentNode.replaceChild(repl, n);
      } else n.remove();
    });

    // Convert common elements to markdown-friendly text nodes
    // bold
    root.querySelectorAll('strong, b').forEach(el => {
      el.replaceWith(doc.createTextNode(`**${el.textContent}**`));
    });
    // italic
    root.querySelectorAll('i, em').forEach(el => {
      el.replaceWith(doc.createTextNode(`*${el.textContent}*`));
    });
    // links
    root.querySelectorAll('a').forEach(a => {
      const txt = a.textContent.trim() || a.href;
      a.replaceWith(doc.createTextNode(`[${txt}](${a.href})`));
    });
    // images
    root.querySelectorAll('img').forEach(img => {
      const alt = img.alt || '';
      a = doc.createTextNode(`![${alt}](${img.src})`);
      img.replaceWith(a);
    });
    // code blocks and inline code
    // Different platforms structure code differently; handle common cases
    // 1) <pre> blocks
    root.querySelectorAll('pre').forEach(pre => {
      // try to detect language label inside
      const code = pre.textContent.replace(/\u00A0/g, ' ').trim();
      pre.replaceWith(doc.createTextNode(`\n\n\`\`\`\n${code}\n\`\`\`\n\n`));
    });
    // 2) inline code elements
    root.querySelectorAll('code').forEach(code => {
      // leave block-level code (we already handled pre), here inline
      if (code.closest('pre')) return;
      code.replaceWith(doc.createTextNode(`\`${code.textContent}\``));
    });
    // lists
    root.querySelectorAll('ul').forEach(ul => {
      const lines = Array.from(ul.children).map(li => `- ${li.textContent.trim()}`).join('\n');
      ul.replaceWith(doc.createTextNode(`\n${lines}\n`));
    });
    root.querySelectorAll('ol').forEach(ol => {
      const lines = Array.from(ol.children).map((li, i) => `${i + 1}. ${li.textContent.trim()}`).join('\n');
      ol.replaceWith(doc.createTextNode(`\n${lines}\n`));
    });
    // headings
    for (let i = 1; i <= 6; i++) {
      root.querySelectorAll(`h${i}`).forEach(h => {
        h.replaceWith(doc.createTextNode(`\n\n${'#'.repeat(i)} ${h.textContent}\n\n`));
      });
    }
    // paragraphs
    root.querySelectorAll('p').forEach(p => {
      p.replaceWith(doc.createTextNode(`\n${p.textContent}\n`));
    });
    // tables (basic)
    root.querySelectorAll('table').forEach(table => {
      const rows = [];
      const ths = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
      if (ths.length) {
        rows.push(`| ${ths.join(' | ')} |`);
        rows.push(`| ${ths.map(() => '---').join(' | ')} |`);
      }
      table.querySelectorAll('tbody tr, tr').forEach(tr => {
        const cols = Array.from(tr.children).map(td => td.textContent.trim());
        if (cols.length) rows.push(`| ${cols.join(' | ')} |`);
      });
      table.replaceWith(doc.createTextNode(`\n${rows.join('\n')}\n`));
    });

    // finally, extract plain text (innerText is safer than innerHTML stripping tags)
    const markdown = root.innerText
      // normalize some characters
      .replace(/\u00A0/g, ' ')
      .replace(/\r\n/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();

    return markdown;
  }

  /* --------------------- Platform-specific conversation extraction --------------------- */
  function getConversationElements() {
    const url = location.href;
    if (url.includes('grok.com')) {
      // Grok: message bubbles
      const elems = $$('div.message-bubble');
      return { platform: 'grok', elements: elems, title: document.title };
    } else if (url.includes('gemini.google.com')) {
      // Gemini: pair user-query-content + model-response
      const userQs = Array.from(document.querySelectorAll('user-query-content'));
      const responses = Array.from(document.querySelectorAll('model-response'));
      const sequence = [];
      for (let i = 0; i < Math.max(userQs.length, responses.length); i++) {
        if (userQs[i]) sequence.push(userQs[i]);
        if (responses[i]) sequence.push(responses[i]);
      }
      return { platform: 'gemini', elements: sequence, title: document.title };
    } else {
      // assume ChatGPT / OpenAI web
      // Query all messages that have a data-message-id attribute or other common markers
      const messages = Array.from(document.querySelectorAll('div[data-message-id], div.message, div.chat-line')).filter(Boolean);
      // fallback: pick chat container messages
      if (!messages.length) {
        const cm = document.querySelector('main') || document.body;
        messages.push(...Array.from(cm.querySelectorAll('div')).slice(0, 0)); // empty fallback (no-op)
      }
      return { platform: 'chatGPT', elements: messages, title: (document.querySelector('#history a[data-active]')?.textContent || document.title) };
    }
  }

  /* --------------------- Build export content and trigger download --------------------- */
  function exportChatAsMarkdown() {
    const { platform, elements, title } = getConversationElements();
    if (!elements || elements.length === 0) {
      alert('No conversation elements found on this page.');
      return;
    }

    // Build Q/A pairs: try to interpret every pair as (user, assistant)
    let markdown = `# Exported conversation\n\n`;
    // For Gemini the elements are paired already; for others we attempt pairing by index
    for (let i = 0; i < elements.length; i += 2) {
      const userEl = elements[i];
      const assistantEl = elements[i + 1];
      if (!userEl || !assistantEl) break;

      const userText = htmlToMarkdown(userEl.innerHTML || userEl.textContent || '', platform);
      const assistantText = htmlToMarkdown(assistantEl.innerHTML || assistantEl.textContent || '', platform);

      markdown += `## Q:\n${userText}\n\n## A:\n${assistantText}\n\n---\n\n`;
    }

    // fallback: if we built nothing using pairs, try sequential export
    if (!/## Q:/.test(markdown)) {
      markdown = elements.map((el, idx) => {
        const role = (idx % 2 === 0) ? 'User' : 'Assistant';
        return `### ${role}:\n${htmlToMarkdown(el.innerHTML || el.textContent || '', platform)}`;
      }).join('\n\n---\n\n');
    }

    const filename = sanitizeFilename(title || document.title || 'chat_export') + '.md';
    downloadText(markdown, filename);
  }

  /* --------------------- UI: a small floating button --------------------- */
  const CSS = `
  .md-export-btn {
    position: fixed;
    top: 12px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2147483647;
    background: #0b63d6;
    color: #fff;
    border-radius: 28px;
    padding: 6px 12px;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    user-select: none;
  }
  .md-export-btn:active { transform: translateX(-50%) scale(0.98); }
  `;
  addStyle(CSS);

  function createButton() {
    const btn = document.createElement('div');
    btn.className = 'md-export-btn';
    btn.textContent = 'Export MD';
    btn.title = 'Export conversation as Markdown';
    btn.onclick = exportChatAsMarkdown;
    document.body.appendChild(btn);
    return btn;
  }

  /* --------------------- Start --------------------- */
  // Wait until DOM is ready; run only once
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    createButton();
  } else {
    window.addEventListener('DOMContentLoaded', createButton, { once: true });
  }

})();
