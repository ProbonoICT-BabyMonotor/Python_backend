import sys, os, time, random
import requests
from bs4 import BeautifulSoup
import winsound as sd

# lib install
###############################################################
try :                                                         #
    import speech_recognition as sr                           #
    from gtts import gTTS                                     #
    import feedparser                                         #
    from playsound import playsound                           #
except ImportError :                                          #
    os.system('python.exe -m pip install --upgrade pip')      #
    os.system('pip install SpeechRecognition')                #
    os.system('pip install gtts')                             #
    os.system('pip install feedparser')                       #
    os.system('pip install playsound==1.2.2')                 #
    sys.exit()                                                #
###############################################################

# TTS(Text to Speech)
###############################################################
def my_tts(text) :                                            #
    print('[AI] : ' + text)                                   #
    tts = gTTS(text = text, lang='ko')                        #
    file_name = 'voice.mp3'                                   #
    tts.save(file_name)                                       #
    p = playsound(file_name, True)                            #
    if os.path.exists(file_name) :                            #
        os.remove(file_name)                                  #
###############################################################

# RSS - google news feed
###############################################################
def my_news() :                                               #
    url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"#
    news_data = []                                            #
    news_rss = feedparser.parse(url)                          #
    for title in news_rss.entries :                           #
        news_data.append(title.title)                         #
    return news_data                                          #
###############################################################

# weather
################################################################################################################################
def weather_info() :                                                                                                           #
    url_weather = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8'     #
    html = requests.get(url_weather)                                                                                           #
    soup = BeautifulSoup(html.text, 'html.parser')                                                                             #
    #지역                                                                                                                      #
    location = soup.find('div', {'class': 'title_area _area_panel'}).find('h2', 'title').text                                  #
    #날씨 정보                                                                                                                 #
    weather = soup.find('div', {'class': 'weather_info'})                                                                      #
    #현재 온도                                                                                                                 #
    temp = weather.find('div', {'class': 'temperature_text'}).text.strip()[5:-1]                                               #
    #날씨 상태                                                                                                                 #
    status = weather.find('span', {'class':'weather before_slash'}).text                                                       #
    #체감                                                                                                                      #
    term = weather.find('dl',  {'class':'summary_list'}).find('dd', {'class':'desc'})                                          #
    term1 = term.text.strip()[:-1]                                                                                             #
    #습도                                                                                                                      #
    term2 = term.find_next('dd', {'class':'desc'}).text.strip()                                                                #
    #미세먼지                                                                                                                  #
    report = weather.find('ul',  {'today_chart_list'}).text.strip()                                                            #
    today = "오늘 {0} 날씨입니다. 현재 온도는 {1}도, 체감 온도는 {2}도, 습도 {3} 입니다.".format(location, temp, term1, term2) #
    today = today + report + "입니다. 오늘의 날씨 정보였습니다."                                                               #
    return today                                                                                                               #
################################################################################################################################

#STT : Speech to Text
########################################################################################
def callback(rec, audio) :                                                             #
    try :     
        start = time.time()
        speech = rec.recognize_google(audio, language='ko', show_all=True )
        print(start-time.time())#
        if speech == [] :                                                              #
            pass                                                                       #
        else :                                                                         #
            speech = str(speech['alternative'][0]['transcript'])                       #
            if speech in "안녕":
                sd.Beep(524*2**0, 500)
                print("[USER] : " + speech)                                                #
                ai(speech)
                
    except sr.UnknownValueError:                                                       #
        print("Google 음성 인식이 오디오를 이해할 수 없습니다.")                       #
    except sr.RequestError as e:                                                       #
        print("Google 음성 인식 서비스에서 결과를 요청할 수 없습니다.; {0}".format(e)) #
########################################################################################

#fortune
#################################################################################################################################
def fortune():                                                                                                                 #
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EB%A7%90%EB%9D%A0%20%EC%9A%B4%EC%84%B8' #
    lst = list()                                                                                                                #
    year = list()                                                                                                               #
    fortune_today = list()                                                                                                      #
    htmls = requests.get(url)                                                                                                   #
                                                                                                                                #
    if htmls.status_code == 200 : # <response [200]> - connected to the Internet!                                               #
        #print(htmls)                                                                                                           #
        #print(htmls.text)                                                                                                      #
        bs = BeautifulSoup(htmls.content, 'html.parser')                                                                        #
                                                                                                                                #
        for meta in bs.find_all('dd'):                                                                                          #
            lst.append(meta.get_text())                                                                                         #
        for meta in bs.find_all('dt'):                                                                                          #
            year.append(meta.get_text())                                                                                        #
        for meta in bs.find_all('p', class_="text _cs_fortune_text"):                                                           #
            fortune_today.append(meta.get_text())                                                                               #
                                                                                                                                #
    else :                                                                                                                      #
        print("Not connected to Internet!")                                                                                     #
                                                                                                                                #
    #title = year[2]                                                                                                            #
    #print(title.center(shutil.get_terminal_size().columns) + '\n')                                                             #
    #print(fortune_today[0]) #오늘 0 : 내일 1 등                                                                                #
    #print(lst[2])                                                                                                              #
                                                                                                                                #
    return fortune_today[0] + lst[2]                                                                                            #
#################################################################################################################################

#####################################################################################
def ai(speech) :                                                                    #                                                                                #
    if '뉴스' in speech :                                                           #
        texts = my_news()                                                           #
        my_tts('오늘 주요 뉴스입니다.')                                             #
        for text in texts[0:5] :                                                    #
            my_tts(text)                                                            #
    elif '날씨' in speech :                                                         #
        my_tts(weather_info())                                                   #
    elif '운세' in speech :                                                         #
        my_tts(fortune())  
        
    elif '농담' in speech :                                                         #
        f = open("joke.txt", "r", encoding="utf8")                                  #
        lines = f.readlines()                                                       #
        rnd = random.randint(0,len(lines)-1)                                        #
        temp = lines[rnd]                                                           #
        q, a = temp.split(",")                                                      #
        f.close()                                                                   #
        my_tts(q)                                                                   #
        my_tts(a)                                                                   #
    elif '종료' in speech :                                                         # 
        my_tts("다음에 또 만나요")                                                  #
        stop_listening(wait_for_stop=False)                                         #
    else :                                                                          #
        my_tts("다시 한번 말씀해주세요.")                                           #
                                                                                    #
#####################################################################################    

rec = sr.Recognizer()
try :
    mic = sr.Microphone(1)
except :
    os.system('pip install PyAudio')                           
    os.exit()
my_tts("무엇을 도와드릴까요?")
stop_listening = rec.listen_in_background(mic, callback)

while True :
    time.sleep(0.1)