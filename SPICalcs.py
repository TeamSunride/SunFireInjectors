import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import CoolProp.CoolProp as CP

def A(d):
    return np.pi * (d / 2)**2
def m_CPI(A, rho0, P1, P2, N, Cd=0.66):
    return A * Cd * N * np.sqrt(2 * rho0 * (P2 - P1))
def CalcCPI(T, substance, P_chamber, N, d):
    P_sat = CP.PropsSI('P', 'T', T + 273.15, 'Q', 0, substance) / 1e5
    D_sat = CP.PropsSI('D', 'T', T + 273.15, 'Q', 0, substance)
    m_CPI_vectorized = np.vectorize(m_CPI)
    return m_CPI_vectorized(A(d), D_sat, P_sat, P_chamber, N), P_sat, D_sat

def SPI_plot(orrifaces=12):
    # Find critical temperature of N2O
    T_critical = CP.PropsSI('Tcrit', 'NitrousOxide') - 273.15
    T_critical -= 0.01

    # Define the subst
    substance = 'NitrousOxide'
    temperatures = np.linspace(-15, T_critical, 2000)    # Ambient temperatures (C)
    P_chamber = 20e5
    N = orrifaces
    d = np.linspace(0.1, 2.5, 100) / 1000

    def plot_masses(T, substance, P_chamber, N, d):
        m, P_sat, D_sat = CalcCPI(T, substance, P_chamber, N, d)
        plt.plot(d * 1000, m, label=f'{T:.1f} C', color=next(color), linewidth=.1, alpha=1)
    plt.figure()
    # set colors to viridis colormap
    colormap = plt.cm.viridis
    color = iter(colormap(np.linspace(0, 1, len(temperatures))))



    for T in temperatures:
        # VLE
        plot_masses(T, substance, P_chamber, N, d)

    sm = ScalarMappable(cmap=colormap, norm=Normalize(vmin=min(temperatures), vmax=max(temperatures)))
    sm.set_array([])
    ax = plt.gca()
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Upstream Temperature (C)')

    # Use Calculate CPI to find mass flow rates for just critical temperature
    m, P_sat, D_sat = CalcCPI(T_critical, substance, P_chamber, N, d)
    # Plot with a filled in region below the curve and x axis
    plt.fill_between(d * 1000, m, color='yellow', alpha=0.2)
    #annotate the center of the filled in region as 'Super Critical'
    plt.annotate('Supercritical', xy=(0.75, 0.25), xycoords='axes fraction',
                 ha='center', va='center', fontsize=12)

    # Plot horizontal line at 1.36 kg/s
    plt.axhline(1.36, color='r', linestyle='--', label='1.36 kg/s')
    # Annotate horizontal line along the line itself
    plt.annotate(f'$\\dot{{m}}_{{N_2O}}=1.36 kg/s$', xy=(0.1, 1.36), xycoords='data',
                 ha='left', va='bottom', fontsize=10, color='r')


    plt.xlabel('Orifice Diameter (mm)')
    plt.ylabel('Mass Flow Rate (kg/s)')
    plt.title(f'Mass Flow Rate vs Orifice Diameter\n for {N} Orifices')
    # plt.show()

if __name__ == '__main__':
    SPI_plot()
    plt.show()

    # plot mass flow rate vs diameter for ambient temperature of 20degC and N = 12 (SPI)
    temps = 20
    d = np.linspace(0.1, 2.5, 100) / 1000
    N = 12
    Pc = 20e5
    m = CalcCPI(temps, 'NitrousOxide', Pc, N, d)[0]
    plt.figure()
    plt.plot(d * 1000, m)
    plt.xlabel('Diameter (mm)')
    plt.ylabel('Mass Flow Rate (kg/s)')
    plt.title('Mass Flow Rate vs Diameter')
    plt.tight_layout()
    plt.show()


