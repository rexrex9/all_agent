
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from conn.llms import get_llm

class ContactInfo(BaseModel):
    """一个人的联系信息。"""
    name: str = Field(description="该人的姓名")
    email: str = Field(description="该人的电子邮件地址")
    phone: str = Field(description="该人的电话号码")

agent = create_agent(
    model=get_llm(),
    tools=[],
    response_format=ContactInfo  # 自动选择 ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "从如下文本中提取信息: John Doe, john@example.com, (555) 123-4567"}]
})


print(result)
# {'messages': [HumanMessage(content='从如下文本中提取信息: John Doe, john@example.com, (555) 123-4567', additional_kwargs={}, response_metadata={}, id='87f23507-5daf-4dc5-a6cd-b6b3e84e9104'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 47, 'prompt_tokens': 218, 'total_tokens': 265, 'completion_tokens_details': None, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'Qwen/Qwen3-Next-80B-A3B-Instruct', 'system_fingerprint': '', 'id': 'ff410762137549fd91a12ecaefc39560', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--36e83809-9198-406c-8afa-13308d3ddf19-0', tool_calls=[{'name': 'ContactInfo', 'args': {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}, 'id': 'call_8c064aa368484e56a49db889', 'type': 'tool_call'}], usage_metadata={'input_tokens': 218, 'output_tokens': 47, 'total_tokens': 265, 'input_token_details': {}, 'output_token_details': {}}), ToolMessage(content="Returning structured response: name='John Doe' email='john@example.com' phone='(555) 123-4567'", name='ContactInfo', id='995d9ffe-4416-4d50-be8f-a8dc7755ddbe', tool_call_id='call_8c064aa368484e56a49db889')], 'structured_response': ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')}
# 可以发现本质上是调用了一次工具，该工具提取的内容存到了"structured_response"这个字段中
print(result["structured_response"])
# name='John Doe' email='john@example.com' phone='(555) 123-4567'
print(type(result["structured_response"]))
# <class '__main__.ContactInfo'>
print(result["structured_response"].name)
# John Doe