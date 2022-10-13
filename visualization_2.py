from turtle import Turtle, Screen

def draw_grid():  # for debugging
    grid = Turtle(visible=False)
    grid.speed('fastest')
    grid.dot()  # visualize origin
    grid.penup()
    grid.goto(-GRID_CELL_SIZE * NUMBER_SQUARES / 2, GRID_CELL_SIZE * (NUMBER_SQUARES / 2 - 1))

    for _ in range(NUMBER_SQUARES - 1):
        grid.pendown()
        grid.forward(NUMBER_SQUARES * GRID_CELL_SIZE)
        grid.penup()
        grid.goto(-GRID_CELL_SIZE * NUMBER_SQUARES / 2, grid.ycor() - GRID_CELL_SIZE)

    grid.goto(-GRID_CELL_SIZE * (NUMBER_SQUARES / 2 - 1), GRID_CELL_SIZE * NUMBER_SQUARES / 2)

    grid.setheading(270)

    for _ in range(NUMBER_SQUARES - 1):
        grid.pendown()
        grid.forward(NUMBER_SQUARES * GRID_CELL_SIZE)
        grid.penup()
        grid.goto(grid.xcor() + GRID_CELL_SIZE, GRID_CELL_SIZE * NUMBER_SQUARES / 2)

    #defining robots turtle
    axes = Turtle(visible=False)
    # robot 1 position
    axes.pu()
    axes.setpos(0,150)
    axes.write("Robot 1", align="center", font=("Times New Roman", 14, "normal"))
    axes.settiltangle(270)
    axes.stamp()
    # robot 2 position
    axes.pu()
    axes.setpos(0,-170)

    axes.settiltangle(90)
    axes.stamp()
    axes.write("Robot 2", align="center", font=("Times New Roman", 14, "normal"))

    am = Turtle(visible=False)

def label():

    trtl = Turtle(visible=True)
    # set position
    trtl.penup()
    trtl.setpos(0,0)
    trtl.pendown()

    # write 0
    trtl.write(150,align="left",font=("Verdana", 12, "bold"))

    # set position again
    trtl.penup()
    trtl.setpos(300,0)
    trtl.pendown()

    # write x
    trtl.write("x",align="left",font=("Verdana", 12, "bold"))

    # set position again
    trtl.penup()
    trtl.setpos(0,300)
    trtl.pendown()

    # write y
    trtl.write("y",align="left",font=("Verdana", 12, "bold"))

    # axes

    trtl.color('green')
    trtl.pensize(3)

    # set position for x axis
    trtl.up()
    trtl.setpos(-150,-150)
    trtl.down()

    # x-axis
    trtl.forward(300)

    # set position for y axis
    trtl.left(90)
    #trtl.up()
    #trtl.setpos(-150,-150)
    #trtl.down()

    # y-axis
    trtl.forward(300)
    trtl.left(90)
    trtl.forward(300)
    trtl.left(90)
    trtl.forward(300)

def gcodePath():
    x, y, t = [], [], []
    x_, y_, t_ = [], [], []

    with open("HQH_R1_Thickness 0.45_Contours 10_Reverse.txt", "r") as myfile:
        for line in myfile.readlines():
            if 'Layer' in line:
                x.append(0.0)
                y.append(0.0)
                t.append(0)
            elif 'Interfacing' in line or "Non-interfacing" in line:
                pass
            else:
                data = line.split()
                #print("data", data)
                x.append(data[0])
                y.append(data[1])
                t.append(data[3])

    with open("HQH_R2_Thickness 0.45_Contours 10.txt", "r") as myfile2:
        for line in myfile2.readlines():
            if 'Layer' in line:
                x_.append(0.0)
                y_.append(0.0)
                t_.append(0)
            elif 'Interfacing' in line or "Non-interfacing" in line:
                pass
            else:
                data = line.split()
                x_.append(data[0])
                y_.append(data[1])
                t_.append(data[3])

    ambot1 = Turtle(visible=True)
    ambot2 = Turtle(visible=True)

    turtles = [ambot1, ambot2]
    color1 = ['blue', 'green', 'yellow']
    color2 = ['red', 'orange', 'pink']
    col_index = 0
    ambot1.speed(9)
    ambot2.speed(9)
    ambot1.penup()
    ambot2.penup()
    for move in range(len(x)):
        if col_index >= len(color2):
            col_index = 0
        ambot1.pencolor(color1[col_index])
        ambot2.pencolor(color2[col_index])
        #ambot2.pencolor('red')
        ambot1.pensize(1)
        ambot2.pensize(1)

        x1 = float(x[move]) - 150.00
        y1 = float(y[move]) - 150.00
        x2 = float(x_[move]) - 150.00
        y2 = float(y_[move]) - 150.00
        # x2 = float(300 - float(x_[move]))
        # y2 = float(300 - float(y_[move]))
        if x1 == -150.0 and y1 == -150.0:
            col_index += 1
        else:

            ambot1.goto(x1, y1)
            ambot2.goto(x2, y2)
            ambot1.pendown()
            ambot2.pendown()


        screen.update()
        #col_index += 1
        # ambot1.clear()
        # ambot2.clear()

GRID_CELL_SIZE = 10  # pixels
NUMBER_SQUARES = 60  # this for creating the 7x7 grid map
screen = Screen()

draw_grid()  # for debugging
label()
gcodePath()
screen.mainloop()
