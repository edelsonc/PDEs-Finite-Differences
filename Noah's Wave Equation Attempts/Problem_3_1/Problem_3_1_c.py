'''
author: Noah

Dirichlet wave equation!
u_tt = u_xx

Here we use a forward difference scheme for the approximation of u_tt
'''
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

dt = 0.25
dx = 0.25
c = 1
s = c**2 * dt**2 / dx**2

x_start, x_end = 0.0, 5.0  # x-bounds
t_start, t_end = 0.0, 6.0  # t-bounds

X = np.arange(x_start, x_end + dx, dx)  # 1D x dimension
T = np.arange(t_start, t_end + dt, dt)  # 1D t dimension

J, N = X.shape[0], T.shape[0] # number of discrete x-axis and t-axis elements
#print J, N


def phi_j(j): #initial condition: u(x,0)
    return 25 - (j*dx)**2

def psi_j(j): #initial velocity: du/dt(x,0)
    return 0

def b(j):
    return 


def initial_u():
    """
    Creates initial condition of wave equation
    """
    u = np.zeros((N,J), dtype='float')

    # the first row
    for j in range(J):   
        u[0,j] = phi_j(j)

    # the second row -- have to solve system of equations -- assumes dirichlet conditions
    alpha = 2*s+1
    beta = -s
    A = np.zeros((J-2,J-2))
    for j in range(J-2):
        if (j-1 >= 1):
            A[j,j-1] = beta
        A[j,j] = alpha
        if (j+1 <= J-4):
            A[j,j+1] = beta
    
    B = np.ndarray((J-2,1))
    for j in range(1,J-2):
        B[j-1] = (-2*s*dt*(psi_j(j+1) + psi_j(j-1)) + (4*s+2)*dt*phi_j(j) + 2*phi_j(j))
        
    X = np.linalg.solve(A,B)
    
    for j in range(1, J-1):
        u[1,j] = X[j-1]
    
    return u

u = initial_u()

# plot first two rows to confirm initial conditions
fig = plt.figure()

ax1 = fig.add_subplot(211)
ax1.set_title("Initial condition")
ax1.plot(u[0])
ax2 = fig.add_subplot(212)
ax2.set_title("n = 1")
ax2.plot(u[1])

plt.show()
#pyplot.savefig("test_0.png")

def picard_engage(u, s, J, N):
    """Implements a simple scheme for solving the diffusion equation for
    the Dirichlet Boundary conditions: u(t, 0) = 0 and u(t, l) = 0.

    Arguments
    ---------
    u -- wave solution, with first two rows already filled in.
    s -- ratio of step distances between points in t, and between points in x
    J -- total number of discrete x-axis points
    N -- total number of discrete t-axis points
    """
    for n in range(N-2):
        for j in range(1, J - 1):
            u[n+2,j] = s*(u[n,j+1] + u[n,j-1]) - (2*s+1)*u[n,j] + 2*u[n+1,j]

        #enforce boundary conditions
        u[n+2,0] = 0
        u[n+2,J-1] = 0
    
    return u

u = picard_engage(u, s, J, N)

# Create an animation of the solution as time elapses
fig, ax = plt.subplots()
ax.set_ylim([-200,400])
#ax.set_autoscale_on(False)
ax.set_xlabel('X')
ax.set_ylabel('u')
wave, = ax.plot(X, u[0,:])

def animate(i):
    ax.set_title("n = %d" % i)
    wave.set_ydata(u[i,:])  # update the data
    return wave,

# Init only required for blitting to give a clean slate.
def init():
    wave.set_ydata(u[0,:])
    return wave,

ani = animation.FuncAnimation(fig, animate, N, init_func=init,
                              interval=6000/N, blit=False, repeat=False)
plt.show()

ani.save('3_1_c.mp4')

# Show (3,3) point in space-time
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.set_title("Time = 3; u(3,3) = %f" % u[T.tolist().index(3),X.tolist().index(3)])
ax1.set_xlabel('X')
ax1.set_ylabel('u')
ax1.plot(u[T.tolist().index(3),:])

plt.show()
plt.savefig('3_1_c.jpg')