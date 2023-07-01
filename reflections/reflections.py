from manim import *

class ReflectionScene(Scene):
    def construct(self):
        self.s = 7. # Length of string
        self.v = 2. # Propagation velocity
        self.reflection_sign = 1 # Set to -1 for negative reflections
        self.show_intro()
        # "Space dimension x on the horizontal axis, vertical axis s may have a number of meanings ..."
        self.show_top_coordinate_system()
        self.wait(1)
        # "... depending on whether we model a rope or string, water or voltage on a cable."
        self.show_sprites()
        self.wait(2)
        self.wave_func = self.pulse
        # "In any case, we can illustrate pulses coming from left to right, which vanish at infinity.
        self.show_incident_plot()
        # "Some specific locations are marked with a dot and excursed as the pulse travels by."
        self.show_blue_dots()
        self.wait(2)
        self.show_pulses(n=2,t=4)
        self.wait(2)

        # FIXME: damped pulse

        # "An infinite cable is silly. Let's replace it with a finite cable and a matched load"
        self.play( FadeOut(self.pml), FadeIn(self.top_termination_dot), Write(self.top_termination_text), FadeIn(self.top_termination_box) )
        # "As expected, nothing changes since all the energy is transferred into the load (e.g. matched antenna)
        self.show_pulses(n=1,t=4)

        # "Now, we swap out the pulse for a harmonic wave with wavelength 2 m."
        # "Note that the two outside dots are spaced one wavelength apart and are excited in phase, while
        # "the center dot is half a wavelength from the others and is excited 180° out of phase."
        self.wave_func = self.sinusoid
        self.demonstrate_wavelength()
        # FIXME: damped sinusoid

        self.wave_func = self.pulse
        self.wait(5)
        # "Since we are interested in reflections, we remove the matched load".
        self.replace_termination('∞  Ω')
        # "Note how the blue incident pulse is reflected, as illustrate by the red reflected pulse."
        self.show_reflected_plot()
        # "We observe the refleciton process in slow motion"
        self.demonstrate_reflections()
        # "Depending on the boundry conditions, reflections with a negative sign can occur. Here, we replace the"
        # "open termination with a short circuit. Again, we observe this in slow motion."
        self.reflection_sign = -1
        self.replace_termination('0   Ω')
        self.demonstrate_reflections()

        # We can also terminate with a slight mismatch and get partial reflections
        # "Note that the animations shown so far are not entirely correct. While the blue incident wave can"
        # "excurse the blue dots, the reflections are unable to do so. However, the reflections should be"
        # "equally capable of excursing the rope, thus we really should look at the sum of the blue and the"
        # "red pulses."
        self.reflection_sign = 0.5
        self.replace_termination('150 Ω')
        self.demonstrate_reflections()
        # "This is what we display in the bottom coordinate system."
        self.show_bottom_coordinate_system()
        self.show_total_plot()
        self.wait(5)
        # "We add yellow dots. Note that the dark dots are spaced half a wavelength apart, and that the light"
        # "yellow dots are also at a spacing of half a wavelength. Furthermore, dark and light dots are spaced"
        # "by a quarter of a wavelength" FIXME
        self.show_yellow_dots()
        self.wait(5)
        # "Note how the reflected pulse is now able to excurse the yellow dots. Furthermore, the right boundary"
        # "of the rope is not excursed at all. This is in line with the practical implementation of the setting"
        # "where the right end is fixed (e.g. at a wall) and thus cannot move."
        self.demonstrate_reflections()
        # "Finally, if we excite the rope with a harmonic oscillation, the sinusiod is reflected back. Note the"
        # "formation of a standing wave pattern, where some nodes spaced apart by half a wavelength remain zero"
        # "at all time, while others are excursed at double the amplitude of the incident wave." These locations"
        # "are marked by dark and light dots, respectively."
        self.wave_func = self.sinusoid
        self.show_pulses(n=1,t=5*self.s/self.v)
        self.wait(4)

        self.reflection_sign = 1
        self.replace_termination('∞  Ω')
        self.show_pulses(n=1,t=5*self.s/self.v)
        self.wait(4)

        self.reflection_sign = -1
        self.replace_termination('0  Ω')
        self.show_pulses(n=1,t=5*self.s/self.v)
        self.wait(4)

        self.reflection_sign = -0.5
        self.replace_termination('17 Ω')
        self.show_pulses(n=1,t=5*self.s/self.v)
        self.wait(4)

        return

    # Return a pulse with the peak located at x0
    def pulse(self,x,reflected,x0=0):
        def f(x):
            return A0 * np.exp(-(x-x0)**2/(2.*sigma**2))
        sigma = 0.1
        A0 = 1.
        if reflected:
            return self.reflection_sign*f(x+self.v*self.t.get_value()-2*self.s)
        else:
            return f(x-self.v*self.t.get_value())

    # Return two pulses with the peaks speaced 2 m apart.
    def double_pulse(self,x,reflected):
        if reflected:
            offset = 2
        else:
            offset = -2
        # Superposition
        return self.pulse(x,reflected) + self.pulse(x,reflected,offset)

    # Return a sinusoid with wavelength 2 m
    def sinusoid(self,x,reflected):
        def f(x):
            return A0 * np.sin(2*np.pi*x/lambd)
        lambd = 2.
        A0 = 1.
        if reflected:
            # Crop the sinusoid: Set values of locations where the wavefront has not reached yet to zero.
            if x < 2*self.s - self.t.get_value()*self.v: return 0.
            return self.reflection_sign*f(x+self.v*self.t.get_value() - self.v*6)
        else:
            # Crop the sinusoid: Set values of locations where the wavefront has not reached yet to zero.
            if self.t.get_value()*self.v < x: return 0.
            return -f(x-self.v*self.t.get_value())

    def show_intro(self):
        text = Text('Reflections').scale(3)
        self.play(Write(text))
        self.wait(2)
        self.play(Unwrite(text))

    def create_coordinate_system(self):
        ax = Axes(
            x_range=[0, self.s],
            y_range=[-1, 1, 0.5],
            y_length=2,
            tips=False,
            x_axis_config={ 'include_numbers': True, },
            y_axis_config={ 'include_numbers': False, },
        )
        x_label = ax.get_x_axis_label("x", edge=DOWN, direction=DOWN)
        y_label = ax.get_y_axis_label("U", edge=LEFT, direction=UL)
        return (ax, VGroup(x_label, y_label))

    def show_top_coordinate_system(self):
        (self.top_ax, labels) = self.create_coordinate_system()

        # Here, we add a bunch of progressively more opaque black rectangles to create
        # a Fade-Out effect on the right side.
        rectangles = VGroup()
        for i in np.linspace(0.,1.2,101):
            rectangle = Rectangle(BLACK, height=4, width=0.01,stroke_width=0.)
            rectangle.set_z_index(1000)
            if i < 0.9:
                rectangle.set_opacity(i)
            else:
                rectangle.set_opacity(1)
            rectangle.move_to( (5.05+i,1,0), aligned_edge=RIGHT)
            rectangles.add(rectangle)
        self.add(rectangles)
        self.pml = rectangles
        boundary_coords = self.top_ax.coords_to_point(self.s,0)
        self.top_termination_dot  = Dot(boundary_coords, radius=0.05)
        self.top_termination_text = Text('50  Ω ').scale(0.4).next_to(self.top_termination_dot, RIGHT)
        self.top_termination_box = Rectangle()
        self.top_termination_box.surround(self.top_termination_text)
        self.top_coordinate_system = VGroup(self.top_ax, labels, self.top_termination_dot, self.top_termination_text, self.top_termination_box)

        self.play(Write(self.top_ax))
        self.wait(2)
        self.play(FadeIn(labels))

    def replace_termination(self, text):
        new_top_termination_text = Text(text).scale(0.4).next_to(self.top_termination_dot, RIGHT)
        if hasattr(self, 'bottom_termination_text'):
            new_bottom_termination_text = Text(text).scale(0.4).next_to(self.bottom_termination_dot, RIGHT)
            self.play(ReplacementTransform(self.top_termination_text, new_top_termination_text), ReplacementTransform(self.bottom_termination_text, new_bottom_termination_text))
        else:
            self.play(ReplacementTransform(self.top_termination_text, new_top_termination_text))

        self.top_coordinate_system.remove(self.top_termination_text)
        self.top_termination_text = new_top_termination_text
        self.top_coordinate_system.add(self.top_termination_text)
        if hasattr(self, 'bottom_termination_text'):
            self.bottom_coordinate_system.remove(self.bottom_termination_text)
            self.bottom_termination_text = new_bottom_termination_text
            self.bottom_coordinate_system.add(self.bottom_termination_text)


    def show_bottom_coordinate_system(self):
        (self.bottom_ax, labels) = self.create_coordinate_system()
        boundary_coords = self.bottom_ax.coords_to_point(self.s,0)
        self.bottom_termination_dot  = Dot(boundary_coords, radius=0.05)
        self.bottom_termination_text = Text(self.top_termination_text.text).scale(0.4).next_to(self.bottom_termination_dot, RIGHT)
        self.bottom_termination_box = Rectangle()
        self.bottom_termination_box.surround(self.top_termination_text)

        self.bottom_coordinate_system = VGroup(self.bottom_ax, labels, self.bottom_termination_dot, self.bottom_termination_text, self.bottom_termination_box).next_to(self.top_coordinate_system, DOWN, buff=0.5)
        self.top_coordinate_system.generate_target()
        self.top_coordinate_system.target.shift(UP)
        self.play(FadeIn(self.bottom_coordinate_system, shift=DOWN), MoveToTarget(self.top_coordinate_system))

    def show_sprites(self):
        file = 'coax.png'
        sprite = ImageMobject(file).scale_to_fit_width(12)
        self.play(FadeIn(sprite))
        self.wait(4)
        self.play(FadeOut(sprite,shift=DOWN))

    def show_incident_plot(self):
        self.t = ValueTracker(-1.)
        self.graph_incident = always_redraw(
            lambda: self.top_ax.plot( lambda x: self.wave_func(x,reflected=False), color=BLUE)
        )
        self.top_coordinate_system.add(self.graph_incident)
        self.play(FadeIn(self.graph_incident))

    def show_dots(self,x_vec,ax,graph,col):
        # Generic function of any marker dot on the rope
        def move_dot(d):
            # We get the x coordinate from the dot itself
            x = ax.point_to_coords( (d.get_x(), 0, 0) )[0]
            # We get the excursion relative to the coordinate system ...
            y = graph.get_point_from_function(x)[1]
            # ... and subtract the center of the coordinate syste,
            y -= ax.get_center()[1]
            d.move_to( ax.coords_to_point(x,y))

        # Initialize dots
        dots = VGroup()
        for (i,x) in enumerate(x_vec):
            dot_point_coords = ax.coords_to_point(x,0)
            dot = Dot(radius=0.08, color=col)
            dot.move_to(dot_point_coords).add_updater(move_dot)
            dots.add(dot)
        self.play(FadeIn(dots))
        return dots

    def show_blue_dots(self):
        self.blue_dots = self.show_dots((2,3,4), self.top_ax, self.graph_incident, BLUE)

    def show_yellow_dots(self):
        self.yellow_dots  = self.show_dots((2,3,4), self.bottom_ax, self.graph_total, YELLOW_E)
        self.wait(5)
        self.yellow_dots += self.show_dots((2.5,3.5,4.5), self.bottom_ax, self.graph_total, YELLOW_B)

    def show_timer(self):
        def f():
            # Negative values are shown as zero to avoid confusion
            if self.t.get_value() < 0:
                return 0
            return self.t.get_value()

        timer = DecimalNumber(0.).scale(2)
        text_left = Tex('t=').scale(2).next_to(timer, LEFT)
        text_right = Tex(' s').scale(2).next_to(timer, RIGHT).shift((0.3,-0.1,0))
        self.timer = VGroup(timer, text_left, text_right)
        self.timer.next_to(self.top_ax, UP, aligned_edge = UP, buff=1.2)

        timer.add_updater(lambda x: x.set_value(f()))
        self.play(FadeIn(self.timer))

    def show_reflected_plot(self):
        self.graph_reflected = always_redraw(
            lambda: self.top_ax.plot( lambda x: self.wave_func(x,reflected=True), color=RED)
        )
        self.graph_reflected.set_z_index(-1) # Behind incident wave
        self.top_coordinate_system.add(self.graph_reflected)

        self.play(FadeIn(self.graph_reflected))

    def show_total_plot(self):
        self.graph_total = always_redraw(
            # Superposition ...
            lambda: self.bottom_ax.plot( lambda x: self.wave_func(x,reflected=False)+self.wave_func(x,reflected=True), color=YELLOW)
        )
        self.bottom_coordinate_system.add(self.graph_total)

        self.play(FadeIn(self.graph_total))

    def show_pulses(self, n, t):
        for i in range(n):
            self.t.set_value(-1.)
            self.play(self.t.animate.set_value(t),run_time=t,rate_func=linear)
        self.t.set_value(-1.)

    def demonstrate_velocity(self):
        self.t.set_value(-1.)
        self.play(self.t.animate.set_value(1),run_time=2)
        text_0 = MathTex(r't_0&=1.0\text{ s}\\x_0&=2\text{ m}').next_to(self.top_coordinate_system, DOWN, buff=0.5)
        text_1 = MathTex(r't_1&=1.5\text{ s}\\x_1&=3\text{ m}').next_to(self.top_coordinate_system, DOWN, buff=0.5)
        text_d = MathTex(r'\Delta t&=0.5\text{ s}\\\Delta x&=1\text{ m}').next_to(self.top_coordinate_system, DOWN, buff=0.5).shift( (4,0,0) )
        text_c = MathTex(r'c = \frac{\Delta x}{\Delta t}=2\frac{\text{m}}{\text{s}}').next_to(self.top_coordinate_system, DOWN, buff=0.5)
        text_tau = MathTex(r'\tau = \frac{\Delta x}{c} = 0.5\text{ s}').next_to(self.top_coordinate_system, DOWN, buff=0.5)
        # plot t0/x0
        self.play(Write(text_0))
        self.wait(4)
        self.play(self.t.animate.set_value(1.5),run_time=2)
        self.play(text_0.animate.shift( (-4,0,0) ))
        # plot t1/x1
        self.play(Write(text_1))
        self.wait(4)
        # plot deltas
        self.play(Write(text_d))
        self.wait(10)
        self.play(FadeOut(text_0,text_1))
        self.play(text_d.animate.shift( (-8,0,0) ))
        # plot velocity
        self.play(Write(text_c))
        self.wait(10)
        self.play(FadeOut(text_d,text_c))
        self.play(self.t.animate.set_value(2.),run_time=2)
        # plot propagation delay
        self.play(Write(text_tau))
        self.play(self.t.animate.set_value(7.),run_time=2)
        self.play(FadeOut(text_tau))
        self.t.set_value(-1.)

    def demonstrate_wavelength(self):
        self.t.set_value(-1.)
        self.play(self.t.animate.set_value(2.75),run_time=5.5,rate_func=linear)
        arrow = DoubleArrow(start=(self.blue_dots[0].get_x(),0,0), end=(self.blue_dots[2].get_x(),0,0), buff=0.).shift( (0, -1.3, 0))
        text = Tex('$\lambda=2$ m').next_to(arrow, DOWN, aligned_edge=DOWN)
        self.play(FadeIn(arrow,text))
        self.wait(4)
        self.play(FadeOut(arrow,text))
        self.play(self.t.animate.set_value(10.),run_time=10,rate_func=linear)
        self.t.set_value(-1.)

    def demonstrate_reflections(self):
        # Normal reflection
        self.t.set_value(-1.)
        self.play(self.t.animate.set_value(7.),run_time=10,rate_func=linear)
        self.t.set_value(-1.)
        # Reflection where we briefly halt when the wavefront hits the boundary
        self.play(self.t.animate.set_value(self.s/self.v),run_time=10)
        self.play(self.t.animate.set_value(2*self.s/self.v+3),run_time=10)
        self.t.set_value(-1.)

class StandingWaves(Scene):
    def construct(self):
        self.axes = VGroup()
        for i in range(3):
            self.axes.add(self.create_coordinate_system().scale(0.25))
        self.axes.arrange(RIGHT, buff=1.5)
#       self.add(self.axes)
        self.t = ValueTracker(0)

        self.add_plot(i=0, n=1, color=RED)
        self.add_plot(i=1, n=2, color=BLUE)
        self.add_plot(i=2, n=3, color=GREEN)
        self.play(self.t.animate.set_value(6.),run_time=10,rate_func=linear)

    def wave_func(self,x,lambd):
        A0 = np.sin(2*np.pi*x/lambd)
        return A0*np.sin(2*np.pi*self.t.get_value())

    def create_coordinate_system(self):
        ax = Axes(
            x_range=[0, 1],
            y_range=[-1, 1, 0.5],
            y_length=2,
            tips=False,
            axis_config={ 'include_numbers': False, },
        )
        return ax

    def add_plot(self, i, n, color):
        graph = always_redraw(
            lambda: self.axes[i].plot( lambda x: self.wave_func(x,2/n), color=color)
        )
        dot1 = Dot(graph.get_left(),  radius=0.05)
        dot2 = Dot(graph.get_right(), radius=0.05)
        self.add(graph, dot1, dot2)
