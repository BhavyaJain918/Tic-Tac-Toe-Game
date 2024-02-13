import socket
import numpy as np
size = 1024
host = ""     # IP Address of Host Server
port = 5050
add = (host , port)
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
try:
    client.connect(add)
except ConnectionRefusedError as cr:
    print(f"Error occurred: {cr}")
    client.close()
    exit()
except ConnectionError as c:
    print(f"Error occurred: {c}")
    client.close()
    exit()
def play_client(matrix1):
    try:
        matrx = eval("np.array(" + matrix1 + ')')
        print("Current matrix: \n" , matrx)
        position = input("Enter position you want to place 'O' on: ")
        coordinate = position.split(" ")
        if matrx[(int(coordinate[0]))][(int(coordinate[1]))] == None:
            matrx[(int(coordinate[0]))][(int(coordinate[1]))] = 'O'
            print("You played: \n" , matrx)
        else:
            print("Invalid position. Your chance is forfeited")
        return np.array2string(matrx , separator = ',')
    except ValueError as ve:
        return ("102")
    except IndexError as ie:
        return ("104")
    
def server1():
    msg1 = client.recv(size).decode()
    print(msg1)
    while True:
        try:
            global mat
            msg3 = client.recv(size).decode()
            client.send("Player 2 is playing...".encode())
            if msg3 == "Player 1 is playing...":
                print(msg3)
                mat = client.recv(size).decode()
            if (mat == "W1" or msg3 == "W2"):
                if mat == "W1": 
                    print("\nGame Over. Player 1 won")
                elif msg3 == "W2":
                    print("\nGame Over. You won") 
                break
            else:    
                res = play_client(mat)
                if res != "102" and res != "104":
                    client.send(res.encode())
                else:
                    print("Enter correct numerical values only")
                    client.send(mat.encode())
        except ConnectionResetError as re:
            print(f"Error occurred: {re}")
            client.close()
            exit()
    client.close()

server1()