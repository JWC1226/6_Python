"""
    함수의 매개변수
"""
print("=" * 65)
print("기본값 매개변수")
print("=" * 40)

# 전달된 값이 없을 경우 기본값으로 저장해서 사용
def connect(host, port=8080, charset='utf-8'):
    print(f"전달된 정보: {host}:{port} ({charset})")
connect("localhost")
connect("localhost", 1521)
connect("localhost", 1521, "euc-kr")
    # 기본값이 있는 매개변수는 뒤쪽에 배치한다 !
# [TIP] 기본값으로 리스트·딕셔너리 같은 가변 객체를 쓰면 모든 호출이 같은 객체를 공유한다 → 기본값은 None 으로 두고 함수 안에서 새로 만든다 (파일 하단 참고)

print("=" * 40)
print("키워드 매개변수")
connect(port=1521, host='localhost')
    # 키워드를 지정하면 순서와 상관없이 값을 전달할 수 있다

print("=" * 40)
print("가변 매개변수")
    # 개수가 정해지지 않은 값들을 전달받을 때, 사용
def total(*numbers):
    print(f"전달 받은 값: {numbers} ({type(numbers)})")
    return sum(numbers)
print(f"total(1, 3) > {total(1, 3)}")
print(f"total(1, 3, 5, 7) > {total(1, 3, 5, 7)}")
print(f"total() > {total()}")

print("=" * 40)
print("키워드 가변 매개변수")
    # 특정 키워드를 지정하여 값들을 전달 받을 때、사용하는 방법이다
def create_user(**data):
    print(f"전달 받은 값: {data} ({type(data)})")
    for k, v in data.items():
        print(f"{k} : {v}")
create_user(name = "사용자", age = 25, address = "서울")
print("=" * 80)

def log(level, *messages, **options):
    print(f"level: {level}")
    print(f"messages : {messages}")
    print(f"options : {options}")
log("INFO", "서버가 시작되었습니다", "포트 번호는 8080 입니다", color="green", timestamp=True)
log("ERROR", color="red")


# ======================================================================
# [실무 TIP] 가변 기본값 함정 / 키워드 전용 매개변수(*)
# * 뒤에 오는 매개변수는 반드시 '이름=값' 형태로만 전달할 수 있어서, 인자 순서를 헷갈리는 실수를 막아준다
# ======================================================================
def add_item_wrong(item, bucket=[]):     # 기본값 리스트는 함수를 정의할 때 한 번만 만들어진다
    bucket.append(item)
    return bucket

def add_item(item, bucket=None):
    if bucket is None:
        bucket = []                       # 호출할 때마다 새 리스트
    bucket.append(item)
    return bucket

print(add_item_wrong("A"), add_item_wrong("B"))   # ['A', 'B'] ['A', 'B'] → 같은 리스트를 공유!
print(add_item("A"), add_item("B"))               # ['A'] ['B']

def send_mail(to, *, subject, retry=3):  # * 뒤의 subject, retry 는 키워드로만 전달 가능
    print(f"to={to}, subject={subject}, retry={retry}")
send_mail("user@kh.co.kr", subject="공지")
