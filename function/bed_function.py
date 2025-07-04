from function import http_request_spring
# Spring으로 HTTP 요청 보내기

# 역류 방지 기능
def backdraft():
    return http_request_spring.getRequest('/chatbot/bed/backdraft/on')

def backdraftOff():
    return http_request_spring.getRequest('/chatbot/bed/backdraft/off')

# 트름 유도 기능
def burp():
    return http_request_spring.getRequest('/chatbot/bed/burp/on')

# 스윙 기능
def swing():
    return http_request_spring.getRequest('/chatbot/bed/swing/on')

# 고정 기능
def fix():
    return http_request_spring.getRequest('/chatbot/bed/fix/on')

# 회전 기능
def spin():
    pass

# 뒤집기 기능
def turnLeft():
    return http_request_spring.getRequest('/chatbot/bed/flip/left/on')


def turnRight():
    return http_request_spring.getRequest('/chatbot/bed/flip/right/on')