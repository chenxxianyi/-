const documents = [
  {
    id: 1,
    name: "深度学习论文阅读方法.pdf",
    type: "pdf",
    size: "8.4 MB",
    uploadedAt: "今天 19:12",
    lastRead: "18 分钟前",
    annotations: 12,
  },
  {
    id: 2,
    name: "产品调研摘录.md",
    type: "md",
    size: "128 KB",
    uploadedAt: "今天 14:08",
    lastRead: "1 小时前",
    annotations: 7,
  },
  {
    id: 3,
    name: "行业分析报告.docx",
    type: "docx",
    size: "2.1 MB",
    uploadedAt: "昨天 21:30",
    lastRead: "昨天",
    annotations: 4,
  },
  {
    id: 4,
    name: "会议纪要.txt",
    type: "txt",
    size: "46 KB",
    uploadedAt: "周一 10:16",
    lastRead: "2 天前",
    annotations: 2,
  },
];

let annotations = [
  {
    id: 101,
    color: "yellow",
    text: "稳定的高亮位置需要保存相对坐标，而不是固定像素。",
    note: "PDF 缩放时避免错位，这是后续实现 AnnotationLayer 的关键。",
    page: 12,
    time: "18 分钟前",
  },
  {
    id: 102,
    color: "blue",
    text: "AI 阅读助手应该是辅助工具。",
    note: "AI 面板不要抢主阅读区注意力。",
    page: 12,
    time: "24 分钟前",
  },
];

let notes = [
  {
    id: 201,
    title: "批注是理解的外部记忆",
    excerpt: "阅读器不仅要展示内容，还要承载用户对内容的组织过程。",
    source: "深度学习论文阅读方法.pdf",
    updatedAt: "刚刚",
  },
  {
    id: 202,
    title: "Markdown 文本锚点方案",
    excerpt: "MVP 保存 selectedText 和简化 range，后续升级文本锚点。",
    source: "产品调研摘录.md",
    updatedAt: "昨天",
  },
];

let activeView = "dashboard";
let activeFilter = "all";
let selectedText = "";
let selectedRange = null;
let zoom = 100;

const titles = {
  dashboard: ["工作台", "继续阅读、整理批注和笔记"],
  documents: ["文件库", "上传、搜索和管理所有阅读资料"],
  reader: ["阅读器", "阅读、划线、批注和 AI 辅助理解"],
  notes: ["笔记", "整理摘录和自己的思考"],
  settings: ["设置", "用户资料、主题和 AI 配置预留"],
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function setView(view) {
  activeView = view;
  $$(".view").forEach((node) => node.classList.toggle("active", node.id === `view-${view}`));
  $$(".nav-item").forEach((node) => node.classList.toggle("active", node.dataset.view === view));

  const [title, subtitle] = titles[view] || titles.dashboard;
  $("#headerTitle").textContent = title;
  $("#headerSubtitle").textContent = subtitle;

  if (view === "documents") {
    renderDocuments();
  }
  if (view === "reader") {
    renderAnnotations();
    renderExcerpts();
  }
  if (view === "notes") {
    renderNotes();
  }
}

function showToast(message) {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.remove("hidden");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => toast.classList.add("hidden"), 2200);
}

function fileBadge(type) {
  const safeType = type.toLowerCase();
  return `<span class="file-badge ${safeType}">${safeType.toUpperCase()}</span>`;
}

function renderRecentFiles() {
  $("#recentFilesBody").innerHTML = documents
    .slice(0, 4)
    .map(
      (doc) => `
        <tr>
          <td><button class="plain-row-link file-cell" data-open-doc="${doc.id}">${fileBadge(doc.type)} ${doc.name}</button></td>
          <td>${doc.type.toUpperCase()}</td>
          <td>${doc.size}</td>
          <td>${doc.lastRead}</td>
          <td>${doc.annotations}</td>
        </tr>
      `,
    )
    .join("");
}

function renderDashboardAnnotations() {
  $("#dashboardAnnotations").innerHTML = annotations
    .slice(0, 4)
    .map(
      (item) => `
        <button class="annotation-item" data-view-trigger="reader">
          <div class="annotation-topline">
            <span class="annotation-color ${item.color}"></span>
            <span class="annotation-meta">Page ${item.page} · ${item.time}</span>
          </div>
          <p class="annotation-text">${item.text}</p>
          <p class="annotation-note">${item.note}</p>
        </button>
      `,
    )
    .join("");
}

function filteredDocuments() {
  const keyword = ($("#documentSearch")?.value || "").trim().toLowerCase();
  return documents.filter((doc) => {
    const matchType = activeFilter === "all" || doc.type === activeFilter;
    const matchKeyword =
      !keyword ||
      doc.name.toLowerCase().includes(keyword) ||
      doc.type.toLowerCase().includes(keyword);
    return matchType && matchKeyword;
  });
}

function renderDocuments() {
  const rows = filteredDocuments();
  $("#countAll").textContent = documents.length;
  $("#documentsEmpty").classList.toggle("hidden", rows.length > 0);

  $("#documentsBody").innerHTML = rows
    .map(
      (doc) => `
        <tr>
          <td>
            <button class="plain-row-link file-cell" data-open-doc="${doc.id}">
              ${fileBadge(doc.type)}
              <span>${doc.name}</span>
            </button>
          </td>
          <td>${doc.type.toUpperCase()}</td>
          <td>${doc.size}</td>
          <td>${doc.uploadedAt}</td>
          <td>${doc.lastRead}</td>
          <td><span class="soft-badge">${doc.annotations}</span></td>
          <td>
            <div class="row-actions">
              <button class="text-button" data-open-doc="${doc.id}">打开</button>
              <button class="text-button" data-rename-doc="${doc.id}">重命名</button>
              <button class="delete-link" data-delete-doc="${doc.id}">删除</button>
            </div>
          </td>
        </tr>
      `,
    )
    .join("");
}

function renderAnnotations() {
  const list = $("#annotationList");
  if (!annotations.length) {
    list.innerHTML = `
      <div class="empty-state">
        <strong>暂无批注</strong>
        <span>选中文本后可以添加高亮和备注。</span>
      </div>
    `;
    return;
  }

  list.innerHTML = annotations
    .map(
      (item, index) => `
        <div class="annotation-item ${index === 0 ? "active" : ""}" data-annotation-id="${item.id}">
          <div class="annotation-topline">
            <span class="annotation-color ${item.color}"></span>
            <span class="annotation-meta">Page ${item.page} · ${item.time}</span>
            <button class="delete-link" data-delete-annotation="${item.id}">删除</button>
          </div>
          <p class="annotation-text">${item.text}</p>
          <p class="annotation-note">${item.note || "暂无备注"}</p>
        </div>
      `,
    )
    .join("");
}

function renderExcerpts() {
  const list = $("#excerptList");
  list.innerHTML = notes
    .map(
      (note) => `
        <button class="note-item" data-view-trigger="notes">
          <strong>${note.title}</strong>
          <span class="note-meta">${note.source} · ${note.updatedAt}</span>
          <p>${note.excerpt}</p>
        </button>
      `,
    )
    .join("");
}

function renderNotes() {
  const keyword = ($("#noteSearch")?.value || "").trim().toLowerCase();
  const rows = notes.filter(
    (note) =>
      !keyword ||
      note.title.toLowerCase().includes(keyword) ||
      note.excerpt.toLowerCase().includes(keyword) ||
      note.source.toLowerCase().includes(keyword),
  );

  $("#noteList").innerHTML = rows
    .map(
      (note, index) => `
        <button class="note-item ${index === 0 ? "active" : ""}" data-note-id="${note.id}">
          <strong>${note.title}</strong>
          <span class="note-meta">${note.source} · ${note.updatedAt}</span>
          <p>${note.excerpt}</p>
        </button>
      `,
    )
    .join("");
}

function setReaderTab(tab) {
  $$(".tab-button").forEach((node) => node.classList.toggle("active", node.dataset.readerTab === tab));
  $$(".tab-pane").forEach((node) => node.classList.toggle("active", node.id === `tab-${tab}`));
}

function simulateUpload() {
  const progress = $("#uploadProgress");
  const label = progress.querySelector("span");
  const bar = progress.querySelector("div span");
  let value = 0;

  progress.classList.remove("hidden");
  label.textContent = "正在上传：研究资料摘录.md";
  bar.style.width = "0%";

  const timer = window.setInterval(() => {
    value += 14;
    bar.style.width = `${Math.min(value, 100)}%`;
    if (value >= 100) {
      window.clearInterval(timer);
      documents.unshift({
        id: Date.now(),
        name: "研究资料摘录.md",
        type: "md",
        size: "92 KB",
        uploadedAt: "刚刚",
        lastRead: "未阅读",
        annotations: 0,
      });
      renderDocuments();
      renderRecentFiles();
      window.setTimeout(() => progress.classList.add("hidden"), 500);
      showToast("上传完成，文件已加入文件库");
    }
  }, 140);
}

function wrapSelection(className) {
  if (!selectedRange || selectedRange.collapsed) {
    return false;
  }

  const span = document.createElement("span");
  span.className = className;

  try {
    selectedRange.surroundContents(span);
    window.getSelection().removeAllRanges();
    return true;
  } catch (error) {
    showToast("跨段落选区已保存到批注列表，正文覆盖层将在 Vue 版本中增强");
    return false;
  }
}

function createAnnotation(color, options = {}) {
  if (!selectedText) {
    showToast("请先在阅读区选中文本");
    return;
  }

  annotations.unshift({
    id: Date.now(),
    color: color === "underline" ? "red" : color,
    text: selectedText,
    note: options.note || "来自 H5 demo 的新批注，可在 Vue 版本中编辑备注。",
    page: 12,
    time: "刚刚",
  });

  renderAnnotations();
  renderDashboardAnnotations();
  setReaderTab("annotations");
  $("#selectionToolbar").classList.add("hidden");
}

function createExcerpt() {
  if (!selectedText) {
    showToast("请先在阅读区选中文本");
    return;
  }

  notes.unshift({
    id: Date.now(),
    title: selectedText.slice(0, 18) || "新摘录",
    excerpt: selectedText,
    source: "深度学习论文阅读方法.pdf",
    updatedAt: "刚刚",
  });

  renderExcerpts();
  renderNotes();
  setReaderTab("excerpts");
  $("#selectionToolbar").classList.add("hidden");
  showToast("已摘录到笔记");
}

function setAiAnswer(type, text) {
  const answer = $("#aiAnswer");
  answer.innerHTML = `
    <strong>${type}</strong>
    <p>${text}</p>
  `;
  setReaderTab("ai");
}

function showAiLoading(callback) {
  $("#aiAnswer").innerHTML = "<strong>AI 阅读助手</strong><p>正在生成 mock 结果...</p>";
  setReaderTab("ai");
  window.setTimeout(callback, 520);
}

function updateZoom(nextZoom) {
  zoom = Math.max(80, Math.min(130, nextZoom));
  $("#zoomValue").textContent = `${zoom}%`;
  $("#readerPage").style.transform = `scale(${zoom / 100})`;
}

function bindEvents() {
  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-view-trigger]");
    if (trigger) {
      setView(trigger.dataset.viewTrigger);
      return;
    }

    const nav = event.target.closest(".nav-item");
    if (nav) {
      setView(nav.dataset.view);
      return;
    }

    const openDoc = event.target.closest("[data-open-doc]");
    if (openDoc) {
      const doc = documents.find((item) => String(item.id) === String(openDoc.dataset.openDoc));
      if (doc) {
        $("#readerTitle").textContent = doc.name;
        $(".reader-file-title span").textContent = `${doc.type.toUpperCase()} · 已保存阅读进度`;
      }
      setView("reader");
      return;
    }

    const renameDoc = event.target.closest("[data-rename-doc], #renameSelected");
    if (renameDoc) {
      const target = documents[0];
      target.name = target.name.replace(/\.(pdf|md|docx|txt)$/i, "（已重命名）.$1");
      renderDocuments();
      renderRecentFiles();
      showToast("已模拟重命名第一份文件");
      return;
    }

    const deleteDoc = event.target.closest("[data-delete-doc]");
    if (deleteDoc) {
      const index = documents.findIndex((item) => String(item.id) === String(deleteDoc.dataset.deleteDoc));
      if (index >= 0) {
        documents.splice(index, 1);
        renderDocuments();
        renderRecentFiles();
        showToast("已模拟软删除文件");
      }
      return;
    }

    const deleteAnnotation = event.target.closest("[data-delete-annotation]");
    if (deleteAnnotation) {
      annotations = annotations.filter((item) => String(item.id) !== String(deleteAnnotation.dataset.deleteAnnotation));
      renderAnnotations();
      renderDashboardAnnotations();
      showToast("批注已删除");
      return;
    }

    const tab = event.target.closest("[data-reader-tab]");
    if (tab) {
      setReaderTab(tab.dataset.readerTab);
      return;
    }

    const aiAction = event.target.closest("[data-ai]");
    if (aiAction) {
      const action = aiAction.dataset.ai;
      showAiLoading(() => {
        if (action === "summary") {
          setAiAnswer("文档总结", "这份文档强调阅读工具应把文档、批注、摘录、笔记和 AI 辅助放在同一个上下文中，核心是降低长文档理解和复盘成本。");
        }
        if (action === "explain") {
          setAiAnswer("文本解释", selectedText ? `这段话的意思是：${selectedText}。它强调实现时要优先保证阅读稳定性。` : "请先在阅读区选中文本，再请求解释。");
        }
        if (action === "translate") {
          setAiAnswer("翻译结果", selectedText ? `Mock translation: ${selectedText}` : "请先在阅读区选中文本，再请求翻译。");
        }
      });
      return;
    }
  });

  $("#documentSearch").addEventListener("input", renderDocuments);
  $("#noteSearch").addEventListener("input", renderNotes);
  $("#uploadTrigger").addEventListener("click", simulateUpload);
  $("#uploadZone").addEventListener("click", simulateUpload);

  $("#uploadZone").addEventListener("dragover", (event) => {
    event.preventDefault();
    $("#uploadZone").classList.add("drag-over");
  });

  $("#uploadZone").addEventListener("dragleave", () => {
    $("#uploadZone").classList.remove("drag-over");
  });

  $("#uploadZone").addEventListener("drop", (event) => {
    event.preventDefault();
    $("#uploadZone").classList.remove("drag-over");
    simulateUpload();
  });

  $$(".filter-item[data-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.filter;
      $$(".filter-item[data-filter]").forEach((node) => node.classList.toggle("active", node === button));
      renderDocuments();
    });
  });

  $("#readerContent").addEventListener("mouseup", () => {
    const selection = window.getSelection();
    const toolbar = $("#selectionToolbar");

    if (!selection || selection.isCollapsed) {
      toolbar.classList.add("hidden");
      return;
    }

    const text = selection.toString().trim();
    if (!text) {
      toolbar.classList.add("hidden");
      return;
    }

    const range = selection.getRangeAt(0);
    const readerContent = $("#readerContent");
    if (!readerContent.contains(range.commonAncestorContainer)) {
      toolbar.classList.add("hidden");
      return;
    }

    const rect = range.getBoundingClientRect();
    selectedText = text;
    selectedRange = range.cloneRange();
    toolbar.style.left = `${Math.min(rect.left, window.innerWidth - 360)}px`;
    toolbar.style.top = `${Math.max(rect.top - 46, 64)}px`;
    toolbar.classList.remove("hidden");
  });

  $("#selectionToolbar").addEventListener("click", (event) => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const action = button.dataset.action;

    if (action === "yellow" || action === "blue" || action === "green") {
      wrapSelection(`dynamic-highlight ${action}`);
      createAnnotation(action);
    }
    if (action === "underline") {
      wrapSelection("dynamic-underline");
      createAnnotation("underline");
    }
    if (action === "note") {
      createAnnotation("yellow", { note: "这里是模拟批注内容，Vue 版本会替换为可编辑输入框。" });
    }
    if (action === "excerpt") {
      createExcerpt();
    }
    if (action === "explain") {
      showAiLoading(() => setAiAnswer("AI 解释", `这段内容可以理解为：${selectedText}`));
    }
  });

  document.addEventListener("mousedown", (event) => {
    const toolbar = $("#selectionToolbar");
    if (!event.target.closest("#selectionToolbar") && !event.target.closest("#readerContent")) {
      toolbar.classList.add("hidden");
    }
  });

  $("#summaryButton").addEventListener("click", () => {
    showAiLoading(() => {
      setAiAnswer("文档总结", "当前文档讨论了长文档阅读中的批注、摘录、笔记与 AI 辅助协作方式。MVP 应优先保证阅读稳定、批注可保存、笔记可回溯。");
    });
  });

  $("#askAiButton").addEventListener("click", () => {
    const question = $("#aiQuestion").value.trim() || "这篇文档主要讲了什么？";
    showAiLoading(() => {
      setAiAnswer("文档问答", `问题：“${question}”。Mock 回答：文档重点在于把阅读、批注和知识整理流程放到同一个工作台中。`);
    });
  });

  $("#zoomIn").addEventListener("click", () => updateZoom(zoom + 10));
  $("#zoomOut").addEventListener("click", () => updateZoom(zoom - 10));

  $("#newNoteButton").addEventListener("click", () => {
    notes.unshift({
      id: Date.now(),
      title: "未命名笔记",
      excerpt: "新的阅读笔记内容。",
      source: "手动创建",
      updatedAt: "刚刚",
    });
    renderNotes();
    showToast("已创建新笔记");
  });

  $("#noteEditor").addEventListener("input", () => {
    $("#saveStatus").textContent = "保存中...";
    window.clearTimeout(bindEvents.saveTimer);
    bindEvents.saveTimer = window.setTimeout(() => {
      $("#saveStatus").textContent = "已保存";
    }, 650);
  });

  $("#syncButton").addEventListener("click", () => {
    showToast("已模拟同步最新阅读数据");
  });
}

function injectUtilityStyles() {
  const style = document.createElement("style");
  style.textContent = `
    .plain-row-link {
      border: 0;
      background: transparent;
      padding: 0;
      text-align: left;
    }
    .soft-badge {
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      border-radius: 999px;
      background: var(--color-bg-muted);
      padding: 0 8px;
      color: var(--color-text-secondary);
      font-size: 12px;
      font-weight: 650;
    }
  `;
  document.head.appendChild(style);
}

function init() {
  injectUtilityStyles();
  renderRecentFiles();
  renderDashboardAnnotations();
  renderDocuments();
  renderAnnotations();
  renderExcerpts();
  renderNotes();
  bindEvents();
}

init();
