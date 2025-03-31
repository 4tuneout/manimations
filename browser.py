import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

# Define the Lorenz system (same as original)
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

# Create a simple interactive visualization
def create_lorenz_visualization(sigma=10, rho=28, beta=8/3, num_curves=5, time=15, dt=0.02):
    # Create figure
    fig = go.Figure()
    
    # Set up the layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-30, 30], title='X'),
            yaxis=dict(range=[-30, 30], title='Y'),
            zaxis=dict(range=[0, 50], title='Z'),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        height=800,
        width=1000,
        title="Lorenz Attractor (σ={}, ρ={}, β={})".format(sigma, rho, beta)
    )
    
    # Generate initial conditions and colors
    initial_conditions = [[1 + i, 1 + i, 1 + i] for i in range(num_curves)]
    colors = ['rgb(68, 1, 84)', 'rgb(59, 81, 138)', 'rgb(34, 144, 140)', 'rgb(96, 200, 96)', 'rgb(253, 231, 37)']
    if num_curves > len(colors):
        # Repeat colors if needed
        colors = colors * (num_curves // len(colors) + 1)
    
    # Generate curves
    for i, state0 in enumerate(initial_conditions):
        points = ode_solution_points(
            lambda t, state: lorenz_system(t, state, sigma, rho, beta),
            state0, time, dt
        )
        
        # Add trace for the curve
        fig.add_trace(
            go.Scatter3d(
                x=points[:, 0], 
                y=points[:, 1], 
                z=points[:, 2],
                mode='lines',
                name=f'Curve {i+1}',
                line=dict(color=colors[i % len(colors)], width=3),
                opacity=0.7
            )
        )
        
        # Add starting point
        fig.add_trace(
            go.Scatter3d(
                x=[points[0, 0]],
                y=[points[0, 1]],
                z=[points[0, 2]],
                mode='markers',
                marker=dict(size=5, color=colors[i % len(colors)]),
                name=f'Start {i+1}',
                showlegend=False
            )
        )
    
    # Show the figure in a browser window
    fig.show()
    
    return fig

# Create and display the visualization
if __name__ == "__main__":
    # You can change these parameters to experiment
    create_lorenz_visualization(
        sigma=10,
        rho=28,
        beta=8/3,
        num_curves=5,
        time=15
    )