"""3x3 구역(1~9)을 나눈 창만 띄우는 코드."""

import tkinter as tk

GRID = 3 #격자를 3칸씩 나눈다는 뜻 숫자를 바꾸면 몇x몇으로 구현됨
SIZE = 720 #창을 처음에 720×720 픽셀로 만든다는 뜻 나중에 수치는 바꾸엉야 할뜻 좀더 크게

def redraw(canvas): #canvas를 받아서 격자를 그리는 함수 redraw를 만든다
    canvas.delete("all") #이전 그림을 지우는 코드
    w, h = canvas.winfo_width(), canvas.winfo_height() # 창에 가로 길이와 세로 길이 w=가로, h=세로 why? 앞에서 창에 크기를 변형시켰을 경우 이 코드가 없다면 이상하게 그려짐
    cw, ch = w / GRID, h / GRID # #720를 3으로 나누어서 3칸으로 만든다는 의미

    for zone in range(1, GRID * GRID + 1): #아래 6줄이 9번 반복된다
        row, col = divmod(zone - 1, GRID) # row=행, col=열, divmod(a, b)는 몫과 나머지를 한 번에 준다. divmod(7, 3)은 (2, 1)이에요. (7 ÷ 3 = 몫 2, 나머지 1) 칸의 위치를 표시
       
        x1, y1 = col * cw, row * ch # 칸에 크기를 구현(칸을 위 코드에서 지정된 위치에 생성, 칸의 모서리 좌표 계산)
        x2, y2 = x1 + cw, y1 + ch # (x1, y1)은 칸의 왼쪽 위 모서리, (x2, y2)는 오른쪽 아래 모서리 *예시 row=1, col=2이면 x1 = 2x240, y1 = 1x240이므로 x2 = 480 + 240 = 720, y2 = 240 + 240 = 480이다.
       
        fill = "#2b3a4a" if (row + col) % 2 == 0 else "#34475a" # 만약 칸의 (row + col) % 2 가 0면 2b3a4a이 색깔로 색칠 아니면 34475a 이 색깔로 색칠한다. like 체스판
       
        canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="white", width=3) # 위에 코드에서 구한 칸의 모서리 좌표를 가지고 그곳에 위에서 fill색으로 안을 칠하고 테두리는 흰색 테두리 두께는 3인 사각형의 칸을 생성한다.
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(zone), fill="white", #생성한 칸 중앙 좌표((x1 + x2) / 2, (y1 + y2) / 2)에 그 칸에 숫자를 문자로 바꾸어 흰색으로, font=(글꼴, 크기, 굵기), min(cw, ch)는 둘 중 작은 값 거기에 0.22 곱해서 칸이 커지면 같이 커진다.
                           font=("TkDefaultFont", int(min(cw, ch) * 0.22), "bold"))


root = tk.Tk() # 창 만들기
root.title("(임시) 구역 나누기") # 생성되 창에 이름
canvas = tk.Canvas(root, width=SIZE, height=SIZE, bg="#111", highlightthickness=0) #생성된 창에 넣을 도화지를 720x720크기로 생성, 테두리를 없샘
canvas.pack(fill="both", expand=True) # 도화지를 창 안에 배치, 창이 커지면 같이 커지게 한다. 
canvas.bind("<Configure>", lambda e: redraw(canvas))   # 창 크기가 바뀌어도 다시 그림
root.bind("<Escape>", lambda e: root.destroy()) #ESC를 누르면 창이 꺼짐
root.mainloop() # 없으면 바로 창이 꺼짐
