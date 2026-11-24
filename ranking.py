import json
import os
import re

NICKNAME_MAX = 15  # 닉네임 최대 글자 수
TOP_N = 10 # 순위표에 보여줄 순위 수
RANKING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking.json")


def validate_nickname(nickname):
    """닉네임이 올바르면 None, 아니면 안내 메시지를 반환한다."""
    if not nickname:
        return "닉네임이 비어 있습니다."
    if len(nickname) > NICKNAME_MAX:
        return f"닉네임은 최대 {NICKNAME_MAX}자까지 입력할 수 있습니다."
    if not re.fullmatch(r"[A-Za-z0-9]+", nickname):
        return "닉네임은 영문과 숫자만 사용할 수 있습니다."
    return None


def load_records(path=RANKING_FILE):
    """기록 파일을 읽어 {닉네임: 점수}를 반환한다.

    파일이 없으면 빈 기록으로 시작한다.
    파일을 열 수 없거나 손상된 경우 오류 메시지를 출력하고 빈 기록으로 시작한다.
    (프로그램은 종료되지 않는다.)
    """
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("기록 형식이 올바르지 않습니다.")
        return {str(name): int(score) for name, score in data.items()}
    except (OSError, ValueError, TypeError) as e:
        print(f"[오류] 기록 파일을 읽을 수 없어 새로 시작합니다: {e}")
        return {}


def save_records(records, path=RANKING_FILE):
    """기록을 파일에 저장한다."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def update_record(records, nickname, score):
    """같은 닉네임은 최고 점수 하나만 유지한다. 기록이 바뀌었으면 True, 아니면 False."""
    if nickname not in records or score > records[nickname]:
        records[nickname] = score
        return True
    return False

def get_top_n(records, n=TOP_N):
    """점수 높은 순으로 정렬해 상위 n개를 [(닉네임, 점수), ...]로 반환한다."""
    return sorted(records.items(), key=lambda item:item[1], reverse=True)[:n]

def get_rank(records, nickname):
    """전체 기록에서 이 닉네임의 순위를 반환한다. 동점이면 같은 순위."""
    best = records[nickname]
    return 1 + sum(1 for score in records.values() if score > best)

def submit_score(nickname,score,path=RANKING_FILE):
    """게임 종료 후 점수를 등록하고 상위 기록을 반환한다.
    닉네임 검사는 호출하는 화면에서 validate_nickname으로 먼저 수행 한다."""
    records = load_records(path)
    if update_record(records, nickname, score):
        save_records(records, path)
    return get_top_n(records)