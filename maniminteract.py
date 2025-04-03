import array
from manim import *  
from manim.opengl import *
from scipy.integrate import solve_ivp
import numpy as np

config.renderer = "opengl" # u have to put in terminal
config.window_size = (1920, 1080)
config.fullscreen = True

# Define the Lorenz system
def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Function to solve the ODE and return the points
def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

# Function to interpolate between colors
def interpolate_color(color1, color2, alpha):
    return color1 * (1 - alpha) + color2 * alpha

# Function to generate color gradient
def generate_color_gradient(num_colors):
    colors = []
    for i in range(num_colors):
        r = i / (num_colors - 1)
        blue_color = interpolate_color(BLUE, YELLOW, r)
        colors.append(blue_color)
    
    return colors

# The Lorenz Attractor Scene using OpenGL
class LorenzAttractorOpenGL(ThreeDScene):
    def construct(self):
        # Set renderer to OpenGL

        
        # Number of curves to generate
        num_curves = 10
        
        # Set up axes for 3D scene
        axes = ThreeDAxes(
            x_range=(-30, 30, 5),
            y_range=(-30, 30, 5),
            z_range=(0, 50, 5),
            axis_config={"include_tip": True}
        )
        
        # Add axes to the scene
        self.add(axes)

        # Set camera orientation with increased height and 90-degree rotation
        self.set_camera_orientation(theta=225 * DEGREES, phi=75 * DEGREES)
        
        # Move camera up by 10 units
        self.move_camera(frame_center=np.array([0,0,2.5]))

        # Add title
        #title = Text("Lorenz Attractor", font_size=24).to_corner(UL)
        #self.add_fixed_in_frame_mobjects(title)
        
        # Generate initial conditions
        initial_conditions = [[1 + i, 1 + i, 1 + i] for i in range(num_curves)]
        
        # Generate color gradient
        colors = generate_color_gradient(num_curves)
        
        # Solve and prepare curves
        curves = []
        moving_dots = []
        manim_points_list = []
        
        for state0, color in zip(initial_conditions, colors):
            # Solve the Lorenz system to get points
            points = ode_solution_points(lorenz_system, state0, 15, dt=0.02)
            
            # Convert points to Manim coordinates
            manim_points = [axes.c2p(x, y, z) for x, y, z in points]
            manim_points_list.append(manim_points)
            
            # Create the curve from the points
            curve = Line()  # Change VMobject to Line for OpenGL compatibility
            curve.set_points_smoothly(manim_points)
            curve.set_color(color)
            curve.set_stroke(width=2, opacity=0.7)
            
            # Create a moving dot
            moving_dot = Dot3D(point=manim_points[0], color=color, radius=0.05)
            
            curves.append(curve)
            moving_dots.append(moving_dot)
        
        # Add the dots to the scene first
        self.add(*moving_dots)  # Ensure moving dots are added before curves
        self.add(*moving_dots)
        
        # Animate the curves with moving dots
        curve_anims = []
        for curve, dot, points in zip(curves, moving_dots, manim_points_list):
            # Create a method to update dot position
            def create_dot_updater(point_list):
                def update_dot(mob, alpha):
                    # Calculate the index based on alpha
                    index = int(alpha * (len(point_list) - 1))
                    mob.move_to(point_list[index])
                return update_dot
            
            # Combine curve creation with dot updating
            curve_anim = AnimationGroup(
                Create(curve, run_time=30, rate_func=linear),
                UpdateFromAlphaFunc(dot, create_dot_updater(points), run_time=30, rate_func=linear)
            )
            curve_anims.append(curve_anim)
        
        # Play the animations
        self.play(*curve_anims)
        
        # Begin camera rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # Wait to show the rotation
        self.wait(60)
        
        # Stop camera rotation
        self.stop_ambient_camera_rotation()
        
        # Final wait
        self.wait(5)

# Run the animation
if __name__ == "__main__":
    # Set to use OpenGL renderer
    config.renderer = "opengl"
    scene = LorenzAttractorOpenGL()
    scene.render()
