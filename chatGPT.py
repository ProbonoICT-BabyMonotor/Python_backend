import os, sys, json

try:
    from openai import OpenAI

except ImportError:
    os.system("pip install openai")
    sys.exit()

def callChatGPT(text):
    f = open('access_key.json')
    data = json.load(f)

    client = OpenAI(api_key=data['chatGPT'])
    completion = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "너는 초보 부모에게 도움을 줄 수 있는 존재야. 이 초보 부모들은 시각장애인이고, 주로 아기에 대해서 물어볼거야. 아기가 아플때 병원에 가라는 소리보다는 직접적으로 도움이 되는 조언 부탁해!"},
            {"role": "user", "content": text},
        ],
    )

    return completion.choices[0].message.content
