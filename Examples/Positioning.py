from manim import *
from manim.utils.unit import Percent, Pixels

class Positioning(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)

        # Add dots to the screen
        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN)
        green_dot.next_to(red_dot, RIGHT + UP)
        self.add(red_dot, green_dot)

        # shift
        square = Square(color=ORANGE)
        square.shift(2*UP + 4*RIGHT)
        self.add(square)

        # move_to
        circle = Circle(color=PURPLE)
        circle.move_to([-3, -2, 0])
        self.add(circle)

        # algin to
        circle_2 = Circle(radius=0.5, color=RED, fill_opacity=0.5)
        circle_3 = circle_2.copy().set_color(YELLOW)
        circle_4 = circle_2.copy().set_color(ORANGE)
        circle_2.align_to(square, UP)
        circle_3.align_to(square, RIGHT)
        circle_4.align_to(square, UP+RIGHT)
        self.add(circle_2)
        self.add(circle_3)
        self.add(circle_4)

class CriticalPoints(Scene):
    def construct(self):
        circle = Circle(color=GREEN, fill_opacity=0.5)
        self.add(circle)

        for direction in [(0,0,0), UP, UR, RIGHT, DR, DOWN, DL, LEFT, UL]:            
            self.add(Cross(scale_factor=0.2).move_to(circle.get_critical_point(direction)))
        
        square = Square(color=RED, fill_opacity=0.5)
        square.move_to([1,0,0], aligned_edge=LEFT)
        self.add(square)

class UsefulUnits(Scene):
    def construct(self):
        for percentage in range(5, 51, 5):
            self.add(Circle(radius=percentage * Percent(X_AXIS)))
            self.add(Square(side_length=2*percentage*Percent(Y_AXIS), color=YELLOW))
        
        dot = Dot()
        dot.shift(100 * Pixels * RIGHT)
        self.add(dot)

class AnimateCirlce(Scene):
    def construct(self):
        lastCircle = None
        for percentage in range(5, 51, 5):
            currentCircle = Circle(radius=percentage * Percent(X_AXIS))

            if lastCircle is not None:
                self.play(ReplacementTransform(lastCircle, currentCircle))
                self.play(Indicate(currentCircle, scale_factor=1.05, color=BLUE))
                continue
            lastCircle = currentCircle

class Grouping(Scene):
    def construct(self):
        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN).next_to(red_dot, RIGHT)
        blue_dot = Dot(color=BLUE).next_to(red_dot, UP)
        dot_group = VGroup(red_dot, green_dot, blue_dot)
        dot_group.to_edge(RIGHT)
        self.add(dot_group)

        circles = VGroup(*[Circle(radius=0.2) for _ in range(10)])
        circles.arrange(UP, buff=0.5)
        self.add(circles)

        stars = VGroup(*[Star(color=YELLOW, fill_opacity=0.5) for _ in range(20)])
        stars.arrange_in_grid(4, 5, 0.2)
        self.add(stars)
        