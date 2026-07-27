# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

## 笔记模块 (Note Module)

### 功能概述

笔记模块用于从 Gitee 私有仓库拉取 Obsidian 笔记并在 Web 端展示，支持以下功能：

- **仓库管理**：添加、查看、同步笔记仓库
- **Git 同步**：从 Gitee 拉取最新笔记内容到本地
- **笔记浏览**：查看 Markdown 笔记列表和详细内容
- **搜索功能**：按文件名或路径搜索笔记
- **Markdown 渲染**：支持标题、列表、代码块等格式

### 技术栈

- Vue 3 + Vite
- Axios（API 请求）
- Markdown 渲染（自定义解析器）

### API 接口

笔记模块通过以下 API 与 Django 后端交互：

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/notes/repositories/` | GET | 获取仓库列表 |
| `/api/notes/repositories/` | POST | 添加新仓库 |
| `/api/notes/repositories/{id}/sync/` | POST | 同步指定仓库 |
| `/api/notes/repositories/{id}/notes/` | GET | 获取笔记列表 |
| `/api/notes/repositories/{id}/notes/{path}/` | GET | 获取笔记内容 |

### 使用方式

1. 访问 `/notes` 页面
2. 点击"添加仓库"按钮，输入：
   - 仓库地址（如：`git@gitee.com:zeng333/note.git`）
   - 本地路径（如：`/tmp/my-notes`）
3. 点击"同步"按钮拉取最新内容
4. 点击仓库卡片查看笔记列表
5. 点击笔记查看详细内容

### 项目结构

```
src/
├── pages/
│   └── NotesPage.vue       # 笔记模块主页面
├── api/
│   └── notes.js            # 笔记 API 封装
└── router/
    └── index.js            # 路由配置（已注册 /notes 路由）
```

### 后端结构

笔记模块后端基于 Django 开发，位于 `hub/notes/` 目录：

```
hub/notes/
├── models.py               # 数据模型（NoteRepository、NoteFile）
├── git_service.py          # Git 操作服务（克隆、拉取、扫描）
├── api/
│   ├── urls.py             # API 路由配置
│   ├── views.py            # API 视图处理
│   └── serializers.py      # 数据序列化
└── apps.py                 # Django 应用配置
```
