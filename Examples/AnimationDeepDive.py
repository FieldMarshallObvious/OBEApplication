from manim import *

from colour import Color

class BasicAnimations(Scene):
    def construct(self):
        polys = VGroup(
        *[
            RegularPolygon(5, radius=1, color=ManimColor.from_rgb(Color(hue=j/5, saturation=1, luminance=0.5).get_rgb()), 
            fill_opacity=0.5)
            for j in range(5)
        ]
        ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys), run_time=2)
        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t, start_anim=5), # rate_func=linear
            Rotate(polys[1], PI, rate_func=smooth, start_anim=0.4),  # default behavior for most animations
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t*PI), start_anim=0.6),
            Rotate(polys[3], PI, rate_func=there_and_back, start_anim=0.8),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1-2*t), start_anim=1),
            run_time=2
        )
        self.wait()

class LaggingGroup(Scene):
    def construct(self):
        squares = VGroup(
        *[
                Square(color=ManimColor.from_rgb(Color(hue=j/20, saturation=1, luminance=0.5).get_rgb()), 
                fill_opacity=0.5)
                for j in range(20)
        ]).arrange_in_grid(4,5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.15))

class AnimateSyntax(Scene):
    def construct(self):
        square = Square(color=GREEN, fill_opacity=0.5)
        circle = Circle(color=RED, fill_opacity=0.5)
        self.add(square, circle)

        self.play(square.animate.shift(UP), circle.animate.shift(DOWN))
        self.play(VGroup(square, circle).animate.rramge(RIGHT, buff=1))
        self.play(circle.animate(rate_func=linear).shift(RIGHT).scale(2))

class AnimateProblem(Scene):
    def construct(self):
        left_square = Square()
        right_square = Square()
        VGroup(left_square, right_square)
        self.add(left_square, right_square)
        self.play(left_square.animate.rotate(PI), Rotate(right_square, PI), run_time=2)
        self.wait()

class AnimateMechanisms(Scene):
    def construct(self):
        circle = Circle()

        circle.generate_target()
        circle.target.set_fill(color=GREEN, opacity=0.5)
        circle.target.shift(2*RIGHT + UP).scale(0.5)

        self.add(circle)
        self.wait()
        self.play(MoveToTarget(circle))

        square = Square()
        square.save_state()
        self.play(FadeIn(square))
        self.play(square.animate.set_color(PURPLE).set_opacit(0.5).shift(2*LEFT).scale(3))
        self.play(square.animate.shift(5*DOWN).rotate(PI/4))
        self.wait()
        self.play(Restore(square), run_time=2)
        self.wait()


class SimpleCustomAnimation(Scene):
    def construct(self):
        def spiral_out(mobject, t):
            radius = 4 * t
            angle = 2*t * 2*PI
            mobject.move_to(radius*(np.cos(angle)*RIGHT + np.sin(angle)*UP))
            mobject.set_color(ManimColor.from_rgb(Color(hue=t, saturation=1, luminance=0.5).get_rgb()))
            mobject.set_opacity(1-t)
        
        d = Dot(color=YELLOW)
        self.add(d)
        self.play(UpdateFromAlphaFunc(d, spiral_out, run_time=3))

class Disperse(Animation):
    def __init__(self, mobject, dot_radius=0.05, dot_number=100, **kwargs):
        super().__init__(mobject, **kwargs)
        self.dot_radius = dot_radius
        self.dot_number = dot_number
    
    def begin(self):
        dots = VGroup(
            *[Dot(radius=self.dot_radius).move_to(self.mobject.point_from_proportion(p))
            for p in np.linspace(0, 1, self.dot_number)]
        )
        for dot in dots:
            dot.initial_position = dot.get_center()
            dot.shift_vector = 2*(dot.get_center() - self.mobject.get_center())
        dots.set_opacity(0)
        self.mobject.add(dots)
        self.dots = dots
        super().begin()
        
    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        scene.remove(self.dots)

    def interpolate_mobject(self, alpha):
        alpha = self.rate_func(alpha)  # manually apply rate function
        if alpha <= 0.5:
            self.mobject.set_opacity(1 - 2*alpha, family=False)
            self.dots.set_opacity(2*alpha)
        else:
            self.mobject.set_opacity(0)
            self.dots.set_opacity(2*(1 - alpha))
            for dot in self.dots:
                dot.move_to(dot.initial_position + 2*(alpha-0.5)*dot.shift_vector)
            
            

class CustomAnimationExample(Scene):
    def construct(self):
        st = Star(color=YELLOW, fill_opacity=1).scale(3)
        self.add(st)
        self.wait()
        self.play(Disperse(st, dot_number=200, run_time=4))