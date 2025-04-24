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

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    elif model_name == "gemini-2.0":
        return init_chat_model(model="gemini-2.0-flash-001", model_provider="google_vertexai", streaming=True)
    elif model_name == "gemini-2.5":
        return init_chat_model(model="gemini-2.5-pro-exp-03-25", model_provider="google_vertexai", streaming=True)
    else:
        raise ValueError(f"Unsupported model: {model_name}")    

def get_checkpointer():
    """缓存并返回MemorySaver实例"""
    return MemorySaver()

class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""
    # Runtime Variables
    next: str

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["data_retriever", "FINISH"]

TEAM_MEMBERS = ["data_retriever"]
RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"

def get_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("coordinator", coordinator_node)
    graph_builder.add_node("planner", planner_node)
    graph_builder.add_node("supervisor", supervisor_node)
    graph_builder.add_node("data_retriever", data_retriver_node)
    graph_builder.set_entry_point("coordinator")
    return graph_builder.compile(checkpointer=get_checkpointer())


def coordinator_node(state: State) -> Command[Literal["planner", "__end__"]]:
    logger.info("Coordinator talking.")

    system_prompt = coordinator.COORDINATOR_PROMPT
    # search_tool = TavilySearchResults(max_results=5)
    # tools = [search_tool]
    llm = get_model("gpt-4o")
    response = llm.invoke([SystemMessage(content=system_prompt)] + state["messages"])

    logger.info(f"Coordinator response: {response}")
    response_content = response.content

    goto = "__end__"
    if "handoff_to_planner" in response_content:
        goto = "planner"
    
    return Command(
        goto = goto,
    )


def planner_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
    logger.info("Planner talking.")
    
    # TODO, leave it blank for now.
    return Command(
        goto = 'supervisor',
    )


def supervisor_node(state: State) -> Command[Literal["data_retriever", "__end__"]]:
    """Supervisor node that decides which agent should act next."""
    logger.info("Supervisor evaluating next action")

    system_prompt = supervisor.SUPERVISOR_PROMPT
    llm = get_model("gpt-4.1").with_structured_output(schema=Router, method="json_mode")

    # preprocess messages to make supervisor execute better. add team name to the message
    messages = deepcopy(state["messages"])
    for message in messages:
        if isinstance(message, BaseMessage) and message.name in TEAM_MEMBERS:
            message.content = RESPONSE_FORMAT.format(message.name, message.content)

    response = llm.invoke([SystemMessage(content=system_prompt)] + messages)

    goto = response["next"]
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Supervisor response: {response}")

    if goto == "FINISH":
        goto = "__end__"
        logger.info("Workflow completed")
    else:
        logger.info(f"Supervisor delegating to: {goto}")

    return Command(
        goto=goto, 
        update={"next": goto}
    )


def data_retriver_node(state: State, config: RunnableConfig) -> Command[Literal["supervisor"]]:
    agent = get_data_retriver_agent();
    response = agent.invoke({"messages": state["messages"]}, config=config)
    data_result = response["messages"][-1].content

    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=data_result,
                    name="data_retriver",
                )
            ]
        },
        goto='supervisor'
    )


def get_data_retriver_agent():
    workspace = "yingkou-dw"
    dbtype = "bigquery"
    metadata = MetadataStore(workspace).query()
    system_prompt = dataquery.SQL_PROMPT.format(workspace=workspace, metadata=metadata, dbtype=dbtype)
    tools = [execute_sql_query]
    return create_react_agent(get_model("gpt-4.1"), tools, prompt=system_prompt)


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
    logger.info("\n\n SQL to execute: ", sql)
    writer = get_stream_writer()
    writer(f"<div style='font-size: 0.9em; color: #666; font-style: italic;'> 🔧 <b>Tool开始执行: execute_sql_query </b>")
    
    dbmanger = get_dbmanager(workspace)
    query_result = dbmanger.execute_query(sql)

    writer(f" 🔧 <b>execute_sql_query 执行结束 </b> </div>")
    logger.debug(f"\n\n sql execute result: {query_result} \n\n")
    
    try:
        return json.dumps(query_result, cls=CustomJSONEncoder)
    except Exception as json_err:
        logger.info(f"JSON序列化失败: {str(json_err)}")
        return f"查询结果 (文本格式):\n{str(query_result)}"



if __name__ == "__main__":
    try:
        graph = get_graph()
        # display(Image(graph.get_graph().draw_mermaid_png()))
        print(graph.get_graph().draw_ascii())
    except Exception as e:
        # This requires some extra dependencies and is optional
        print("Error: ", e)

