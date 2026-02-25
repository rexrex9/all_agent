from langchain.agents import create_agent
from langchain.tools import tool
from conn.llms import get_llm
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(description="商品名称")
    price: float = Field(description="价格")

class Args(BaseModel):
    product: Product = Field(description="商品")

@ tool(name_or_callable="get_product_infom", description="提取商品信息", args_schema=Args)
def get_product_infom(product):
    print(product)
    return f"商品名称：{product.name}, 价格：{product.price}"


agent = create_agent(
    model=get_llm(), # 传一个llm
    tools=[get_product_infom], # 工具函数列表
    system_prompt="你是一个助手", # 系统提示
)

user_input = "在以下文本中提取商品信息，3块钱的杯子。"
res = agent.invoke(
    input={"messages": [{"role": "user", "content": user_input}]} # 用户输入
)

print(res["messages"][-1].content) # 打印AI的回复