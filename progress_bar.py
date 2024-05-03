from manim import *
import random

class ProgressBar(VGroup):
    def __init__(self, completed_color=GREEN, failed_color=RED, task_title="", rectangle_height=0.5, failures=3, max_steps=10, **kwargs):
        super().__init__(**kwargs)
        self.completed_color = completed_color
        self.failed_color = failed_color
        self.task_title = task_title
        self.rectangle_height = rectangle_height
        self.failures = failures
        self.max_steps = max_steps
        self.current_width = 0

        self.setup_bar_outline()
        self.setup_initial_fill()
        self.setup_text()
        self.setup_structure()

        self.failure_point = random.randint(0, max_steps - 1)

    def setup_bar_outline(self):
        self.bar_outline = Rectangle(width=6, height=self.rectangle_height, color=WHITE)
        self.bar_outline.set_fill(BLACK, opacity=1)
        self.add(self.bar_outline)

    def setup_initial_fill(self):
        self.initial_fill = Rectangle(width=0.1, height=self.rectangle_height, color=WHITE)
        self.initial_fill.set_fill(WHITE, opacity=1)
        self.initial_fill.set_stroke(width=0)
        self.current_fill = self.initial_fill
        self.add(self.current_fill)

    def setup_text(self):
        self.task_text = Text(self.task_title).next_to(ORIGIN, LEFT)
        self.add(self.task_text)

    def setup_structure(self):
        self.task_text.next_to(ORIGIN, LEFT)
        self.bar_outline.next_to(self.task_text, RIGHT, buff=0.5)
        self.initial_fill.next_to(self.bar_outline.get_left(), RIGHT, buff=0)


class ProgressBarComplete(Animation):
    def __init__(self, mobject: ProgressBar, **kwargs):
        if not isinstance(mobject, ProgressBar):
            raise ValueError(f"mobject must be an instance of ProgressBar, is type:{type(mobject)}")
        super().__init__(mobject, **kwargs)
        self.failures = 3

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)

    def interpolate_mobject(self, alpha):
        step_size = 6 / self.mobject.max_steps
        current_step = int(alpha * self.mobject.max_steps)
        #print("current step:", current_step)
        new_width = current_step * step_size
        #print("New width is", new_width)
        if new_width > 6:
            new_width = 6

        new_fill = Rectangle(width=new_width, height=self.mobject.rectangle_height, color=WHITE)
        new_fill.set_fill(WHITE, opacity=1)
        new_fill.set_stroke(width=0)
        new_fill.next_to(self.mobject.bar_outline.get_left(), RIGHT, buff=0)
        self.mobject.current_fill.interpolate(self.mobject.current_fill, new_fill, alpha)

class CustomProgressBar(Scene):
    def construct(self):
        
        progressBars = []
        animations = []
        tasks = ["Path Sine Wave", "Fail Interview", "Eat Babies"] 
        def check_bar(mob, dt):
            current_fill = mob.current_fill
            bar_outline = mob.bar_outline
            initial_fill = mob.initial_fill
            task_text = mob.task_text

            if dt == mob.failure_point:
                    current_fill.set_fill(RED)
                    current_fill.set_stroke(color=RED)
                    bar_outline.set_stroke(color=RED)
                    self.play(
                        Indicate(current_fill, scale_factor=1.3, color=RED_C)                 
                    )
                    self.play(Transform(current_fill, initial_fill))
                    current_fill = initial_fill
                    bar_outline.set_stroke(color=WHITE)
            if mob.current_width == 6:
                self.play(
                    Wiggle(current_fill,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=current_fill.get_center()),
                    Wiggle(bar_outline,scale_factor=1.2, rotation_angle=0.15, rotate_about_point=bar_outline.get_center()),
                )
                self.wait(1)
                self.play(
                    FadeOut(bar_outline, shift=DOWN), 
                    FadeOut(initial_fill, shift=DOWN), 
                    FadeOut(task_text, shift=DOWN)
                )

        for location, task_title in enumerate(tasks):
            try:
                adjusted_location = len(tasks) - location 
                bar = ProgressBar(task_title=task_title)
                bar.shift(UP*adjusted_location)
                bar.add_updater(check_bar)
                progressBars.append(bar)
                self.add(bar)
                self.play(
                    FadeIn(bar.bar_outline, shift=DOWN), 
                    FadeIn(bar.initial_fill, shift=DOWN), 
                    FadeIn(bar.task_text, shift=DOWN)
                )
                animations.append(ProgressBarComplete(bar, scene=self, run_time=5))
            except Exception as e:
                logger.error(f"Error creating ProgressBar for '{task_title}': {e}")

        #self.play(AnimationGroup(*animations, run_time=5))
        self.wait(1)

    def create_progress_bar(self, task_title: str, location: int):
        rectangle_height = 0.2
        # Create the outline of the progress bar
        bar_outline = Rectangle(width=6, height=rectangle_height, color=WHITE).shift(DOWN*location)
        bar_outline.set_fill(BLACK, opacity=1)

        # Initialize the progress bar with a very small fill
        initial_fill = Rectangle(width=0.1, height=rectangle_height, color=WHITE).shift(DOWN*location)
        initial_fill.set_fill(WHITE, opacity=1)
        initial_fill.set_stroke(width=0)
        initial_fill.next_to(bar_outline.get_left(), RIGHT, buff=0)

        # Create text
        task_text = Text(task_title).next_to(ORIGIN, LEFT).shift(DOWN*location)

        bar_outline.next_to(task_text, RIGHT, buff=0.5)
        initial_fill.next_to(bar_outline.get_left(), RIGHT, buff=0)

        # Add the outline and initial fill to the scene
        self.add(bar_outline, initial_fill, task_text)
        self.play(
            FadeIn(bar_outline, shift=DOWN), 
            FadeIn(initial_fill, shift=DOWN), 
            FadeIn(task_text, shift=DOWN)
        )

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
                        Indicate(current_fill, scale_factor=1.3, color=RED_C)                 
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
        self.play(
            FadeOut(bar_outline, shift=DOWN), 
            FadeOut(initial_fill, shift=DOWN), 
            FadeOut(task_text, shift=DOWN)
        )
