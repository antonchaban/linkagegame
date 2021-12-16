from tkinter import *

from game_process import GameProcess


class GameController:
    def __init__(self):
        self.gp = GameProcess()
        self.colors = ['white', 'red', 'blue', 'green', 'yellow', 'black', 'grey']

        self.width = 1280
        self.height = 720
        self.window = Tk()
        self.window.title("Linkage Game")
        self.window.minsize(self.width, self.height)
        self.window.maxsize(self.width, self.height)

        self.buttons = []
        self.color_buttons = []
        self.color_label = None
        self.dir_buttons = []
        self.dir_label = None
        self.steps = None
        self.score = None
        self.win_text = Label(text='', font=('Comic Sans MS', 25))
        self.win_text['fg'] = 'Black'
        self.win_text.place(x=self.width / 2 - 40, y=30)

        self.create_steps()
        self.create_blocks()
        self.create_color_buttons()
        self.create_dir_buttons()
        self.paint()
        btn = Button(self.window, bd=2, text='Start', command=self.start, font=('Comic Sans MS', 25))
        btn.place(x=1100, y=300, width=120, height=40)

        self.difficulty = IntVar()
        self.difficulty.set(1)
        self.easy = Radiobutton(text="Easy",
                                variable=self.difficulty, value=1, font=('Comic Sans MS', 10))
        self.easy.place(x=1100, y=400)
        self.normal = Radiobutton(text="Normal",
                                  variable=self.difficulty, value=2, font=('Comic Sans MS', 10))
        self.normal.place(x=1100, y=420)
        self.hard = Radiobutton(text="Hard",
                                variable=self.difficulty, value=3, font=('Comic Sans MS', 10))
        self.hard.place(x=1100, y=440)
        self.window.mainloop()

    def start(self):
        if not self.gp.active:
            self.easy['state'] = 'disable'
            self.normal['state'] = 'disable'  # active
            self.hard['state'] = 'disable'
            self.win_text['text'] = ''
            if self.gp.step > 1:
                self.gp = GameProcess()
            self.gp.difficulty = self.difficulty.get()
            self.gp.active = True
            self.next_step()

    def create_steps(self):
        self.steps = Label(text='Current Step: 1', font=('Comic Sans MS', 10))
        self.steps.place(x=0, y=700)
        self.score = Label(text='Current Score: 1', font=('Comic Sans MS', 14))
        self.score.place(x=1100, y=40)

    def next_step(self):
        self.gp.step += 1
        self.steps['text'] = 'Current Step: ' + str(self.gp.step)
        self.score['text'] = 'Current Score: ' + str(self.gp.n_groups())
        if self.gp.step % 2 == 1:
            dic = self.gp.AI_step()
            self.add((dic[2], dic[3]), dic[0], dic[1])

    def paint(self):
        for k in range(7):
            for p in range(7):
                color = self.colors[self.gp.get_block(k, p)]
                self.buttons[k][p].config(bg=color, activebackground=color, activeforeground=color)

        for i in range(4):
            self.color_buttons[i]['text'] = self.gp.field.color_nums[i]

    def create_blocks(self):
        btn_size = 50
        start_pos = (self.width / 2 - 50 * 3.5, self.height / 2 - 50 * 3.5)
        posY = 0

        for i in range(7):
            buttons_row = []
            posX = 0
            for j in range(7):
                btn = Button(self.window, bd=2,
                             command=lambda c=(i, j): self.click_field_button(c))
                btn.place(x=start_pos[0] + posX, y=start_pos[1] + posY, width=btn_size, height=btn_size)
                buttons_row.append(btn)
                posX += btn_size
            posY += btn_size
            self.buttons.append(buttons_row)

    def create_color_buttons(self):
        color_button_size = 40
        self.color_label = Label(text='^')
        self.color_label.place(x=1080 + color_button_size / 4 - 1, y=150)
        for i in range(1, 5):
            btn = Button(self.window, bd=2, text='6', command=lambda c=i: self.change_color(c))
            btn.place(x=1080 + (i - 1) * 50, y=100, width=color_button_size, height=color_button_size)
            btn.config(bg=self.colors[i], activebackground=self.colors[i], activeforeground=self.colors[i])
            self.color_buttons.append(btn)

    def create_dir_buttons(self):
        dir_button_size = 40
        self.dir_label = Label(text='->')
        self.dir_label.place(x=1180, y=210)
        dirs = {0: '|', 1: '—'}
        for i in range(2):
            btn = Button(self.window, bd=2, text=dirs[i], command=lambda c=i: self.change_direction(c))
            btn.place(x=1200, y=200 + i * 50, width=dir_button_size, height=dir_button_size)
            self.color_buttons.append(btn)

    def add(self, c, color=None, dir=None):
        if color is None:
            color = self.gp.choosed_color

        if dir is None:
            dir = self.gp.choosed_dir

        res = self.gp.add(color, dir, c[0], c[1])
        if res != -1:
            possibility = self.gp.possibility()
            self.paint()
            if possibility == 1:
                self.gp.clear6()
                self.paint()
                self.next_step()
            elif possibility == 0:
                if self.gp.n_groups() >= 12:
                    self.win_text['text'] = 'Win More: ' + str(self.gp.n_groups())
                else:
                    self.win_text['text'] = 'Win Less: ' + str(self.gp.n_groups())
                self.gp.active = False
                self.easy['state'] = 'active'
                self.normal['state'] = 'active'
                self.hard['state'] = 'active'
                return

            self.next_step()
            # print('g', self.gp.n_groups())

    def click_field_button(self, c):
        if self.gp.active:
            self.add(c)

    def change_color(self, color):
        self.gp.choosed_color = color
        self.color_label.place(x=1080 + (color - 1) * 50 + 10 - 1, y=150)

    def change_direction(self, dir):
        self.gp.choosed_dir = dir
        self.dir_label.place(x=1180, y=210 + dir * 50)
