import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

FPS = 30
DELTA_T = 1/FPS

class System:
    def __init__(self, m, k, c):
        self.m = m
        self.k = k
        self.c = c
        self.A = np.array([[-self.c/self.m, -self.k/self.m],[1, 0]])
        self.B = np.array([[1/self.m],[0]])
        self.delta_t = DELTA_T
    
    def forward(self, x0, u):
        x1 = (self.A@x0 + self.B*u)*DELTA_T + x0
        return x1
    

if __name__=='__main__':
    test = System(1,20,1)
    x = np.array([[0],[0]])
    def u(i):
        if i < 10:
            return 5
        elif i < 200:
            return 10
        elif i < 300:
            return 20
        else:
            return 0
    x_list = [x]

    for i in range(1, 500):
        x = test.forward(x, u(i))
        x_list.append(x)
    
    x_list = np.array(x_list)
    
    # Physical parameters
    mass_position_x = np.array([0])
    spring_fixed_point = -2
    spring_length = 1.5
    mass_width = 0.5
    damper_length = 1

    # Prepare the plot
    fig, ax = plt.subplots()
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    
    # Create objects for mass, spring, and damper
    mass = plt.Rectangle((0, -0.25), mass_width, 0.5, fc='blue')
    ax.add_patch(mass)
    spring, = ax.plot([], [], lw=2, color='black')
    damper, = ax.plot([], [], lw=4, color='gray')

    def init():
        mass.set_xy((0, -0.25))
        spring.set_data([], [])
        damper.set_data([], [])
        return mass, spring, damper

    def update(frame):
        # Calculate new position for mass based on displacement
        displacement = x_list[frame, 1, 0]
        mass.set_x(displacement)

        # Update the spring
        spring_x = np.linspace(spring_fixed_point, displacement, 100)
        spring_y = 0.05 * np.sin(10 * np.pi * (spring_x - spring_fixed_point) / (displacement - spring_fixed_point + 1e-6))
        spring.set_data(spring_x, spring_y)
        
        # Update the damper
        damper_x = [spring_fixed_point + spring_length, displacement]
        damper_y = [0, 0]
        damper.set_data(damper_x, damper_y)
        
        return mass, spring, damper

    print(len(x_list))
    ani = FuncAnimation(fig, update, frames=len(x_list), init_func=init, blit=True, repeat=False, interval=DELTA_T*1000)
    ani.save('mass_spring_damper.gif', writer=PillowWriter(fps=FPS))
    plt.show()