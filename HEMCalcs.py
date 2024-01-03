import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D

def A(d):
    return np.pi * (d / 2) ** 2

def mHEM(A, rho2, h1, h2, N, Cd=0.66):
        return N * A * Cd * rho2 * np.sqrt(2*(h1 - h2))


T1 = 10 # Upstream temperature (C)
P2 = 20e5 # Downstream pressure (Pa)
N = 12 # Number of orrifaces

def HEM_CP(T1, P2, subst='NitrousOxide'):
    h1 = CP.PropsSI('H', 'T', T1 + 273.15, 'Q', 0, subst)
    s1 = CP.PropsSI('S', 'T', T1 + 273.15, 'Q', 0, subst)

    # Find downstream enthalpy for liquid with upstream entropy and downstream pressure
    h2 = CP.PropsSI('H', 'P', P2, 'S', s1, subst)

    rho2 = CP.PropsSI('D', 'P', P2, 'S', s1, subst)
    return h1, h2, rho2

def plotting(d, T, N):
    h1, h2, rho2 = HEM_CP(T, P2)

    m_HEM_vectorized = np.vectorize(mHEM)
    return m_HEM_vectorized(A(d), rho2, h1, h2, N)

def HEMmassflowrate():
    temps = np.linspace(-10, 32, 500)
    d = np.linspace(0.1, 2.5, 100) / 1000


    plt.figure()
    # set colors to viridis colormap
    colormap = plt.cm.viridis
    color = iter(colormap(np.linspace(0, 1, len(temps))))

    for T in temps:
        m = plotting(d, T, N)
        plt.plot(d * 1000, m, label=f'{T:.1f} C', color=next(color), linewidth=.3, alpha=1)

    sm = ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(temps), vmax=max(temps)))
    sm.set_array([])
    ax = plt.gca()
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Upstream Temperature (C)')
    plt.xlabel('Diameter (mm)')
    plt.ylabel('Mass Flow Rate (kg/s)')
    plt.title('Mass Flow Rate vs Diameter vs Temperature')
    plt.show()


def NormalisedHEM():
    # Plot Mass Flow Rate vs Upstream temperature for d =0.5mm and N = 1
    temps = np.linspace(-10, 70, 500)
    d = 1
    N = 1

    m = plotting(d, temps, N) / 0.66
    plt.figure()
    plt.plot(temps, m/1e4)
    plt.xlabel('Upstream Temperature (C)')
    plt.ylabel(r'Normalised mass Flow Rate $\left( \frac{kg}{m^2} \right)$ x10$^{-4}$')
    plt.title('Mass Flow Rate vs Upstream Temperature')
    plt.tight_layout()
    plt.show()

# Plot Mass Flow Rate vs diameter(0 to 2) for ambient temperature of 20degC and N = 12
temps = 20
d = np.linspace(0.1, 2.5, 100) / 1000
N = 12

m = plotting(d, temps, N)
plt.figure()
plt.plot(d * 1000, m)
plt.xlabel('Diameter (mm)')
plt.ylabel('Mass Flow Rate (kg/s)')
plt.title('Mass Flow Rate vs Diameter')
plt.tight_layout()
plt.show()