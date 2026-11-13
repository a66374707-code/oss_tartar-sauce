import re

NICKNAME_MAX = 15

def validate_nickname(nickname):
     """닉네임이 올바르면 None, 아니면 안내 메시지를 반환한다."""
     if not nickname:
        return "닉네임이 비어 있습니다."
     if len(nickname)> NICKNAME_MAX:
         return f"닉네임은 최대 {NICKNAME_MAX}자까지 입력할 수 있습니다."
     if not re.fullmatch(r"[A_Za-z0-9]+", nickname):
         return "닉네임은 영문과 숫자만 사용할 수 있습니다."
     return None
