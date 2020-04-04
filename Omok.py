import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import inf as infinity
import datetime
import copy
from os import system
#기본적인 UI구성요소를 제공하는 클레스들은 PyQt5.QtWidgets모듈에 포함되어 있음
#https://codetorial.net/entry/reimplement2
#https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py
#https://oceancoding.blogspot.com/2019/03/blog-post.html
#https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
width = 900 #화면 size
height = 670
board_l = 640 #board size
BLACK = +1 #흑돌 ,백돌
WHITE = 0
HIGH = 3  #level
MID = 2
LOW = 1
MINIMAX = 0 #알고리즘
ALPHABETA = 1
#evaluation function - state, score // 오목 7개의 상태와 8번째에 score입력
BLACK_STATE = [[-1, 1, 1, 1, 1, 1, -1, 100], [0, 1, 1, 1, 1, 1, -1, 100], [-1, 1, 1, 1, 1, 1, 0, 100],
        [1, 1, 1, 1, 1, 1, -1, 100], [-1, 1, 1, 1, 1, 1, 1, 100], [1, 1, 1, 1, 1, 1, 1, 100],
        [-1, 1, 1, 1, 1, -1, -1, 70],
        [-1, 1, -1, 1, 1, 1, -1, 33], [-1, 1, 1, -1, 1, 1, -1, 33], [-1, 1, 1, 1, -1, 1, -1, 33],
        [1, 1, -1, 1, 1, 1, -1, 33], [-1, 1, 1, -1, 1, 1, 1, 33],
        [-1, 1, -1, 1, 1, 1, 0, 32], [ -1, 1, 1, -1, 1, 1, 0, 32], [-1, 1, 1, 1, -1, 1, 0, 32],
        [0, 1, -1, 1, 1, 1, -1, 32], [ 0, 1, 1, -1, 1, 1, -1, 32], [0, 1, 1, 1, -1, 1, -1, 32],
        [0, 1, -1, 1, 1, 1, 0, 23], [ 0, 1, 1, -1, 1, 1, 0, 23], [0, 1, 1, 1, -1, 1, 0, 23],
        [-1, 1, 1, 1, -1, -1, -1, 12],
        [-1, 1, 1, 1, 1, 0, -1, 27], [0, 1, 1, 1, 1, -1, -1, 27],
        [-1, 1, -1, 1, 1, -1, -1, 7], [-1, 1, 1, -1, 1, -1, -1, 7],
        [-1, 1, 1, -1, 1, 0, -1, 3], [-1, 1, -1, 1, 1, 0, -1, 3],
        [0, 1, 1, -1, 1, -1, -1, 3], [0, 1, -1, 1, 1, -1, -1, 3],
        [-1, 1, 1, 1, 0, -1, -1, 6], [0, 1, 1, 1, -1, -1, -1, 6],
        [-1, 1, 1, -1, -1, -1, -1, 2],
        [-1, 1, 1, 0, -1, -1, -1, 1], [0, 1, 1, -1, -1, -1, -1, 1]]
WHITE_STATE = [[-1, 0, 0, 0, 0, 0, 0, -1, 100], [1, 0, 0, 0, 0, 0, 0, -1, 100], [-1, 0, 0, 0, 0, 0, 0, 1, 100],
        [0, 0, 0, 0, 0, 0, -1, 100], [-1, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100],
        [-1, 0, 0, 0, 0, -1, -1, 70],
        [-1, 0, -1, 0, 0, 0, -1, 33], [-1, 0, 0, -1, 0, 0, -1, 33], [-1, 0, 0, 0, -1, 0, -1, 33],
        [0, 0, -1, 0, 0, 0, -1, 33], [-1, 0, 0, -1, 0, 0, 0, 33],
        [-1, 0, -1, 0, 0, 0, 1, 32], [ -1, 0, 0, -1, 0, 0, 1, 32], [-1, 0, 0, 0, -1, 0, 1, 32],
        [1, 0, -1, 0, 0, 0, -1, 32], [ 1, 0, 0, -1, 0, 0, -1, 32], [1, 0, 0, 0, -1, 0, -1, 32],
        [1, 0, -1, 0, 0, 0, 1, 23], [ 1, 0, 0, -1, 0, 0, 1, 23], [1, 0, 0, 0, -1, 0, 1, 23],
        [-1, 0, 0, 0, -1, -1, -1, 12],
        [-1, 0, 0, 0, 0, 1, -1, 27], [1, 0, 0, 0, 0, -1, -1, 27],
        [-1, 0, -1, 0, 0, -1, -1, 7], [-1, 0, 0, -1, 0, -1, -1, 7],
        [-1, 0, 0, -1, 0, 1, -1, 3], [-1, 0, -1, 0, 0, 1, -1, 3],
        [1, 0, 0, -1, 0, -1, -1, 3], [1, 0, -1, 0, 0, -1, -1,3],
        [-1, 0, 0, 0, 1, -1, -1, 6], [1, 0, 0, 0, -1, -1, -1, 6],
        [-1, 0, 0, -1, -1, -1, -1, 2],
        [-1, 0, 0, 1, -1, -1, -1, 1], [1, 0, 0, -1, -1, -1, -1, 1]]

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = [[-1 for x in range(15)] for y in range(15)] #바둑 있는 곳들 표시하는 15 * 15 배열
        # Level box에서 선택한 level - 탐색 depth를 나타냄
        self.level = LOW
        # 3 by 3  rule
        self.rule = 1
        # first player를 표시 - 선수는 무조건 흑돌
        self.human = BLACK
        self.computer = WHITE
        # algorithm 표시
        self.algorithm = ALPHABETA

        self.initUI()

    #UI 초기 설정
    def initUI(self):
        self.setWindowTitle('OMOK')
        self.setWindowIcon(QIcon('board.png'))
        self.resize(width, height)  # 스크린의 크기 조정
        self.center()  # 화면 정중앙에 프로그램 배치
        #수평 layout - 2개의 수직 layout을 뒷부분에서 추가할 것
        formbox = QHBoxLayout()
        self.setLayout(formbox)
        #수직 layout
        left = QVBoxLayout()    #오목판
        right = QVBoxLayout()   #설정 - option , start button, exit button

        # 좌 레이아웃 박스에 그래픽 뷰 추가 - 오목판
        self.graphicsView = QGraphicsView(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setFixedSize(board_l, board_l)
        self.init_board()
        self.graphicsView.setHorizontalScrollBarPolicy((Qt.ScrollBarAlwaysOff))
        self.graphicsView.setVerticalScrollBarPolicy((Qt.ScrollBarAlwaysOff))
        left.addWidget(self.graphicsView)

        #우 레이아웃 박스에 widget 추가
        #new game button
        newGame_B = QPushButton('new game', self)
        right.addWidget(newGame_B)
        newGame_B.resize(newGame_B.sizeHint())
        newGame_B.clicked.connect(self.init_board) #init_board()함수로 연결돼 보드를 초기화 한다.
        # 그룹박스에 사용할 위젯
        #option group box - first player, level, 3 by 3, algorithm box가 포함된다.
        gb = QGroupBox('Options')
        right.addWidget(gb)
        gg = QGridLayout()
        gb.setLayout(gg)
        #first player box
        self.lbl = QLabel('First Player', self)
        gg.addWidget(self.lbl, 0, 0)
        player_CB = QComboBox(self)
        gg.addWidget(player_CB, 0, 1)
        player_CB.addItem('사람')
        player_CB.addItem('컴퓨터')
        player_CB.activated[str].connect(self.onActivated) #button 클릭시 이동 함수 onActivated()
        #level combo box
        self.lbl = QLabel('LEVEL', self)
        gg.addWidget(self.lbl, 1, 0)
        level_CB = QComboBox(self)
        gg.addWidget(level_CB, 1, 1)
        level_CB.addItem('하급')
        level_CB.addItem('중급')
        level_CB.addItem('상급')
        level_CB.activated[str].connect(self.onActivated)
        # 3 by 3 combo box
        self.lbl = QLabel('3 by 3', self)
        gg.addWidget(self.lbl, 2, 0)
        rule_CB = QComboBox(self)
        gg.addWidget(rule_CB, 2, 1)
        rule_CB.addItem('allow')
        rule_CB.addItem('disallow')
        rule_CB.activated[str].connect(self.onActivated)
        #algorithm combo box
        self.lbl = QLabel('algorithm', self)
        gg.addWidget(self.lbl, 3, 0)
        algo_CB = QComboBox(self)
        gg.addWidget(algo_CB, 3, 1)
        algo_CB.addItem('minimax')
        algo_CB.addItem('alpha-beta')
        algo_CB.activated[str].connect(self.onActivated)
        # quit button
        quit_B = QPushButton('Exit', self)
        right.addWidget(quit_B)
        quit_B.resize(quit_B.sizeHint())
        quit_B.clicked.connect(QCoreApplication.instance().quit) #프로그램을 종료

        #전체 폼박스에 좌우 박스 배치
        formbox.addLayout(left)
        formbox.addLayout(right)
        formbox.setStretchFactor(left, 1)
        formbox.setStretchFactor(right, 0)

#        self.setMouseTracking(True)

        self.show()

    # 창을 화면의 중심으로 설정
    def center(self):
        qr = self.frameGeometry()  # 창의 위치와 크기 정보 가져옴
        cp = QDesktopWidget().availableGeometry().center()  # 모니터 화면의 가운데 위치 파악
        qr.moveCenter(cp)  # 창의 위치를 화면의 중심의 위치로 이동
        self.move(qr.topLeft())  # 창을 qr위치로 이동

    # 오목판 초기화 및 관련 설정 초기화
    def init_board(self):
        self.grid = [[-1 for x in range(15)] for y in range(15)] #바둑 위치 표시하는 배열을 -1로 reset
        # minimax에서 탐색할 boundary로 사용 - b_x1, b_y1, b_x2, b_y2
        self.b_x1 = infinity
        self.b_y1 = infinity
        self.b_x2 = -infinity
        self.b_y2 = -infinity
        #오목판 UI 만들기 - 틀, 15 * 15 선
        #board 틀
        brush = QBrush(QColor(204, 153, 0))
        pen = QPen(QColor(204, 153, 0))
        rect = QRectF(-320, -320, board_l, board_l)
        self.scene.addRect(rect, pen, brush)
        pen = QPen(Qt.black)
        rect = QRectF(-280, -280, board_l-80, board_l-80)
        self.scene.addRect(rect, pen, brush)
        #board 내부 선 15 * 15
        for i in range(1, 14):
            line = QLineF(-280+i*40, -280, -280+i*40, 280)
            self.scene.addLine(line, pen)
            line = QLineF(-280, -280+i*40, 280, -280+i*40)
            self.scene.addLine(line, pen)

        if self.computer == BLACK: #컴퓨터가 선수인경우 가운데에 검은돌 배치하고 시작
            self.draw_baduk(7, 7, self.computer)  # 오목판 정중앙에 검은색 돌 배치

    #옵션의 combo box들에 대한 정보 처리
    #param : combo box의 click된 text
    def onActivated(self, text):
        #level button
        if text == '상급':
            self.level = 3
        elif text == '중급':
            self.level = 2
        elif text == '하급':
            self.level = 1
        #firt player button
        if text == '컴퓨터':
            self.human = WHITE
            self.computer = BLACK
        elif text == '사람':
            self.human = BLACK
            self.computer = WHITE
        #rule button
        if text == 'allow':
            self.rule = 1
        elif text == 'disallow':
            self.rule = 0
        #algorithm button
        if text == 'minimax':
            self.algorithm = MINIMAX
        elif text == 'alpha-beta':
            self.algorithm = ALPHABETA
        # 설정 적용하기 위해 오목판 아무것도 없는 상태로 만들기
        self.init_board()

    #화면상 x,y 좌표를 grid위 i, j로 바꾸기
    #return : grid위 (i, j)
    def xyTogrid(self, x, y):
        x_q, x_r = divmod(x, 40) #칸 사이 간격이 40이므로
        y_q, y_r = divmod(y, 40)
        if x_r >= 20:
            x_q += 1
        if y_r >= 20:
            y_q += 1

        return x_q, y_q

    # 바둑돌 배치
    # param : grid위 (i, j), 돌의 색상(0이면 흰색, 1이면 검은색)
    def draw_baduk(self, x_q, y_q, baduk):
        y = -280 + (y_q) * 40
        x = -280 + (x_q) * 40

        if baduk == 0:  # 0이면 흰색돌
            self.grid[x_q][y_q] = 0  # 흰색 바둑돌 set - grid에 표시
            pen = QtGui.QPen(QtCore.Qt.white)
            brush = QtGui.QBrush(QtCore.Qt.white)
            rect = QRectF(QPointF(x-18, y-18), QSizeF(36, 36))
            self.scene.addEllipse(rect, pen, brush)
        elif baduk == 1:
            self.grid[x_q][y_q] = 1  # 검은색 바둑돌 set - grid에 표시
            pen = QtGui.QPen(QtCore.Qt.black)
            brush = QtGui.QBrush(QtCore.Qt.black)
            rect = QRectF(QPointF(x - 18, y - 18), QSizeF(36, 36))
            self.scene.addEllipse(rect, pen, brush)

    # 보드내 클릭된 위치에 HUMAN 오목 배치 후 알고리즘을 통해 AI 오목 배치하는 함수
    # param: 마우스버튼 클릭시 좌표
    def mousePressEvent(self, e):
        x = e.x() - 55
        y = e.y() - 55
        # 보드내 위치할 경우
        if x >= 0 and x <= 560 and y >= 0 and y <= 560:
            x, y = self.xyTogrid(x, y) #grid위 (i, j)로 가져오기
            if (self.grid[x][y] != -1): #해당 grid[i][j]가 이미 오목 놓여진 경우 인식 안됨
                return
            self.draw_baduk(x, y, self.human) # human 오목 배치
            # 돌 배치후 이겼는지 평가. - 이기면 return 0
            dd = self.outcome(self.grid)
            if dd == 0: #인간이 이긴 경우 - message 창 띄우기
                reply = QMessageBox.question(self, 'message', 'win!', QMessageBox.Yes, QMessageBox.Yes)
            elif dd == -1: #비기거나 결판 안난 경우
                #탐색을 위한 경계 재설정
                self.b_x1, self.b_y1, self.b_x2, self.b_y2 = self.boundary(x, y, self.b_x1, self.b_y1, self.b_x2, self.b_y2)
            #    print(self.b_x1, self.b_y1, self.b_x2, self.b_y2)

                #판이 꽉 찬 경우 비김 - message 창 띄우기
                if self.b_x1 < 0 and self.b_x2 > 14 and self.b_y1 < 0 and self.b_y2 > 14:
                    reply = QMessageBox.question(self, 'message', '비김!', QMessageBox.Yes, QMessageBox.Yes)
                    return

                #HUMAN이 이기지 않았을 경우 AI 배치 -> minimax algorithm or alpha-beta
                if self.algorithm == MINIMAX:
                    #3초 timer를 만든다. 알고리즘 탐색시 결과가 3초이내 나오게 하기위해서
                    self.timer = datetime.datetime.now() + datetime.timedelta(seconds=3)
                    x, y, dd = self.minimax(self.grid, 0, self.computer, x, y, self.b_x1, self.b_y1, self.b_x2, self.b_y2)
                else: #alpha-beta pruning
                    # 3초 timer를 만든다. 알고리즘 탐색시 결과가 3초이내 나오게 하기위해서
                    #self.timer = datetime.datetime.now() + datetime.timedelta(seconds=3)
                    x, y, dd = self.alpha_beta(self.grid, 0, self.computer, [-1, -1, -infinity], [-1, -1, infinity], self.b_x1, self.b_y1, self.b_x2, self.b_y2)
                self.draw_baduk(x, y, self.computer) #바둑 배치
                self.b_x1, self.b_y1, self.b_x2, self.b_y2 = self.boundary(x, y, self.b_x1, self.b_y1, self.b_x2, self.b_y2) #경계 재설정
            #    print(self.b_x1, self.b_y1, self.b_x2, self.b_y2)
            #승패 판정 다시하기
            dd = self.outcome(self.grid)
            if dd == 1: #컴퓨터가 이긴 경우 - message창 띄우기
                reply = QMessageBox.question(self, 'message', 'lose!', QMessageBox.Yes, QMessageBox.Yes)
            elif dd == -1:
                # 판이 꽉 찬 경우 비김 - message 창 띄우기
                if self.b_x1 < 0 and self.b_x2 > 14 and self.b_y1 < 0 and self.b_y2 > 14:
                    reply = QMessageBox.question(self, 'message', '비김!', QMessageBox.Yes, QMessageBox.Yes)

    #주어진 x, y를 통해 경계 다시 설정 - 탐색시 사용될 경계
    #param : 새로 등록된 grid 좌표 (x, y) , 기존 경계 (x1, y1, x2, y2)
    #return : 새로운 경계 (x1, y1, x2, y2)
    def boundary(self, x, y, x1, y1, x2, y2):
        #기존 경계에 x or y있거나 벗어난 곳에 있을 경우 경계 바꿔준다.
        if x < x1:
            x1 = x-1
            if x1 < 0:
                x1 = 0
        if y < y1:
            y1 = y-1
            if y1 < 0:
                y1 = 0
        if x > x2:
            x2 = x+1
            if x2 > 14:
                x2 = 14
        if y > y2:
            y2 = y+1
            if y2 > 14:
                y2 = 14
        return [x1, y1, x2, y2]

    #3 by 3 을 검사 - disallow일 경우를 위해
    # param : 현재 grid, 새로 등록된 grid 좌표(x, y), 등록된 좌표의 player
    # return : 가능(1), 불가능(0)
    '''   def rule33(self, state, x, y, player):
        if player == self.computer:
            if x-3>=0 and state[x-3][y] == -1 and state[x-2][y] == player and state[x-1][y] == player:  # -1 1 1 x
                if y - 3 >= 0 and state[x][y - 3] == -1 and state[x][y - 2] == player and state[x][y - 1] == player:  # -1 1 1 y

                    if y + 3 <= 14 and state[x][y + 3] == -1 and state[x][y + 2] == player and state[x][y + 1] == player:  # y 1 1 -1

                    if x - 3 >= 0 and y - 3 >= 0 and state[x - 3][y - 3] == -1 and state[x - 2][y - 2] == player and state[x - 1][y - 1] == player:  # -1 1 1 x

                    if x - 3 >= 0 and y + 3 >= 0 and state[x - 3][y + 3] == -1 and state[x - 2][y + 2] == player and state[x - 1][y + 1] == player:  # -1 1 1 x
                        ff
                    if x + 3 >= 0 and y - 3 >= 0 and state[x + 3][y - 3] == -1 and state[x + 2][y - 2] == player and state[x + 1][y - 1] == player:  # -1 1 1 x
                        ff
                    if x + 3 >= 0 and y + 3 >= 0 and state[x + 3][y + 3] == -1 and state[x + 2][y + 2] == player and state[x + 1][y + 1] == player:  # -1 1 1 x
            if x+3<=14 and state[x+3][y] == -1 and state[x+2][y] == player and state[x+1][y] == player:  # x 1 1 -1

            if y - 3 >= 0 and state[x][y - 3] == -1 and state[x][y - 2] == player and state[x][y - 1] == player:  # -1 1 1 y

            if y + 3 <= 14 and state[x][y + 3] == -1 and state[x][y + 2] == player and state[x][y + 1] == player:  # y 1 1 -1

            if x-3>=0 and y-3>=0 and state[x-3][y-3] == -1 and state[x-2][y-2] == player and state[x-1][y-1] == player:  # -1 1 1 x

            if x - 3 >= 0 and y + 3 >= 0 and state[x - 3][y + 3] == -1 and state[x - 2][y + 2] == player and state[x - 1][y + 1] == player:  # -1 1 1 x
                ff
            if x + 3 >= 0 and y - 3 >= 0 and state[x + 3][y - 3] == -1 and state[x + 2][y - 2] == player and state[x + 1][y - 1] == player:  # -1 1 1 x
                ff
            if x + 3 >= 0 and y + 3 >= 0 and state[x + 3][y + 3] == -1 and state[x + 2][y + 2] == player and state[x + 1][y + 1] == player:  # -1 1 1 x

        else: #player == human
    '''

    #alpha-beta pruning algorithm
    #처음 시작시 a = [-1, -1, -infinity] , b = [-1, -1, infinity]
    #param : 현재 grid상태, 노드 깊이, human or computer, alpha, beta, boundary
    #return : min or max 깊이에서의 각 node별 min or max 값과 해당 좌표
    def alpha_beta(self, state, depth, player, a, b, x1, y1, x2, y2):
        best = [-1, -1, 0]  # x, y, score
        print('현재 ', depth, ' ', self.level)
        if depth == self.level:  # 난이도별 탐색 깊이를 다르게 설정한다.
            # 지정한 평가함수로 값 판별하여 val에 저장
            best[2] = self.evaluate(state, x1, y1, x2, y2)
            return best
        #boundary 내부에 바둑 하나씩 배치시키며 경우 및 score 찾기 - alpha beta pruning 시작
        chk = [[0 for x in range(15)] for y in range(15)]
        mov = {(0, -1), (0, 1), (-1, 0) , (1, 0)}
        if player == self.computer:  # max 노드
            best[2] = a[2]
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    #timer값 이상이 되면 그 즉시 탐색을 중단하고 값을 반환한다.
                    #if datetime.datetime.now() >= self.timer:
                    #    return best
                    if state[i][j] == -1 or chk[i][j] != 0:  # 빈 cell이거나 이미 check한 cell인 경우 넘어감
                        continue
                    #check하지 않은 흑 or 백 cell인 경우 상.하.좌.우 빈셀에 바둑 배치
                    for (mi, mj) in mov:
                        if i+mi < 0 or i+mi >= 15 or j+mj < 0 or j+mj >= 15:
                            continue
                        if state[i+mi][j+mj] != -1 or chk[i+mi][j+mj] != 0:
                            continue
                        state[i+mi][j+mj] = self.computer
                        chk[i+mi][j+mj] = 1
                        tx1, ty1, tx2, ty2 = self.boundary(i+mi, j+mj, x1, y1, x2, y2) #바둑 배치 후 경계 재설정하여 재귀함수 파라미터로 넣기
                        xx, yy, score = self.alpha_beta(state, depth + 1, self.human, best, b, tx1, ty1, tx2, ty2)
                        #alpha 작업 - max
                        if best[2] < score:
                            best[2] = score
                            if depth == 0:
                                best[0] = i+mi
                                best[1] = j+mj
                        state[i+mi][j+mj] = -1  # 원상복구
                        # pruning 발생 상황 - 발생시 해당 노드의 하위부분 보지 않고 넘어간다
                        if b[2] <= best[2]:
                            print('pruning------')
                            return best
        else:  # HUMAN - min 노드
            best[2] = b[2]
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    if state[i][j] == -1 or chk[i][j] != 0:  # 빈 cell이거나 이미 check한 cell인 경우 넘어감
                        continue
                    #check하지 않은 흑 or 백 cell인 경우 상.하.좌.우 빈셀에 바둑 배치
                    for (mi, mj) in mov:
                        if i+mi < 0 or i+mi >= 15 or j+mj < 0 or j+mj >= 15:
                            continue
                        if state[i+mi][j+mj] != -1 or chk[i+mi][j+mj] != 0:
                            continue
                        state[i+mi][j+mj] = self.human
                        chk[i + mi][j + mj] = 1
                        tx1, ty1, tx2, ty2 = self.boundary(i+mi, j+mj, x1, y1, x2, y2)
                        # 바둑 배치 후 경계 재설정하여 재귀함수 파라미터로 넣기
                        score = self.alpha_beta(state, depth + 1, self.computer, a, best, tx1, ty1, tx2, ty2)
                        #beta 작업 - min
                        if best[2] > score[2]:
                            best[2] = score[2]
                        state[i+mi][j+mj] = -1 #원상복구
                        # pruning 발생 상황 - 발생시 해당 노드의 하위부분 보지 않고 넘어간다
                        if best[2] <= a[2]:
                            print('pruning------')
                            return best
        #pruning 발생 안된경우 return 값
        return best

    #minimax algorithm
    # param : 현재 board, node index, human or computer, 탐색 바운더리 (사각형[[x1, y1], [x2, y2]])
    # return : 현 state에서 평가함수 값 중 가장 큰 or 작은 값과 해당 좌표 (좌표(x, y), socre)
    def minimax(self, state, depth, player, x, y, x1, y1, x2, y2):
        best = [-1, -1, 0] #x, y, score
        if depth == self.level: #난이도별 탐색 깊이를 다르게 설정한다.
            #지정한 평가함수로 값 판별하여 best[2]에 저장
            best[2] = self.evaluate(state, x1, y1, x2, y2)
            return best
        if player == self.computer: #max node
            best[2] = -infinity
        else: #human - min node
            best[2] = infinity
        #minimax algorithm 시작 - boundary 내에만 본다
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                # timer값 이상이 되면 그 즉시 탐색을 중단하고 값을 반환한다.
                if datetime.datetime.now() >= self.timer:
                    return best
                if state[i][j] != -1: #빈 cell인지 확인
                    continue
                if player == self.computer:
                    state[i][j] = self.computer
                    # 바둑 배치 후 경계 재설정하여 재귀함수 파라미터로 넣기
                    tx1, ty1, tx2, ty2 = self.boundary(i, j, x1, y1, x2, y2)
                    score = self.minimax(state, depth+1, self.human, i, j, tx1, ty1, tx2, ty2)
                    if score[2] > best[2]: #max value
                        best[2] = score[2]
                        best[0] = i
                        best[1] = j
                    state[i][j] = -1 #원상복구
                else: #HUMAN
                    state[i][j] = self.human
                    # 바둑 배치 후 경계 재설정하여 재귀함수 파라미터로 넣기
                    tx1, ty1, tx2, ty2 = self.boundary(i, j, x1, y1, x2, y2)
                    score = self.minimax(state, depth+1, self.computer, i, j, tx1, ty1, tx2, ty2)
                    if score[2] < best[2]: #min value
                        best[2] = score[2]
                        best[0] = i
                        best[1] = j
                    state[i][j] = -1

        return best

    #evaluate function - 평가치를 이용하여 score 계산
    #param : 현 grid, boundary
    #return : 계산된 평가치
    def evaluate(self, state, x1, y1, x2, y2):
        score = 0
        #boundary board
        for i in range(x1, x2+1):
            for j in range(y1, y2+1):
                #evalutaion function - black state 경우
                for loc in BLACK_STATE:
                    #column
                    flag = True #STATE와 같은 모양 확인
                    blank = False #빈 or 흰색 cell 연속 2번나오는지 확인 - 연속 두번이면 한 state비교 끝난 것
                    for k in range(0, 7):
                        #연속 두번 빈 cell or 흰색 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == WHITE:
                            if blank == False:
                                blank = True
                            else: #blank == True
                                if k == 1:  #맨 처음 연속 2번이 빈 or 흰색 cell이면 flag는 false, 중간에 연속2번 나오는건 상관 없다
                                    flag = False
                                break
                        else: #검은색 cell
                            blank = False
                        if j+k > 15 or i>15: #경계 넘어가도 break
                            flag = False
                            break
                        #벽인지 확인 - j+k가 벽일 경우 벽은 흰색으로 간주한다. 따라서 loc[k] 가 0인지만 확인하면 됨
                        if j+k == 15 or i == 15:
                            if loc[k] != WHITE:
                                flag = False
                                break
                            continue
                        #STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i][j+k]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK: #컴퓨터가 선수경우 black_state는 컴퓨터에게 유리한것으로 양수값 더한다.
                            score += loc[7]
                        else: #사람이 선수경우 black_state는 컴퓨터에게 불리함. score에 음수값을 더한다.
                            score -= loc[7] * 2.4
                        break
                    #row
                    flag = True  # STATE와 같은 모양 확인
                    blank = False  # 빈 ot 흰색 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        # 연속 두번 빈 cell or 흰색 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 0:
                            if blank == False:
                                blank = True
                            else:  # blank == True
                                break
                        else:  # 검은 cell
                            blank = False
                        # 벽인지 확인
                        if i+k > 15 or j > 15:
                            flag = False
                            break
                        if i + k == 15 or j == 15:
                            if loc[k] != 0:
                                flag = False
                                break
                            continue
                        # STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i+k][j]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 black_state는 컴퓨터에게 유리한것으로 양수값 더한다.
                            score += loc[7]
                        else:  # 사람이 선수경우 black_state는 컴퓨터에게 불리함. score에 음수값을 더한다.
                            score -= loc[7] * 2.4
                        break
                    #right_diagnoals
                    flag = True  # STATE와 같은 모양 확인
                    blank = False  # 빈 ot 흰색 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        # 연속 두번 빈 cell or 흰색 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 0:
                            if blank == False:
                                blank = True
                            else:  # blank == True
                                break
                        else:  # 검은 cell
                            blank = False
                        # 벽인지 확인
                        if j+k > 15 or i+k > 15:
                            flag = False
                            break
                        if j + k == 15 or i + k == 15:
                            if loc[k] != 0:
                                flag = False
                                break
                            continue
                        # STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i+k][j + k]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 black_state는 컴퓨터에게 유리한것으로 양수값 더한다.
                            score += loc[7]
                        else:  # 사람이 선수경우 black_state는 컴퓨터에게 불리함. score에 음수값을 더한다.
                            score -= loc[7] * 2.4
                        break
                    #left_diagonals
                    flag = True  # STATE와 같은 모양 확인
                    blank = False  # 빈 ot 흰색 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        # 연속 두번 빈 cell or 흰색 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 0:
                            if blank == False:
                                blank = True
                            else:  # blank == True
                                break
                        else:  # 검은 cell
                            blank = False
                        # 벽인지 확인
                        if j+k > 15 or i-k < -1:
                            flag = False
                            break
                        if j + k == 15 or i-k == -1:
                            if loc[k] != 0:
                                flag = False
                                break
                            continue
                        # STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i - k][j + k]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 black_state는 컴퓨터에게 유리한것으로 양수값 더한다.
                            score += loc[7]
                        else:  # 사람이 선수경우 black_state는 컴퓨터에게 불리함. score에 음수값을 더한다.
                            score -= loc[7] * 2.4
                        break
                # evalutaion function - white state 경우
                for loc in WHITE_STATE:
                    #column
                    flag = True #STATE와 같은 모양 확인
                    blank = False #빈 or 검정 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        #연속 두번 빈 cell or 검정 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 1:
                            if blank == False:
                                blank = True
                            else: #blank == True
                                break
                        else: #흰색 cell
                            blank = False
                        if j+k > 15 or i > 15:
                            flag = False
                            break
                        #벽인지 확인
                        if j+k == 15 or i == 15:
                            if loc[k] != 1:
                                flag = False
                                break
                            continue
                        #STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i][j+k]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 white_state는 컴퓨터에게 불리것으로 음수값 더한다.
                            score -= loc[7] * 2.4
                        else:  # 사람이 선수경우 white_state는 컴퓨터에게 유리함. score에 양수값을 더한다.
                            score += loc[7]
                        break
                    #row
                    flag = True  # STATE와 같은 모양 확인
                    blank = False  # 빈 ot 검정 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        # 연속 두번 빈 cell or 검정 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 1:
                            if blank == False:
                                blank = True
                            else:  # blank == True
                                break
                        else:  # 흰 cell
                            blank = False
                        # 벽인지 확인
                        if i+k > 15 or j > 15:
                            flag = False
                            break
                        if i + k == 15 or j == 15:
                            if loc[k] != 1:
                                flag = False
                                break
                            continue
                        # STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i+k][j]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 white_state는 컴퓨터에게 불리것으로 음수값 더한다.
                            score -= loc[7] * 2.4
                        else:  # 사람이 선수경우 white_state는 컴퓨터에게 유리함. score에 양수값을 더한다.
                            score += loc[7]
                        break
                    #right_diagnoals
                    flag = True  # STATE와 같은 모양 확인
                    blank = False  # 빈 ot 검정 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        # 연속 두번 빈 cell or 검정 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 1:
                            if blank == False:
                                blank = True
                            else:  # blank == True
                                break
                        else:  # 흰 cell
                            blank = False
                        # 벽인지 확인
                        if j+k > 15 or i+k > 15:
                            flag = False
                            break
                        if j + k == 15 or i + k == 15:
                            if loc[k] != 1:
                                flag = False
                                break
                            continue
                        # STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i+k][j + k]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 white_state는 컴퓨터에게 불리것으로 음수값 더한다.
                            score -= loc[7] * 2.4
                        else:  # 사람이 선수경우 white_state는 컴퓨터에게 유리함. score에 양수값을 더한다.
                            score += loc[7]
                        break
                    #left_diagonals
                    flag = True  # STATE와 같은 모양 확인
                    blank = False  # 빈 ot 검정 cell 연속 2번나오는지 확인
                    for k in range(0, 7):
                        # 연속 두번 빈 cell or 검정 cell 나오는지 확인
                        if loc[k] == -1 or loc[k] == 1:
                            if blank == False:
                                blank = True
                            else:  # blank == True
                                break
                        else:  # 흰 cell
                            blank = False
                        # 벽인지 확인
                        if j+k > 15 or i-k < -1:
                            flag = False
                            break
                        if j + k == 15 or i-k == -1:
                            if loc[k] != 1:
                                flag = False
                                break
                            continue
                        # STATE의 해당 자리와 같은 값인지 확인
                        if loc[k] != state[i - k][j + k]:
                            flag = False
                            break
                    # 같은 모양 찾으면 score에 점수 더하고 다음 으로 넘어가기
                    if flag == True:
                        if self.computer == BLACK:  # 컴퓨터가 선수경우 white_state는 컴퓨터에게 불리것으로 음수값 더한다.
                            score -= loc[7] * 2.4
                        else:  # 사람이 선수경우 white_state는 컴퓨터에게 유리함. score에 양수값을 더한다.
                            score += loc[7]
                        break

        return score

    # 현재 board의 상태
    # param : 현 grid
    # return : 인간승(0), 인간패(1), 비김 or 결정 안됨 (-1)
    def outcome(self, state):
        if self.wins(state, self.computer):
            score = +1
        elif self.wins(state, self.human):
            score = 0
        else:
            score = -1
        return score

    # player의 오목알이 연속으로 5개 있는 것 찾기 - winner
    # param : 현 grid, computer or human
    # return : player의 승(1), 이외에(0)
    def wins(self, state, player):
        for i in range(0,15): #x
            for j in range(0, 15): #y
                flag = True #5줄이 모두 같을 경우 유지됨 아닐경우 false
                # row
                for k in range(0, 5):
                    if j+4 > 14 or state[i][j+k] != player:
                        flag = False
                        break
                if flag == True:
                    return True #5줄 찾은 경우 true 반환
                flag = True  # 5줄이 모두 같을 경우 유지됨 아닐경우 false
                # column
                for k in range(0, 5):
                    if i+4 > 14 or state[i+k][j] != player:
                        flag = False
                        break
                if flag == True:
                    return True  # 5줄 찾은 경우 true 반환
                # right_diagonals
                flag = True  # 5줄이 모두 같을 경우 유지됨 아닐경우 false
                for k in range(0, 5):
                    if i+4 > 14 or j+4 > 14 or state[i+k][j + k] != player:
                        flag = False
                        break
                if flag == True:
                    return True  # 5줄 찾은 경우 true 반환
                # left_diagonals
                flag = True  # 5줄이 모두 같을 경우 유지됨 아닐경우 false
                for k in range(0, 5):
                    if i-4 < 0 or j+4 > 14 or state[i-k][j + k] != player:
                        flag = False
                        break
                if flag == True:
                    return True  # 5줄 찾은 경우 true 반환
        return False #모든 행을 다 찾았지만 없을 경우 false 반환

if __name__ == '__main__':  # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv)  # 모든 pyqt5 어플리케이션은 application 객체를 생성
    ex = MyApp()
    sys.exit(app.exec_())
