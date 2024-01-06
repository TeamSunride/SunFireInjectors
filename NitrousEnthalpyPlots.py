import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from matplotlib.ticker import FuncFormatter

# Define the subst
subst = 'NitrousOxide'

# Define temperature range (in Kelvin)
T_min = CP.PropsSI(subst, 'Tmin') + 0.01  # slightly above the minimum temperature
T_max = CP.PropsSI(subst, 'Tcrit')        # critical temperature
temperatures = np.linspace(T_min, T_max, int(1e3))

def get_saturations(T):
    liquid_enthalpy = []
    vapor_enthalpy = []
    saturation_pressures = []

    # Calculate densities and pressures at each temperature
    for T in temperatures:
        lh = CP.PropsSI('H', 'T', T, 'Q', 0, subst)  # liquid enthalpy
        vh = CP.PropsSI('H', 'T', T, 'Q', 1, subst)  # vapor enthalpy
        psat = CP.PropsSI('P', 'T', T, 'Q', 0, subst) # saturation pressure

        liquid_enthalpy.append(lh)
        vapor_enthalpy.append(vh)
        saturation_pressures.append(psat)

    return liquid_enthalpy, vapor_enthalpy, saturation_pressures

def find_critical(subst):
    T_critical = CP.PropsSI('Tcrit', subst)
    P_critical = CP.PropsSI('Pcrit', subst)
    H_critical = CP.PropsSI('H', 'T', T_critical, 'P', P_critical, subst)
    return T_critical, P_critical, H_critical

def enthaly_temperature_plot(ax, subst, temperatures):
    liquid_enthalpy, vapor_enthalpy,_ = get_saturations(temperatures)
    T_critical, _, H_critical = find_critical(subst)

    # Covert to bar, kJ/kg and deg C
    temperatures = np.array(temperatures) - 273.15
    liquid_enthalpy = np.array(liquid_enthalpy) * 1e-3
    vapor_enthalpy = np.array(vapor_enthalpy) * 1e-3
    T_critical -= 273.15
    H_critical *= 1e-3

    ax.plot(temperatures, liquid_enthalpy, label='Saturated Liquid Enthalpy')
    ax.plot(temperatures, vapor_enthalpy, label='Saturated Vapor Enthalpy')
    ax.fill_between(temperatures, liquid_enthalpy, vapor_enthalpy, color='gray', alpha=0.2)
    ax.plot(T_critical, H_critical, 'kx', label='Critical Point')
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Enthalpy (kJ/kg)')
    ax.set_title('Enthalpy vs Temperature')

def isobar_plot(ax, subst, isoP):
    P = isoP * 1e5
    T = np.linspace(260,370, 500)
    h = CP.PropsSI('H', 'P', P, 'T', T, subst) * 1e-3
    ax.plot(T- 273.15, h, label=f'Isobar at {isoP:.1f} bar')

    try:
        hv = CP.PropsSI('H', 'P', P, 'Q', 1, subst) * 1e-3
        hl = CP.PropsSI('H', 'P', P, 'Q', 0, subst) * 1e-3
        tv = CP.PropsSI('T', 'P', P, 'Q', 1, subst) - 273.15
        tl = CP.PropsSI('T', 'P', P, 'Q', 0, subst) - 273.15


        ax.axvline(tv, color='gray', linestyle='--', label=f'$T_{{sat}}$ = {tv:.1f} °C')
        ax.plot(tv, hv, 'ro', label=f'$h_{{v}}$ = {hv:.1f} kg/m$^3$')
        ax.plot(tl, hl, 'bo', label=f'$h_{{l}}$ = {hl:.1f} kg/m$^3$')
    except:
        pass

def enthaly_pressure_plot(ax, subst, temperatures):
    liquid_enthalpy, vapor_enthalpy, saturation_pressures = get_saturations(temperatures)
    _,P_critical, H_critical = find_critical(subst)

    # Covert to bar, kJ/kg and deg C
    pressures = np.array(saturation_pressures) * 1e-5
    liquid_enthalpy = np.array(liquid_enthalpy) * 1e-3
    vapor_enthalpy = np.array(vapor_enthalpy) * 1e-3
    P_critical *= 1e-5
    H_critical *= 1e-3

    ax.plot(pressures, liquid_enthalpy, color='tab:blue', label='Saturated Liquid Enthalpy')
    ax.plot(pressures, vapor_enthalpy, color='tab:orange', label='Saturated Vapor Enthalpy')
    ax.fill_between(pressures, liquid_enthalpy, vapor_enthalpy, color='gray', alpha=0.2)
    ax.plot(P_critical, H_critical, 'kx', label='Critical Point')
    ax.set_xlabel('Pressure (bar)')
    ax.set_ylabel('Enthalpy (kJ/kg)')
    ax.set_title('Enthalpy vs Pressure')

def isotherm_plot(ax, subst, isoT):
    T = isoT + 273.15
    P = np.linspace(1, 90, 500) * 1e5
    h = CP.PropsSI('H', 'P', P, 'T', T, subst) * 1e-3
    ax.plot(P * 1e-5, h, color='tab:green',label=f'Isobar at {isoT:.1f} °C')

    try:
        hv = CP.PropsSI('H', 'P', P, 'Q', 1, subst) * 1e-3
        hl = CP.PropsSI('H', 'P', P, 'Q', 0, subst) * 1e-3
        pv = CP.PropsSI('P', 'T', T, 'Q', 1, subst) * 1e-5  # Calculate the saturation pressure at the isothermal temperature

        # Find the index where P is closest to pv
        idx = (np.abs(P*1e-5 - pv)).argmin()

        # Extract the corresponding values of hv and hl
        hv_at_pv = hv[idx]
        hl_at_pv = hl[idx]

        ax.axvline(pv, color='gray', linestyle='--')
        ax.plot(pv, hv_at_pv, 'ro', label=f'$h_{{v}}$ = {hv_at_pv:.1f} kJ/kg')
        ax.plot(pv, hl_at_pv, 'bo', label=f'$h_{{l}}$ = {hl_at_pv:.1f} kJ/kg')
    except:
        pass

def plot_enthalpies(isoT=40, isoP=71):
    fig, axs = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Plot enthalpy vs temperature
    enthaly_temperature_plot(axs[0], subst, temperatures)
    isobar_plot(axs[0], subst, isoP)

    # Plot enthalpy vs pressure
    enthaly_pressure_plot(axs[1], subst, temperatures)
    isotherm_plot(axs[1], subst, isoT)

    axs[0].set_xlim(-10, 60)
    axs[1].set_xlim(0, 90)
    axs[0].legend(loc = 'lower right')
    axs[1].legend(loc = 'lower right')
    plt.suptitle(f'$N_{2}O$ Enthalpy Curves', fontsize=20)


def enthalpy_sliders():
    isoT_slider = widgets.FloatSlider(
        value=15,
        min=-10,
        max=60,
        step=0.5,
        description='Tsat (°C)',
        continuous_update=False
    )

    isoP_slider = widgets.FloatSlider(
        value=40,
        min=1,
        max=90,
        step=.5,
        description=f'Psat (bar)',
        continuous_update=False
    )
    return isoT_slider, isoP_slider

if __name__ == '__main__':
    plot_enthalpies()
    plt.show()
    # print critical point values
    T_critical, P_critical, H_critical = find_critical(subst)
    print(f'T_critical = {T_critical:.2f} K')
    print(f'T_critical = {T_critical - 273.15:.2f} °C')
    print('\n')
    print(f'P_critical = {P_critical:.2f} Pa')
    print(f'P_critical = {P_critical * 1e-5:.2f} bar')

