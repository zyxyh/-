from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import random


cols = 30 #列数
rows = 16 #行数
mine_size = 30
MINE_COUNT = 99 # 地雷总数

def get_around(cr):
    "返回(c, r)周围列和行的坐标"
    # 这里注意，range 末尾是开区间，所以要加 1
    c,r = cr
    return [(i, j) for i in range(max(0, c - 1), min(cols - 1, c + 1) + 1)
            for j in range(max(0, r - 1), min(rows - 1, r + 1) + 1) if i != c or j != r]

class Mine():
    def __init__(self, cr):
        self.cr = cr
        self.fillcolor = "#BDB76B"
        self.outlinecolor = "#dcdcdc"
        
    def update(self, canvas, status):
        x0 = self.cr[0] * mine_size
        y0 = self.cr[1] * mine_size                
        self.fillcolor = "#BDB76B"
        OpenedYesNo = ('0' <= status <= '8')
        if OpenedYesNo:
            self.fillcolor = "#E0FFFF"
        
        canvas.create_rectangle(x0+1,y0+1,x0+mine_size-1,y0+mine_size-1,                    
            fill=self.fillcolor,outline=self.outlinecolor,width=2)
        if OpenedYesNo and int(status) > 0:
            canvas.create_text(x0+15,y0+18,text=status,font=ft1)
        if (not OpenedYesNo) and status in ('*', '?', 'B', 'M'):
            canvas.create_text(x0+15,y0+18,text=status,font=ft1)
            
            
class MineFrame():
    def __init__(self):
        self.MineBlock = [[Mine((i, j)) for i in range(cols)] for j in range(rows)]
        self.MineTable = [[False for i in range(cols)] for j in range(rows)]
        self.StatusTable = [['' for i in range(cols)] for j in range(rows)]
        # ''原始状态不能确定， '*'标记为地雷， '?'标记为问号
        # 'm'假设为地雷， 'b'假设不是地雷
        # '0'-'8'表示揭开并显示周围的地雷数
    def getstatus(self,cr):
        return self.StatusTable[cr[1]][cr[0]]
    def setstatus(self,cr,s):
        self.StatusTable[cr[1]][cr[0]] = s
    def init(self):
        self.MineTable = [[False for i in range(cols)] for j in range(rows)]
        self.StatusTable = [['' for i in range(cols)] for j in range(rows)]
        
    def spread_mines(self,cr):  # cr及周围不安排地雷
        "第一次点击，设置其周围没有地雷"
        around = get_around(cr)
        m = 0
        while m < MINE_COUNT :
            c0 = random.randint(0,cols-1)
            r0 = random.randint(0,rows-1)
            if (c0,r0) not in around and  not((c0 == cr[0]) and (r0 == cr[1])):
                if self.MineTable[r0][c0] == False:
                    self.MineTable[r0][c0] = True
                    m += 1
    
    def get_aroundmines(self, cr): # 得到某处周围的地雷数
        "得到某处周围的地雷数"
        count = 0
        for m in get_around(cr):
            c,r = m
            if self.MineTable[r][c] :
                count += 1
        return(count)
    
    def count_marked_mines(self): # 返回全部已经标记为地雷的数
        "返回全部已经标记为地雷的数"
        marked_mines = 0
        for i in range(rows):
            marked_mines += self.StatusTable[i].count('*')
        return marked_mines
    
    def count_around_marked_mines(self, cr): # 地雷或假定为地雷的数 '*' 或 'm'
        "数出某处周围已经标记的地雷或假定为地雷的数'*' 或 'm','M'"
        count = 0
        for m in get_around(cr):
            if self.getstatus(m) in ('*','m','M'): 
                count += 1
        return(count)

    def count_around_not_marked(self, cr): # 状态为''的数
        "返回某处周围没有揭开，没有标记地雷的数,状态为''的数"
        count = 0
        for m in get_around(cr):
            if self.getstatus(m) == '':
                count += 1
        return(count)
    
    def around_opened(self, cr):
        "周围是否有已经被揭开了" # 不是全部打开了
        aroundopened = False
        for m in get_around(cr):
            if '0' <= self.getstatus(m) <='8':
                aroundopened = True
                break
        return aroundopened
    def around_unopened(self, cr):
        "周围是否有 没有被揭开的" 
        aroundunopened = False
        for m in get_around(cr):
            if self.getstatus(m) in ('','?','b','m','B','M') :
                aroundunopened = True
                break
        return aroundunopened    
    
    def success(self):     
        "根据总的揭开的数，判断是否胜利"
        count = 0
        for i in range(rows):
            for j in range(cols):
                if '0' <= self.getstatus((j,i)) <= '8':
                    count += 1
        return count == cols * rows - MINE_COUNT

    def get_incertain_list(self):
        "返回待定的没有揭开的列表"
        return [(j,i) for i in range(rows) for j in range(cols) \
                if self.StatusTable[i][j]  == '' and self.around_opened((j,i))]
        
    def get_blankborderlist(self):
        "返回揭开的旁边有没揭开的列表"
        return [(j,i) for i in range(rows) for j in range(cols) \
                if '0'<=(self.StatusTable[i][j])<='8' and \
                    self.around_unopened((j,i))]
    
    def update(self, canvas):
        for i in range(rows):
            for j in range(cols):
                self.MineBlock[i][j].update(canvas,self.StatusTable[i][j])
    
    def bomb(self, canvas):  # 地雷引爆了   要把canvas传给markmine()
        for i in range(rows):
            for j in range(cols):
                if (self.MineTable[i][j]) and self.StatusTable[i][j] == '': # 是地雷但没有被揭开
                    self.MineBlock[i][j].update(canvas,'*') 
        
    def tip_mine(self, cr):
        "如果周围的地雷数，等于周围没有被标记的地雷数+周围标记的数,把没有揭开的标记为地雷"
        tipmine = 0
        if self.get_aroundmines(cr) == self.count_around_not_marked(cr) + \
            self.count_around_marked_mines(cr):
            # 如果它周围的地雷数，等于它周围没有被标记的地雷数+周围标记的数
            for m in get_around(cr):
                if self.getstatus(m) == '':
                    self.setstatus(m,'*')# 把周围没有被揭开的，且没有标记的标记为地雷
                    tipmine += 1
        return  tipmine       
                        
    def tip_notmine(self,cr):
        "如果周围的地雷数，等于周围标记的地雷数，把没有标记的揭开"
        tipnotmine = 0
        aroundmines = self.get_aroundmines(cr)
        if aroundmines == 0 or aroundmines == self.count_around_marked_mines(cr):
            for m in get_around(cr):
                if self.getstatus(m) == '':
                    self.setstatus(m,str(self.get_aroundmines(m)))
                    tipnotmine += 1
        return tipnotmine
    
    def tip(self):
        tipmine = 0
        tipnotmine = 0
        for m in self.get_blankborderlist():
            tipmine += self.tip_mine(m)
            tipnotmine += self.tip_notmine(m)
        if (tipmine + tipnotmine) > 0:
            self.tip()
    
    def check(self):
        blankborderlist = self.get_blankborderlist()
        for m in blankborderlist:
            a = self.get_aroundmines(m)
            b = self.count_around_marked_mines(m)
            c = self.count_around_not_marked(m)
            if a > b+c or a < b:
                print(m,'地雷',a,'  标记的地雷',b, '  周围空白',c)
                return False
        return True
    def suppose1(self):
        
        supposecount = 0
        for b in self.get_blankborderlist():
            aroundmines = self.get_aroundmines(b)
            around_not_marked = self.count_around_not_marked(b)
            around_marked_mines = self.count_around_marked_mines(b)
            # print(b,'地雷：',aroundmines, '没有标记的：',around_not_marked , '已经标记的',around_marked_mines)
            if aroundmines == around_not_marked + around_marked_mines:
                # 如果它周围的地雷数，等于它周围没有被标记的地雷数+周围标记的数
                for around in get_around(b):
                    if self.getstatus(around) == '':
                        self.setstatus(around,'m') # 假定为地雷
                        supposecount += 1
            if aroundmines == around_marked_mines:
                for around in get_around(b):
                    if self.getstatus(around) == '':
                        self.setstatus(around,'b') # 假定可以揭开了
                        supposecount += 1
        if supposecount > 0 :
            print('推导出来几个：',supposecount)
            self.suppose1()
        else:
            return
    def suppose(self):
        incertainlist = self.get_incertain_list()
        # blankborderlist = self.get_blankborderlist()
        for m in incertainlist:
            self.setstatus(m,'m') # 假定为地雷
            self.suppose1()
            for m1 in incertainlist:
                print(m1,self.getstatus(m1),end="")
            print()
            print(self.check())
            if self.check() == False: #假定为地雷，检查不对，因此确定不是地雷，可揭开
                self.setstatus(m,'B')
                for m1 in incertainlist:
                    print(m,self.getstatus(m1),end="")
                print()
                continue
            
            currentstatus1 = [] # 把推定的状态记录下来
            for m1 in incertainlist:
                currentstatus1.append([m1,self.getstatus(m1)])

            for m1 in incertainlist: #先把上个循环假定的回位
                if self.getstatus(m1) in ('b','m'):
                    self.setstatus(m1,'')                

            self.setstatus(m,'b')
            self.suppose1()
            for m1 in incertainlist:
                print(m1,self.getstatus(m1),end="")
            print()
            print(self.check())
            if self.check() == False: #假定为空白，检查不对，因此确定是地雷
                self.setstatus(m,'M')
                for m1 in incertainlist:
                    print(m,self.getstatus(m))
                continue    

            currentstatus2 = []
            for m1 in incertainlist:
                currentstatus2.append([m1,self.getstatus(m1)])

            for m1 in incertainlist: #先把上个循环假定的回位
                if self.getstatus(m1) in ('b','m'):
                    self.setstatus(m1,'')           
            '''
            for s in range(len(currentstatus1)):
                cr1,cs1 = currentstatus1[s]
                cr2,cs2 = currentstatus2[s]
                print(cr1,cr2,cs1,cs2)
                if cr1 == cr2 :
                    if cs1 == 'm' and cs2 == 'm':
                        self.StatusTable[cr1[1]][cr1[0]] = 'M'
                    if cs1 == 'b' and cs2 == 'b':
                        self.StatusTable[cr1[1]][cr1[0]] = 'B' 
            
        for m in incertainlist:
            if self.getstatus(m) == 'B':
                self.setstatus(m,str(self.get_aroundmines(m)))
                #print(m,'B', str(self.get_aroundmines(m)))
            elif self.getstatus(m) == 'M':
                self.setstatus(m,'*')
                #print(m,'M')
        '''        
                    


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.mineframe = MineFrame()        
        self.time = 0
        self.mines_remainder = MINE_COUNT

        self.create_widgets()
 
    def create_widgets(self):
        self.frame0 = Frame(self,width=cols*mine_size, height=rows*mine_size) #左边框架，放置canvas
        self.frame0.pack(side='left')
        self.canvas = Canvas(self.frame0, width=cols*mine_size, height=rows*mine_size) # 俄罗斯方块板
        self.canvas.pack()
        self.SVar1 = StringVar()
        self.SVar1.set(str(self.time))
        self.SVar2 = StringVar()
        self.SVar2.set(str(self.mines_remainder))
        
        self.frame1 = Frame(self,width=80, height=rows*mine_size,bg="#cccccc") # 右边框架，防止标签等
        self.frame1.pack(side='right')

        self.label1 = Label(self.frame1,textvariable=self.SVar1, width=4, font=("黑体", 20),relief = "raised")
        self.label1.place(x=10, y=30)   # 显示时间
        self.label2 = Label(self.frame1,textvariable=self.SVar2, width=5, font=("黑体", 16),relief = "raised")
        self.label2.place(x=10, y=100)   # 显示剩余地雷数
        
        self.btnRestart = Button(self.frame1,text="重新开始",width=8,command=self.newGame)
        self.btnRestart.place(x=5,y=200)  # 重新开始按钮
        self.btnTip = Button(self.frame1,text="提示",width=8,command=self.tip)
        self.btnTip.place(x=5,y=250)  # 提示
        self.btnSuppose = Button(self.frame1,text="推理",width=8,command=self.suppose)
        self.btnSuppose.place(x=5,y=300)  # 提示
    
    #新开始一个游戏
    def newGame(self):
        self.time = 0
        self.SVar1.set('0')
        self.mines_remainder = MINE_COUNT
        self.SVar2.set(str(self.mines_remainder))
        self.time_stop = True
        self.firstclick = True
        self.mineframe.init()
        self.mineframe.update(self.canvas)
        self.messagetitle = ""
        self.canvas.bind("<Button-1>", self.mouseLeftClick)
        self.canvas.bind("<Button-3>", self.mouseRightClick)
        
    def mouseLeftClick(self, event):  # 鼠标左键事件
        c=event.x//mine_size
        r=event.y//mine_size
        if self.firstclick :
            self.firstclick = False
            self.time_stop = False
            self.mineframe.spread_mines((c,r))
            self.show_time()
        if self.mineframe.StatusTable[r][c] == '': # 如果它没有被揭开，就揭开它
            self.open(c,r)
        
    #鼠标右键事件        
    def mouseRightClick(self, event):
        c=event.x//mine_size
        r=event.y//mine_size 
        if self.mineframe.StatusTable[r][c] in \
            ('0','1','2','3','4','5','6','7','8') :
            if self.mineframe.count_around_marked_mines((c,r)) == \
                self.mineframe.get_aroundmines((c,r)):  
                    #如果它周围地雷数不等于已经标注的地雷数
                for m in get_around((c,r)):
                    if self.mineframe.StatusTable[m[1]][m[0]] == '':
                        self.open(m[0],m[1])
        else:
            if self.mineframe.StatusTable[r][c] == '':   #原始状态
                self.mineframe.StatusTable[r][c] = '*'  #标记为地雷
                self.mines_remainder -= 1
                self.SVar2.set(str(self.mines_remainder))
            elif self.mineframe.StatusTable[r][c] == '*':  #已经标注为地雷
                self.mineframe.StatusTable[r][c] = '?'  #标记为'?'
                self.mines_remainder += 1
                self.SVar2.set(str(self.mines_remainder))
            elif self.mineframe.StatusTable[r][c] == '?':   #如果标记为'?'
                self.mineframe.StatusTable[r][c] = ''  #改回原始状态
            self.mineframe.MineBlock[r][c].update(self.canvas,\
                self.mineframe.StatusTable[r][c])
            
    def open(self,c,r):
        if self.mineframe.MineTable[r][c] :  # 如果是地雷，gameover
            self.messagetitle = '揭开地雷！Game Over!'
            self.stop()
        else:
            aroundmines = self.mineframe.get_aroundmines((c,r))
            self.mineframe.StatusTable[r][c] = str(aroundmines)
            self.mineframe.MineBlock[r][c].update(self.canvas,str(aroundmines))

            if aroundmines == 0: # 如果不是地雷，且周围地雷为0
                for m in get_around((c,r)):
                    if self.mineframe.StatusTable[m[1]][m[0]] == '':
                        self.open(m[0],m[1]) 

        if self.mineframe.success():
            self.messagetitle = "恭喜你胜利了,用时%s秒"%(self.time//1000)
            self.stop()            
            
    def tip(self):
        self.mineframe.tip()
        self.mineframe.update(self.canvas)
        self.mines_remainder = MINE_COUNT - self.mineframe.count_marked_mines()
        self.SVar2.set(str(self.mines_remainder))
    
    def suppose(self):
        self.mineframe.suppose()
        self.mineframe.update(self.canvas)
        self.mines_remainder = MINE_COUNT - self.mineframe.count_marked_mines()
        self.SVar2.set(str(self.mines_remainder))
            
    def show_time(self):
        if self.time_stop:
            return
        self.time += 1000
        self.SVar1.set(str(self.time//1000))
        self.master.after(1000,self.show_time)
        
    def stop(self):
        self.time_stop = True
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.mineframe.bomb(self.canvas)  # 地雷引爆了
        if messagebox.askretrycancel(title=self.messagetitle,message='Try again?'):
            self.newGame()


if __name__ == '__main__':
    root = Tk()
    ft1 = tkFont.Font(family='黑体', size=24, weight=tkFont.BOLD)
    app = Application(master=root)
    app.master.title("扫雷   岳慧练习作品")
    app.newGame()
    app.mainloop()

