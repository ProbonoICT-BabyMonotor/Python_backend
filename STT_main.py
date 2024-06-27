## https://console.picovoice.ai/

#####################################################################
## 프로그램 실행 전
## 마이크의 Device Index를 손보기 (Speech_recongition, pvrecorder)
## test_code > Test_mic_number.py 코드 실행하여 테스트
##
## 노트북 자체 마이크는 절대 안됨!! 소음 때문인지도..
#####################################################################


import os, sys, json, random, time
from urllib import request
from bs4 import BeautifulSoup
import asyncio
from chatGPT import callChatGPT
from function import baby_sleep, bed_function, sensor

try :
    import speech_recognition as sr                                                          
    import pvporcupine
    import pvleopard
    from pvrecorder import PvRecorder
    from gtts import gTTS    
    from playsound import playsound
    import feedparser                                    
except ImportError :
    os.system('pip install SpeechRecognition')                                                    
    os.system('pip install --upgrade pip')      
    os.system('pip install pvporcupine')                
    os.system('pip install pvrecorder')               
    os.system('pip install pvleopard') 
    os.system('pip install gtts')                      
    os.system('pip install feedparser') 
    os.system('pip install playsound==1.2.2')                           
    sys.exit() 

print("[대기] 잠시만 기다려주세요..")

## API Key Setting
f = open('access_key.json')
data = json.load(f)

async def my_tts(text):
    print('[AI] : ' + text)
    tts = gTTS(text=text, lang='ko')

    # 임시 음성 파일 경로 설정
    file_name = 'voice.mp3'
    file_path = os.path.abspath(file_name)

    # 음성 파일 저장
    tts.save(file_path)

    # 비동기적으로 재생
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, playsound, file_path)

    # 재생 후 파일 삭제
    if os.path.exists(file_path):
        os.remove(file_path)

# 예시: STT 함수 내부에서 비동기로 my_tts 호출
async def STT():
    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ko-KR')
            print('You said: {}'.format(text))
            await ai(text)  # ai 함수에서 my_tts를 호출할 때는 await 사용
        except Exception as err:
            print(err)
            await my_tts("잘 못 들었어요. 다시 말해주세요.")
            await STT()


### 뉴스 #############################################################
def my_news() :                                               
    url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    news_data = []                                            
    news_rss = feedparser.parse(url)                          
    for title in news_rss.entries :                           
        news_data.append(title.title)                         
    return news_data  

### 날씨 #############################################################
def weather_info() :                                                                                                           
    url_weather = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"    
    html = request.urlopen(url_weather)

    soup = BeautifulSoup(html, 'html.parser')                                                                             
    # location 태그를 찾습니다.
    output = ""
    for location in soup.select("location"):
        # 내부의 city, wf, tmn, tmx 태그를 찾아 출력합니다.
        city = location.select("city").string
        weather = location.select_one("wf").string
        min = location.select_one("tmn").string
        max = location.select_one("tmx").string
        
    #미세먼지                                                                                                                  
    today = "오늘 {0} 날씨입니다. 오늘 날씨는 {1}이고, 최고 온도는 {2}도, 최저 온도는 {3}도 입니다.".format(city, weather, max, min) 
    today = today + "오늘의 날씨 정보였습니다."                                                               
    return today                                    

### 운세 #############################################################
def fortune():                                                                                                                 
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EB%A7%90%EB%9D%A0%20%EC%9A%B4%EC%84%B8' 
    lst = list()                                                                                                                
    year = list()                                                                                                               
    fortune_today = list()                                                                                                      
    htmls = requests.get(url)                                                                                                   
                                                                                                                                
    if htmls.status_code == 200 : # <response [200]> - connected to the Internet!                                               
        #print(htmls)                                                                                                           
        #print(htmls.text)                                                                                                      
        bs = BeautifulSoup(htmls.content, 'html.parser')                                                                        
                                                                                                                                
        for meta in bs.find_all('dd'):                                                                                          
            lst.append(meta.get_text())                                                                                         
        for meta in bs.find_all('dt'):                                                                                          
            year.append(meta.get_text())                                                                                        
        for meta in bs.find_all('p', class_="text _cs_fortune_text"):                                                           
            fortune_today.append(meta.get_text())   

    else :                                                                                                                      
        print("Not connected to Internet!")  

    return fortune_today[0] + lst[2]

async def baby(speech):
    future1 = asyncio.ensure_future(my_tts("인공지능이 답변을 생성중입니다. 시간이 걸릴 수 있으니, 잠시 대기해주세요."))
    future2 = asyncio.ensure_future(callChatGPT(speech))
    
    await asyncio.gather(future1, future2)
    
    await my_tts(future2.result())

### 판단 #############################################################
async def ai(speech) :    
    #-------------------  침대 제어  -----------------------#
    ## 역류 방지
    if ('역류 방지' in speech and '켜' in speech) or '기울여' in speech:
        bed_function.backdraft()
    
    ## 트름 유도
    elif ('트름' in speech and '시켜줘' in speech) or ('트림' in speech and '시켜줘' in speech) or '트름 유도' in speech or '트림 유도' in speech:
        bed_function.burp()
    
    ## 침대 스윙    
    elif '스윙' in speech or '재워줘' in speech:
        bed_function.swing()
    
    ## 침대 고정
    elif '고정' in speech and '침대' in speech:
        bed_function.fix()
    
    #------------------- 수면 상태 (AI) -----------------------#
    ## 아기 수면 상태 체크
    elif ('자고 있어' in speech or '깨어 있어' in speech or '자는 중' in speech or '자니' in speech):
        baby_sleep.babySleep()
    
    ## ChatGPT
    elif ('인공' in speech and '지능' in speech) or 'ai' in speech or 'AI' in speech or 'gpt' in speech:
        await baby(speech)    
    
    #-------------------    센서    -----------------------#
    ## 현재 아기 상태 체크
    elif (('지금 아기' in speech and '어때' in speech) or ('지금 아이' in speech and '어때' in speech) or ('지금 아기' in speech and '상태' in speech and '어때' in speech) or ('지금 아이' in speech and '상태' in speech and '어때' in speech)):
        sensor.babyStatus()
    
    ## 주변 환경 체크
    elif ((('방 온도' in speech or '방 습도' in speech) and '어때' in speech) or (('온도' in speech or '습도' in speech) and '어떻게' in speech) or ('환경' in speech and '체크' in speech)):
        sensor.surroundings()
    
    #-------------------    기타    -----------------------#
    elif '뉴스' in speech :                                                           
        texts = my_news()                                                           
        await my_tts('오늘 주요 뉴스입니다.')                                             
        for text in texts[0:5] :                                                    
            await my_tts(text)

    elif '날씨' in speech :                                                         
        await my_tts("현재 날씨는 준비중이에요.")
        # await my_tts(weather_info())

    elif '운세' in speech :                                                         
        await my_tts(fortune())   
        
    elif '농담' in speech or '개그' in speech or '조크' in speech or '웃긴 얘기' in speech :                                                         
        f = open("joke.txt", "r", encoding="utf8")                                  
        lines = f.readlines()                                                       
        rnd = random.randint(0,len(lines)-1)                                        
        temp = lines[rnd]                                                           
        q, a = temp.split(",")                                                      
        f.close()                                                                   
        await my_tts(q)                                                                   
        await my_tts(a)

    elif '종료' in speech :                                                         
        await my_tts("다음에 또 만나요")                                                 
    
    else :                                                                          
        await my_tts("다시 한번 말씀해주세요.")
        await STT()

## Wake word Setting
porcupine = pvporcupine.create(
    access_key = data['key'],
    keyword_paths=[os.getcwd()+"\안녕_ko_windows_v3_0_0.ppn"],
    model_path=os.getcwd()+"\porcupine_params_ko.pv",
)

## STT Setting
leopard = pvleopard.create(access_key = data['key'], model_path=os.getcwd()+"\leopard_params_ko.pv")

f.close()


# Porcupine으로 키워드 감지 후 STT 함수 비동기 실행
async def detect_keyword():
    ## Mic Setting (device_index 변경해야함)
    
    # devices = PvRecorder.get_available_devices()
    # print(devices)
    
    recorder = PvRecorder(frame_length=512, device_index=1)
    recorder.start()
    while True:
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)
        if keyword_index == 0:
            recorder.delete()
            await my_tts("무엇을 도와드릴까요?")
            await STT()
            recorder = PvRecorder(frame_length=512, device_index=1)
            recorder.start()

# 비동기 루프 시작
async def main():
    # 임시 음성 파일 경로 설정
    file_name = 'turn_on.mp3'
    file_path = os.path.abspath(file_name)

    # 비동기적으로 재생
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, playsound, file_path)
    print("[실행 가능] 마이크가 준비되었습니다")
    
    await detect_keyword()

# 비동기 루프 실행
if __name__ == '__main__':
    asyncio.run(main())