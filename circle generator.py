import turtle
import random

def spawn_cel(max_radius):
   t = turtle.Turtle()
   t.speed(0)
   t.hideturtle()

   screen = turtle.Screen()
   w = screen.window_width() // 2
   h = screen.windowheight() // 2


    x = random.randint(-w, w)
    y = random.randint(-h, h)
    radius = random.randint(10, max_radius)
    color = (random.random(), random.random(), random.random())

    t.penup()
    t.goto(x, y - radius)
    t.pendown()

    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

    screen.mainloop()
