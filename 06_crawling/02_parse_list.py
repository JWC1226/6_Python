"""
    목록 파싱
"""
import requests, json, csv
from bs4 import BeautifulSoup
from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, parse_stocks

resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()              # 응답 코드가 200이 아니면 예외를 발생
html = resp.text
soup = BeautifulSoup(html, 'lxml')
row = soup.select_one("tr.stock-row")
try:
    row.select_one("td.test").text   # 해당하는 클래스가 없을 때
except Exception as e:
    print(f"오류:: {e}")
print(f"td.test > {get_text(row, 'td.test')}")
print("=" * 70)

stocks = parse_stocks(html)
print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
for s in stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")
print("=" * 70)

# 파일로 저장
    # json
    # csv > 상품명, 가격, 재고
    #       아이폰, 3000000, 20

# json 저장하기
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
save_json(stocks, "stocks.json")
# 경로를 따로 지정하지 않을 경우, 현재 터미널 위치에 저장된다 (실행하는 위치)
# [TIP] Path(__file__).parent / "stocks.json" 처럼 "파일 기준" 경로를 쓰면 어디서 실행해도 같은 폴더에 저장된다

# csv 저장하기
def save_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        # [TIP] 엑셀에서 열 csv 는 encoding="utf-8-sig"(BOM 포함)로 저장해야 한글이 깨지지 않는다
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        # fieldnames > 컬럼 순서
        writer.writeheader()    # csv 파일 맨 첫 줄에 컬럼 이름들로 작성한다
        writer.writerows(data)  # dict 리스트 전체를 각각의 행으로 작성한다 (기록)
save_csv(stocks, "stocks.csv")


# ======================================================================
# [실무 TIP] pandas 로 바꿔서 다루기 - 딕셔너리 리스트 > DataFrame
# 수집 결과를 DataFrame 으로 바꾸면 정렬·필터 후 to_csv / to_json 으로 한 줄에 저장할 수 있다 (08_pandas 에서 자세히 다룬다)
# ======================================================================
import pandas as pd

stocks_df = pd.DataFrame(stocks)
print(stocks_df.sort_values("rate", ascending=False).head(3).to_string(index=False))
# stocks_df.to_csv("stocks.csv", index=False, encoding="utf-8-sig")    # 엑셀 호환 csv 저장
