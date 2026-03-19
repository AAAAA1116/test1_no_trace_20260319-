# SQLite 语法小抄：在项目里运行 py sqlite_demo.py 看效果
import sqlite3

# 连接：没有就自动建一个 .db 文件
conn = sqlite3.connect("demo.db")
cur = conn.cursor()

# --- 建表 ---
# 表名 posts，三列：id(主键自增)、标题、内容
cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT
    )
""")

# --- 增 INSERT ---
cur.execute("INSERT INTO posts (title, body) VALUES (?, ?)", ("第一篇", "内容啊啊"))
cur.execute("INSERT INTO posts (title, body) VALUES (?, ?)", ("第二篇", "内容嘿嘿"))
# 用 ? 占位，后面元组传值，防注入

# --- 查 SELECT ---
cur.execute("SELECT * FROM posts")          # * 表示所有列
rows = cur.fetchall()                       # 取出全部行
print("全部:", rows)

cur.execute("SELECT id, title FROM posts WHERE id = ?", (1,))
one = cur.fetchone()
print("id=1:", one)

# --- 改 UPDATE ---
cur.execute("UPDATE posts SET title = ? WHERE id = ?", ("第一篇（已改）", 1))

# --- 删 DELETE ---
# cur.execute("DELETE FROM posts WHERE id = ?", (2,))

# 改删之后必须提交才写入文件
conn.commit()

# 再查一次看结果
cur.execute("SELECT * FROM posts")
print("提交后:", cur.fetchall())

cur.close()
conn.close()
