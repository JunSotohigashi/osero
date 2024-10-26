import tkinter
from tkinter.scrolledtext import ScrolledText


class MyApp1(tkinter.Frame):
    gridSize = 80
    gridOffsetX = 10
    gridOffsetY = 10
    turn = 1
    state = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        # キャンバスを作成
        self.canvas = tkinter.Canvas(root, bg="white", height=660, width=660)
        # グリッドを書く
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(
                    i * self.gridSize + self.gridOffsetX,
                    j * self.gridSize + self.gridOffsetY,
                    (i + 1) * self.gridSize + self.gridOffsetX,
                    (j + 1) * self.gridSize + self.gridOffsetY,
                    fill="green",
                    tag="grid",
                )
        # stateの反映
        for i in range(8):
            for j in range(8):
                if self.state[i][j] == 1:
                    self.canvas.create_oval(
                        i * self.gridSize + self.gridOffsetX,
                        j * self.gridSize + self.gridOffsetY,
                        (i + 1) * self.gridSize + self.gridOffsetX,
                        (j + 1) * self.gridSize + self.gridOffsetY,
                        fill="black",
                        tag="cyl",
                    )
                elif self.state[i][j] == -1:
                    self.canvas.create_oval(
                        i * self.gridSize + self.gridOffsetX,
                        j * self.gridSize + self.gridOffsetY,
                        (i + 1) * self.gridSize + self.gridOffsetX,
                        (j + 1) * self.gridSize + self.gridOffsetY,
                        fill="white",
                        tag="cyl",
                    )
        # キャンパスを描画
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.ButtonPress1)

        self.txtBox = ScrolledText(root, font=("", 10), height=5, width=70)
        self.txtBox.place(x=50, y=680)
        self.txtBox.insert("end", "=====オセロ=====\n")
        if self.turn == 1:
            self.txtBox.insert("end", "黒のターン：")
            self.txtBox.see("end")
        elif self.turn == -1:
            self.txtBox.insert("end", "白のターン：")
            self.txtBox.see("end")
        self.scoreBox = ScrolledText(root, font=("", 10), height=5, width=20)
        self.scoreBox.place(x=580, y=680)
        self.scoreBox.delete("1.0", "end")
        self.scoreBox.insert("end", "黒：{}\n白：{}\n残り：{}".format(2, 2, 60))
        self.calcNext()

    def applyState(self):
        # 盤面を描画
        self.canvas.delete("cyl")
        for i in range(8):
            for j in range(8):
                if self.state[i][j] == 1:
                    self.canvas.create_oval(
                        i * self.gridSize + self.gridOffsetX,
                        j * self.gridSize + self.gridOffsetY,
                        (i + 1) * self.gridSize + self.gridOffsetX,
                        (j + 1) * self.gridSize + self.gridOffsetY,
                        fill="black",
                        tag="cyl",
                    )
                elif self.state[i][j] == -1:
                    self.canvas.create_oval(
                        i * self.gridSize + self.gridOffsetX,
                        j * self.gridSize + self.gridOffsetY,
                        (i + 1) * self.gridSize + self.gridOffsetX,
                        (j + 1) * self.gridSize + self.gridOffsetY,
                        fill="white",
                        tag="cyl",
                    )

    def compute(self, x, y, state, turn):
        changes = []
        change = []
        # 盤面の変化を演算
        # +X
        for i in range(x + 1, 8):
            if state[i][y] == turn:
                changes += change
                change = []
                break
            elif state[i][y] != 0:
                change.append([i, y])
            else:
                change = []
                break
        change = []
        # -X
        for i in range(x - 1, -1, -1):
            if state[i][y] == turn:
                changes += change
                change = []
                break
            elif state[i][y] != 0:
                change.append([i, y])
            else:
                change = []
                break
        change = []
        # +Y
        for j in range(y + 1, 8):
            if state[x][j] == turn:
                changes += change
                change = []
                break
            elif state[x][j] != 0:
                change.append([x, j])
            else:
                change = []
                break
        change = []
        # -Y
        for j in range(y - 1, -1, -1):
            if state[x][j] == turn:
                changes += change
                change = []
                break
            elif state[x][j] != 0:
                change.append([x, j])
            else:
                change = []
                break
        change = []
        # +X+Y
        l1 = range(x + 1, 8)
        l2 = range(y + 1, 8)
        for n in range(min(len(l1), len(l2))):
            i = l1[n]
            j = l2[n]
            if state[i][j] == turn:
                changes += change
                change = []
                break
            elif state[i][j] != 0:
                change.append([i, j])
            else:
                change = []
                break
        change = []
        # -X+Y
        l1 = range(x - 1, -1, -1)
        l2 = range(y + 1, 8)
        for n in range(min(len(l1), len(l2))):
            i = l1[n]
            j = l2[n]
            if state[i][j] == turn:
                changes += change
                change = []
                break
            elif state[i][j] != 0:
                change.append([i, j])
            else:
                change = []
                break
        change = []
        # -X-Y
        l1 = range(x - 1, -1, -1)
        l2 = range(y - 1, -1, -1)
        for n in range(min(len(l1), len(l2))):
            i = l1[n]
            j = l2[n]
            if state[i][j] == turn:
                changes += change
                change = []
                break
            elif state[i][j] != 0:
                change.append([i, j])
            else:
                change = []
                break
        change = []
        # +X-Y
        l1 = range(x + 1, 8)
        l2 = range(y - 1, -1, -1)
        for n in range(min(len(l1), len(l2))):
            i = l1[n]
            j = l2[n]
            if state[i][j] == turn:
                changes += change
                change = []
                break
            elif state[i][j] != 0:
                change.append([i, j])
            else:
                change = []
                break

        return changes

    def calcNext(self):
        self.canvas.delete("score")
        if True:  # self.turn == 1:
            max_score = -1
            max_index = []
            for i in range(8):
                for j in range(8):
                    if self.state[i][j] == 0:
                        change = self.compute(i, j, self.state, self.turn)
                        if max_score < len(change):
                            max_score = len(change)
                            max_index = [(i, j)]
                        elif max_score == len(change):
                            max_index.append((i, j))
                        self.canvas.create_text(
                            (i + 0.5) * self.gridSize + self.gridOffsetX,
                            (j + 0.5) * self.gridSize + self.gridOffsetY,
                            text="{}".format(len(change)),
                            tags="score",
                            fill="red",
                        )
            for i in max_index:
                self.canvas.create_oval(
                    i[0] * self.gridSize + self.gridOffsetX,
                    i[1] * self.gridSize + self.gridOffsetY,
                    (i[0] + 1) * self.gridSize + self.gridOffsetX,
                    (i[1] + 1) * self.gridSize + self.gridOffsetY,
                    tag="score",
                )

    # クリック時のイベント
    def ButtonPress1(self, event):
        # クリック座標をグリッド座標に変換
        x = int((event.x - self.gridOffsetX) / self.gridSize)
        y = int((event.y - self.gridOffsetY) / self.gridSize)

        changes = self.compute(x, y, self.state, self.turn)

        # 盤面の変化を適用
        if len(changes) != 0:
            if self.turn == 1:
                self.state[x][y] = 1
            elif self.turn == -1:
                self.state[x][y] = -1
            for i in changes:
                self.state[i[0]][i[1]] = self.turn

            self.txtBox.insert("end", "成功\n")
            self.txtBox.see("end")

            white = 0
            black = 0
            blank = 0
            for i in self.state:
                for j in i:
                    if j == 0:
                        blank += 1
                    elif j == 1:
                        black += 1
                    elif j == -1:
                        white += 1
            self.scoreBox.delete("1.0", "end")
            self.scoreBox.insert(
                "end", "黒：{}\n白：{}\n残り：{}".format(black, white, blank)
            )
            if blank == 0:
                self.turn = 0

            # ターン終了
            if self.turn == 1:
                next = False
                for i in range(8):
                    for j in range(8):
                        if self.state[i][j] == 0:
                            if len(self.compute(i, j, self.state, -1)) != 0:
                                next = True
                                break
                if next:
                    self.turn = -1
                    self.txtBox.insert("end", "白のターン：")
                    self.txtBox.see("end")
                else:
                    self.txtBox.insert(
                        "end", "白のターン：置ける場所がない！\n黒のターン："
                    )
                    self.txtBox.see("end")
            elif self.turn == -1:
                next = False
                for i in range(8):
                    for j in range(8):
                        if self.state[i][j] == 0:
                            if len(self.compute(i, j, self.state, 1)) != 0:
                                next = True
                                break
                if next:
                    self.turn = 1
                    self.txtBox.insert("end", "黒のターン：")
                    self.txtBox.see("end")
                else:
                    self.txtBox.insert(
                        "end", "黒のターン：置ける場所がない！\n白のターン："
                    )
                    self.txtBox.see("end")
            else:
                self.txtBox.insert("end", "ゲームセット：")
                if white > black:
                    self.txtBox.insert("end", "白の勝ち！")
                elif white < black:
                    self.txtBox.insert("end", "黒の勝ち！")
                else:
                    self.txtBox.insert("end", "引き分け")
                self.txtBox.see("end")
            self.applyState()

        else:
            self.txtBox.insert("end", "そこに置くことはできない！\n")
            if self.turn == 1:
                self.txtBox.insert("end", "黒のターン：")
                self.txtBox.see("end")
            elif self.turn == -1:
                self.txtBox.insert("end", "白のターン：")
                self.txtBox.see("end")
            self.txtBox.see("end")

        self.calcNext()
        self.canvas.pack()


root = tkinter.Tk()
root.geometry("800x800")  # Windowのサイズ設定
root.title("Osero")  # タイトル作成
app = MyApp1(master=root)
app.mainloop()
