from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import random
from enum import Enum

cols = 30 #列数
rows = 16 #行数
mine_size = 30
MINE_COUNT = 99 # 地雷总数

class MineStatus(Enum):
    normal = 1  # 未点击
    opened = 2  # 已点击
    mine = 3    # 地雷
    flag = 4    # 标记为地雷
    ask = 5   # 标记为问号
    bomb = 6    # 踩中地雷
    hint = 7    # 被双击的周围
    double = 8  # 正被鼠标左右键双击
    # 
    
class GameStatus(Enum):
    ready = 1   # ready
    start = 2 
    over = 3    # game over
    win = 4     # win
    
def get_around(c, r):
    "返回(c, r)周围列和行的坐标"
    # 这里注意，range 末尾是开区间，所以要加 1
    return [(i, j) for i in range(max(0, c - 1), min(cols - 1, c + 1) + 1)
            for j in range(max(0, r - 1), min(rows - 1, r + 1) + 1) if i != c or j != r]
class Mine():
    def __init__(self, c, r):
        self.MineYesNo = False   # 是否是地雷
        self.OpenedYesNo = False  # 有没有被揭开
        self.Marked = ''   # 标记，''没有标记， '*'标记为地雷， '?'标记为问号
        self.MineAround = 0 # 不是地雷，0-8表示周围的地雷数
        self.tip = 2 # 2 为不确定，1 是地雷 0 是空白
        self.c = c
        self.r = r
        
    def draw_mine(self, canvas):
        x0 = self.c * mine_size
        y0 = self.r * mine_size                
        canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
            fill="#BDB76B",outline="#dcdcdc",width=2)
    def markmine(self, canvas, s): # s为'','*','?','1-8'
        x0 = self.c * mine_size
        y0 = self.r * mine_size
        if s in ('', '*', '?') :
            canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
                    fill="#BD7D6B",outline="#dcdcdc",width=2)
            canvas.create_text(x0+15,y0+18,text=s,\
                font=tkFont.Font(family='黑体', size=24, weight=tkFont.BOLD))
        elif s == '0':
            canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
                    fill="#E0FFFF",outline="#dcdcdc",width=1)
        else :
            canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
                    fill="#E0FFFF",outline="#dcdcdc",width=1)
            canvas.create_text(x0+15,y0+15,text=s,\
                font=tkFont.Font(family='黑体', size=16, weight=tkFont.BOLD))    
    def mark(self,canvas,value):
        pass
    
    def tip(self,canvas,value):
        pass
    def draw_tip(self,canvas, mineyesno = True):
        x0 = self.c * mine_size
        y0 = self.r * mine_size                
        color = 'red'
        if mineyesno == False:
            color = 'green'
        canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
            fill="#BDB76B",outline=color,width=2)
    def update(self,canvas):
        x0 = self.c * mine_size
        y0 = self.r * mine_size                
        fillcolor = "#BDB76B"
        if self.OpenedYesNo:
            fillcolor = "#E0FFFF"
        outlinecolor = "#dcdcdc"
        '''
        if self.tip == 2:
            outlinecolor = "#dcdcdc"
        elif self.tip == 1:
            outlinecolor = 'red'
        elif self.tip == 0:
            outlinecolor = 'green'
        '''
        canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
            fill=fillcolor,outline=outlinecolor,width=2)
        if self.OpenedYesNo and self.MineAround > 0:
            canvas.create_text(x0+15,y0+18,text=str(self.MineAround),\
                font=tkFont.Font(family='黑体', size=24, weight=tkFont.BOLD))
        if self.OpenedYesNo == False and self.Marked in('*', '?'):
            canvas.create_text(x0+15,y0+18,text=self.Marked,\
                font=tkFont.Font(family='黑体', size=24, weight=tkFont.BOLD))
        
                    
class MineBlock():
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(cols)] for j in range(rows)]

    def init(self):
        for i in range(rows):
            for j in range(cols):
                self._block[i][j].MineYesNo = False
                self._block[i][j].MineYesNo = False   # 是否是地雷
                self._block[i][j].OpenedYesNo = False  # 有没有被揭开
                self._block[i][j].Marked = ''   # 标记，''没有标记， '*'标记为地雷， '?'标记为问号
                self._block[i][j].MineAround = 0 # 不是地雷，0-8表示周围的地雷数
                self._block[i][j].tip = 2 # 2 为不确定，1 是地雷 0 是空白
    def spread_mines(self,c,r):  # 从某处点开，设置某处周围没有地雷
        around = get_around(c,r)
        mines = 0
        while mines < MINE_COUNT :
            c0 = random.randint(0,cols-1)
            r0 = random.randint(0,rows-1)
            if (c0,r0) not in around and  not((c0 == c) and (r0 == r)):
                if self._block[r0][c0].MineYesNo == False:
                    self._block[r0][c0].MineYesNo = True
                    mines += 1
        for i in range(rows):
            for j in range(cols):
                if self._block[i][j].MineYesNo == False :
                    self._block[i][j].MineAround = self.get_aroundmines(j,i)
                    
        '''
        如果要全部分布地雷，可如下埋雷：
        for i in random.sample(range(cols * rows), MINE_COUNT):
            self._block[i // cols][i % rows].MineYesNo = True
        '''

    def get_aroundmines(self, c, r): # 数出某处周围的地雷数
        count = 0
        for m in get_around(c,r):
            c,r = m
            if self._block[r][c].MineYesNo is True:
                count += 1
        return(count)
    
    def count_around_marked_mines(self, c, r): 
        # 数出某处周围已经标记的地雷数
        count = 0
        for m in get_around(c,r):
            c,r = m
            if self._block[r][c].Marked == '*':
                count += 1
        return(count)

    def count_around_not_marked(self, c, r): 
        # 返回某处周围没有标记地雷的数
        count = 0
        for m in get_around(c,r):
            c,r = m
            if self._block[r][c].OpenedYesNo == False and self._block[r][c].Marked == '':
                count += 1
        return(count)
    def around_opened(self, c, r):
        aroundopened = False
        for m in get_around(c,r):
            if self._block[m[1]][m[0]].OpenedYesNo :
                aroundopened = True
                break
        return aroundopened
    
    def count_opened(self):     # 返回总的揭开的数
        count = 0
        for i in range(rows):
            for j in range(cols):
                if self._block[i][j].OpenedYesNo:
                    count += 1
        return count

    def get_incertain_list(self,canvas):
        incertain_list = []
        for i in range(rows):
            for j in range(cols):
                if self._block[i][j].OpenedYesNo == False and \
                    self._block[i][j].Marked == '' and \
                        self.around_opened(j,i):
                    incertain_list.append((j,i))
                    #canvas.create_rectangle(j*mine_size+1,i*mine_size+1,
                    # (j+1)*mine_size-1,(i+1)*mine_size-1,fill="#BD7D6B",outline="red")
                    
    def draw_mines(self, canvas):
        canvas.create_rectangle(0,0,cols*mine_size,rows*mine_size,width=3)
        for c in range(cols):
            for r in range(rows):
                self._block[r][c].draw_mine(canvas)
                
    def bomb(self, canvas):  # 地雷引爆了   要把canvas传给markmine()
        for i in range(rows):
            for j in range(cols):
                if (self._block[i][j].MineYesNo == True) and \
                    self._block[i][j].OpenedYesNo == False: # 是地雷但没有被揭开
                    self._block[i][j].update(canvas) 
        
        
    def tip1(self, canvas):
        tipcount = 0
        for r in range(rows):
            for c in range(cols):
                if self._block[r][c].OpenedYesNo : # 如果它被揭开了
                    # and 0 <= self._block[i][j].MineAround <= 8:
                    around = get_around(c,r)
                    if self._block[r][c].MineAround == self.count_around_not_marked(c,r) + \
                        self.count_around_marked_mines(c,r):
                        # 如果它周围的地雷数，等于它周围没有被标记的地雷数+周围标记的数
                        for m in around:
                            i,j = m
                            if self._block[j][i].OpenedYesNo == False and self._block[j][i].Marked =='':
                                self._block[j][i].tip = 1
                                tipcount += 1
                                self._block[j][i].Marked = '*'
                                # 把周围没有被揭开的，且没有标记的标记为地雷
                                #self._block[j][i].update(canvas)
                    #如果周围的地雷数，等于周围标记的地雷数
                    if self._block[r][c].MineAround == self.count_around_marked_mines(c,r):
                        for m in around:
                            i,j = m
                            if self._block[j][i].OpenedYesNo == False and self._block[j][i].Marked =='':
                                self._block[j][i].tip = 0
                                self._block[j][i].OpenedYesNo = True
                                tipcount += 1
                                #self._block[j][i].update(canvas) 
        return tipcount
        
    def tip(self, canvas):
        while self.tip1(canvas) > 0:
            self.tip1(canvas)
        self.update(canvas)
        #incertain_list = self.get_incertain_list(canvas)
        #print(incertain_list)
    def update(self, canvas):
        for r in range(rows):
            for c in range(cols):
                self._block[r][c].update(canvas)


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.create_widgets()

    def create_widgets(self):
        self.frame0 = Frame(self,width=cols*mine_size, height=rows*mine_size) #左边框架，放置canvas
        self.frame0.pack(side='left')
        self.canvas = Canvas(self.frame0, width=cols*mine_size, height=rows*mine_size) # 俄罗斯方块板
        self.canvas.pack()
        self.mineframe = MineBlock()    
        self.time = 0
        self.mines_remainder = MINE_COUNT
        
        self.SVar1 = StringVar()
        self.SVar1.set(str(self.time))
        self.SVar2 = StringVar()
        self.SVar2.set(str(self.mines_remainder))
        
        self.frame1 = Frame(self,width=80, height=rows*mine_size,bg="#cccccc") # 右边框架，防止标签等
        self.frame1.pack(side='right')

        self.label1 = Label(self.frame1,textvariable=self.SVar1, font=("黑体", 20),bg="#cccccc")
        self.label1.place(x=10, y=30)   # 显示时间
        self.label2 = Label(self.frame1,textvariable=self.SVar2, font=("黑体", 16),bg="#cccccc")
        self.label2.place(x=10, y=100)   # 显示剩余地雷数
        
        self.btnRestart = Button(self.frame1,text="重新开始",width=8,command=self.newGame)
        self.btnRestart.place(x=5,y=200)  # 重新开始按钮
        self.btnTip = Button(self.frame1,text="提示",width=8,command=self.tip)
        self.btnTip.place(x=5,y=250)  # 提示
    
    def tip(self):
        '''
        for i in range(rows):
            for j in range(cols):
                if self.mineframe._block[i][j].OpenedYesNo : # and 0 <= self.mineframe._block[i][j].MineAround <= 8:
                    self.mineframe.tip(self.canvas,j,i)
        incertain_list = self.mineframe.get_incertain_list()
        for m in incertain_list:
            c,r = m
        '''
        self.mineframe.tip(self.canvas)
    def show_time(self):
        if self.time_stop:
            return
        self.time += 200
        self.SVar1.set(str(self.time//1000))
        self.master.after(200,self.show_time)
        
    def open(self,c,r):
        if self.mineframe._block[r][c].MineYesNo:  # 如果是地雷，gameover
            self.game_over()
        else:
            self.mineframe._block[r][c].OpenedYesNo = True
            aroundmines = self.mineframe._block[r][c].MineAround 
            self.mineframe._block[r][c].update(self.canvas)
            if aroundmines == 0: # 如果不是地雷，且周围地雷为0
                for m in get_around(c,r):
                    if self.mineframe._block[m[1]][m[0]].OpenedYesNo == False:
                        self.open(m[0],m[1]) 

        opened_mines = self.mineframe.count_opened()
        if opened_mines == (cols*rows-MINE_COUNT):
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.win()

    #新开始一个游戏
    def newGame(self):
        self.time = 0
        self.SVar1.set(str(self.time//1000))
        self.mines_remainder = MINE_COUNT
        self.SVar2.set(str(self.mines_remainder))
        self.time_stop = True
        self.firstclick = True
        self.mineframe.init()
        self.mineframe.draw_mines(self.canvas)

        self.canvas.bind("<Button-1>", self.mouseLeftClick)
        self.canvas.bind("<Button-3>", self.mouseRightClick)

        self.master.update()
        
    def game_over(self):
        self.time_stop = True
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.mineframe.bomb(self.canvas)  # 地雷引爆了
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
            self.time_stop = False
            # self.mineframe.init()
            self.mineframe.spread_mines(c,r)
            self.show_time()
        if self.mineframe._block[r][c].OpenedYesNo == False: #如果它没有被揭开，就揭开它
            self.open(c,r)
        
    #鼠标右键事件        
    def mouseRightClick(self, event):
        c=event.x//mine_size
        r=event.y//mine_size 
        if self.mineframe._block[r][c].OpenedYesNo == True :
            if self.mineframe.count_around_marked_mines(c,r) == \
                self.mineframe._block[r][c].MineAround:  #如果它周围地雷数不等于已经标注的地雷数
                for m in get_around(c,r):
                    if self.mineframe._block[m[1]][m[0]].Marked == '':
                        self.open(m[0],m[1])
        else:
            if self.mineframe._block[r][c].Marked == '':   #原始状态
                self.mineframe._block[r][c].markmine(self.canvas,'*')
                self.mineframe._block[r][c].Marked = '*'
                self.mines_remainder -= 1
                self.SVar2.set(str(self.mines_remainder))
            elif self.mineframe._block[r][c].Marked == '*':   #已经标注为地雷
                self.mineframe._block[r][c].markmine(self.canvas,'?') #标注为？
                self.mineframe._block[r][c].Marked = '?'
                self.mines_remainder += 1
                self.SVar2.set(str(self.mines_remainder))
            elif self.mineframe._block[r][c].Marked == '?':   #改回原始状态
                self.mineframe._block[r][c].markmine(self.canvas,'')
                self.mineframe._block[r][c].Marked = ''


if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.master.title("扫雷   岳慧练习作品")
    app.newGame()
    app.mainloop()
