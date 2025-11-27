import turtle

def draw_triangle(size=100, color="blue"):
    """
    Draw an equilateral triangle using the turtle graphics module.
    
    Args:
        size (int): Length of each side of the triangle in pixels
        color (str): Color of the triangle
    """
    if not isinstance(size, (int, float)) or size <= 0:
        raise ValueError("Size must be a positive number")
    
    if not isinstance(color, str):
        raise TypeError("Color must be a string")
    
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    
    pen = turtle.Turtle()
    pen.speed(1)
    pen.color(color)
    pen.pensize(2)
    
    # Draw equilateral triangle (3 sides, 120 degrees each)
    for _ in range(3):
        pen.forward(size)
        pen.left(120)
    
    pen.hideturtle()
    turtle.done()


if __name__ == "__main__":
    # Draw a blue triangle with default size
    draw_triangle(size=150, color="blue")