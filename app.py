from flask import Flask, request, send_file, jsonify, send_from_directory
import sqlite3
from utils.llm_client import get_sql_from_llm

app = Flask(__name__)
DB_PATH = "db/sales.db"

# 用于展示给LLM的 schema 提示
TABLE_INFO = """
sales(id, date, product, region, sales_volume, revenue, employee_id, customer_id)
employees(id, name, region, position, hire_date)
customers(id, name, industry, region)
"""

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("question", "")

    try:
        # 1. 获取SQL
        sql = get_sql_from_llm(question, TABLE_INFO)
        print(f"[DEBUG] SQL generated:\n{sql}")

        # 2. 执行SQL
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        conn.close()

        return jsonify({
            "question": question,
            "sql": sql,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    if '发一张wallpaper' in user_input:
        return send_file('pics/njs-wallpaper.jpg', mimetype='image/jpeg')
    return jsonify({'response': '暂不支持该指令'}), 200


from werkzeug.serving import make_server
 
if __name__ == '__main__':
    server = make_server('127.0.0.1', 5000, app)
    server.serve_forever()
    app.run()

