from manim import *
from scipy.integrate import solve_ivp
import numpy as np
import colorsys

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

# Function to generate color gradient
def generate_color_gradient(num_colors):
    colors = []
    for i in range(num_colors):
        # Interpolate between light blue and yellow
        r = i / (num_colors - 1)
        blue_color = interpolate_color(BLUE, YELLOW, r)
        colors.append(blue_color)
    
    return colors

# The Lorenz Attractor Scene
class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Number of curves to generate
        num_curves = 10
        
        # Set up axes for 3D scene
        axes = ThreeDAxes(
            x_range=(-30, 30, 5),
            y_range=(-30, 30, 5),
            z_range=(0, 50, 5),
            axis_config={"include_tip": True}
        )
        
        # Move the frame center down by 5 units
        self.camera.frame_center = np.array([0, 0, 3])
        
        # Set camera orientation with increased height and 90-degree rotation
        self.set_camera_orientation(theta=135 * DEGREES, phi=75 * DEGREES, zoom=0.8)
        
        # Add axes to the scene
        self.add(axes)
        
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
            curve = VMobject()
            curve.set_points_smoothly(manim_points)
            curve.set_color(color)
            curve.set_stroke(width=2, opacity=0.7)
            
            # Create a moving dot
            moving_dot = Dot3D(point=manim_points[0], color=color, radius=0.05)
            
            curves.append(curve)
            moving_dots.append(moving_dot)
        
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
        
        # Add the axes and dots to the scene first
        self.add(*moving_dots)
        
        # Play the animations
        self.play(*curve_anims)
        
        # Optional: Rotate camera around y-axis
        self.begin_ambient_camera_rotation(rate=PI/2)
        
        # Wait to show the rotation
        self.wait(20)
        
        # Stop camera rotation
        self.stop_ambient_camera_rotation()
        
        # Final wait
        self.wait(10)