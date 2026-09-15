print("=" * 56)
"""
    실습용 사이트에서 종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출
    - 요청 주소: ??
    TODO: 오늘 (09/15) 18시까지 이메일로 제출 (정적 페이지)
"""
import re
import requests  # HTTP 요청(GET/POST 등)을 보내고 응답을 받기 위한 라이브러리
from bs4 import BeautifulSoup  # 응답받은 HTML 문자열을 태그 구조(DOM)로 다룰 수 있게 해주는 라이브러리

BASE = "https://kh-lab.rockua.ai.kr"
TIMEOUT = 5
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

# requests.get(url, params=...): params에 넘긴 dict는 자동으로 "?key=value" 형태의 쿼리스트링으로 붙여서 요청한다
resp = requests.get(f"{BASE}/stocks", params={"sector": "S08"}, headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()  # 응답 코드가 200이 아니면(요청 실패) 예외를 발생시켜서 이후 코드가 실행되지 않도록 막는다
resp.encoding = "utf-8"  # 응답 문자열의 인코딩을 명시적으로 utf-8로 지정해 한글이 깨지지 않도록 한다
html = resp.text  # 응답 본문(HTML 문자열)만 꺼낸다

print(f"요청 주소: {resp.url}")
print(f"상태 코드: {resp.status_code} / 본문 길이: {len(html):,}자")
print("=" * 95)

# BeautifulSoup(html, 'lxml'): 문자열 형태의 html을 태그 트리 구조로 변환(파싱)해서 soup 객체로 만든다
soup = BeautifulSoup(html, "lxml")

# select("tr.stock-row"): CSS 선택자와 일치하는 모든 태그를 리스트로 반환한다 (없으면 빈 리스트)
rows = soup.select("tr.stock-row")
print(f"IT서비스 섹터 종목 개수: {len(rows)}")
print("=" * 95)

def get_text(node, selector, default=""):
    # select_one(selector): 조건에 맞는 첫 번째 태그 1개만 반환한다 (없으면 None)
    tag = node.select_one(selector)
    # get_text(strip=True): 태그 안의 텍스트만 꺼내면서 앞뒤 공백/줄바꿈을 제거한다
    return tag.get_text(strip=True) if tag else default

def get_number(node, selector, default=0):
    text = get_text(node, selector)
    # re.sub(r"[^\d]", "", text): 정규식을 이용해 숫자(\d)가 아닌 문자를 전부 빈 문자열로 치환(제거)한다
    numbers = re.sub(r"[^\d]", "", text)
    return int(numbers) if numbers else default

def parse_rate(text, default=None):
    if not text:
        return default
    # re.search(r"-?[\d.]+", text): 부호(-)와 소수점을 포함한 숫자 패턴을 문자열에서 찾아낸다
    m = re.search(r"-?[\d.]+", text)
    return float(m.group()) if m else default

stocks = []
for row in rows:
    stocks.append({
        "code": get_text(row, "td.col-code"),
        "name": get_text(row, "td.col-name a"),
        "sector": get_text(row, "td.col-sector"),
        "price": get_number(row, "td.col-price"),
        "rate": parse_rate(get_text(row, "td.col-change")),
        "volume": get_number(row, "td.col-volume"),
        "market": get_text(row, "td.col-market span"),
    })

# f"{값:<8}" 처럼 콜론 뒤에 정렬 기호(<좌측, >우측)와 폭을 지정하면 표 형태로 출력할 수 있다
print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}{'거래량':>12}{'시장':>12}")
for s in stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12,}{s['rate']:>8}%{s['volume']:>12,}{s['market']:>12}")
print("=" * 95)