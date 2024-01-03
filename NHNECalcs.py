import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP
import ipywidgets as widgets

from HEMCalcs import plotting, A
from SPICalcs import CalcCPI, m_CPI

def NHNEPlot(T, N, kap):
    d = np.linspace(0.1, 6, 1000) / 1000
    Pc = 20e5

    mNom = 1.36
    mHEM = plotting(d, T, N)
    mSPI = CalcCPI(T, 'NitrousOxide', Pc, N, d)[0]
    mkappa = (1 / (1 + kap)) * mSPI + (1 - (kap / (1 + kap))) * mHEM

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
    plt.title(f'Mass Flow Rate vs Diameter\n {N} Orifices at $T_{{tank}} =${T}°C')
    plt.xlim(0, 2.5)
    plt.ylim(0, 2)
    plt.tight_layout()
    plt.legend()


# Create sliders for the temperature, the number of orifices and the kappa value
def NHNESliders():
    T_slider = widgets.FloatSlider(
        value=30,
        min=-10,
        max=60,
        step=0.5,
        description=r'$T_{\text{tank}}$ (°C)',
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
        description=r'$\kappa$',
        continuous_update=False
    )
    return T_slider, N_slider, kap_slider

