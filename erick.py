from tkinter import *

import random

class MSCell(Label):
    '''one cell of a minesweeper grid'''
    
    def __init__(self,master,pos,num,isBomb):
        '''MSCell(num,isBomb) -> MSCell
        a Minesweeper cell
        num is the value of the cell.
        bool isBomb is weather or not the tile is a bomb'''
        Label.__init__(self,master,text=' ',fg='black',bg='white',width=2,height=1,relief='ridge',font=('Arial',18))
        self.master = master
        self.pos = pos
        self.num = num
        self.isBomb = isBomb
        self.flagged = False
        self.revealed = False
        self.grid(row=pos[0],column=pos[1])
        # Set up clicking
        self.bind('<Button-1>', self.reveal)
        self.bind('<Button-2>', self.toggle_flagged)
        self.bind('<Button-3>', self.toggle_flagged) # Didn't work with jsut B2
        self.colormap = ['white','blue','darkgreen','red','purple','maroon','cyan','black','gray']
    
    def get_num(self):
        return self.num

    def is_bomb(self):
        return self.isBomb

    def exploded(self):
        return self.isBomb and self.revealed

    def flagged(self):
        return self.flagged

    def revealed(self):
        return self.revealed

    def toggle_flagged(self,event):
        if not self.revealed:
            self.flagged = not self.flagged
            self.draw()
        self.update_label()

    def reveal(self,event):
        if not self.flagged and not self.isBomb:
            self.revealed = True
            self.draw()

        if self.isBomb:
            messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
            exit()
        
        self.reveal_checks()
        
    def rev(self):
        if not self.flagged and not self.isBomb:
            self.revealed = True
            self.draw()
            self.reveal_checks()

        if self.isBomb:
            pass

    def reveal_checks(self):
        pass

    def update_label(self):
        pass

    def draw(self):
        if self.flagged:
            self['relief'] = 'ridge'
            self['text'] = '*'
            self['fg'] = 'black'
            self['bg'] = 'white'
        elif self.revealed:
            self['relief'] = 'sunken'
            if self.num > 0:
                self['text'] = self.num
            else:
                self.master.check(self.pos)
                self['text'] = ' '
            self['fg'] = self.colormap[self.num]
            self['bg'] = 'gray'
        else:
            self['relief'] = 'ridge'
            self['text'] = ' '
            self['bg'] = 'white'
            

class MSFrame(Frame):
    '''a Minesweeper Frame'''

    def __init__(self,master,width,height,bombs):
        Frame.__init__(self,master)
        self.grid()
        self.width = width
        self.height = height
        self.cells = []
        self.bombsRemaining = bombs
        for row in range(height):
            rowMSCells = []
            for column in range(width):
                isBomb = random.random() < bombs/(width*height) and self.bombsRemaining > 0
                rowMSCells.append(MSCell(self,[row,column],0,isBomb))
                if isBomb:
                    self.bombsRemaining -= 1
            self.cells.append(rowMSCells)
        while self.bombsRemaining > 0:
            for row in self.cells:
                for cell in row:
                    isBomb = random.random() < bombs/(width*height) and self.bombsRemaining > 0
                    cell.isBomb = isBomb
                    if isBomb:
                        self.bombsRemaining -= 1
                self.cells.append(rowMSCells)
        for row in self.cells:
            for cell in row:
                self.check_number(cell)
                cell.grid(row=cell.pos[0],column=cell.pos[1])

    def check_number(self,cell):
        for x in range(cell.pos[0]-1,cell.pos[0]+2):
            for y in range(cell.pos[1]-1,cell.pos[1]+2):
                if ((not x >= 12) and (not y > 9) and (not x < 0) and (not y < 0) and (x<10)):
                    if self.cells[x][y].isBomb:
                        cell.num += 1
    def check(self,pos):
        x = pos[0]
        y = pos[1]
        print(self.cells[x][y+1].get_num())
        self.cells[x][y+1].rev()
        self.cells[x][y-1].rev()
    
    def check_explode(self):
        pass
 
    def check_win(self):
        pass
 
def play_minesweeper(width,height,bombs):
    root = Tk()
    root.title('Minesweeper')
    game = MSFrame(root,width,height,bombs)
    game.mainloop()

play_minesweeper(12,12,15)
