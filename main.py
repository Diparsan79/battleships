def render(board_width,board_height, shots):
    header= "+"+ "-" * board_width + "+"
    print(header)
    for i in range(board_height):
        row = [  ]
        print("|" + " " * board_width + "|")

    print(header)

    

if __name__ =="__main__":
    render(10,10, [(2,1),(3,1), (4,5), (8,1)])
    inpt = input("where do you want to shoot?\n")
    xstr,ystr = inpt.split(",")
    x = int(xstr)
    y = int(ystr)

    