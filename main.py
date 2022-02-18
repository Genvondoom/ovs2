import socket
import threading
import utility
import mysqlengine

HEADER = 64
PORT = 3309  # browse about ports
SERVER = "127.0.0.1"  # socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # famil, type of addresses
server.bind(ADDR)


def handle_clients(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    loggedIn = False
    selectedElection = ""
    user = ""

    try:

        while connected:
            msg = conn.recv(2048).decode()
            data = msg.split(',')

            if data[0] == "login":

                if mysqlengine.checkLogin(mysqlengine.cursor, data[1], data[2]) is True:
                    conn.send("success.".encode())
                    user = data[1]
                    print(f"[ALERT]: USER {user} HAS SUCCESSFULLY LOGGED IN!!")
                    loggedIn = True
                elif mysqlengine.checkLogin(mysqlengine.cursor, data[1], data[2]) is False:
                    print(f"[WARNING] LOGIN FAILED")
                    conn.send("login error.".encode())
            # Create election
            elif loggedIn == True:
                if data[0] == "create election":
                    data = utility.createElection(data[1:])
                    print(data)
                    if mysqlengine.insertElection(mysqlengine.cursor, mysqlengine.connection, data) == "done":
                        conn.send("election created.".encode())
                        print(f"[ALERT]: USER {user} CREATED Election {data[1]}")
                    elif mysqlengine.insertElection(mysqlengine.cursor, mysqlengine.connection,
                                                    data[1:]) == "duplicate":
                        conn.send(f"election already exists.".encode())
                        print(f"[WARNING]: USER {user} TRIED TO CREATE DUPLICATE ELECTION {data[1]}!!")

                elif data[0] == "view election":
                    temp = mysqlengine.getElections(mysqlengine.cursor)
                    print(f"[ALERT]: SENDING USER {user} ELECTION LIST....")
                    for x in temp:
                        conn.send(f"{utility.listToStingConverter(x)}.".encode())

                    conn.send("stop.".encode())
                    print(f"[ALERT]: ELECTION LIST SENT TO USER {user}!!")

                elif data[0] == "select election":

                    temp2 = mysqlengine.selectElection(mysqlengine.cursor, data[1])
                    print(f"[ALERT] USER {user} SENDING SELECTED ELECTION {selectedElection}")
                    if temp2 is not False:
                        for x in temp2:
                            conn.send(f"{utility.listToStingConverter(x)}.".encode())
                        conn.send("stop.".encode())
                        selectedElection = data[1]
                        print(f"[ALERT] USER {user} SENT SELECTED ELECTION {selectedElection}")

                    elif temp2 is False:
                        conn.send(f"{utility.listToStingConverter(['not found'])}.".encode())
                        conn.send("stop.".encode())
                        print(F"[WARNING] USER {user} SELECTED ELECTION THAT DOESN'T EXIST")

                elif data[0] == "join election":
                    if selectedElection and user:
                        utility.generateToken(selectedElection, user)
                        datatemp = [utility.generateToken(selectedElection, user), user, selectedElection, "active"]
                        datatemp.insert(2, data[1])
                        temp3 = mysqlengine.joinElection(mysqlengine.cursor, mysqlengine.connection, datatemp)
                        if temp3 == "done":
                            print("Okay")
                            conn.send("sucess.".encode())
                        elif temp3 == "duplicate":
                            print("duplicate")
                            conn.send("duplicate.".encode())

                    # Create Election
            elif data[0] == "signup" and loggedIn == False:
                print(f"[ALERT]: CREATING USER ACCOUNT {data[1]}.....")
                if mysqlengine.insertUsers(mysqlengine.cursor, mysqlengine.connection, data[1:]) == "done":
                    conn.send("account created.".encode())
                    print(f"[ALERT]: USER ACCOUNT {data[1]} SUCCESSFULLY CREATED!!")
                elif mysqlengine.insertUsers(mysqlengine.cursor, mysqlengine.connection, data[1:]) == "duplicate":
                    conn.send(f"username already exists.".encode())
                    print(f"[ALERT]: USER ACCOUNT {data[1]} ALREADY EXIST!!")

            elif data[0] == "logout":
                loggedIn = False
                conn.send("logged out.".encode())
                print(f"[ALERT] USER {user} HAS LOGGED OUT!!")

            else:
                conn.send("message received.".encode())




    except BrokenPipeError:
        connected = False
        conn.close()
        print(f"[{addr}] HAS BEEN DISCONNECTED!!")
    except ConnectionResetError:
        connected = False
        conn.close()
        print(f"[{addr}] HAS BEEN DISCONNECTED!!")


def start():
    server.listen()
    print(f"[LISTENING]: SERVER is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION]: connecting to {addr}")
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting . . . ")
start()
