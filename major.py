from online.major import Chat

c = Chat()


if __name__ == '__main__':
    from utils.general_utils.steam_util import stream_print
    cid = '3c46d42655b94e0f97b211ee2a371bb2'
    while True:
        user_input = input("用户：")
        res = c.chat(user_input, cid)
        stream_print(res)
