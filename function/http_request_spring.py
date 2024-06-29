import requests, json

f = open('function/server_config.json')
ip = json.load(f)["ip"]
    
# GET 요청 보내기
def getRequest(goto):
    response = requests.get(ip+goto+"?memberNumber="+str(6))
    # print(response.json())       # JSON 응답 출력
    return response.status_code

# POST 요청 보내기 [추후 수정 필요]
def postRequest(goto):
    response = requests.post(ip+goto)
    response = requests.post('https://jsonplaceholder.typicode.com/posts', json=payload)
    print(response.status_code)  # 상태 코드 출력
    print(response.json())       # JSON 응답 출력
