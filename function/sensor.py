from function import http_request_spring
# Spring으로 HTTP 요청 보내기

# 주변 환경 체크
def surroundings():
    pass

# 아기 현 상태 체크
def babyStatus():
    return http_request_spring.getRequest('/chatbot/sensor/babyStatus/now')