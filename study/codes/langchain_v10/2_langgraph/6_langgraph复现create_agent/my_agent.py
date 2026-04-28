from typing_extensions import TypedDict,Required,Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode
from langchain.messages import AnyMessage,SystemMessage
import operator
def create_agent(model, tools, system_prompt):

    class AgentState(TypedDict):
        messages: Required[Annotated[list[AnyMessage], operator.add]]
        # Required 必填参数
        # Annotated[参数类型，参数的更新方式] 添加类型注解
        # list[AnyMessage] # 列表类型
        # operator.add 列表的更新方式，添加元素

    # ReAct的system_prompt
    default_system_prompt = """
    你是一个智能助手，使用ReAct（Reasoning and Acting）模式解决问题。请按照以下步骤思考：

    1. 思考(Thought)：分析问题，决定下一步行动
    2. 行动(Action)：调用工具或回答问题
    3. 观察(Observation)：获取工具执行结果
    
    以下是用户自定义的system_prompt:
    """

    system_prompt = default_system_prompt + system_prompt
    model = model.bind_tools(tools) # 绑定工具
    # 两个节点
    # 1.model节点
    def model_node(state: AgentState):
        # 每次调用应当把system_prompt放在messages的开头
        messages = [SystemMessage(content=system_prompt)] + state['messages']
        # 模型调用
        return {'messages': [model.invoke(messages)]}
    # 2.工具节点 (ToolNode)

    # 条件函数
    def flag_fun(state):
        """判断是否是工具调用"""
        return 'true' if state['messages'][-1].tool_calls else 'false'

    agent = StateGraph(AgentState)
    agent.add_node('llm', model_node)
    agent.add_node('tools', ToolNode(tools))

    agent.add_edge(START, 'llm')
    agent.add_conditional_edges('llm',flag_fun,{'true':'tools', 'false':END})
    agent.add_edge('tools', 'llm')

    agent = agent.compile() # 编译

    return agent