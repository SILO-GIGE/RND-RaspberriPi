'''
#버튼클릭 간단예제
import tkinter as tk
def countUp(): # event
    global count
    count+=1
    #L.config(text=str(count))
    L['text']=str(count)
count=0
win=tk.Tk()
font1,font2=('݉맑은고딕', 36,'bold'),('݉맑은고딕', 16)
L=tk.Label(win,text='0',font=font1)
L.pack()
B=tk.Button(win,text='눌러봐!',width=20, height=2,
        command=countUp,font=font2)
B.pack()
win.mainloop()

'''

# 버튼 ++ -- exit표시
# 버튼에따라 숫자 변경
import tkinter as tk

def countUp():
    global count
    count+=1
    L.config(text=str(count))
def countDown():
    global count
    count-=1
    L.config(text=str(count))
count=0
win=tk.Tk()
font1,font2=('݉맑은고딕', 36,'bold'),('맑은고딕', 16)
L=tk.Label(win,text='0',font=font1)
L.pack(side=tk.TOP)
tk.Button(win,text='++',width=10,height=2,
        command=countUp,font=font2).pack(side=tk.LEFT)
tk.Button(win,text='--',width=10,height=2,
        command=countDown,font=font2).pack(side=tk.LEFT)
tk.Button(win,text='exit',width=10,height=2,
        command=win.destroy,font=font2).pack(side=tk.LEFT)
win.mainloop()


