import os, json, time

try :
    from pvrecorder import PvRecorder
    import pvporcupine
    import speech_recognition as sr 
    
except ImportError :
    os.system('pip install pvrecorder')
    os.system('pip install pvporcupine')                
    os.system('pip install SpeechRecognition')                                                    

# 폴더 위치 확인하기
f = open(os.getcwd()+'/access_key.json')
data = json.load(f)

def printLine():
    print("-" * 80);
    

def test_pvrecorder():
    ## Wake word Setting
    porcupine = pvporcupine.create(
        access_key = data['key'],
        keyword_paths=[os.getcwd()+"/안녕_ko_raspberry-pi_v3_0_0.ppn"],
        model_path=os.getcwd()+"/porcupine_params_ko.pv",
    )
    
    devices = PvRecorder.get_available_devices()
    for idx, val in enumerate(devices): 
        print(f"[{idx}] : {val} ")
        
    printLine()
    index = int(input("> 테스트 하고 싶은 기기의 번호를 눌러주세요.\n> 입력 : "))

    recorder = PvRecorder(frame_length=512, device_index=index)
    recorder.start()
    
    print("테스트 시작합니다. 10초 이내에 \"안녕\"이라고 말하세요.")
    
    start = time.time()
    Test = False
    while True:
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)
        
        if keyword_index == 0:
            print(f"[{index} : {devices[index]}] 기기 사용이 가능합니다.")
            Test = True
            break
            
        if time.time() - start > 10:
            break
    
    if not Test: 
        temp_input = input("테스트 실패했습니다. 다른 기기로 테스트 할까요? (Y/N) \n> 입력 : ")
        if temp_input == "Y": 
            test_pvrecorder()
    
def test_speech_recognition():
    recog = sr.Microphone.list_microphone_names()
    for idx, val in enumerate(recog):
        print(f"{idx} : {val}")
    
    printLine()
    index = int(input("> 테스트 하고 싶은 기기의 번호를 눌러주세요.\n> 입력 : "))

    print("테스트 시작합니다. 10초 이내에 \"안녕\"이라고 말하세요.")

    start = time.time()
    Test = False
    
    r = sr.Recognizer()
    with sr.Microphone(device_index=index) as source:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio, language='ko-KR')
            if "안녕" in text:
                print(f"[{index} : {recog[index]}] 기기 사용이 가능합니다.")
        
        except AttributeError:
            temp_input = input("연결되지 않은 기기입니다. 다른 기기로 테스트 할까요? (Y/N) \n> 입력 : ")
            if temp_input == "Y": 
                test_speech_recognition()
                
        except Exception as err:
            temp_input = input("테스트 실패했습니다. 다른 기기로 테스트 할까요? (Y/N) \n> 입력 : ")
            if temp_input == "Y": 
                test_speech_recognition()
                
        


def main():
    printLine()
    print("어떤 것을 테스트 하시겠어요?")
    print("1. pvrecorder / 2. speech_recognition [번호만 입력해주세요.]")
    num = int(input("> 입력 : "))
    
    if num == 1:
        test_pvrecorder()
    
    elif num == 2:
        test_speech_recognition()
    
    else:
        print("잘못 입력하셨습니다.")    
    
    

if __name__ == '__main__':
    main()