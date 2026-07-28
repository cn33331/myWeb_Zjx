import { marked } from 'marked';
import hljs from 'highlight.js';
import DOMPurify from 'dompurify';
import katex from 'katex';

// 配置 marked
marked.setOptions({
  gfm: true,
  breaks: true,
  highlight: function(code, lang) {
    try {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang, ignoreIllegals: true }).value;
      }
      return hljs.highlightAuto(code).value;
    } catch (e) {
      return code;
    }
  }
});

// 自定义 renderer 处理数学公式
const renderer = new marked.Renderer();

// 生成 slug 用于标题 ID
function generateSlug(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

// 自定义 heading renderer，添加 id 属性
renderer.heading = function(text, level, raw) {
  const slug = generateSlug(raw) || `heading-${Math.random().toString(36).substr(2, 9)}`;
  return `<h${level} id="${slug}">${text}</h${level}>\n`;
};

// 行内数学公式 $...$
renderer.inlineMath = function(latex) {
  try {
    return katex.renderToString(latex, { throwOnError: false });
  } catch (e) {
    return `<code>${latex}</code>`;
  }
};

// 块级数学公式 $$...$$
renderer.blockMath = function(latex) {
  try {
    return `<div class="math-block">${katex.renderToString(latex, { throwOnError: false, displayMode: true })}</div>`;
  } catch (e) {
    return `<pre><code>${latex}</code></pre>`;
  }
};

marked.use({ renderer });

// 预处理：处理数学公式和 Mermaid
function preprocessMarkdown(content) {
  let processed = content;
  
  // 处理块级数学公式 $$...$$
  processed = processed.replace(/\$\$([\s\S]*?)\$\$/g, (match, latex) => {
    return `\n<div class="math-block">${latex.trim()}</div>\n`;
  });
  
  // 处理行内数学公式 $...$ (但不要匹配 $$)
  processed = processed.replace(/(?<!\$)\$(?!\$)([^$\n]+?)\$(?!\$)/g, (match, latex) => {
    return `<span class="math-inline">${latex.trim()}</span>`;
  });
  
  // 处理 Mermaid 图表
  processed = processed.replace(/```mermaid\n([\s\S]*?)```/g, (match, mermaidCode) => {
    return `\n<div class="mermaid" data-mermaid="${encodeURIComponent(mermaidCode.trim())}">Mermaid 图表加载中...</div>\n`;
  });
  
  return processed;
}

// 后处理：渲染数学公式和 Mermaid
function postprocessHTML(html) {
  // 渲染块级数学公式
  html = html.replace(/<div class="math-block">([\s\S]*?)<\/div>/g, (match, latex) => {
    try {
      return `<div class="math-block">${katex.renderToString(latex.trim(), { throwOnError: false, displayMode: true })}</div>`;
    } catch (e) {
      return match;
    }
  });
  
  // 渲染行内数学公式
  html = html.replace(/<span class="math-inline">([\s\S]*?)<\/span>/g, (match, latex) => {
    try {
      return katex.renderToString(latex.trim(), { throwOnError: false });
    } catch (e) {
      return match;
    }
  });
  
  return html;
}

// 主渲染函数
export function renderMarkdown(content) {
  if (!content) return '';
  
  try {
    // 预处理
    const processed = preprocessMarkdown(content);
    
    // 使用 marked 渲染
    const rawHtml = marked.parse(processed);
    
    // 后处理（数学公式）
    const processedHtml = postprocessHTML(rawHtml);
    
    // 使用 DOMPurify 清理（防止 XSS）
    const cleanHtml = DOMPurify.sanitize(processedHtml, {
      ADD_TAGS: ['div', 'span'],
      ADD_ATTR: ['class', 'data-mermaid']
    });
    
    return cleanHtml;
  } catch (e) {
    console.error('Markdown 渲染失败:', e);
    return `<p style="color: red;">渲染失败: ${e.message}</p>`;
  }
}

// 单独渲染 Mermaid 图表
export async function renderMermaid(code) {
  try {
    const mermaid = (await import('mermaid')).default;
    mermaid.initialize({ startOnLoad: false, theme: 'default' });
    const id = 'mermaid-' + Math.random().toString(36).substr(2, 9);
    const { svg } = await mermaid.render(id, code);
    return svg;
  } catch (e) {
    console.error('Mermaid 渲染失败:', e);
    return `<p style="color: red;">Mermaid 渲染失败: ${e.message}</p>`;
  }
}

// 处理页面中所有 Mermaid 图表
export async function renderAllMermaids(container) {
  if (!container) return;
  
  const mermaidElements = container.querySelectorAll('.mermaid');
  for (const el of mermaidElements) {
    const encodedCode = el.getAttribute('data-mermaid');
    if (encodedCode) {
      try {
        const code = decodeURIComponent(encodedCode);
        const svg = await renderMermaid(code);
        el.innerHTML = svg;
        el.removeAttribute('data-mermaid');
        el.classList.remove('mermaid');
        el.classList.add('mermaid-rendered');
      } catch (e) {
        el.innerHTML = '<p style="color: red;">Mermaid 渲染失败</p>';
      }
    }
  }
}

// 生成目录（TOC）
export function generateToc(content) {
  if (!content) return [];
  
  const toc = [];
  const lines = content.split('\n');
  
  for (const line of lines) {
    const match = line.match(/^(#{1,6})\s+(.+)/);
    if (match) {
      const level = match[1].length;
      const title = match[2].trim();
      
      // 生成 slug（与 marked 生成的 ID 对应）
      const slug = title
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fff\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');
      
      toc.push({
        level,
        title,
        slug: slug || `heading-${toc.length}`
      });
    }
  }
  
  return toc;
}
