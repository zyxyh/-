from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont
import random
import time
root = Tk() #窗口
cols = 30 #列数
rows = 16 #行数
mine_size = 30
mines = 99  # 地雷总数
minesLeft = mines #剩余地雷数
#state = ('Blank','IsMine','NotSure','OPENED') #状态
mineArr = [[0] * cols for _ in range(rows)]  #二维数组赋值
mineStateArr = [[0] * cols for _ in range(rows)]  #二维数组赋值
mineWH = 20  #单个块的宽和高
root.title('扫雷')
root.minsize(680,330)
ft1 = tkFont.Font(family='微软雅黑', size=16, weight=tkFont.BOLD)
ft2 = tkFont.Font(family='微软雅黑', size=24, weight=tkFont.BOLD)
cv = Canvas(root,width=1004,height=500,bg = 'gray')
cv.create_rectangle(0,0,mineWH*cols,mineWH*rows,outline='black')
cv.pack(side='left')
strLeftMines = StringVar()
strLeftMines.set(str(minesLeft))
lbl2 = Label(root,textvariable=strLeftMines)
lbl2.place(x=630,y=150)

lbl1 = Label(root,fg='green')
lbl1.place(x=630,y=50)

counter = 0
def counter_label(label):
    def count():
        global counter
        counter += 1
        label.config(text=str(counter))
        label.after(1000, count)
    count()
counter_label(lbl1)
# 随机安插地雷
def distribute():
    for i in range(mines):
        while True :
            a = int(random.random() * cols)
            b = int(random.random() * rows)
            if mineArr[b][a] == 0:
                mineArr[b][a] = 1
                break

# 数出某处周围的地雷数    
def minecount(x,y):
    c = 0
    l1 = max(0,x-1)
    l2 = min(rows,x+2)
    r1 = max(0,y-1)
    r2 = min(cols,y+2)

    for i in range(l1,l2):
        for j in range(r1,r2):
            if mineArr[i][j] == 1:
               c += 1
            # c = c + mineArr[i][j]
    return(c)
def win():
    countOpened = 0
    for i in range(rows):
        for j in range(cols):
            if mineStateArr[i][j] == 4:
                countOpened += 1
    
    if countOpened == (rows * cols - mines):
        return True
    else:
        return False
    
def open(r,c):
    c1 = max(0,c-1)
    c2 = min(cols,c+2)
    r1 = max(0,r-1)
    r2 = min(rows,r+2)
    if mineStateArr[r][c] == 4:    # 4 = 表示被揭开了
        if minecount(r,c) != 0:    #并且周围地雷不等于0
            #求出周围被确定的地雷数
            mineMarked = 0
            for i in range(r1,r2):
                for j in range(c1,c2):
                    if  mineStateArr[i][j] == 1:
                        mineMarked += 1
            if mineMarked == minecount(r,c):  # 如果周围地雷找出来了，把周围没有被揭开的地雷揭开
                for i in range(r1,r2):
                    for j in range(c1,c2):     
                        if not (r == i and c == j):
                            if mineStateArr[i][j] == 0:
                                open(i,j)      
    elif mineStateArr[r][c] == 0:  # 0 = blank没有被揭开
        mineStateArr[r][c] = 4   # 4 = 表示被揭开了
        if mineArr[r][c] == 1:   # 是地雷
            gameover()
            #return
        else: #不是地雷
            minesAround =  minecount(r,c)  #求出周围地雷数
            if minesAround != 0:   #如果周围地雷数不是0，把地雷数标出来
                cv.create_rectangle(c*mineWH,r*mineWH,(c+1)*mineWH,(r+1)*mineWH,fill='white')                
                cv.create_text(c*mineWH+10,r*mineWH+10,text=str(minesAround),font=ft1) 
                # return
            else:    #如果周围地雷数是0，把周围的都揭开           
                for i in range(r1,r2):
                    for j in range(c1,c2):
                        if not (r == i and c == j):
                            cv.create_rectangle(c*mineWH,r*mineWH,(c+1)*mineWH,(r+1)*mineWH,fill='white')
                            open(i,j)
    if win():
        tryagain = tkinter.messagebox.askokcancel(title='恭喜你胜利了',message='再来一次?')
        if tryagain:
            newGame()        
#游戏结束
def gameover():
    for i in range(rows):
        y = i*mineWH
        for j in range(cols):
            x = j*mineWH
            if mineArr[i][j] == 1:
                if mineStateArr[i][j] != 1:
                    cv.create_text(x+10,y+14,text='*',font=ft2,fill = 'red') 
    if tkinter.messagebox.askretrycancel(title='Game Over',message='Try again?'):
        newGame()

#新开始一个游戏
def newGame():
    for i in range(rows):
        y = i*mineWH
        for j in range(cols):
            mineArr[i][j] = 0
            mineStateArr[i][j] = 0
            x = j*mineWH
            cv.create_rectangle(x,y,x+mineWH-1,y+mineWH-1,outline='red')
            cv.create_rectangle(x,y,x+mineWH-2,y+mineWH-2,fill='blue')
            #cv.create_text(x+10,y+10,text=str(mineStateArr[i][j]))
    distribute()
    global minesLeft     #每个函数里都要声明是全局变量才能修改函数外部的变量值
    minesLeft = mines    #恢复到原始值
    strLeftMines.set(str(minesLeft))
    global counter
    counter = 0
    counter_label(lbl1)

#鼠标左键事件
def mouseLeftClick(event):
    c=int(event.x/mineWH)
    r=int(event.y/mineWH)
    if c > cols-1 or r > rows-1: #如果在外面点击则返回
        return
    elif mineStateArr[r][c] == 0: #如果它没有被揭开，就揭开它
        open(r,c)
#鼠标右键事件        
def mouseRightClick(event):
    c=int(event.x/mineWH)
    r=int(event.y/mineWH) 
    if c > cols-1 or r > rows-1 :  #如果在外面点击则返回
        return
    
    if mineStateArr[r][c]==4:   #如果它已经被揭开了
        if minecount(r,c) != 0:  #如果它周围地雷数不等于0
            open(r,c)             #尝试把它周围的都揭开
    elif mineStateArr[r][c]==0:   #Blank
        cv.create_text(c*mineWH+10,r*mineWH+14,text='*',font=ft2,fill = 'red')
        mineStateArr[r][c]=1 # 标记为地雷
        global minesLeft
        minesLeft -= 1
        # print('Rbutton minesLeft=',minesLeft,mines)
        strLeftMines.set(str(minesLeft))
    elif mineStateArr[r][c]==1:   #已经标记为地雷
        mineStateArr[r][c]=2       #标记为问号 ？
        cv.create_rectangle(c*mineWH,r*mineWH,c*mineWH+mineWH-2,r*mineWH+mineWH-2,fill='blue')
        cv.create_text(c*mineWH+10,r*mineWH+10,text='?',font=ft1)
        minesLeft += 1
        strLeftMines.set(str(minesLeft))
    elif mineStateArr[r][c]==2:  #标记为？
        cv.create_rectangle(c*mineWH,r*mineWH,c*mineWH+mineWH-2,r*mineWH+mineWH-2,fill='blue')
        #cv.create_text(c*mineWH+10,r*mineWH+10,text=' ',font=ft1)
        mineStateArr[r][c]=0   #取消标记
    else:
        return        
         

btn = Button(root,text='New',command=newGame)
btn.place(x=630,y=200)

newGame()
root.bind("<Button-1>",mouseLeftClick)
root.bind("<Button-3>",mouseRightClick)
root.mainloop()