import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

def VLE_diagram():

    # Define the subst
    substance = 'NitrousOxide'

    # Define temperature range (in Kelvin)
    T_min = CP.PropsSI(substance, 'Tmin') + 0.01  # slightly above the minimum temperature
    T_max = CP.PropsSI(substance, 'Tcrit')        # critical temperature
    temperatures = np.linspace(T_min, T_max, int(2e3))

    def get_saturations(T):
        liquid_density = []
        vapor_density = []
        saturation_pressures = []

        # Calculate densities and pressures at each temperature
        for T in temperatures:
            ld = CP.PropsSI('D', 'T', T, 'Q', 0, substance)         # liquid density
            vd = CP.PropsSI('D', 'T', T, 'Q', 1, substance)         # vapor density
            psat = CP.PropsSI('P', 'T', T, 'Q', 0, substance) / 1e5 # saturation pressure

            liquid_density.append(ld)
            vapor_density.append(vd)
            saturation_pressures.append(psat)

        return liquid_density, vapor_density, saturation_pressures

    plt.figure()
    # Get saturation data
    liquid_density, vapor_density, saturation_pressures = get_saturations(temperatures)

    """Density vs Temperature"""
    # Plot saturation curves with Temperature on x-axis
    plt.plot(temperatures, liquid_density, label='Saturated Liquid Density')
    plt.plot(temperatures, vapor_density, label='Saturated Vapor Density')
    plt.fill_between(temperatures, liquid_density, vapor_density, color='gray', alpha=0.2)

    # Add critical point
    T_critical = CP.PropsSI('Tcrit', substance)
    D_critical = CP.PropsSI('rhocrit', substance)

    plt.plot(T_critical, D_critical, 'kx', label='Critical Point')

    # Plot isobar
    isoP = 50 * 1e5
    isoP_Ts = np.linspace(260,370, 500)
    rho = CP.PropsSI('D', 'P', isoP, 'T', isoP_Ts, substance)
    plt.plot(isoP_Ts, rho, label=f'Isobar at {(isoP / 1e5):.1f} bar')
    T_sat = CP.PropsSI('T', 'P', isoP, 'Q', 0, substance)

    # Calculate the liquid saturation density at the isobar
    rho_sat = CP.PropsSI('D', 'P', isoP, 'Q', 0, substance)

    # Calculate the vapor saturation density at the isobar
    rho_vap = CP.PropsSI('D', 'P', isoP, 'Q', 1, substance)

    # Plot saturation points
    D_V = CP.PropsSI('D', 'P', isoP, 'Q', 1, substance)
    D_L = CP.PropsSI('D', 'P', isoP, 'Q', 0, substance)
    T_V = CP.PropsSI('T', 'P', isoP, 'Q', 1, substance)
    T_L = CP.PropsSI('T', 'P', isoP, 'Q', 0, substance)
    plt.plot(T_V, D_V, 'ro', label=f'$\\rho_{{V, sat}}$ = {D_V:.2f} kg/m$^3$')
    plt.plot(T_L, D_L, 'bo', label=f'$\\rho_{{L, sat}}$ = {D_L:.2f} kg/m$^3$')

    dD = D_V - D_L
    # Insert an arrow to show the direction of increasing heat transfer (vertical Q with arrow)
    plt.annotate('', xy=(T_L+3, D_L), xytext=(T_L+3, D_L + dD), arrowprops=dict(facecolor='black', shrink=0.25))
    plt.annotate('', xy=(T_V-3, D_V), xytext=(T_V-3, D_V - dD), arrowprops=dict(facecolor='black', shrink=0.25))

    plt.annotate(f'$W_{{in}}$\n$+m$', xy=(T_L+6, D_critical), fontsize=16)
    plt.annotate(f'$Q_{{in}}$\n$+V$', xy=(T_L-10, D_critical), fontsize=16)
    plt.xlim(260, 320)
    # plt.legend()
    plt.xlabel('Temperature [K]')
    plt.ylabel('Density [kg/m$^3$]')
    plt.title('Density vs Temperature for VLE of $N_2 O$')
    plt.show()

if __name__ == '__main__':
    VLE_diagram()