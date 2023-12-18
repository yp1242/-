import copy

#定义四种移动方式
up = 0
right = 1
down = 2
left = 3


#定义棋子
#（可能的棋子为1个长方形横条，4个长方形竖条，1个正方形棋子，4个小方块）
#一个棋子对象，有4个成员变量（使用成员变量描述棋子状态）
#chess_type:
#长方形横条的chess_type为2，长方形竖条的chess_type为3，正方形的chess_type为4
#小方块的chess_type为5。
#chess_position：每个棋子左上角的格子的二维坐标。
#direction: 该数组表示棋子是否可以往上下左右四个方向移动（及移动后是否超出边界）
#moveable：该布尔值表示棋子是否可以被至少往一个方向移动
class chess_piece:
    def __init__(self, name, chess_type, chess_position):
        self.name = name
        self.chess_type = chess_type
        self.chess_position= chess_position
        self.direction = [0,0,0,0]
        self.moveable = False
        
#定义表示棋盘状态的节点
class node:
    def __init__(self):
        #棋盘共有20个格子，每个格子由1个0来初始化。在真正的棋盘（0）外包围了
        #一圈1，是为了用1判断棋子移动后是否超出棋盘范围。
        self.board = [[1,1,1,1,1,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,1,1,1,1,1]]
        #curr_status存储棋盘当前的状态（存储当前棋盘中的棋子）
        self.curr_status = []
        #curr_move用于计数，用于记录当前节点的所有子节点（所有移动的可能性）
        #是否都被推入队列。若curr_move大于等于my_queue的长度，代表当前节点的所有
        #子节点都已被推入队列。
        self.curr_move = 0
        #next_step存储在curr_status下，所有可能的下一步状态
        self.next_status = []
        #parent存储当前节点的父节点。为每个节点存储父节点，是为了在找到解时，
        #通过父节点回溯，计算得到该解所用的步数。
        self.parent = None

    #find_symmetric函数计算当前状态curr_status的对称状态，用于剪枝
    def find_symmetric(self):
        sym = copy.deepcopy(self.board)
        for i in range(1,6):
            for j in range(1,3):
                sym[i][j],sym[i][5-j] = sym[i][5-j],sym[i][j]
        return sym

    #update_chess_piece函数更新某一个棋子所占据的位置
    def update_chess_piece(self,my_chess_piece):
        #由于初始化棋盘时，在真正的棋盘周围包了一圈1，所以
        #需要在棋子横纵坐标上都加1。
        x = my_chess_piece.chess_position[0]+1
        y = my_chess_piece.chess_position[1]+1
        z = my_chess_piece.chess_type
        if(x<0 or y<0 or x>5 or y>6):
            return
        #如果棋子为长方形横条，则占据的棋盘横坐标为x，占据的棋盘纵坐标为y和y+1
        if x<=5 and y<=6 and my_chess_piece.chess_type == 2:
            self.board[x][y] = my_chess_piece.chess_type
            self.board[x][y+1] = my_chess_piece.chess_type
        #如果棋子为长方形竖条，则占据的棋盘横坐标为x和x+1，占据的棋盘纵坐标为y
        elif x<=5 and y<=6 and my_chess_piece.chess_type == 3: 
            self.board[x][y] = my_chess_piece.chess_type
            self.board[x+1][y] = my_chess_piece.chess_type
        #如果棋子为正方形
        elif x<=5 and y<=6 and  my_chess_piece.chess_type == 4:
            self.board[x][y] = my_chess_piece.chess_type
            self.board[x+1][y] = my_chess_piece.chess_type
            self.board[x][y+1] = my_chess_piece.chess_type
            self.board[x+1][y+1] = my_chess_piece.chess_type
        elif x<=5 and y<=6: #如果棋子为小方块，或为真正棋盘的外圈包的1。
            self.board[x][y] = my_chess_piece.chess_type

    #update_board函数更新棋盘
    def update_board(self):
        #每次都会根据初始状态更新棋盘
        self.board = [[1,1,1,1,1,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,0,0,0,0,1],
                      [1,1,1,1,1,1]]
        for x in self.curr_status:
            self.update_chess_piece(x)

    #update_chess_movable更新棋子是否可以被移动（移动后是否超出棋盘边界）
    #该函数会更新棋子的moveable属性和direction属性
    def update_chess_moveable(self,my_chess_piece):
        x = my_chess_piece.chess_position[0] + 1
        y = my_chess_piece.chess_position[1] + 1
        my_chess_piece.direction=[0,0,0,0]
        if(x<0 or y<0 or x>5 or y>6):
            return
        if my_chess_piece.chess_type == 2:
            if x<=5 and y<=6 and y-1>=0:
                if self.board[x][y-1] == 0 :
                    my_chess_piece.direction[left] = 1  
            if x<=5 and y<=6 and x-1>=0 and y+1<=6:
                if self.board[x-1][y] == 0 and self.board[x-1][y+1] == 0:
                    my_chess_piece.direction[up] = 1   
            if x<=5 and y<=6 and x+1<=5 and y+1<=6:
                if self.board[x+1][y] == 0 and self.board[x+1][y+1] == 0:
                    my_chess_piece.direction[down] = 1   
            if x<=5 and y<=6 and y+2<=6:
                if self.board[x][y+2] == 0:
                    my_chess_piece.direction[right] = 1   
        elif my_chess_piece.chess_type == 3:
            if x<=5 and y<=6 and y-1>=0 and x+1<=5:
                if self.board[x][y-1] == 0 and self.board[x+1][y-1] == 0:   
                    my_chess_piece.direction[left] = 1  
            if x<=5 and y<=6 and x-1>=0:
                if self.board[x-1][y] == 0:                               
                 my_chess_piece.direction[up] = 1   
            if x<=5 and y<=6 and x+2<=5:
                if self.board[x+2][y] == 0:                               
                    my_chess_piece.direction[down] = 1   
            if y+1<=6 and x+1<=5:
                if self.board[x][y+1] == 0 and self.board[x+1][y+1] == 0:   
                    my_chess_piece.direction[right] = 1   
        elif my_chess_piece.chess_type == 4:
            if x<=5 and y<=6 and y-1>=0 and x+1<=5:
                if self.board[x][y-1] == 0 and self.board[x+1][y-1] == 0:
                    my_chess_piece.direction[left]=1  
            if x<=5 and y<=6 and x-1>=0 and y+1<=6:
                if self.board[x-1][y] == 0 and self.board[x-1][y+1] == 0:
                    my_chess_piece.direction[up] =1    
            if x<=5 and y<=6 and x+2<=5 and y+1<=6:
                if self.board[x+2][y] == 0 and self.board[x+2][y+1] == 0:
                    my_chess_piece.direction[down] = 1   
            if x<=5 and y<=6 and y+2<=6 and x+1<=5:
                if self.board[x][y+2] == 0 and self.board[x+1][y+2] == 0:
                    my_chess_piece.direction[right] = 1   
        else:
            if x<=5 and y<=6 and y-1>=0:
                if self.board[x][y-1] == 0 :
                    my_chess_piece.direction[left] = 1  
            if x<=5 and y<=6 and x+1>=0:
                if self.board[x-1][y] == 0 :
                    my_chess_piece.direction[up] = 1   
            if x<=5 and y<=6 and x+1<=5:
                if self.board[x+1][y] == 0:
                    my_chess_piece.direction[down] = 1   
            if x<=5 and y<=6 and y+1<=6:
                if self.board[x][y+1] == 0:
                    my_chess_piece.direction[right] = 1   
        if sum(my_chess_piece.direction) > 0:
            my_chess_piece.moveable=True
            
    #update_board_moveable更新当前棋盘是否还有可移动的可能性。
    #即更新每个棋子的可移动性（moveable和direction属性）。
    def update_board_moveable(self):
        #遍历棋盘中的棋子
        for x in self.curr_status:
            #print(x.chess_position[0])
            #print("\n")
            #print(x.chess_position[1])
            self.update_chess_moveable(x)

    def moving_queue(self):
        #next_status存储棋子可以移动的方向（上下左右所对应的数字0，1，2，3）
        self.next_status = []
        self.curr_move = 0
        for x in self.curr_status:
            if x.moveable: #如果棋子至少可以往一个方向移动
                for i in range(4):
                    if x.direction[i] == 1:
                        self.next_status.append([i,x.name])

    #在移动棋子这个函数中，x为只有两个元素的list。
    #x[0]表示当前棋子的移动方向，x[1]表示当前棋子的chess_type。
    def move_chess_piece(self,x):
        #遍历棋盘中的棋子，尝试移动每一个chess_type为x[1]的可移动的棋子。
        for i in self.curr_status:
            if i.name != x[1]:
                continue
            if x[0] == up:
                i.chess_position[0] -= 1
            elif x[0]==down:
                i.chess_position[0] += 1  
            elif x[0]==left:
                i.chess_position[1] -= 1  
            elif x[0]==right:
                i.chess_position[1] += 1

    #有四种情况可以判定已找到解（成功将正方形移到下方中间处）：
    #注意：chess_position为棋子左上角的坐标。
    #注意：棋子的横纵坐标分别+1，可以得到棋子在board上的坐标。
    #（1）正方形棋子左上角坐标为[3,1]；
    #（2）正方形棋子左上角坐标为[2,1]，且棋盘[5,2]和[5,3]的格子处为0（空），即
    #该正方形棋子下方为空，可以被直接移出；
    #（3）正方形棋子左上角坐标为[3,0]，且棋盘[4,3]和[5,3]的格子处为0（空），即
    #该正方形棋子已被挪到棋盘左下方，且该棋子的右侧为空；
    #（4）正方形棋子左上角坐标为[3,2]，且棋盘[4,2]和[5,2]的格子处为0（空），即
    #该正方形棋子已被挪到棋盘右下方，且该棋子的左侧为空；             
    def success(self):
        #遍历棋盘中的棋子找到正方形棋子
        for i in self.curr_status:
            if i.chess_type == 4:
                if i.chess_position[0]==3 and i.chess_position[1]==1:                
                    return True
                if i.chess_position[0]==2 and i.chess_position[1]==1:
                    if self.board[4+1][1+1]==0 and self.board[4+1][2+1]==0:
                        return True
                if i.chess_position[0]==3 and i.chess_position[1]==0:
                    if self.board[3+1][2+1]==0 and self.board[4+1][2+1]==0:
                        return True
                if i.chess_position[0]==3 and i.chess_position[1]==2:
                    if self.board[3+1][1+1]==0 and self.board[4+1][1+1]==0:
                        return True
        return False

    def print_board(self):
        for i in self.board:
            print(i)



#初始化棋盘（初始化的方法有很多种，可以从外部传入参数，传入该函数，
#作为每个棋子初始化的坐标）
#这里为了方便使用，直接为棋子坐标赋值。

#已产生的棋盘
boards_list = []
#为广度优先搜索而存储节点的队列
que = []
#创造根节点
root = node()

#初始化棋子
#main_square = chess_piece(4,[0,1])
#ver_rectangle1 = chess_piece(3,[0,0])
#ver_rectangle2 = chess_piece(3,[0,3])
#ver_rectangle3 = chess_piece(3,[2,0])
#ver_rectangle4 = chess_piece(3,[2,3])
#hori_rectangle = chess_piece(2,[2,1])
#square1 = chess_piece(5,[3,1])
#square2 = chess_piece(5,[3,2])
#square3 = chess_piece(5,[4,0])
#square4 = chess_piece(5,[4,3])

main_square = chess_piece("main_square",4,[0,1])
ver_rectangle1 = chess_piece("ver_rectangle1",3,[0,0])
ver_rectangle2 = chess_piece("ver_rectangle2",3,[0,3])
ver_rectangle3 = chess_piece("ver_rectangle3",3,[2,3])
ver_rectangle4 = chess_piece("ver_rectangle4",3,[3,0])
hori_rectangle = chess_piece("hori_rectangle",2,[2,0])
square1 = chess_piece("square1",5,[3,1])
square2 = chess_piece("square2",5,[3,2])
square3 = chess_piece("square3",5,[4,3])
square4 = chess_piece("square4",5,[2,2])

#将棋子添加进根节点的curr_status
root.curr_status.append(main_square)
root.curr_status.append(ver_rectangle1)
root.curr_status.append(ver_rectangle2)
root.curr_status.append(ver_rectangle3)
root.curr_status.append(ver_rectangle4)
root.curr_status.append(hori_rectangle)
root.curr_status.append(square1)
root.curr_status.append(square2)
root.curr_status.append(square3)
root.curr_status.append(square4)

root.update_board() #根据初始化结果，更新棋盘上的棋子分布情况
root.update_board_moveable()
root.moving_queue()

#将生成的棋盘添加进boards_list
boards_list.append(root.board)

#将根节点推入队列，开始广度优先搜索的循环部分
que.append(root)


while True: #如果要为搜索设定搜索次数上限，改变这里的循环条件即可
    if(len(que)<=0):
        print("No Solution found")
        break;
    while True: #找到一个当前节点的未入队列的子节点时，会跳出该循环
        #判断当前队列的队首节点的全部子节点是否都已入队列，若是，将其从队首移出。
        if(len(que)<=0):
            break;
        if que[0].curr_move >= len(que[0].next_status):
            que.pop(0)
            continue
        curr_node = copy.deepcopy(que[0])
        curr_node.move_chess_piece(curr_node.next_status[curr_node.curr_move])
        que[0].curr_move += 1
        curr_node.update_board()
        #剪枝（如果遇到曾经出现过的棋盘状态，或和曾经出现过的棋盘对称的棋盘状态，则
        #不推入队列，直接跳过）
        if curr_node.board in boards_list:
            continue
        elif curr_node.find_symmetric() in boards_list:
            continue
        else:
            break
        
    #curr_node为当前队首节点的一个子节点（下一步状态的其中一步）
    curr_node.update_board_moveable()
    curr_node.moving_queue()
    curr_node.parent = que[0]
    boards_list.append(curr_node.board)
    if curr_node.success():
        print("Find a solution")
        curr_node.print_board()
        #通过父节点回溯计算，得到当前的解花了多少步
        count = 0     
        while True:
            if curr_node.parent:
                count += 1
                curr_node = curr_node.parent
            else:
                break
        print("#Steps: {}".format(count))
    else: #如果curr_node不是该问题的解，将其推入队列，继续循环
        que.append(curr_node)
