# test_websocket.py
import asyncio
import json
import websockets


async def test_websocket():
    uri = "ws://localhost:9115/chat"

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")

            # 发送查询
            query = {"query": "写个a.txt,随便写点什么",'thread_id':'123'}
            await websocket.send(json.dumps(query))
            print(f"Sent: {query}")

            # 接收流式响应
            print("Receiving streaming response:")
            while True:
                try:
                    response = await websocket.recv()
                    if response == "[END]":
                        print("\n[Stream ended]")
                        break
                    else:
                        # 实时打印每个 chunk，不换行
                        print(response, end="\n", flush=True)
                except websockets.exceptions.ConnectionClosed:
                    print("\nConnection closed")
                    break

    except Exception as e:
        print(f"Error: {e}")


# 运行测试
asyncio.run(test_websocket())