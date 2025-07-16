from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain import LLMChain
from langchain.prompts import PromptTemplate

import openai
import time
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import os
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings

#API key
user_api_key="sk-c8f499bd18954c3097f072c14ba1eb25"     #Your personal Deepseek API key.
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')
langchain_tracing_v2 = os.getenv('LANGCHAIN_TRACING_V2', 'true')
langchain_endpoint = os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')
#LangSmith for tracking
os.environ['LANGCHAIN_TRACING_V2'] = langchain_tracing_v2
os.environ['LANGCHAIN_ENDPOINT'] = langchain_endpoint
os.environ['LANGCHAIN_API_KEY'] = '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'

llm = ChatOpenAI(
        model="deepseek-chat",
        # model="deepseek-reasoner",
        openai_api_key=user_api_key,
        openai_api_base="https://api.deepseek.com",
        temperature=0.0
    )
import re
def convert_mysql_to_sqlite_sql(sql: str) -> str:
    sql = sql.strip()

    # 移除 markdown 格式代码块
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # 替换 MySQL 日期函数
    sql = re.sub(r"DATE_SUB\s*\(\s*CURRENT_DATE\s*\(\s*\)\s*,\s*INTERVAL\s+(\d+)\s+DAY\s*\)", r"DATE('now', '-\1 day')", sql)
    sql = re.sub(r"DATE_SUB\s*\(\s*CURRENT_DATE\s*\(\s*\)\s*,\s*INTERVAL\s+(\d+)\s+MONTH\s*\)", r"DATE('now', '-\1 month')", sql)

    # CURRENT_DATE() ➜ DATE('now')
    sql = re.sub(r"CURRENT_DATE\s*\(\s*\)", "DATE('now')", sql)

    # 替换 IFNULL ➜ COALESCE（SQLite 推荐）
    sql = sql.replace("IFNULL", "COALESCE")

    # 替换 true/false 为 1/0（SQLite 没有 true/false 类型）
    sql = sql.replace("TRUE", "1").replace("FALSE", "0")

    # 替换 LIMIT x OFFSET y ➜ SQLite 兼容（大部分兼容，但注意语法顺序）
    # 不处理子查询结构，适合简单查询

    return sql
def get_sql_from_llm(natural_language_query: str, table_info: str):
    query = f"""
    你是一个将中文自然语言问题转换为SQL语句的助手。请根据以下表结构和问题，输出仅包含SQL语句（不要添加解释）。

    表结构如下：
    {table_info}

    问题：{natural_language_query}

    SQL：
    """

    agent = initialize_agent(tools=[],
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )
    response = agent.invoke(query)
    sql_raw = response['output']
    sql = convert_mysql_to_sqlite_sql(sql_raw)
    return sql
    
