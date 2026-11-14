import re
import os
import json

NICKNAME_MAX = 15
RANKING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking.json")

def validate_nickname(nickname):
     """닉네임이 올바르면 None, 아니면 안내 메시지를 반환한다."""
     if not nickname:
        return "닉네임이 비어 있습니다."
     if len(nickname)> NICKNAME_MAX:
         return f"닉네임은 최대 {NICKNAME_MAX}자까지 입력할 수 있습니다."
     if not re.fullmatch(r"[A-Za-z0-9]+", nickname):
         return "닉네임은 영문과 숫자만 사용할 수 있습니다."
     return None

def load_records(path=RANKING_FILE):
    """기록 파일을 읽어 {닉네임: 점수}를 반환한다.
    파일이 없으면 빈 기록으로 시작한다.
    파일을 열 수 없거나 손상된 경우 오류 메세지를 출력하고 빈 기록으로 시작한다.
    (프로그램은 종료되지 않는다.)"""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("기록 파일이 올바른 형식이 아닙니다.")
        return {str(name): int(score) for name, score in data.items()}
    except (OSError, ValueError, TypeError) as e:
         print(f"[오류] 기록 파일을 읽을 수 없어 새로 시작합니다: {e}")
    return {}
def save_records(records, path=RANKING_FILE):
    """기록을 파일에 저장한다."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
