"""랭킹 시스템 화면

게임과 연결하는 방법 (한 기기에서 여러 사람이 번갈아 플레이):

    nickname = ranking_gui.ask_nickname(root)       # 게임 시작 전
    if nickname is None:
        ...                                         # 취소했으면 게임 시작 안 함
"""
import tkinter as tk
from tkinter import messagebox, simpledialog

import ranking


def ask_nickname(parent):
    """게임 시작 전에 호출한다. 올바른 닉네임이 입력될 때까지 다시 묻고, 취소하면 None을 반환한다."""
    while True:
        nickname = simpledialog.askstring(
            "닉네임 입력",
            f"닉네임을 입력하세요 (영문·숫자, 최대 {ranking.NICKNAME_MAX}자)",
            parent=parent,
        )
        if nickname is None:
            return None
        error = ranking.validate_nickname(nickname)
        if error is None:
            return nickname
        messagebox.showerror("입력 오류", error, parent=parent)


if __name__ == "__main__":
    # 닉네임 입력창만 시험해 보는 창
    root = tk.Tk()
    root.title("랭킹 테스트")
    root.geometry("280x130")

    def on_start():
        nickname = ask_nickname(root)
        if nickname is None:
            messagebox.showinfo("취소", "닉네임 입력을 취소했습니다.", parent=root)
        else:
            messagebox.showinfo("입력 완료", f"{nickname}님, 환영합니다!", parent=root)

    tk.Button(root, text="게임 시작", command=on_start).pack(expand=True)
    root.mainloop()