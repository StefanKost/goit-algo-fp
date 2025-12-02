import turtle
import math


def draw_tree(t, length, level, max_level):
    if level == 0:
        return

    # Determine color
    if level > max_level * 0.4:
        # Trunk: brown
        t.pencolor(139, 69, 19)
    else:
        # Branches/Leaves: gradient green
        green_value = int(100 + 155 * ((max_level * 0.4 - level) / (max_level * 0.4)))  # dark -> light
        t.pencolor(0, green_value, 0)

    t.forward(length)

    pos = t.pos()
    ang = t.heading()

    # Left branch
    t.left(45)
    draw_tree(t, length / math.sqrt(2), level - 1, max_level)

    # Return to original position and heading
    t.penup()
    t.setpos(pos)
    t.setheading(ang)
    t.pendown()

    # Right branch
    t.right(45)
    draw_tree(t, length / math.sqrt(2), level - 1, max_level)

    # Return to original position and heading
    t.penup()
    t.setpos(pos)
    t.setheading(ang)
    t.pendown()


def main():
    level = int(input("Enter the number of levels (5 - 12): "))

    wn = turtle.Screen()
    wn.title("Pythagoras Tree")
    wn.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.left(90)
    t.penup()
    t.goto(0, -200)
    t.pendown()

    # Enable RGB colors
    turtle.colormode(255)
    draw_tree(t, 200, level, level)

    wn.mainloop()


if __name__ == "__main__":
    main()
