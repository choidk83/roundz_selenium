import re

filename = 'ALZip1128.exe'

match = re.search(r'(_co|_go)', filename)
if match:
    # _co 또는 _go가 있는 경우
    repl_json = re.match(r'^[a-zA-Z]+', filename).group().lower() + '_co.json'
    if match.group() == '_co':
        dictionary = 'co'
    elif match.group() == '_go':
        dictionary = 'go'
else:
    # _co 또는 _go가 없는 경우
    repl_json = re.match(r'^[a-zA-Z]+', filename).group().lower() + '.json'
    dictionary = 'pub'
print(repl_json, dictionary)

# 이걸로 파일명으로 기업/공공용 구분해서 알툴즈 배포는 될 것 같음
# 알툴즈 변경은 html에서 제품별로 선택지를 추가해줘야함
# 예) 알집(pub), 알집(co), 알집(go) 이런식으로 선택지가 어마어마하게 추가가 되야 함
# 선택지에 따라 json 파일 값이 달라져야 하고 dictionary도 달라져야 함
# 예) 알집(go) 선택 시 json명: alzip_co.json / 딕셔너리: go가 되야 함
