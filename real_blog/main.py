import re
from pathlib import Path

import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="个人博客")

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content" / "posts"


def render_markdown(text: str) -> str:
    if not text or not text.strip():
        return ""
    return markdown.markdown(text, extensions=["extra"])


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>首页</title></head>
    <body>
        <h1>个人博客</h1>
        <p>博客 + 小软件展示，慢慢加。</p>
        <ul>
            <li><a href="/blog">博客</a></li>
            <li><a href="/tools">小软件</a></li>
            <li><a href="/docs">API 文档</a></li>
        </ul>
    </body>
    </html>
    """


# 写死的数据，后面可换成 SQLite。有 slug 的文章会从 content/posts/{slug}/body.md 读正文
POSTS = [
    {"id": 1, "title": "第一篇试水", "summary": "随便写点摘要"},
    {"id": 2, "title": "第二篇", "summary": "再写点"},
    {
        "id": 3,
        "title": "做一个自己的网站？快速上手无废话！",
        "summary": "小皮+WordPress 本地建站",
        "slug": "做网站教程",
    },
]

TOOLS = [
    {
        "id": 1,
        "name": "ThemeSwitcher",
        "desc": "Windows 10/11 主题自动深浅色切换小工具",
        "url": "https://github.com/AAAAA1116/ThemeSwitcher",
    },
    {
        "id": 2,
        "name": "Boot-up",
        "desc": "管理 Windows 开机自启的小工具",
        "url": "https://github.com/AAAAA1116/Boot-up",
    },
    {
        "id": 3,
        "name": "ContextMenuManager",
        "desc": "管理 Windows 右键菜单（如添加 Cursor）的小工具",
        "url": "https://github.com/AAAAA1116/ContextMenuManager",
    },
]


@app.get("/blog", response_class=HTMLResponse)
async def blog_list():
    items = "".join(
        f'<li><a href="/blog/{p["id"]}">{p["title"]}</a> — {p["summary"]}</li>'
        for p in POSTS
    )
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>博客</title></head>
    <body>
        <h1>博客</h1>
        <p><a href="/">← 回首页</a></p>
        <ul>{items}</ul>
    </body></html>
    """


@app.get("/blog/{post_id}", response_class=HTMLResponse)
async def blog_detail(post_id: int):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        return "<p>没有这篇文章</p>"
    slug = post.get("slug")
    from_body = False
    if slug:
        post_dir = CONTENT_DIR / slug
        body_path = None
        for name in ("body.md", "body.txt"):
            p = post_dir / name
            if p.exists():
                body_path = p
                break
        if body_path:
            body_raw = body_path.read_text(encoding="utf-8")
            body_html = render_markdown(body_raw)
            body_html = re.sub(
                r'src="(?!https?://)([^"]+)"',
                rf'src="/posts/{slug}/\1"',
                body_html,
            )
            content = f'<div class="post-body">\n{body_html}\n</div>'
            from_body = True
        else:
            content = f"<p>{post['summary']}</p><p>（body.md 或 body.txt 不存在）</p>"
    else:
        content = f"<p>{post['summary']}</p>"
    title_block = "" if from_body else f"<h1>{post['title']}</h1>\n        "
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>{post["title"]}</title></head>
    <body>
        {title_block}{content}
        <p><a href="/blog">← 返回列表</a></p>
    </body></html>
    """


@app.get("/tools", response_class=HTMLResponse)
async def tools_list():
    items = "".join(
        f'<li><a href="{t["url"]}" target="_blank">{t["name"]}</a> — {t["desc"]}</li>'
        for t in TOOLS
    )
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>小软件</title></head>
    <body>
        <h1>小软件</h1>
        <p><a href="/">← 回首页</a></p>
        <ul>{items}</ul>
    </body></html>
    """


@app.get("/tools/{tool_id}", response_class=HTMLResponse)
async def tool_detail(tool_id: int):
    tool = next((t for t in TOOLS if t["id"] == tool_id), None)
    if not tool:
        return "<p>没有这个小工具</p>"
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8"><title>{tool["name"]}</title></head>
    <body>
        <h1>{tool["name"]}</h1>
        <p>{tool["desc"]}</p>
        <p><a href="/tools">← 返回列表</a></p>
    </body></html>
    """


# 静态文件：/posts/做网站教程/1.png → content/posts/做网站教程/1.png
app.mount("/posts", StaticFiles(directory=str(CONTENT_DIR)), name="posts")

