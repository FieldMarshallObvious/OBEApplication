from manim import *

class BasicUpdated(Scene):
    """Basic updater which shows how updater continues through plays"""
    def construct(self):
        blue_dot = Dot(color=BLUE)
        dot_label = Text("Hello dot!").next_to(blue_dot, UP)
        dot_label.add_updater(
            lambda mobject: mobject.next_to(blue_dot, UP)
        )
        self.add(blue_dot, dot_label)
        self.play(blue_dot.animate.shift(RIGHT))
        self.play(blue_dot.animate.scale(3))
        self.play(blue_dot.animate.center())

class AllUpdaterTypes(Scene):
    """Shows Scene updaters with mobject updaters"""
    def construct(self):
        red_dot = Dot(color=RED).shift(LEFT)
        pointer = Arrow(ORIGIN, RIGHT).next_to(red_dot, LEFT)
        pointer.add_updater(
            lambda mobject: mobject.next_to(red_dot, LEFT)
        )
        def shifter(mobject, dt):
            mobject.shift(2*dt*RIGHT)
        
        red_dot.add_updater(shifter)

        def scene_scaler(dt):
            for mobject in self.mobjects:
                mobject.set(width=1/(1 +np.linalg.norm(mobject.get_center())))
        
        self.add_updater(scene_scaler)

        self.add(red_dot, pointer)
        self.update_self(0)
        self.wait(5)

class UpdaterAnimation(Scene):
    """Shows how updaters work through wait and suspended"""
    def construct(self):
        red_dot = Dot(color=RED).shift(LEFT)
        rotating_square = Square()
        rotating_square.add_updater(
            lambda mobject, dt: mobject.rotate(PI*dt)
        )

        def shifter(mobject, dt):
            mobject.shift(2*dt*RIGHT)
        red_dot.add_updater(shifter)

        # Square will continue using updater
        self.add(red_dot, rotating_square)
        self.wait(1)
        # We will forcibly stop red_dot from running
        red_dot.suspend_updating()

        # After this red_dot will resume animation
        self.play(
            red_dot.animate.shift(UP),
            rotating_square.animate.move_to([-2,-2,0])
        )
        self.wait(1)

class BasicValueTracker(Scene):
    """How to use value trackers
    
    Value Trackers --> An invisible mobject which stores numbers, this allows other mobjects to be animated off this number
    """
    def construct(self):
        line = NumberLine(x_range=[-5,5])
        position = ValueTracker(0)
        pointer = Vector(DOWN)
        pointer.add_updater(
            lambda mobject: mobject.next_to(
                line.number_to_point(position.get_value()), UP
            )
        )
        pointer.update() # Can run updater mannually here
        self.add(line, pointer)
        self.wait()
        self.play(position.animate.set_value(4))
        self.play(position.animate.set_value(-2))

class ValueTrackerPlot(Scene):
    def construct(self):
        a = ValueTracker(1)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-8.5, 8.5, 2], x_length=4, y_length=6)
        parabola = ax.plot(lambda x: x**2, color=RED)
        # Make parabola based on value tracker
        parabola.add_updater(
            lambda mobject: mobject.become(ax.plot(lambda x: a.get_value() * x**2, color=RED))
        )
        # Display the current value of the value tracker
        a_number = DecimalNumber(
            a.get_value(),
            color=RED,
            num_decimal_places=3,
            show_ellipsis=False
        )
        a_number.add_updater(
            lambda mobject: mobject.set_value(a.get_value()).next_to(parabola, RIGHT)
        )
        self.add(ax, parabola, a_number)
        self.play(a.animate.set_value(2))
        self.play(a.animate.set_value(-2))
        self.play(a.animate.set_value(1))
        self.wait()