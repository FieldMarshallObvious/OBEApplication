from manim import *

class SineAlongCircle(Scene):
    def construct(self):
        # Define the axes
        ax = Axes(
            x_range=[-1, 8], 
            y_range=[-3, 3],
            tips=True,
            axis_config={"include_numbers": True, "tip_shape": StealthTip},
        )
        
        # Create the circle
        sin_circle = Circle(radius=1, color=WHITE).move_to(ax.c2p(0,0) + 1*LEFT)
        
        # Create the dot
        dot = Dot(color=RED).move_to(sin_circle.get_critical_point(RIGHT))

        sin_curve = ax.plot(lambda x: np.sin(x), color=RED)

        path_curve = ax.plot(lambda x: np.sin(x), color=YELLOW, fill_opacity=0, x_range=[0, 7])
        path_curve.z_index = 0
        sin_curve.z_index = 1
        
        def update_dot(mob, dt):
            rate = (2*PI)/15  # Speed control
            # Update the parameter t, decrease to move backwards
            mob.t += rate * dt

            # Ensure t stays within the valid range
            mob.t %= 2 * PI

            # Update the position of the dot
            mob.move_to(path_curve.point_from_proportion(mob.t / (2 * PI)))
            
        dot.t = 0
        # Initialize the offset for the dot's rotation
        self.t_offset =0

        self.add(ax, sin_circle, sin_curve, dot, path_curve)
        self.add(dot.add_updater(update_dot))

        self.play(sin_circle.animate.shift(6.5*RIGHT), run_time=8, rate_func=linear)
        self.play(sin_circle.animate.shift(6.5*LEFT), run_time=10, rate_func=linear)
        
        # Remove updater to avoid conflict with other animations or renders
        dot.remove_updater(update_dot)

        # End the scene
        self.wait()
