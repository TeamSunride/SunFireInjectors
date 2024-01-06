import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from matplotlib.ticker import FuncFormatter

# Define the subst
substance = 'NitrousOxide'

# Define temperature range (in Kelvin)
T_min = CP.PropsSI(substance, 'Tmin') + 0.01  # slightly above the minimum temperature
T_max = CP.PropsSI(substance, 'Tcrit')        # critical temperature
temperatures = np.linspace(T_min, T_max, int(1e3))

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

def plot_curves(isoT=15, isoP=60):
    isoT += 273.15

    # Create figure and axes
    fig, axs = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Get saturation data
    liquid_density, vapor_density, saturation_pressures = get_saturations(temperatures)

    """Density vs Temperature"""
    # Plot saturation curves with Temperature on x-axis
    axs[0].plot(temperatures, liquid_density, label='Saturated Liquid Density')
    axs[0].plot(temperatures, vapor_density, label='Saturated Vapor Density')
    axs[0].fill_between(temperatures, liquid_density, vapor_density, color='gray', alpha=0.2)

    # Add critical point
    T_critical = CP.PropsSI('Tcrit', substance)
    D_critical = CP.PropsSI('rhocrit', substance)
    # print(f'T_critical = {T_critical:.2f} K')
    # print(f'D_critical = {D_critical:.2f} kg/m^3')
    axs[0].plot(T_critical, D_critical, 'kx', label='Critical Point')

    # Plot isobar
    isoP *= 1e5
    isoP_Ts = np.linspace(260,370, 500)
    try:
        rho = CP.PropsSI('D', 'P', isoP, 'T', isoP_Ts, substance)
        axs[0].plot(isoP_Ts, rho, label=f'Isobar at {(isoP / 1e5):.1f} bar')
        T_sat = CP.PropsSI('T', 'P', isoP, 'Q', 0, substance)
        axs[0].axvline(T_sat, color='gray', linestyle='--', label=f'$T_{{sat}}$ = {T_sat-273.15:.1f} °C')
        # Plot saturation points
        D_V = CP.PropsSI('D', 'P', isoP, 'Q', 1, substance)
        D_L = CP.PropsSI('D', 'P', isoP, 'Q', 0, substance)
        T_V = CP.PropsSI('T', 'P', isoP, 'Q', 1, substance)
        T_L = CP.PropsSI('T', 'P', isoP, 'Q', 0, substance)
        axs[0].plot(T_V, D_V, 'ro', label=f'$\\rho_{{V, sat}}$ = {D_V:.2f} kg/m$^3$')
        axs[0].plot(T_L, D_L, 'bo', label=f'$\\rho_{{L, sat}}$ = {D_L:.2f} kg/m$^3$')

        # # Annotate the density of the saturated liquid and vapor use LaTeX formatting and put into boxes
        # axs[0].annotate(f'{D_L:.2f} kg/m$^3$', xy=(T_L, 900))
        # axs[0].annotate(f'{D_V:.2f} kg/m$^3$', xy=(T_V, 0))
    except:
        pass

    # Label plot

    axs[0].set_title('Density vs Temperature')

    # Example values for the limits and increments in Celsius
    x_min_celsius = -10  # Minimum value in Celsius
    x_max_celsius = 60  # Maximum value in Celsius
    increments_celsius = 10  # Increment step in Celsius

    # Convert these values to Kelvin for setting limits and ticks
    x_min_kelvin = x_min_celsius + 273.15
    x_max_kelvin = x_max_celsius + 273.15
    increments_kelvin = increments_celsius

    # Set the limits for the x-axis
    axs[0].set_xlim(x_min_kelvin, x_max_kelvin)

    # Set the ticks for the x-axis
    # np.arange creates an array from x_min_kelvin to x_max_kelvin with a step of increments_kelvin
    axs[0].set_xticks(np.arange(x_min_kelvin, x_max_kelvin + 1, increments_kelvin))

    # Modify the x-axis to show temperature in degrees Celsius
    axs[0].xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f'{(val - 273.15):.0f}'))

    # Set the label for the x-axis
    axs[0].set_xlabel('Temperature (°C)')



    axs[0].set_ylabel(f'Density kg/m$^3$')
    axs[0].legend()


    """Density vs Pressure"""
    # Plot saturation curves with Pressure on x-axis
    axs[1].plot(saturation_pressures, liquid_density, label='Saturated Liquid Density')
    axs[1].plot(saturation_pressures, vapor_density, label='Saturated Vapor Density')
    axs[1].fill_between(saturation_pressures, liquid_density, vapor_density, color='gray', alpha=0.2)

    P_critical = CP.PropsSI('Pcrit', substance) / 1e5
    # print(f'P_critical = {P_critical:.2f} bar')
    axs[1].plot(P_critical, D_critical, 'kx', label='Critical Point')

    # Plot isotherm
    isoT_Ps = np.linspace(1e4, 90e5, 500)
    try:
        rho = CP.PropsSI('D', 'T', isoT, 'P', isoT_Ps, substance)
        isoT_Ps_bar = [pressure / 1e5 for pressure in isoT_Ps]  # Convert to bar
        axs[1].plot(isoT_Ps_bar, rho, label=f'Isotherm at {isoT-273.15:.1f} °C')
        P_sat = CP.PropsSI('P', 'T', isoT, 'Q', 0, substance)
        axs[1].axvline(P_sat / 1e5, color='gray', linestyle='--', label=f'$P_{{sat}}$ = {P_sat / 1e5:.2f} bar')

        # Plot saturation points
        D_V = CP.PropsSI('D', 'T', isoT, 'Q', 1, substance)
        D_L = CP.PropsSI('D', 'T', isoT, 'Q', 0, substance)
        P_V = CP.PropsSI('P', 'T', isoT, 'Q', 1, substance) / 1e5
        P_L = CP.PropsSI('P', 'T', isoT, 'Q', 0, substance) / 1e5
        axs[1].plot(P_V, D_V, 'ro', label=f'$\\rho_{{V, sat}}$ = {D_V:.2f} kg/m$^3$')
        axs[1].plot(P_L, D_L, 'bo', label=f'$\\rho_{{L, sat}}$ = {D_L:.2f} kg/m$^3$')

        # # Annotate the density of the saturated liquid and vapor use LaTeX formatting and put into boxes
        # axs[1].annotate(f'{D_L:.2f} kg/m$^3$', xy=(P_L+2, D_L+50))
        # axs[1].annotate(f'{D_V:.2f} kg/m$^3$', xy=(P_V + 3, 0))
    except:
        pass

    axs[1].set_title('Density vs Pressure')
    axs[1].set_xlabel('Pressure (bar)')
    axs[1].set_xlim(0, 90)
    axs[1].legend(loc = 'upper right')

    # Display plot
    plt.suptitle(f'$N_{2}O$ Density Curves', fontsize=20)
    plt.tight_layout()
    plt.show()

def density_sliders():
    isoT_slider = widgets.FloatSlider(
        value=15,
        min=-10,
        max=60,
        step=0.5,
        description= f'Tsat (°C)',
        continuous_update=False
    )

    isoP_slider = widgets.FloatSlider(
        value=40,
        min=1,
        max=90,
        step=.5,
        description= f'Psat (bar)',
        continuous_update=False
    )
    return isoT_slider, isoP_slider

if __name__ == '__main__':
    plot_curves()