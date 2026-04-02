#!/usr/bin/env python3
"""
Generate personalized greetings based on scene, recipient, and style

Usage:
    python generate_greeting.py --scene <scene> --recipient <recipient> --style <style>

Parameters:
    --scene: Greeting scene (daily, holiday, business, special)
    --recipient: Recipient type (friend, family, colleague, client)
    --style: Greeting style (formal, informal, brief, detailed)
"""

import argparse

# Greeting templates
greetings = {
    "daily": {
        "friend": {
            "formal": "你好！希望你今天一切顺利，心情愉快。",
            "informal": "嘿！最近怎么样？过得还好吗？",
            "brief": "你好！",
            "detailed": "你好！希望你今天有个美好的开始，工作顺利，生活愉快，记得照顾好自己哦！"
        },
        "family": {
            "formal": "亲爱的家人，你好！希望你一切安好。",
            "informal": "嘿，家人！最近怎么样？想你了！",
            "brief": "你好！",
            "detailed": "亲爱的家人，你好！希望你身体健康，心情愉悦，每一天都过得充实而快乐。"
        },
        "colleague": {
            "formal": "您好！希望您今天工作顺利。",
            "informal": "嘿，同事！今天工作怎么样？",
            "brief": "您好！",
            "detailed": "您好！希望您今天工作顺利，项目进展顺利，与同事合作愉快。"
        },
        "client": {
            "formal": "尊敬的客户，您好！希望您一切安好。",
            "informal": "您好！最近怎么样？",
            "brief": "您好！",
            "detailed": "尊敬的客户，您好！感谢您一直以来的支持与信任，希望您事业顺利，生活美满。"
        }
    },
    "holiday": {
        "friend": {
            "formal": "节日快乐！愿您在这个特别的日子里收获满满。",
            "informal": "节日快乐！玩得开心哦！",
            "brief": "节日快乐！",
            "detailed": "节日快乐！希望你在这个特别的日子里与亲朋好友共度美好时光，收获满满的快乐和幸福。"
        },
        "family": {
            "formal": "节日快乐，亲爱的家人！愿我们一起度过美好的时光。",
            "informal": "节日快乐，家人们！咱们一起好好庆祝！",
            "brief": "节日快乐！",
            "detailed": "节日快乐，亲爱的家人！希望我们能一起度过这个美好的节日，创造更多温馨的回忆。"
        },
        "colleague": {
            "formal": "节日快乐，尊敬的同事！愿您假期愉快。",
            "informal": "节日快乐，同事！好好放松一下！",
            "brief": "节日快乐！",
            "detailed": "节日快乐，亲爱的同事！希望您在假期里好好休息，充电后以更好的状态投入工作。"
        },
        "client": {
            "formal": "节日快乐，尊敬的客户！愿您和家人度过美好的假期。",
            "informal": "节日快乐！希望您过得开心！",
            "brief": "节日快乐！",
            "detailed": "节日快乐，尊敬的客户！感谢您一直以来的支持，希望您和家人度过一个温馨、快乐的假期。"
        }
    },
    "business": {
        "friend": {
            "formal": "您好！希望我们的合作能够顺利进行。",
            "informal": "嘿！咱们的合作一定会很愉快的！",
            "brief": "您好！",
            "detailed": "您好！很高兴能与您合作，希望我们能够携手共进，创造更加美好的未来。"
        },
        "family": {
            "formal": "亲爱的家人，您好！希望我们的事业能够蒸蒸日上。",
            "informal": "嘿，家人！咱们的事业一定会越来越红火的！",
            "brief": "您好！",
            "detailed": "亲爱的家人，您好！希望我们的事业能够蒸蒸日上，为我们的未来打下坚实的基础。"
        },
        "colleague": {
            "formal": "您好！希望我们能够紧密合作，共同完成工作目标。",
            "informal": "嘿，同事！咱们一起加油，把工作做好！",
            "brief": "您好！",
            "detailed": "您好！希望我们能够紧密合作，相互支持，共同完成工作目标，创造更好的业绩。"
        },
        "client": {
            "formal": "尊敬的客户，您好！感谢您选择我们的服务，我们将竭诚为您服务。",
            "informal": "您好！感谢您的支持，我们会努力做到最好！",
            "brief": "您好！",
            "detailed": "尊敬的客户，您好！感谢您选择我们的服务，我们将竭诚为您提供最优质的产品和服务，满足您的需求。"
        }
    },
    "special": {
        "friend": {
            "formal": "恭喜您！愿您在这个特别的时刻收获更多的幸福。",
            "informal": "恭喜你！太厉害了！",
            "brief": "恭喜！",
            "detailed": "恭喜你！在这个特别的时刻，我为你感到骄傲和开心，愿你未来的道路更加顺利，收获更多的幸福和成功。"
        },
        "family": {
            "formal": "亲爱的家人，恭喜您！愿我们一起分享这个喜悦的时刻。",
            "informal": "恭喜啦，家人！太高兴了！",
            "brief": "恭喜！",
            "detailed": "亲爱的家人，恭喜您！这个特别的时刻值得我们共同庆祝，愿我们一起分享这份喜悦，未来的日子更加美好。"
        },
        "colleague": {
            "formal": "恭喜您！您的努力和才华终于得到了认可。",
            "informal": "恭喜你！太棒了！",
            "brief": "恭喜！",
            "detailed": "恭喜您！您的努力和才华终于得到了认可，这是您应得的荣誉，希望您在未来的工作中取得更大的成就。"
        },
        "client": {
            "formal": "恭喜您，尊敬的客户！愿您的事业蒸蒸日上。",
            "informal": "恭喜您！太厉害了！",
            "brief": "恭喜！",
            "detailed": "恭喜您，尊敬的客户！您的成功是对您努力的最好回报，愿您的事业蒸蒸日上，未来更加辉煌。"
        }
    }
}

def generate_greeting(scene, recipient, style):
    """Generate a greeting based on the given parameters"""
    try:
        return greetings[scene][recipient][style]
    except KeyError:
        return "抱歉，无法生成符合要求的问候语，请检查参数是否正确。"

def main():
    parser = argparse.ArgumentParser(description='Generate personalized greetings')
    parser.add_argument('--scene', type=str, required=True, 
                        choices=['daily', 'holiday', 'business', 'special'],
                        help='Greeting scene')
    parser.add_argument('--recipient', type=str, required=True, 
                        choices=['friend', 'family', 'colleague', 'client'],
                        help='Recipient type')
    parser.add_argument('--style', type=str, required=True, 
                        choices=['formal', 'informal', 'brief', 'detailed'],
                        help='Greeting style')
    
    args = parser.parse_args()
    greeting = generate_greeting(args.scene, args.recipient, args.style)
    print(greeting)

if __name__ == "__main__":
    main()
