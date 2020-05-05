import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import random

cols = 30 #列数
rows = 16 #行数
mine_size = 30

class mineFrame():
    def __init__(self, canvas):
        self.canvas = canvas
        self.init()
        
    def init(self):
        self.mines_total = 99
        self.mine_table = [[0] * cols for _ in range(rows)]
        self.mine_status_table = [[''] * cols for _ in range(rows)]
        # '':初始状态    '*'：标记为地雷   '?'：标记为问号   '0'-'8'：揭开了
        for i in range(cols):
            for j in range(rows):
                self.mine_table[j][i] = 0
                self.mine_status_table[j][i] = ''
            
    # 随机安插地雷
    def spread_mines(self,c,r):
        c1,r1,c2,r2 = self.get_around(c,r)
        mines = 0
        while mines < self.mines_total :
            c0 = random.randint(0,cols-1)
            r0 = random.randint(0,rows-1)
            if not (c1 <= c0 <= c2 and r1 <= r0 <= r2):
                if self.mine_table[r0][c0] == 0:
                    self.mine_table[r0][c0] = 1
                    mines += 1
    
    def get_around(self, c, r): # 返回某处周围的范围
        c1 = max(0,c-1)
        c2 = min(cols,c+2)
        r1 = max(0,r-1)
        r2 = min(rows,r+2)
        return (c1,r1,c2,r2)
    
    def get_aroundmines(self, c, r): # 数出某处周围的地雷数
        c1,r1,c2,r2 = self.get_around(c,r)
        count = 0
        for i in range(r1,r2):
            for j in range(c1,c2):
                if self.mine_table[i][j] and not(i == r and j == c):
                    count += 1
                
        return(count)
    
    def count_around_marked_mines(self, c, r): 
        # 数出某处周围已经标记的地雷数
        c1,r1,c2,r2 = self.get_around(c,r)
        mine_marked = 0
        for i in range(r1,r2):
            for j in range(c1,c2):
                if self.mine_status_table[i][j] == '*' \
                    and not(i == r and j == c):
                    mine_marked += 1
                
        return(mine_marked)
    def count_around_not_marked(self, c, r): 
        # 数出某处周围已经标记的地雷数
        c1,r1,c2,r2 = self.get_around(c,r)
        not_marked = 0
        for i in range(r1,r2):
            for j in range(c1,c2):
                if self.mine_status_table[i][j] == '' \
                    and not(i == r and j == c):
                    not_marked += 1
                
        return(not_marked)
    
    def draw_mine(self):
        self.canvas.create_rectangle(0,0,cols*mine_size,rows*mine_size,width=3)
        for c in range(cols):
            for r in range(rows):
                x0 = c * mine_size
                y0 = r * mine_size                
                self.canvas.create_rectangle(x0+1,y0+1,
                                             x0+mine_size-1,y0+mine_size-1,                    
                    fill="#BDB76B",outline="#dcdcdc",width=2)
    def draw_tip(self,c,r,color='red'):
        x0 = c * mine_size
        y0 = r * mine_size                
        self.canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
            fill="#BDB76B",outline=color,width=2)
    
    def markmine(self, c, r, s): # s为'','*','?','1-8'
        x0 = c * mine_size
        y0 = r * mine_size
        if s in ('', '*', '?') :
            self.canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
                    fill="#BD7D6B",outline="#dcdcdc",width=2)
            self.canvas.create_text(x0+15,y0+18,text=s,\
                font=tkFont.Font(family='黑体', size=24, weight=tkFont.BOLD))
        elif s == '0':
            self.canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
                    fill="#E0FFFF",outline="#dcdcdc",width=1)
        else :
            self.canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
                    fill="#E0FFFF",outline="#dcdcdc",width=1)
            self.canvas.create_text(x0+15,y0+15,text=s,\
                font=tkFont.Font(family='黑体', size=16, weight=tkFont.BOLD))
        
    def bomb(self):  # 地雷引爆了
        for i in range(rows):
            for j in range(cols):
                if self.mine_table[i][j] == 1 : # and self.mine_status_table[i][j] != '*'
                    self.markmine(j,i,'*') 
    
    def count_opened(self):
        count = 0
        for i in range(rows):
            for j in range(cols):
                if self.mine_status_table[i][j] not in ('','*','?'):
                    count += 1
        return count
        
    def tip(self,c,r):
        c1,r1,c2,r2 = self.get_around(c,r)
        if self.get_aroundmines(c,r) == self.count_around_not_marked(c,r) + \
            self.count_around_marked_mines(c,r):
            for i in range(c1,c2):
                for j in range(r1,r2):
                    if self.mine_status_table[j][i] =='':
                        self.draw_tip(i,j)
        if self.get_aroundmines(c,r) == self.count_around_marked_mines(c,r):
            for i in range(c1,c2):
                for j in range(r1,r2):
                    if self.mine_status_table[j][i] =='':
                        self.draw_tip(i,j,'green')                
        
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.create_widgets()

    def create_widgets(self):
        self.frame0 = tk.Frame(self,width=cols*mine_size, height=rows*mine_size) #左边框架，放置canvas
        self.frame0.pack(side='left')
        self.canvas = tk.Canvas(self.frame0, width=cols*mine_size, height=rows*mine_size) # 俄罗斯方块板
        self.canvas.pack()
        self.mineframe = mineFrame(self.canvas)    
        self.time = 0
        self.mines_remainder = self.mineframe.mines_total
        
        self.SVar1 = tk.StringVar()
        self.SVar1.set(str(self.time))
        self.SVar2 = tk.StringVar()
        self.SVar2.set(str(self.mines_remainder))
        
        self.frame1 = tk.Frame(self,width=80, height=rows*mine_size,bg="#cccccc") # 右边框架，防止标签等
        self.frame1.pack(side='right')

        self.label1 = tk.Label(self.frame1,textvariable=self.SVar1, font=("黑体", 20),bg="#cccccc")
        self.label1.place(x=10, y=30)   # 显示时间
        self.label2 = tk.Label(self.frame1,textvariable=self.SVar2, font=("黑体", 16),bg="#cccccc")
        self.label2.place(x=10, y=100)   # 显示剩余地雷数
        
        self.btnRestart = tk.Button(self.frame1,text="重新开始",width=8,command=self.newGame)
        self.btnRestart.place(x=5,y=200)  # 重新开始按钮
        self.btnTip = tk.Button(self.frame1,text="提示",width=8,command=self.tip)
        self.btnTip.place(x=5,y=250)  # 提示
    
    def tip(self):
        for i in range(rows):
            for j in range(cols):
                if self.mineframe.mine_status_table[i][j] \
                    in ('1','2','3','4','5','6','7','8'):
                    self.mineframe.tip(j,i)
                    
    
    def show_time(self):
        if self.time_stop:
            return
        self.time += 200
        self.SVar1.set(str(self.time//1000))
        self.master.after(200,self.show_time)
        
    def open(self,c,r):
        if self.mineframe.mine_table[r][c]:
            self.game_over()
        else:
            aroundmines = self.mineframe.get_aroundmines(c,r) 
            if aroundmines == 0:
                self.mineframe.mine_status_table[r][c] = '0'
                self.mineframe.markmine(c,r,'0')
                c1,r1,c2,r2 = self.mineframe.get_around(c,r)
                for i in range(c1,c2):
                    for j in range(r1,r2):     
                        if not (c == i and r == j):
                            if self.mineframe.mine_status_table[j][i] == '':
                                self.open(i,j) 
            else:
                self.mineframe.mine_status_table[r][c] = str(aroundmines) 
                self.mineframe.markmine(c,r,str(aroundmines))
        
        opened_mines = self.mineframe.count_opened()
        if opened_mines == (cols*rows-self.mineframe.mines_total):
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.win()

    #新开始一个游戏
    def newGame(self):
        self.time = 0
        self.SVar1.set(str(self.time//1000))
        self.mines_remainder = self.mineframe.mines_total
        self.SVar2.set(str(self.mines_remainder))
        self.time_stop = False
        self.firstclick = True

        self.mineframe.draw_mine()

        self.canvas.bind("<Button-1>", self.mouseLeftClick)
        self.canvas.bind("<Button-3>", self.mouseRightClick)

        self.master.update()
        
    def game_over(self):
        self.time_stop = True
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.mineframe.bomb()  # 地雷引爆了
        if messagebox.askretrycancel(title='揭开地雷！Game Over!',message='Try again?'):
            self.newGame()
    def win(self):
        self.time_stop = True
        s="恭喜你胜利了,用时%s秒"%(self.time//1000)
        if messagebox.askretrycancel(title=s,message='Try again?'):
            self.newGame()
    #鼠标左键事件
    def mouseLeftClick(self, event):
        c=event.x//mine_size
        r=event.y//mine_size
        if self.firstclick :
            self.firstclick = False
            self.mineframe.init()
            self.mineframe.spread_mines(c,r)
            self.show_time()
        if self.mineframe.mine_status_table[r][c] == '': #如果它没有被揭开，就揭开它
            self.open(c,r)
    #鼠标右键事件        
    def mouseRightClick(self, event):
        c=event.x//mine_size
        r=event.y//mine_size 
        if self.mineframe.mine_status_table[r][c]=='':   #原始状态
            self.mineframe.markmine(c,r,'*')
            self.mineframe.mine_status_table[r][c]='*'
            self.mines_remainder -= 1
            self.SVar2.set(str(self.mines_remainder))
        elif self.mineframe.mine_status_table[r][c]=='*':   #原始状态
            self.mineframe.markmine(c,r,'?')
            self.mineframe.mine_status_table[r][c]='?'
            self.mines_remainder += 1
            self.SVar2.set(str(self.mines_remainder))
        elif self.mineframe.mine_status_table[r][c]=='?':   #原始状态
            self.mineframe.markmine(c,r,'')
            self.mineframe.mine_status_table[r][c]=''
            
        elif self.mineframe.count_around_marked_mines(c,r) == \
                    self.mineframe.get_aroundmines(c,r):  #如果它周围地雷数不等于已经标注的地雷数
            c1,r1,c2,r2 = self.mineframe.get_around(c,r)
            for i in range(c1,c2):
                for j in range(r1,r2):     
                    if not (c == i and r == j):
                        if self.mineframe.mine_status_table[j][i] == '':
                            self.open(i,j)  # 把没有揭开的揭开


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.master.title("扫雷   岳慧练习作品")
    app.newGame()
    app.mainloop()