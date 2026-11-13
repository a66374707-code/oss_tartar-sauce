"""zone_grid.py의 3x3 구역에 랜덤으로 공이 날아오는 표시를 추가한 코드."""

# 기존 찬울이가 만든 3x3 구역(1~9)을 나눈 창만 띄우는 코드
import tkinter as tk
import random
import time  
 
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#공이 다가오는 표시 코드

arrive_min = 1.5 # 공이 도착하는데 걸리는 최소시간
arrive_max = 3.0 # 공이 도착하는데 걸리는 최대시간
ball_min = 0.02 # 공이 가장 작을 때의 반지름
ball_max = 0.20 # 공이 가장 클 때의 반지름
 
ball = {"zone": 0, "start": 0.0, "arrive": 0.0} # zone은 공이 올 구역 번호를 나타내는거라서 처음에는 0으로 둬서 아무구역도 아니라고 표시함 
        
def zone_center(canvas, zone):   
    w, h = canvas.winfo_width(), canvas.winfo_height() # 창의 크기
    cw, ch = w / GRID, h / GRID # 한 칸의 가로, 세로 길이
    row, col = divmod(zone - 1, GRID) #구역번호를 행과 열로 나타냄
    x1, y1 = col * cw, row * ch # 칸의 크기를 구현
    x2, y2 = x1 + cw, y1 + ch # 칸의 크기를 구현
    return (x1 + x2) / 2, (y1 + y2) / 2, min(cw, ch) # 중앙x, 중앙y 위치를 반환함(이 위치에 공을 그리기 위해서), min은 가로 세로 길이 중에서 더 작은 길이에 맞춰 그려야 칸을 벗어나지 않음
 
def ball_start():   
    ball["zone"] = random.randint(1, GRID * GRID) # 9구역중에서 랜덤으로 공이 나오게 함
    ball["arrive"] = random.uniform(arrive_min, arrive_max) # 1.5~3.0초 중에서 랜덤으로 도착하게 함
    ball["start"] = time.time() # 지금 시간을 출발 시간으로 저장함
    ball_move() # 공이 나타나고, 크기가 커지기 시작함
 
def ball_move(): 
    passed = time.time() - ball["start"] # 출발 후 지난 시간
    t = passed / ball["arrive"] # 공이 다 도착했는지(공의 크기가 다 커졌는지)를 표현
    if t > 1: # 공의 크기가 1을 넘지 않도록함(max로 정해둔 공의 크기보다 커지면 안되서)
        t = 1                            
 
    cx, cy, cell = zone_center(canvas, ball["zone"]) # 공이 올 칸의 중앙 좌표와 칸 크기
    size = ball_min + (ball_max - ball_min) * (t) # 공이 커지는 속도를 min을 최소로 놓고 t에따라 커지게 함
    r = cell * size # create_oval은 픽셀값만 받아서 반지름을 픽셀로 변환해야됨
 
    if t < 1:
        root.after(10, ball_move) # 공이 max크기까지 그려지기 전까지 0.010초 마다 다시 그림
    else:
        root.after(1000, ball_start) # 공이 다 도착했으니까 1초 뒤에 새로운 공을 다시 보냄

    canvas.delete("ball") # 칸과 숫자는 냅두고 공만 지움
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white", outline="black", width=3, tags="ball")
    # 중앙에서 반지름 r만큼 떨어진 원을 그림
    # width는 공의 테두리 두께,tags는 공을 지우고 다른곳에 공 위치를 나타낼때 공만 지우기 위해 공을 가리킬려고 만듦
    # 공을 탁구공처럼 흰색에다가 테두리 검은색으로 하긴했는데 숫자랑 똑같이 흰색이라 잘 안보임. 수정해야될듯(검은색 테두리 두께 넓혀도되고)
 

root.after(5000, ball_start) # 창이 뜨고 5초 뒤에 첫 공 출발(시작해놓고 탁구를 칠 자세를 잡아야하니까 5초로 정해둠. 이것도 나중에 바꾸거나 하면 될듯)
root.mainloop() # 없으면 바로 창이 꺼짐
