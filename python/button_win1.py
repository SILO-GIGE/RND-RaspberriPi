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
