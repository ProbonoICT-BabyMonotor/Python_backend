import os, sys, json
import asyncio

try:
    from openai import OpenAI

except ImportError:
    os.system("pip install openai")
    sys.exit()

async def callChatGPT(text):
    f = open('access_key.json')
    data = json.load(f)

    print("ChatGPT 호출중...")
    client = OpenAI(api_key=data['chatGPT'])
    completion = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "너는 초보 부모에게 도움을 줄 수 있는 존재야. 이 초보 부모들은 시각장애인이고, 주로 아기에 대해서 물어볼거야. 아기가 아플때 병원에 가라는 소리보다는 직접적으로 도움이 되는 조언 부탁해! 하지만 너무 길지 않게 이야기해줘. 300자 이내로 이야기해줘. 아기는 굉장히 0세에서 2세 사이의 나이를 가지고 있어"},
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content
