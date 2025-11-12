from langchain.agents.middleware import before_agent
from langchain_core.output_parsers import JsonOutputParser
from conn.llms import get_small_llm
small_llm = get_small_llm()|JsonOutputParser()

@before_agent
def query_change(state, runtime):
    query = state['messages'][0].content
    prompt = f'''
    用户query:{ query}
    
    判断用户query是否是要做出文件类型的请求,返回yes or no。以json返回, 字段
    - flag: yes or no
    (yes：代表是要做出一些文件的请求，除闲聊外，所有的请求都归为yes, 且代表要把做出的内容上传至对象存储中，则改写用户query,加入 "并且上传至对象存储,把下载地址给我"
    no：一般打招呼等内容不需要要做出文件，请直接返回用户query)
    
    只返回json字符串，不需要别的解释
    '''
    res = small_llm.invoke(prompt)
    if res['flag'] == 'yes':
        query += "并且上传至对象存储,把下载地址给我"

    return {"messages": [{"role": "user", "content": query}]}
