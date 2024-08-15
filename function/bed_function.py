from function import http_request_spring
# Spring으로 HTTP 요청 보내기

# 역류 방지 기능
def backdraft():
    return http_request_spring.getRequest('/chatbot/bed/backdraft')

# 트름 유도 기능
def burp():
    return http_request_spring.getRequest('/chatbot/bed/burp')

# 스윙 기능
def swing():
    return http_request_spring.getRequest('/chatbot/bed/swing')

# 고정 기능
def fix():
    return http_request_spring.getRequest('/chatbot/bed/fix')

# 회전 기능
def spin():
    pass

# 뒤집기 기능
def turn():
    pass