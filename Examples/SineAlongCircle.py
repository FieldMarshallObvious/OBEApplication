from manim import *
from scipy.misc import derivative

class SineAlongCircle(Scene):
    def construct(self):
        # Define the axes
        ax = Axes(
            x_range=[-1, 8], 
            y_range=[-4, 4],
            tips=True,
            axis_config={"include_numbers": True, "tip_shape": StealthTip},
        )
        
        # Create the circle
        sin_curve = ax.plot(lambda x: np.sin(x), color=RED)
        sin_circle = Circle(radius=1, color=WHITE).move_to(ax.c2p(0,0) + 1*LEFT)
        # Create the dot
        dot = Dot(color=RED).move_to(sin_circle.get_critical_point(RIGHT))

        self.curve_start = np.array([-4.5,0,0])
        self.t_offset = 0
        

        
        def update_dot(mob, dt):
            rate_of_change = dt * abs(np.sin(dt)) * 30
            if self.t_offset > 1 * np.pi:
                rate_of_change *= 0.9

            self.t_offset += rate_of_change
            mob.move_to(sin_circle.point_from_proportion((self.t_offset/ TAU) % 1))
        
        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = dot.get_center()[0]
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve
        
        def move_circle(mob, dt):
            speed_factor = 1 if self.t_offset < 1 * np.pi else abs(np.sin(dt)) * 25
            new_x = sin_circle.get_center()[0] + dt * speed_factor
            new_y = sin_circle.get_center()[1]
            new_position = [new_x, new_y, sin_circle.get_center()[2]]
            mob.move_to(new_position)

        
        sine_curve_line = always_redraw(get_curve)
            
        # Initialize the offset for the dot's rotation
        self.t_offset = 0

        self.add(ax, sin_circle, dot, sine_curve_line, sin_curve)
        self.add(dot.add_updater(update_dot))
        self.add(sin_circle.add_updater(move_circle))

        self.wait(24)        
        # Remove updater to avoid conflict with other animations or renders
        dot.remove_updater(update_dot)
        sine_curve_line.remove_updater(move_circle)

        # End the scene
        self.wait()

class Sine_Curve(Scene):
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()

        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.orgin_point = np.array([-4,0,0])
        self.curve_start = np.array([-3,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r'\pi'), MathTex(r'2 \pi'),
            MathTex(r'3 \pi'), MathTex(r'4 \pi'),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1+2*i,0,0]), DOWN )
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.orgin_point)

        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        orgin_point = self.orgin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(orgin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x,y,0]), color=YELLOW_A, stroke_width=2 )


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)