"""
집에서 즐기는 탁구 - 3x3 구역 화면 출력 (grid.c 의 파이썬 버전)

구역 번호 배치 (사용자 기준, 거울 모드 기준):
  +---+---+---+
  | 1 | 2 | 3 |
  +---+---+---+
  | 4 | 5 | 6 |
  +---+---+---+
  | 7 | 8 | 9 |
  +---+---+---+

실행:  python grid.py
"""

import os
import random
import sys
import time

GRID_SIZE = 3   # 3x3
CELL_W = 11     # 칸 가로 폭(문자 수)
CELL_H = 5      # 칸 세로 높이(줄 수)


def enable_ansi():
    """Windows 10 이상 콘솔에서 ANSI 이스케이프 코드를 사용하도록 설정"""
    if os.name == "nt":
        os.system("")  # 빈 명령 실행만으로 가상 터미널 처리가 켜진다


def clear_screen():
    sys.stdout.write("\033[H\033[J")


def print_border():
    """+-----------+-----------+-----------+ 형태의 가로 경계선"""
    print(("+" + "-" * CELL_W) * GRID_SIZE + "+")


def cell_line(cell_no, line, is_target):
    """
    한 칸의 한 줄(line: 0 ~ CELL_H-1)을 문자열로 만든다.
    - 가운데 줄에는 구역 번호
    - target 칸이면 반전 색상으로 강조하고 위쪽에 공(O) 표시
    """
    buf = [" "] * CELL_W

    if line == CELL_H // 2:
        buf[CELL_W // 2] = str(cell_no)
    if is_target and line == 1:
        buf[CELL_W // 2] = "O"

    text = "".join(buf)
    if is_target:
        text = "\033[7m" + text + "\033[0m"  # 반전 시작 / 끝
    return "|" + text


def draw_grid(target=0):
    """
    3x3 화면을 그린다.
    target: 공이 오는 구역 번호(1~9), 표시가 없으면 0
    """
    clear_screen()
    print_border()

    for row in range(GRID_SIZE):
        for line in range(CELL_H):
            parts = []
            for col in range(GRID_SIZE):
                cell_no = row * GRID_SIZE + col + 1
                parts.append(cell_line(cell_no, line, cell_no == target))
            print("".join(parts) + "|")
        print_border()

    if target > 0:
        print(f"공이 {target}번 구역으로 옵니다!")
    else:
        print("준비...")
    sys.stdout.flush()


def main():
    enable_ansi()

    # 처음엔 표시 없이 그리드만 출력
    draw_grid(0)
    time.sleep(1.5)

    # 데모: 랜덤 구역을 10번 표시 (이후 게임 로직에서 이 부분을 대체)
    for _ in range(10):
        target = random.randint(1, 9)
        draw_grid(target)
        time.sleep(1.0)


if __name__ == "__main__":
    main()
