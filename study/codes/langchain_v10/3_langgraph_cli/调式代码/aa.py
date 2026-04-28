import requests

url = 'http://127.0.0.1:2024/threads'

res = requests.post(url,
    headers={
      "Content-Type": "application/json"
    },
    json={
      "thread_id": "",
      "metadata": {},
      "if_exists": "raise",
      "ttl": {
        "strategy": "delete",
        "ttl": 1
      },
      "supersteps": [
        {
          "updates": [
            {
              "values": [
                {}
              ],
              "command": {
                "update": None,
                "resume": None,
                "goto": {
                  "node": "",
                  "input": None
                }
              },
              "as_node": ""
            }
          ]
        }
      ]
    }
)


print(res.text)