from manim import *

class CustomProgressBar(Scene):
    def construct(self):
        # Create the outline of the progress bar
        bar_outline = Rectangle(width=6, height=1, color=WHITE)
        bar_outline.set_fill(BLACK, opacity=1)

        # Initialize the progress bar with a very small fill
        initial_fill = Rectangle(width=0.1, height=1, color=WHITE)
        initial_fill.set_fill(WHITE, opacity=1)
        initial_fill.set_stroke(width=0)
        initial_fill.next_to(bar_outline.get_left(), RIGHT, buff=0)

        # Add the outline and initial fill to the scene
        self.add(bar_outline, initial_fill)

        # Variable to keep track of the current fill object
        current_fill = initial_fill

        # Animate the progress bar
        for i in range(1, 11):  # Example: 10 steps to fill the bar
            new_width = 0.6 * i  # Incremental width
            if new_width > 6:
                new_width = 6

            new_fill = Rectangle(width=new_width, height=1, color=WHITE)
            new_fill.set_fill(WHITE, opacity=1)
            new_fill.set_stroke(width=0)
            new_fill.next_to(bar_outline.get_left(), RIGHT, buff=0)

            # Replace the old fill with the new one in the animation
            self.play(Transform(current_fill, new_fill))
            if new_width == 6:
                break  # Stop if the bar is full
        
        # Determine if the progress completes or fails
        success = True  # Change this to False to simulate failure


        if success:
            current_fill.set_fill(GREEN)
            current_fill.set_stroke(color=GREEN)
            bar_outline.set_fill(GREEN)
            bar_outline.set_stroke(color=GREEN) 
        else:
            current_fill.set_fill(RED)
            current_fill.set_stroke(color=RED)
            bar_outline.set_fill(RED)
            bar_outline.set_stroke(color=RED) 

        # If success, emphasize green
        self.play(
            Wiggle(current_fill,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=current_fill.get_center()),
            Wiggle(bar_outline,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=current_fill.get_center()),
        )
        self.wait(1)

# To run this scene, use the following command in your terminal:
# manim -pql your_script_name.py CustomProgressBar
