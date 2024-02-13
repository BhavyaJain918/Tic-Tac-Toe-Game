import socket
import numpy as np
size = 1024
host = socket.gethostbyname(socket.gethostname())
port = 5050
add = (host , port)
mat = [[None , None , None] , 
       [None , None , None] , 
       [None , None , None]]
soc = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
soc.bind(add)
global num
num = np.array(mat)

def decide(matrix_):
    diagonal = np.diag(matrix_)
    flip1 = np.fliplr(matrix_)
    diagonal2 = np.diag(flip1)
    res_colx = np.all(matrix_ == 'X' , axis = 0)
    res_rowx = np.all(matrix_ == 'X' , axis = 1)
    res_colx1 = np.all(matrix_ == 'O' , axis = 0)
    res_rowx1 = np.all(matrix_ == 'O' , axis = 1)
    if all(d == 'X' for d in diagonal) or all(df == 'X' for df in diagonal2) or (True in res_colx) or (True in res_rowx):
        return ("W1")
    elif all(diag1 == 'O' for diag1 in diagonal) or all(df1 == 'O' for df1 in diagonal2) or (True in res_colx1) or (True in res_rowx1):
        return ("W2")
    else:
        return 1
    
def play_server():
    global num
    try:
        position = input("Enter position you want to place 'X' on: ")
        coord = position.split(" ")
        if num[(int(coord[0]))][(int(coord[1]))] == None:
            num[(int(coord[0]))][(int(coord[1]))] = 'X'
            print("You played: \n" , num)
        else:
            print("Invalid position. Your chance is forfeited")
        return np.array2string(num , separator = ',')
    except ValueError as v:
        return ("101")
    except IndexError as i:
        return ("103")
    
def resp(response):
    global num
    num = eval("np.array(" + response + ')')
    print("Opponent played: \n" , num)

def goto(connect , res , status):
    try:
        connect.send(res.encode())
        print(status)
        cl_res = connect.recv(size).decode()
        resp(cl_res)
    except ConnectionAbortedError as ca:
        print("Connection aborted")

def client(connect , address):
    global num
    print(f"Connection established with {address}")
    print("Welcome to the game of Tic-Tac-Toe. You are Player 1. Your token is 'X'.\n Place you token on an appropriate position as and when your chance comes in order to win the game.")
    connect.send("Welcome to the game of Tic-Tac-Toe. You are Player 2.Your token is 'O'.\n Place you token on an appropriate position as and when your chance comes in order to win the game.".encode())
    print(num)
    while True:
        try:
            ret = decide(num)
            if ret == 1:
                connect.send("Player 1 is playing...".encode())
                status = connect.recv(size).decode()
                res = play_server() 
                ret1 = decide(num)
                if ret1 == 1:
                    if res != "101" and res != "103":
                        goto(connect , res , status)
                    else:
                        print("Enter correct numerical values only")
                        goto(connect , np.array2string(num , separator = ',') , status)
                else:
                    continue
            else:
                if ret == "W1":
                    print("\nGame Over. You won")
                else:
                    print("\nGame Over. Player 2 won")
                connect.send(ret.encode())
                break
        except ConnectionResetError as rec:
            print(f"Error occurred: {rec}")
            connect.close()
            exit()
    soc.close()

def init():
    soc.listen(1)
    conn , addr = soc.accept()
    client(conn , addr)
print(f"Ready to start the game. Your IP Address is: {host}. Share this IP Address to play with a friend remotely.")
init()