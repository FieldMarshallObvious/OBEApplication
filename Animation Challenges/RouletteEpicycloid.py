from manim import *

class Easy(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Inputs
        k = float(input("What is your desired k: "))
        R = 1.5
        r = R/k

        animation_time = 5

        # Setup shapes
        large_circle = Circle(color=BLUE, radius=R)
        small_circle = Circle(color=PURPLE, radius=r).next_to(large_circle, RIGHT, buff=0)
        small_circle.rotate_about_origin(180*DEGREES)
        small_circle.next_to(large_circle, RIGHT, buff=0)
        dot = Dot(color=YELLOW).move_to(small_circle.get_critical_point(LEFT))
        line = Line(dot.get_center(), small_circle.get_center(), color=BLACK, stroke_width=2)

        self.curve = VGroup()
        self.curve.add(Line(large_circle.get_critical_point(RIGHT),large_circle.get_critical_point(RIGHT)))

        # Animation state
        self.circle_origin = small_circle.get_center()
        self.t_offset = 0
        self.num_rotations = 0

        def update_dot(mob, dt, rate_function=linear):
            rate = k/animation_time
            self.t_offset += dt*rate
            self.t_offset %= 1 
            if not np.array_equal(small_circle.get_center(), self.circle_origin): 
                mob.move_to(small_circle.point_from_proportion(rate_function(self.t_offset)))

        
        def get_curve():
            last_line = self.curve[-1]
            x = dot.get_center()[0]
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        def get_line():
            return Line(dot.get_center(), small_circle.get_center(), color=BLACK, stroke_width=2)
        
        
        trace_dot = always_redraw(get_curve)

        # Add objects
        follow_line = always_redraw(get_line)
        self.add(follow_line)
        self.add(large_circle,small_circle, dot, trace_dot)
        self.play(
            Create(large_circle.set_points(large_circle.get_points()[::1])), 
            Create(small_circle.set_points(small_circle.get_points()[::1])), 
            GrowFromCenter(dot),
            GrowFromCenter(follow_line)
        )
        
        self.wait(1)

        # Trace Epicycloid
        dot.add_updater(update_dot)

        self.play(
            Rotate(small_circle, angle=2*PI, about_point=large_circle.get_center(), rate_func=linear, run_time=animation_time)        
        )

        dot.remove_updater(update_dot)

        self.wait(2)

class Hard(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Inputs
        ks = [3,4,5,7]
        animation_time = 5

        # Setup shapes
        ax = Axes(
            x_range=[-7,7], y_range=[-3.5,3.5], 
            axis_config={"include_numbers":True},
            tips=True
        )
        ax.set_color(BLACK)
        
        R = (ax.c2p(3,0)[0] - ax.c2p(0,0)[0])

        large_circle = Circle(color=BLUE, radius=R)
        large_circle.move_to(ax.c2p(0,0))
        self.add(large_circle, ax)
        self.play(Create(large_circle), Create(ax))
        for k in ks:
            r = R/k
            small_circle = Circle(color=BLACK, radius=r).next_to(large_circle, RIGHT, buff=0)
            small_circle.rotate_about_origin(180*DEGREES)
            small_circle.next_to(large_circle, RIGHT, buff=0)
            dot = Dot(color=RED).move_to(small_circle.get_critical_point(LEFT))

            self.curve = VGroup()
            self.curve.add(Line(large_circle.get_critical_point(RIGHT),large_circle.get_critical_point(RIGHT)))

            # Animation state
            self.circle_origin = small_circle.get_center()
            self.t_offset = 0
            self.num_rotations = 0
            self.run_time = 0
            self.last_dt = 0

            def update_dot(mob, dt, rate_function=linear):
                rate = k/animation_time
                self.last_dt = dt
                self.run_time += dt
                self.t_offset += dt*rate
                self.num_rotations += 1 if self.t_offset >= 1 else 0
                self.t_offset %= 1 
                if self.run_time < animation_time - 1.9*dt: 
                    mob.move_to(small_circle.point_from_proportion(rate_function(self.t_offset)))
                else:
                    mob.move_to(small_circle.get_critical_point(LEFT))
            
            def get_curve():
                last_line = self.curve[-1]
                x = dot.get_center()[0]
                y = dot.get_center()[1]

                if self.run_time < animation_time - 2.1*self.last_dt:
                    new_line = Line(last_line.get_end(),np.array([x,y,0]), color=RED)
                    self.curve.add(new_line)


                return self.curve

            def get_line():
                return Line(dot.get_center(), small_circle.get_center(), color=BLACK, stroke_width=2)
            
            
            trace_dot = always_redraw(get_curve)

            follow_line = always_redraw(get_line)
            self.add(small_circle, dot, trace_dot, follow_line)
            self.play(
                Create(small_circle.set_points(small_circle.get_points()[::1])), 
                GrowFromCenter(dot),
                GrowFromCenter(follow_line)
            )
            
            self.wait(1)

            # Trace Epicycloid
            dot.add_updater(update_dot)

            self.play(
                Rotate(small_circle, angle=2*PI, about_point=large_circle.get_center(), rate_func=linear, run_time=animation_time)        
            )

            self.wait(3)

            self.play(
                FadeOut(small_circle), 
                FadeOut(follow_line), 
                FadeOut(trace_dot),
                FadeOut(dot)
            )
            self.wait(2)
        self.play(
            Uncreate(ax),
            Uncreate(large_circle)
        )
        self.wait(2)
