from manim import *
import random

class CustomProgressBar(Scene):
    def construct(self):
        rectangle_height = 0.5
        # Create the outline of the progress bar
        bar_outline = Rectangle(width=6, height=rectangle_height, color=WHITE)
        bar_outline.set_fill(BLACK, opacity=1)

        # Initialize the progress bar with a very small fill
        initial_fill = Rectangle(width=0.1, height=rectangle_height, color=WHITE)
        initial_fill.set_fill(WHITE, opacity=1)
        initial_fill.set_stroke(width=0)
        initial_fill.next_to(bar_outline.get_left(), RIGHT, buff=0)

        # Add the outline and initial fill to the scene
        self.add(bar_outline, initial_fill)

        # Variable to keep track of the current fill object
        current_fill = initial_fill

        # Animate the progress bar
        for i in range(1, 4):
            fail_point = random.randint(1, 9) if i < 3 else 12
            for j in range(1, 11):  # Example: 10 steps to fill the bar
                new_width = 0.6 * j  # Incremental width
                if new_width > 6:
                    new_width = 6

                new_fill = Rectangle(width=new_width, height=rectangle_height, color=WHITE)
                new_fill.set_fill(WHITE, opacity=1)
                new_fill.set_stroke(width=0)
                new_fill.next_to(bar_outline.get_left(), RIGHT, buff=0)

                # Replace the old fill with the new one in the animation
                self.play(Transform(current_fill, new_fill))

                if j == fail_point:
                    current_fill.set_fill(RED)
                    current_fill.set_stroke(color=RED)
                    bar_outline.set_stroke(color=RED)
                    self.play(
                        Wiggle(current_fill,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=current_fill.get_center()),
                        Wiggle(bar_outline,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=bar_outline.get_center()),
                    )
                    self.play(Transform(current_fill, initial_fill))
                    current_fill = initial_fill
                    bar_outline.set_stroke(color=WHITE)
                    break


                if new_width == 6:
                    break  # Stop if the bar is full
            
        current_fill.set_fill(GREEN)
        current_fill.set_stroke(color=GREEN)
        bar_outline.set_fill(GREEN)
        bar_outline.set_stroke(color=GREEN) 

        # If success, emphasize green
        self.play(
            Wiggle(current_fill,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=current_fill.get_center()),
            Wiggle(bar_outline,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=bar_outline.get_center()),
        )
        self.wait(1)
