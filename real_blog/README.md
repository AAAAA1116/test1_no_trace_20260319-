# 个人博客（简历项目）

- 技术：Python + FastAPI
- 用途：博客 + 自己写的小软件展示

## 本地运行

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

浏览器打开 http://127.0.0.1:8000 ，API 文档 http://127.0.0.1:8000/docs

## 后续可做（按需、慢慢来）

- 用 **模板**（如 Jinja2）写页面，少手写 HTML
- 加 **文章/小软件** 的列表接口和页面
- 数据存 **SQLite**（先不碰数据库也行，用列表模拟）
- 部署到 **Vercel / Railway / 自己的服务器**
