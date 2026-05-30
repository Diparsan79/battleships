
def render(board_width, board_height, shots):
    header = "+" + "-" * board_height + "+"
    print(header)
    
    for y in range(board_height):
        row = []
        for x in range(board_width):
            if (x,y) in shots:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|"+ "".join(row) + "|")
        
    print(header)

if __name__ =="__main__":
    render(10,10,[(3,1), (4,5), (8,1)])

    inp = input("Where do you want to shoot? \n")
    xstr, ystr = inp.split(",")
    x = int(xstr)
    y = int(ystr)
