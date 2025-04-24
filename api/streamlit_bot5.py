import streamlit as st
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from typing import Any
import traceback
from prompt import planner, coordinator, supervisor, dataquery
from db import get_dbmanager
from db.metastore import MetadataStore
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import TavilySearchResults
import uuid
from dotenv import load_dotenv
import json
from langchain_core.messages import SystemMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_core.runnables import RunnableConfig
from langgraph.config import get_stream_writer
import decimal
from datetime import date, datetime
from typing_extensions import TypedDict
from langgraph.graph import MessagesState
import logging
from langgraph.types import Command
from typing import Literal
import logging
from copy import deepcopy
from langchain_core.messages import HumanMessage, BaseMessage
from agent import get_graph

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    with st.sidebar:
        st.title("数据分析助手")
        st.markdown("---")
        st.write("这是一个数据分析助手，可以帮助你分析数据并生成可视化图表。")
        
        # 添加清除会话按钮
        if st.button("清除会话"):
            st.session_state.messages = [
                {"role": "assistant", "content": "你好，我是您的助手，可以帮助您分析数据，搜寻资料，并生成报告和图表。请问有什么可以帮助您？"}
            ]
            st.session_state.thread_id = str(uuid.uuid4())
            if "structured_messages" in st.session_state:
                st.session_state.structured_messages = []
            st.rerun()

    st.title("告诉我您的需求")

    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "你好，我是您的助手，可以帮助您分析数据，搜寻资料，并生成报告和图表。请问有什么可以帮助您？"}
        ]
    
    # 初始化thread_id，用于跟踪会话
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = str(uuid.uuid4())
    
    # 显示历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)  # 允许HTML渲染

    # 处理用户输入
    if prompt := st.chat_input(placeholder="输入您的需求..."):
        # 显示用户消息
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 获取graph
        graph = get_graph()
        
        # 只在第一次交互时传递完整历史（包括初始助手消息和第一个用户消息），之后只传递最新消息
        if len(st.session_state.messages) <= 2:
            agent_messages = [(msg["role"], msg["content"]) for msg in st.session_state.messages]
        else:
            # 只传递最新消息
            agent_messages = [("user", prompt)]
        
        # 使用callback处理agent的响应
        with st.chat_message("assistant"):
            config = {
                "configurable": {"thread_id": st.session_state.thread_id}
            }
            message_placeholder = st.empty()
            output = ""

            # 使用stream_mode=["messages", "custom"]，可以同时获取messages和custom的流式输出
            for stream_mode, chunk in graph.stream({"messages": agent_messages}, config, stream_mode=["messages", "custom"]):
                if stream_mode == "messages": 
                    # chunk is tuple of AIMessage
                    if isinstance(chunk, tuple):
                        output += ''.join(item.content for item in chunk if hasattr(item, "content"))
                    else:
                        output += str(chunk)
                elif stream_mode == "custom":
                    output += str(chunk)
                message_placeholder.markdown(output, unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": output})



if __name__ == "__main__":
    DEBUG = True
    main()
