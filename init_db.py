import sqlite3
import random
from datetime import datetime, timedelta

# 建立连接
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# 删除旧表（方便重复执行）
cursor.executescript('''
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;
''')

# 创建员工表
cursor.execute('''
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    region TEXT,
    position TEXT,
    hire_date TEXT
)
''')

# 创建客户表
cursor.execute('''
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    industry TEXT,
    region TEXT
)
''')

# 创建销售表（含外键）
cursor.execute('''
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product TEXT,
    region TEXT,
    sales_volume INTEGER,
    revenue REAL,
    employee_id INTEGER,
    customer_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
''')

# 插入员工数据
positions = ['销售员', '客户经理', '销售主管']
regions = ['华东', '华南', '华北', '西南', '东北']
employees = []

for i in range(15):
    name = f"员工{i+1}"
    region = random.choice(regions)
    position = random.choice(positions)
    hire_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000))
    employees.append((name, region, position, hire_date.strftime('%Y-%m-%d')))

cursor.executemany('''
INSERT INTO employees (name, region, position, hire_date)
VALUES (?, ?, ?, ?)
''', employees)

# 插入客户数据
industries = ['制造业', '互联网', '零售', '医疗', '教育']
customers = []

for i in range(20):
    name = f"客户{i+1}"
    industry = random.choice(industries)
    region = random.choice(regions)
    customers.append((name, industry, region))

cursor.executemany('''
INSERT INTO customers (name, industry, region)
VALUES (?, ?, ?)
''', customers)

# 插入销售数据
products = ['手机', '笔记本电脑', '耳机', '电视', '平板']
start_date = datetime(2025, 1, 1)
sales = []

for i in range(300):
    date = start_date + timedelta(days=random.randint(0, 180))
    product = random.choice(products)
    region = random.choice(regions)
    volume = random.randint(10, 100)
    revenue = round(volume * random.uniform(300, 1500), 2)
    employee_id = random.randint(1, len(employees))
    customer_id = random.randint(1, len(customers))
    sales.append((date.strftime('%Y-%m-%d'), product, region, volume, revenue, employee_id, customer_id))

cursor.executemany('''
INSERT INTO sales (date, product, region, sales_volume, revenue, employee_id, customer_id)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', sales)

conn.commit()
conn.close()
print("✅ 新版数据库初始化完毕，已生成 sales.db，含员工、客户、销售数据")
