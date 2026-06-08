# 知识型阅读工作台 H5 Demo

这是基于根目录《前端开发文档.md》和本地设计资料整理出的纯 H5 前端 demo。

目标不是做最终工程版本，而是先验证产品界面方向、信息层级、阅读器布局、批注交互和整体视觉是否符合预期。确认后可迁移为 Vue 3 + Vite + TypeScript + Pinia + Naive UI + Tailwind CSS 项目。

## 打开方式

直接在浏览器中打开：

```text
h5-demo/index.html
```

## 已包含页面

- 工作台：继续阅读、最近批注、最近上传。
- 文件库：类型筛选、搜索、上传 loading、文件表格、重命名和删除 mock。
- 阅读器：三栏布局、顶部工具栏、仿 PDF 阅读页、选中文本工具条、右侧批注 / 摘录 / AI 面板。
- 笔记：笔记列表、编辑器、自动保存状态、来源回跳。
- 设置：用户资料、主题预留、存储空间和 AI 配置预留。

## 已包含交互

- 主导航切换页面。
- 文件库搜索和类型筛选。
- 模拟文件上传进度。
- 点击文件进入阅读器。
- 阅读器缩放。
- 选中文本后显示浮动工具条。
- 创建高亮、下划线、批注。
- 删除批注。
- 摘录到笔记。
- AI 总结、解释、翻译和问答 mock。
- 笔记编辑自动保存状态。

## 设计取向

Demo 采用克制型知识工具风：

- 浅色主题。
- 固定左侧导航。
- 文件库使用表格，不做卡片墙。
- 阅读器以正文为中心，左右面板轻量。
- 批注和笔记使用文本列表。
- AI 面板作为辅助工具，不做聊天娱乐化界面。
- 少阴影、少装饰、少强视觉效果。

## Vue 3 迁移映射

当前 H5 结构可以迁移为：

- `AppLayout.vue`：`.app-shell`、`.sidebar`、`.workspace`
- `Sidebar.vue`：主导航
- `HeaderBar.vue`：顶部栏
- `DashboardView.vue`：`#view-dashboard`
- `DocumentsView.vue`：`#view-documents`
- `ReaderView.vue`：`#view-reader`
- `ReaderShell.vue`：`.reader-shell`
- `ReaderTopBar.vue`：`.reader-topbar`
- `SelectionToolbar.vue`：`.selection-toolbar`
- `AnnotationSidebar.vue`：右侧批注 tab
- `AiPanel.vue`：右侧 AI tab
- `NotesView.vue`：`#view-notes`
- `SettingsView.vue`：`#view-settings`

`app.js` 中的 mock state 后续可拆到：

- `authStore.ts`
- `documentStore.ts`
- `annotationStore.ts`
- `noteStore.ts`

样式 token 后续可迁移到：

- `src/styles/tokens.css`
- `src/styles/base.css`
- `src/styles/reader.css`

## 当前限制

- PDF 阅读页是静态仿真，不是真实 PDF.js 渲染。
- 高亮 DOM 包裹只适合简单选区，跨段落选区仅保存到右侧批注列表。
- AI 返回为本地 mock。
- 上传、删除、重命名都是前端内存 mock。
- 移动端已做基础响应式，但最终 Vue 版本需要补抽屉和更完整手势体验。
