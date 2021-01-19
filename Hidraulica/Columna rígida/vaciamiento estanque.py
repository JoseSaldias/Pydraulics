# -*- coding: utf-8 -*-
"""
Nov 2020

Ejemplo vaciamiento de estanque
"""
import numpy as np
import matplotlib.pyplot as plt

def rk4(f, g, x0, y0, t_i, t_f, dt):
    t = np.arange(t_i, t_f, dt)
    x , y = np.zeros(len(t)), np.zeros(len(t))
    x[0], y[0] = x0, y0
    
    for i in range(len(t) - 1):
        k1 = dt * f(x[i], y[i], t[i])
        l1 = dt * g(x[i], y[i], t[i])
        k2 = dt * f(x[i] + k1/2, y[i] + l1/2, t[i] + dt/2)
        l2 = dt * g(x[i] + k1/2, y[i] + l1/2, t[i] + dt/2)
        k3 = dt * f(x[i] + k2/2, y[i] + l2/2, t[i] + dt/2)
        l3 = dt * g(x[i] + k2/2, y[i] + l2/2, t[i] + dt/2)
        k4 = dt * f(x[i] + k3, y[i] + l3, t[i] + dt)
        l4 = dt * g(x[i] + k3, y[i] + l3, t[i] + dt)
        
        x[i+1] = x[i] + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
        y[i+1] = y[i] + (1/6) * (l1 + 2*l2 + 2*l3 + l4)
    
    return t, x, y

# Constantes globales
g = 9.81 # m/s2
f = 0.02

# Datos de estanque
h0 = 10 # m
r_e = 2 # m
a_e = np.pi * r_e**2

# Datos de tubería
q0 = 0 # m3/s
r_t = 0.175 #m
a = np.pi * r_t**2
l = 1500 #m


f1 = lambda h,q,t: -q/a_e
f2 = lambda h,q,t: g*a*h/l - f*q*np.abs(q)/(2*2*r_t*a)

t, h_estanque, caudal = rk4(f1, f2, h0, q0, 0, 2000, 1)


from matplotlib import rc 
rc('font', **{'family': 'DejaVu Sans', 'serif': ['Computer Modern']}) 
rc('text', usetex=True) 

fig = plt.figure(figsize=[8,5])
ax = fig.add_subplot(111)
ax2 = ax.twinx()

p1 = ax.plot(t, h_estanque, color='r', label = "a", linestyle='--')
p2 = ax2.plot(t, caudal*1000, color='purple', label="b")

plt.legend([p1[0], p2[0]], ["Altura de agua en estanque", "Caudal de salida"])

plt.title("Altura Estanque: {} m\nDiametro Estanque: {} m\nDiametro\
          Tuberia: {} m".format(h0, 2*r_e, 2*r_t))

ax.set_xlabel("Tiempo [s]", fontsize=14, labelpad=10)
ax.set_ylim(0, max(h_estanque)*1.1)
ax2.set_ylim(0, max(caudal*1000)*1.1)

ax.set_ylabel(r"Altura [m]",labelpad=5 ,fontsize=14)
ax2.set_ylabel(r"Caudal [$L/s$]", labelpad=15, fontsize=14)

plt.grid(color='gray', alpha=0.2, linestyle='--')
plt.savefig(fname='Ejemplo.png', dpi=500)
plt.show()
