# CONTRACTS.md — API/数据契约（所有 agent 必须遵守）

> 制定/维护流程：需求解读 Agent（AI）起草/更新文案；人只需审阅确认后将其写入/更新本文件。

本项目：个人博客（Python + FastAPI，博客 + 小软件展示）

## 全局约定
- 后端：FastAPI，返回 HTML 或 JSON 按路由约定。
- 静态资源：`content/posts/{slug}/` 下图片等通过 `/posts/{slug}/xxx` 访问。

## 内容与路由
- 首页：`/`，博客入口：`/blog`，文章详情：`/blog/{post_id}`。
- 文章正文：优先从 `content/posts/{slug}/body.md` 或 `body.txt` 读取，无 slug 则仅显示摘要。
- 小软件列表：`/tools`，详情：`/tools/{tool_id}`。
- API 文档：`/docs`（FastAPI 自带）。

## 数据（当前）
- 文章列表与工具列表暂在 `main.py` 中写死；后续可迁至 SQLite 等，由迁移或约定文件说明。
