from utils.llm_client import get_sql_from_llm
import sqlite3

# ✅ 设置表结构信息（与训练用数据库保持一致）
TABLE_INFO = '''
sales(id, date, product, region, sales_volume, revenue, employee_id, customer_id)
employees(id, name, region, position, hire_date)
customers(id, name, industry, region)
'''

# ✅ 中文自然语言问题
question = "最近一个月卖出的产品按销量降序排序？"

# ✅ 第一步：调用 LLM 获取 SQL
print("🧠 正在将自然语言转换为 SQL...")
sql = get_sql_from_llm(question, TABLE_INFO)
print("✅ 生成的 SQL：\n", sql)

# ✅ 第二步：执行 SQL 查询
print("\n📊 正在执行 SQL 查询...")
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()
try:
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    print("✅ 查询结果：")
    for row in result:
        print(row)
except Exception as e:
    print("❌ 执行 SQL 时出错：", e)
finally:
    conn.close()


