## https://console.picovoice.ai/

import os, sys, json, time
import requests

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

## TTS 사용하여 음성 출력
def my_tts(text):
    print('[AI] : ' + text)
    tts = gTTS(text=text, lang='ko')
    file_name = 'voice.mp3'
    file_path = os.path.abspath(file_name)
    tts.save(file_path)
    playsound(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

def my_news() :                                               
    url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    news_data = []                                            
    news_rss = feedparser.parse(url)                          
    for title in news_rss.entries :                           
        news_data.append(title.title)                         
    return news_data  

## Wake word Setting
porcupine = pvporcupine.create(
    access_key = data['key'],
    keyword_paths=[os.getcwd()+"\안녕_ko_windows_v3_0_0.ppn"],
    model_path=os.getcwd()+"\porcupine_params_ko.pv",
)

## STT Setting
leopard = pvleopard.create(access_key = data['key'], model_path=os.getcwd()+"\leopard_params_ko.pv")

f.close()


## Mic Setting (device_index 변경해야함)
### devices = PvRecorder.get_available_devices()
recorder = PvRecorder(frame_length=512, device_index=1)
recorder.start()
print("[준비 완료] 마이크 입력이 준비되었습니다")

def STT():
    r = sr.Recognizer()
    with sr.Microphone(1) as source:
        print('Speack Anything :')
        audio = r.listen(source)
    
        try:
            text = r.recognize_google(audio, language='ko-KR')
            print('You said : {}'.format(text))
        except:
            my_tts("잘 못 들었어요. 다시 말해주세요.")
            STT()

while True:
    pcm = recorder.read()
    keyword_index = porcupine.process(pcm)
    if keyword_index == 0:
        recorder.delete()
        my_tts("무엇을 도와드릴까요?")
        STT()
        recorder = PvRecorder(frame_length=512, device_index=1)
        recorder.start()
        
        
        
        
        
