import os
import openai

# 设置 DeepSeek API key
openai.api_key = os.getenv("sk-b159a6fbe2f140558164113d384fc2c5")
openai.api_base = "https://api.deepseek.com/v1"  # deepseek 固定地址

def get_sql_from_llm(natural_language_query: str, table_info: str):
    prompt = f"""
你是一个将中文自然语言问题转换为SQL语句的助手。请根据以下表结构和问题，输出仅包含SQL语句（不要添加解释）。

表结构如下：
{table_info}

问题：{natural_language_query}

SQL：
"""
    response = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message["content"].strip()
