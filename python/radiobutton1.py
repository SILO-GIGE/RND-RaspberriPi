"""
#토핑고르기 라디오버튼 위젯
import tkinter as tk

win = tk.Tk()
v = tk.IntVar()
f = ('݉맑은고딕', 16)
L1 = tk.Label(win, text='''당신의 아이스크림의 토핑을 고르시오.''', justify='left', font=f)
L1.pack(anchor=tk.W, padx=20)
R1 = tk.Radiobutton(win, text='초콜릿', font=f, variable=v, value=0)
R1.pack(anchor=tk.W, padx=20)
R2 = tk.Radiobutton(win, text='딸기', font=f, variable=v, value=1)
R2.pack(anchor=tk.W, padx=20)
R3 = tk.Radiobutton(win, text='쿠키', font=f, variable=v, value=2)
R3.pack(anchor=tk.W, padx=20)
win.mainloop()
"""
# Radiobutton위젯 - 토핑고르기
import tkinter as tk

data = {0: '없음', 1: '초콜릿', 2: '딸기', 3: '쿠키'}

def choose():
    L2.config(text=f'{data[v.get()]} 선택!')

win = tk.Tk()
v = tk.IntVar()
f = ('݉맑은고딕', 16)
L1 = tk.Label(win, text='''당신의아이스크림의 토핑을 고르시오.''', justify='left', font=f)
L1.pack(anchor=tk.W, padx=20)

for k, st in data.items():
    tk.Radiobutton(win, text=st, font=f, variable=v, value=k, command=choose).pack(anchor=tk.W, padx=20)

L2 = tk.Label(win, text='없음!', font=f)
L2.pack(padx=20)

win.mainloop()
