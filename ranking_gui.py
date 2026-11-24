"""랭킹 시스템 화면 (tkinter).

게임과 연결하는 방법 (한 기기에서 여러 사람이 번갈아 플레이):

    nickname = ranking_gui.ask_nickname(root)       # 게임 시작 전
    if nickname is None:
        ...                                         # 취소했으면 게임 시작 안 함
    ... 게임 플레이 ...
    ranking_gui.show_result(root, nickname, score)  # 게임 종료 후
"""
import random
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import ranking

FONT = "맑은 고딕"


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


def show_result(parent, nickname, score):
    """게임 종료 후 호출한다. 점수를 등록하고, 이번 점수와 TOP 10을 한 화면에 보여준다."""
    top = ranking.submit_score(nickname, score)

    win = tk.Toplevel(parent)
    win.title("결과")
    win.geometry("360x480")

    tk.Label(win, text=f"{nickname}님의 점수", font=(FONT, 12)).pack(pady=(15, 0))
    tk.Label(win, text=f"{score}점", font=(FONT, 28, "bold")).pack()
    tk.Label(win, text="TOP 10", font=(FONT, 16, "bold")).pack(pady=(15, 5))

    table = ttk.Treeview(win, columns=("rank", "name", "score"), show="headings", height=10)
    table.heading("rank", text="순위")
    table.heading("name", text="닉네임")
    table.heading("score", text="점수")
    table.column("rank", width=60, anchor="center")
    table.column("name", width=170, anchor="center")
    table.column("score", width=90, anchor="center")
    table.tag_configure("me", background="#ffe08a")   # 내 줄 강조

    for rank, (name, point) in enumerate(top, start=1):
        tag = ("me",) if name == nickname else ()
        table.insert("", "end", values=(rank, name, point), tags=tag)
    table.pack(padx=15)

    tk.Button(win, text="닫기", command=win.destroy).pack(pady=12)
    parent.wait_window(win)


if __name__ == "__main__":
    # 게임 없이 랭킹 화면만 시험해 보는 창 (점수는 랜덤)
    root = tk.Tk()
    root.title("랭킹 테스트")
    root.geometry("280x130")

    def on_play():
        nickname = ask_nickname(root)
        if nickname is None:
            return
        score = random.randint(0, 1000)   # 실제 게임에서는 플레이 결과 점수
        show_result(root, nickname, score)

    tk.Button(root, text="게임 시작 (랜덤 점수)", command=on_play).pack(expand=True)
    root.mainloop()