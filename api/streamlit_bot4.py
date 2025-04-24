import streamlit as st
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from typing import Any
import traceback
from db import get_dbmanager
from db.metastore import MetadataStore
from langchain_core.messages import HumanMessage
from langchain_core.callbacks import BaseCallbackHandler
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import TavilySearchResults
import uuid
from dotenv import load_dotenv
import base64
import json
from e2b_code_interpreter import Sandbox
from langchain_core.messages import SystemMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from prompt import planning, dataquery
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.config import get_stream_writer
import decimal
from datetime import date, datetime

load_dotenv()

# 初始化全局变量，用于缓存模型和checkpointer
@st.cache_resource
def get_model(model_name: str):
    """缓存并返回LLM模型实例"""
    if model_name == "gpt-4o":
        return init_chat_model( model="gpt-4o", model_provider="openai", streaming=True)
    elif model_name == "gpt-4o-mini":
        return init_chat_model( model="gpt-4o-mini", model_provider="openai", streaming=True)
    elif model_name == "gpt-4.1":
        return init_chat_model( model="gpt-4.1", model_provider="openai", streaming=True)
    elif model_name == "deepseek-reasoner":
        return init_chat_model(model="deepseek-reasoner", model_provider="deepseek", temperature=1.0, streaming=True)
        # return ChatOpenAI(model="deepseek-reasoner", base_url="https://genaiapi.cloudsway.net/v1/ai/yvmSooRghzahEnas", api_key="OJH88G8VbD1crCZhYiM6")
    elif model_name == "gemini-2.0":
        return init_chat_model(model="gemini-2.0-flash-001", model_provider="google_vertexai", streaming=True)
    elif model_name == "gemini-2.5":
        return init_chat_model(model="gemini-2.5-pro-exp-03-25", model_provider="google_vertexai", streaming=True)
    else:
        raise ValueError(f"Unsupported model: {model_name}")    

@st.cache_resource
def get_checkpointer():
    """缓存并返回MemorySaver实例"""
    return MemorySaver()

# @st.cache_resource
# def get_team():
#     graph = StateGraph(PlanExecute)
#     graph.add_node("planner", plan_step)
#     graph.add_node("executor", execute_step)

#     graph.add_edge(START, "planner")
#     graph.add_edge("planner", "executor")
#     graph.add_edge("executor", END)
#     return graph.compile(checkpointer=get_checkpointer())

@st.cache_resource
def get_coordinator():
    search_tool = TavilySearchResults(max_results=5)
    tools = [data_query_agent, chart_generate_agent, search_tool]
    system_prompt = planning.COORDINATOR_PROMPT
    agent = create_react_agent(get_model("gpt-4.1"), tools, prompt=system_prompt, checkpointer=get_checkpointer())
    return agent;


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
        graph = get_coordinator()
        
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

            # # use messages stream mode
            # for chunk, metadata in graph.stream({"messages": agent_messages}, config, stream_mode="messages"):
            #     output += str(chunk.content)
            #     message_placeholder.markdown(output, unsafe_allow_html=True)

            st.session_state.messages.append({"role": "assistant", "content": output})



class PlanExecute(TypedDict):
    input: str
    plan: str
    result: str


# Each tool function can take a config argument. 
# In order for the config to be correctly propagated to the function, you MUST always add a RunnableConfig type annotation for your config argument
@tool
def data_query_agent(question: str, config: RunnableConfig) -> Any:
    """查询数据库中的数据并返回查询结果。
    
    该工具会将问题转换为SQL查询并执行。
    
    Args:
        question: 用户的问题，不要提供SQL，只需要提出需求。
    
    Returns:
        查询结果，通常是JSON格式的数据
    """
    try:
        writer = get_stream_writer()
        writer(f"<div style='font-size: 0.9em; color: #666; font-style: italic;'> 🔧 <b>Agent开始执行: data_query_agent </b> <p>输入: {question} </p> ")

        workspace = "yingkou-dw" # default workspace
        dbtype = "bigquery"
        metadata = MetadataStore(workspace).query()
        system_prompt = dataquery.SQL_PROMPT.format(workspace=workspace, metadata=metadata, dbtype=dbtype)
        tools = [execute_sql_query]
        messages = [HumanMessage(question)]

        agent = create_react_agent(get_model("gpt-4.1"), tools, prompt=system_prompt, name="data_query_agent")
        result = agent.invoke({"messages": messages}, config=config)

        writer(f" 🔧 <b>data_query_agent 执行完毕</b> </div>")
        # print(f"\n\n data_query_agent result: {result} \n\n")
        # TODO, return strucuted message?
        return result["messages"][-1].content
    except Exception as e:
        # error_msg = f"data query failed: {str(e)}"
        stack_trace = traceback.format_exc()
        error_msg = f"数据查询失败 (data_query_agent): \n错误类型: {type(e).__name__}\n错误信息: {str(e)}\n堆栈跟踪:\n{stack_trace}"
        print(f"\n\n===== DATA QUERY AGENT ERROR =====\n{error_msg}\n===========================\n\n")
        writer(f"<div style='color: red; background: #ffeeee; padding: 10px; border-radius: 5px; margin: 10px 0;'><b>查询出错</b>: {str(e)}</div>")
        return f"查询执行失败: {str(e)}---{stack_trace}"


@tool
def chart_generate_agent(request: str, config: RunnableConfig, data: str=None) -> Any:
    """生成图表并返回HTML图像。
    
    该工具会根据用户的问题生成图表。数据可以直接在request中提供，也可以在data参数中
    如果数据量不大，建议直接在request参数中包含数据
    
    Args:
        request: 用户关于图表的问题
        data: 可选。用于处理的数据，也可以是文件路径。
    
    Returns:
        HTML图像
    """
    try:
        # TODO, upload data file to e2b sandbox
        writer = get_stream_writer()
        writer(f"<div style='font-size: 0.9em; color: #666; font-style: italic;'> 🔧 <b>Agent开始执行: chart_generate_agent </b> <p>输入: {request}; 数据: {data} </p> ")

        system_prompt = dataquery.CHART_PROMPT
        tools = [run_code]
        content = f"用户的问题: {request}\n 数据: {data}\n"
        print(f"\n\n chart_generate_agent， user content: {content} \n\n")
        messages = [HumanMessage(content)]
        agent = create_react_agent(get_model("gpt-4.1"), tools, prompt=system_prompt, name="chart_generate_agent")
        result = agent.invoke({"messages": messages}, config=config)

        writer(f" 🔧 <b>chart_generate_agent 执行完毕</b> </div>")
        # TODO, return structured message?
        return result["messages"][-1].content
    except Exception as e:
        # error_msg = f"chart generate failed: {str(e)}"
        stack_trace = traceback.format_exc()
        error_msg = f"图表生成失败 (chart_generate_agent): \n错误类型: {type(e).__name__}\n错误信息: {str(e)}\n堆栈跟踪:\n{stack_trace}"
        print(f"\n\n===== CHART GENERATE AGENT ERROR =====\n{error_msg}\n===========================\n\n")
        writer(f"<div style='color: red; background: #ffeeee; padding: 10px; border-radius: 5px; margin: 10px 0;'><b>图表生成出错</b>: {str(e)}</div>")
        return f"查询执行失败: {str(e)}---{stack_trace}"



# 创建自定义JSON编码器处理特殊类型
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # 处理Decimal类型
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # 处理Date类型
        elif isinstance(obj, date) and not isinstance(obj, datetime):
            return obj.isoformat()
        # 处理DateTime类型
        elif isinstance(obj, datetime):
            return obj.isoformat()
        # 处理bytes类型
        elif isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        # 处理集合类型
        elif isinstance(obj, set):
            return list(obj)
        # 处理其他不可序列化类型
        try:
            return str(obj)
        except:
            return f"不可序列化对象: {type(obj).__name__}"
        # 其他类型使用默认编码器处理
        return super(CustomJSONEncoder, self).default(obj)

@tool
def execute_sql_query(workspace: str, sql: str) -> Any:
    """执行给定SQL语句并返回查询结果。

    Args:
        workspace: 工作区名称
        sql: 要执行的SQL语句
    
    Returns:
        JSON格式的SQL查询结果
    """
    try:
        print("\n\n SQL to execute: ", sql)
        writer = get_stream_writer()
        writer(f"<div style='font-size: 0.9em; color: #666; font-style: italic;'> 🔧 <b>Tool开始执行: execute_sql_query </b>")
        
        dbmanger = get_dbmanager(workspace)
        query_result = dbmanger.execute_query(sql)

        writer(f" 🔧 <b>execute_sql_query 执行结束 </b> </div>")

        # 使用自定义JSON编码器处理特殊类型
        print(f"\n\n sql execute result: {query_result} \n\n")
        
        # 尝试使用自定义编码器进行JSON序列化
        try:
            return json.dumps(query_result, cls=CustomJSONEncoder)
        except Exception as json_err:
            print(f"JSON序列化失败: {str(json_err)}")
            # 退回到文本表示
            return f"查询结果 (文本格式):\n{str(query_result)}"
            
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_msg = f"SQL执行失败: \n错误类型: {type(e).__name__}\n错误信息: {str(e)}\n堆栈跟踪:\n{stack_trace}"
        print(f"\n\n===== SQL EXECUTION ERROR =====\n{error_msg}\n===========================\n\n")
        writer(f"<div style='color: red; background: #ffeeee; padding: 10px; border-radius: 5px; margin: 10px 0;'><b>SQL执行出错</b>: {str(e)}</div>")
        return f"<details><summary style='color: red;'><b>SQL执行失败</b>: {str(e)}</summary><pre style='background: #f8f8f8; padding: 10px; overflow: auto;'><code>{sql}</code>\n\n{stack_trace}</pre></details>"

@tool
def run_code(code: str) -> any:
    """使用E2B沙箱执行Python代码，支持数据分析和可视化。
    
    Args:
        code: 要执行的Python代码，应当是完整且自包含的，包括所有必要的导入语句。
             可以直接使用的类库：
             - jupyter
             - numpy
             - pandas
             - matplotlib
             - seaborn
    Returns:
        代码执行的结果，包括输出、错误信息和生成的图表（如果有）
    """
    try:
        writer = get_stream_writer()
        writer(f"<div style='font-size: 0.9em; color: #666; font-style: italic;'> 🔧 <b>Tool开始执行: run_code </b>")

        # 获取沙箱实例
        sandbox = Sandbox()
        print("sandbox create, code to execute: ", code)    
        
        # 执行代码
        execution = sandbox.run_code(code)
        
        # 打印完整的结果结构
        print('Code execution finished!')
        print(f'Results: {execution.results}')

        # 检查结果中是否包含PNG图像, 保存图片到文件
        first_result = execution.results[0]
        if first_result.png:
        # Save the png to a file. The png is in base64 format.
            with open('./tmp/chart.png', 'wb') as f:
                f.write(base64.b64decode(first_result.png))
            print('Chart saved as chart.png')
            
        html_image = f"""
        <div>
            <img src="data:image/png;base64,{first_result.png}" style="max-width: 100%;">
        </div>
        """

        writer(f" 🔧 <b>run_code 执行结束 </b> </div>")
        return html_image
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_msg = f"代码执行失败: \n错误类型: {type(e).__name__}\n错误信息: {str(e)}\n堆栈跟踪:\n{stack_trace}"
        print(f"\n\n===== CODE EXECUTION ERROR =====\n{error_msg}\n===========================\n\n")
        writer(f"<div style='color: red; background: #ffeeee; padding: 10px; border-radius: 5px; margin: 10px 0;'><b>代码执行出错</b>: {str(e)}</div>")
        
        code_with_line_numbers = "\n".join([f"{i+1}: {line}" for i, line in enumerate(code.split("\n"))])
        return f"""
        <details>
            <summary style='color: red;'><b>代码执行失败</b>: {str(e)}</summary>
            <div style='background: #f8f8f8; padding: 10px; overflow: auto; margin-top: 10px;'>
                <h4>执行的代码:</h4>
                <pre><code>{code_with_line_numbers}</code></pre>
                <h4>错误堆栈:</h4>
                <pre>{stack_trace}</pre>
            </div>
        </details>
        """



if __name__ == "__main__":
    DEBUG = False
    main()

