"""
    BeautifulSoup
    : HTML 및 XML 문서에서 원하는 데이터를 쉽게 추출할 수 있도록 해주는 스크래핑 라이브러리이다
      1. requests 로 요청 후、문자열(html, xml)을 응답 받는다
      2. bs4의 find, select를 활용해서 특정 텍스트를 추출한다
"""
import requests
# ModuleNotFoundError: No Module named 'requests'
    # >> 해당 모듈 설치 필요! pip install requests
from bs4 import BeautifulSoup

# TODO: config 모듈에서 BASE, TIMEOUT, HEADERS 변수만 import
from config import BASE, TIMEOUT, HEADERS
resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()    # 200 이 아니면 예외를 발생
# [TIP] 같은 사이트에 여러 번 요청할 때는 requests.Session() 을 사용하면 연결을 재사용해서 빠르다 (11_pipeline/extract.py 참고)
html = resp.text
print(f"{BASE}/stocks    [{resp.status_code}] {len(html):,}자")
print("=" * 55)

# 문자열 >> 태그 구조
# bs4는 문자열을 DOM 트리처럼 다룰 수 있게 만들어준다
soup = BeautifulSoup(html, 'lxml')
print(f"title >> {soup.title.text if soup.title else '없음'}")

# 기존에 Javascript를 통해 DOM을 조작한 것처럼 bs이 같은 역할을 한다!
    # select (함수 이용): CSS 선택자를 사용하여 해당 요소들을 반환 / 없는 경우 [] (빈 리스트)
    # select_one: CSS 선택자를 사용하여 해당 요소 1개를 반환 / 없는 경우 None
rows_select = soup.select("tr.stock-row")
print(f"tr.stock-row 개수: {len(rows_select)}")
first = soup.select_one("tr.stock-row")
price_tag = first.select_one("td.col-price")
print(f"td.col-price text: {price_tag.text}")
print(f"td.col-price text: {price_tag.text!r}")

print("=" * 35)
# f-string 에서 !r 을 사용하면 repr() 이 호출되어 숨겨진 공백(\n, \t 등)까지 그대로 출력해준다
print(f"td.col-price text: {price_tag.get_text()!r}")
print(f"td.col-price text: {price_tag.get_text(strip=True)!r}")

# 속성 값을 추출하고자 할 때 >> get()
name_link = first.select_one("td.col-name a")
print(f"name_link['href']: {name_link['href']}")    # 직접 접근
print(f"name_link.get('href'): {name_link.get('href')}")    # .get() 메소드를 사용한 접근
print(f"name_link.get('href'): {name_link.get('href', '없음')}")    # .get() 메소드의 기본값을 설정

# TODO: 첫 번째 행의 전체 데이터를 추출
for sel in ["td.col-code", "td.col-name a", "td.col-sector", "td.col-price", "td.col-volume", "td.col-change", "td.col-market span"]:
    tag = first.select_one(sel)
    value = tag.get_text(strip=True) if tag else "없음"
    print(f"{sel:<20} {value}")


# ======================================================================
# [실무 TIP] 선택자 + 컴프리헨션으로 여러 값을 한 번에 추출
# select() 결과는 리스트이므로 컴프리헨션과 함께 쓰면 '모든 종목명', '모든 링크'를 한 줄로 뽑을 수 있다
# ======================================================================
names = [a.get_text(strip=True) for a in soup.select("tr.stock-row td.col-name a")]
links = [a.get("href") for a in soup.select("tr.stock-row td.col-name a")]
print(f"종목명 {len(names)}개: {names[:5]}")
print(f"링크 예시: {links[:2]}")
