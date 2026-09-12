"""
    with 문 (context manager)
    - 자원의 획득과 반납을 자동으로 처리하는 제어 구조
    - 블록을 벗어날 때, 자동으로 close 처리를 해준다 (직접 f.close() 불필요)
"""
import os   # 운영체제와 상호작용하여 파일 경로를 탐색、폴더 생성/삭제、환견 변수 조회 등을 지원하는 모듈이다.
import json # JSON 관련 변환 기능을 제공하는 모듈이다 (JSON <--> dict/list)
print("=" * 70)
print(__file__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 서비스 루트를 기준으로 파일명이 나오게 된다.
    # 습관적으로 abspath를 붙여서 절대 경로로 만들어주는 것이 좋다.
    # os.path.dirname(os.path.abspath(__file__)) >> 절대 경로에서 폴더 경로만 생성하게 된다.
# os.path.abspath(__file__) : 절대 경로를 반환한다.
# os.path.dirname(path) : 경로에서 폴더 경로만 반환한다.
print(BASE_DIR)
TXT_PATH = os.path.join(BASE_DIR, "_sample.txt")
JSON_PATH = os.path.join(BASE_DIR, "_sample.json")
print(f"TXT_PATH: {TXT_PATH}")
print(f"JSON_PATH: {JSON_PATH}")
print("=" * 70)

"""
# 직접 파일을 처리 (with X)
f = open(TXT_PATH, "w", encoding="utf-8")
f.write("금요일, 2026, 09, 11, 피곤\n")
f.close()  # close를 직접 호출해야 한다.
"""
# with 문을 사용하여 파일을 처리 (with O)
# mode="w" : 쓰기 모드
with open(TXT_PATH, "w", encoding="UTF-8") as f:
    f.write("금요일, 2026, 09, 11, 못감\n")
    f.write("토요일, 2026, 09, 12, HR 10km\n")
print(f"저장 완료 {os.path.basename(TXT_PATH)}")

# moder = "r" : 읽기 모드
with open(TXT_PATH, "r", encoding="UTF-8") as f:
    content = f.read()
print(f"[파일 내용]")
print(content)
print("=" * 70)

for line in content.strip().split("\n"):
    print(" ***** ")
    print(line)
print("=" * 70)
products = [
    {"code": "001123", "name": "iphone Duo", "price": 3300000},
    {"code": "004123", "name": "Galaxy Z Flip8", "price": 1680000},
]
"""
# JSOM으로 저장 (파일 쓰기)
with open(JSON_PATH, "w", encoding="UTF-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print(f" 저장 완료 {os.path.basename(JSON_PATH)}")
print(f"enssure_ascii=True >> {json.dumps(products, ensure_ascii=True)}")
print(f"enssure_ascii=False >> {json.dumps(products, ensure_ascii=False)}")
"""

# JSON으로 읽기 (파일 읽기)
with open(JSON_PATH, "r", encoding="UTF-8") as f:
    json_contents = json.load(f)
print(f"type > {type(json_contents)}")
for c in json_contents:
    # print(f"data type > {type(c)}")
    print(f"{c['name']}, {c['price']}")