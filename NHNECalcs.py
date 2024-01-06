import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP
import ipywidgets as widgets

from HEMCalcs import plotting, A
from SPICalcs import CalcSPI, m_CPI

def NHNEPlot(T, N, kap, Cd, Nom):
    d = np.linspace(0.1, 6, 1000) / 1000
    Pc = 20e5

    mNom = Nom
    mHEM = plotting(d, T, N, Cd)  # remove Cd=Cd
    mSPI = CalcSPI(T, 'NitrousOxide', Pc, N, d, Cd)[0]
    mkappa = ((kap / (1 + kap)) * mSPI) + (1/(1 + kap) * mHEM)

    plt.plot(d * 1000, mHEM, label=r'$\dot{m}_{HEM}$')
    plt.plot(d * 1000, mSPI, label=r'$\dot{m}_{SPI}$')
    plt.plot(d * 1000, mkappa, label=f'$\\dot{{m}}_{{\\kappa}}$, $\\kappa={kap}$')
    plt.axhline(mNom, color='r', linestyle='--', label=f'$\\dot{{m}}_{{Design}}={mNom}$ kg/s')

    plt.fill_between(d * 1000, mHEM, mSPI, color='lightgrey', alpha=0.5)

    idx_HEM = np.argmin(np.abs(mHEM - mNom))
    idx_SPI = np.argmin(np.abs(mSPI - mNom))
    idx_kappa = np.argmin(np.abs(mkappa - mNom))

    d_HEM = d[idx_HEM] * 1000
    d_SPI = d[idx_SPI] * 1000
    d_kappa = d[idx_kappa] * 1000

    plt.plot(d_HEM, mNom, color='tab:blue', marker='o', label=f'$d_{{HEM}}={d_HEM:.2f}$ mm')
    plt.plot(d_SPI, mNom, color='tab:orange', marker='o', label=f'$d_{{SPI}}={d_SPI:.2f}$ mm')
    plt.plot(d_kappa, mNom, color='tab:green', marker='o', label=f'$d_{{\\kappa}}={d_kappa:.2f}$ mm')
    plt.xlabel('Diameter (mm)')
    plt.ylabel('Mass Flow Rate (kg/s)')
    plt.title(f'Mass Flow Rate vs Diameter\n {N} Orifices at $T_{{tank}} =${T:.2f}°C')
    plt.xlim(0, 3)
    plt.ylim(0, 2)
    plt.tight_layout()
    plt.legend()


# Create sliders for the temperature, the number of orifices and the kappa value
def NHNESliders():
    T_slider = widgets.FloatSlider(
        value=30,
        min=-10,
        max=32,
        step=0.5,
        description=f'T',
        continuous_update=False
    )
    N_slider = widgets.IntSlider(
        value=12,
        min=1,
        max=50,
        step=1,
        description='N',
        continuous_update=False
    )
    kap_slider = widgets.FloatSlider(
        value=1.4,
        min=0,
        max=2,
        step=0.01,
        description=f'kappa',
        continuous_update=False
    )

    Cd_slider = widgets.FloatSlider(
        value=0.6,
        min=0,
        max=1.5,
        step=0.01,
        description=f'Cd',
        continuous_update=False
    )
    Nom_slider = widgets.FloatSlider(
        value=1.36,
        min=.3,
        max=2.5,
        step=0.01,
        description=f'mass',
        continuous_update=False
    )
    return T_slider, N_slider, kap_slider, Cd_slider, Nom_slider

