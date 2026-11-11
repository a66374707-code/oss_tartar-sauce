/*
 * 집에서 즐기는 탁구 - 3x3 구역 화면 출력
 *
 * 구역 번호 배치 (사용자 기준, 거울 모드 기준):
 *   +---+---+---+
 *   | 1 | 2 | 3 |
 *   +---+---+---+
 *   | 4 | 5 | 6 |
 *   +---+---+---+
 *   | 7 | 8 | 9 |
 *   +---+---+---+
 *
 * 빌드:  gcc grid.c -o grid
 * 실행:  ./grid      (Windows: grid.exe)
 */

#define _DEFAULT_SOURCE  /* Linux/macOS에서 usleep 사용을 위해 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#define SLEEP_MS(ms) Sleep(ms)
#else
#include <unistd.h>
#define SLEEP_MS(ms) usleep((ms) * 1000)
#endif

#define GRID_SIZE 3   /* 3x3 */
#define CELL_W    11  /* 칸 가로 폭(문자 수) */
#define CELL_H    5   /* 칸 세로 높이(줄 수) */

 /* Windows 10 이상 콘솔에서 ANSI 이스케이프 코드를 사용하도록 설정 */
static void enable_ansi(void)
{
#ifdef _WIN32
    HANDLE h = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD mode = 0;
    if (h != INVALID_HANDLE_VALUE && GetConsoleMode(h, &mode)) {
        SetConsoleMode(h, mode | 0x0004); /* ENABLE_VIRTUAL_TERMINAL_PROCESSING */
    }
#endif
}

static void clear_screen(void)
{
    printf("\033[H\033[J");
}

/* +-----------+-----------+-----------+ 형태의 가로 경계선 */
static void print_border(void)
{
    for (int c = 0; c < GRID_SIZE; c++) {
        putchar('+');
        for (int i = 0; i < CELL_W; i++) putchar('-');
    }
    printf("+\n");
}

/*
 * 한 칸의 한 줄(line: 0 ~ CELL_H-1)을 출력한다.
 * - 가운데 줄에는 구역 번호
 * - target 칸이면 반전 색상으로 강조하고 위쪽에 공(O) 표시
 */
static void print_cell_line(int cell_no, int line, int is_target)
{
    char buf[CELL_W + 1];

    for (int i = 0; i < CELL_W; i++) buf[i] = ' ';
    buf[CELL_W] = '\0';

    if (line == CELL_H / 2)
        buf[CELL_W / 2] = (char)('0' + cell_no);
    if (is_target && line == 1)
        buf[CELL_W / 2] = 'O';

    putchar('|');
    if (is_target) printf("\033[7m");   /* 반전 시작 */
    printf("%s", buf);
    if (is_target) printf("\033[0m");   /* 반전 끝 */
}

/*
 * 3x3 화면을 그린다.
 * target: 공이 오는 구역 번호(1~9), 표시가 없으면 0
 */
static void draw_grid(int target)
{
    clear_screen();
    print_border();

    for (int row = 0; row < GRID_SIZE; row++) {
        for (int line = 0; line < CELL_H; line++) {
            for (int col = 0; col < GRID_SIZE; col++) {
                int cell_no = row * GRID_SIZE + col + 1;
                print_cell_line(cell_no, line, cell_no == target);
            }
            printf("|\n");
        }
        print_border();
    }

    if (target > 0)
        printf("공이 %d번 구역으로 옵니다!\n", target);
    else
        printf("준비...\n");
    fflush(stdout);
}

int main(void)
{
    enable_ansi();
    srand((unsigned)time(NULL));

    /* 처음엔 표시 없이 그리드만 출력 */
    draw_grid(0);
    SLEEP_MS(1500);

    /* 데모: 랜덤 구역을 10번 표시 (이후 게임 로직에서 이 부분을 대체) */
    for (int i = 0; i < 10; i++) {
        int target = rand() % 9 + 1;
        draw_grid(target);
        SLEEP_MS(1000);
    }

    return 0;
}
