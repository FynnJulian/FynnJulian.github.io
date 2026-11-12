# bielliptic transfer orbit solver for circular orbits
import matplotlib.pyplot as plt
from config import *
#from Fire_sequence import *


def bielliptic_solver(transfer_orbit):

    v_initial = ((μ_earth / (r_earth + initial_orbit)))**0.5

    a = 1/2 * (initial_orbit + 2*r_earth + transfer_orbit)

    v_burn1 = ((2 / (initial_orbit + r_earth) - 1 / a ) * μ_earth)**0.5

    delta_v1 = v_burn1 - v_initial

    # phase 1 complete

    v_Apogee_transfer = ((2 / (transfer_orbit + r_earth) - 1 / a ) * μ_earth)**0.5

    a_tranfer2 = 1/2 * (final_orbit + 2*r_earth + transfer_orbit)

    v_burn2 = ((2 / (transfer_orbit + r_earth) - 1 / a_tranfer2 ) * μ_earth)**0.5

    delta_v2 = abs(v_burn2 - v_Apogee_transfer)

    #phase 2 complete

    v_final_transfer = ((2 / (final_orbit + r_earth) - 1 / a_tranfer2 ) * μ_earth)**0.5

    v_final = (μ_earth / (final_orbit + r_earth))**0.5

    delta_v3 = abs(v_final - v_final_transfer)

    #phase 3 complete

    total = abs( delta_v1 + delta_v2 + delta_v3)

    return total

def Hohmann():

    v_initial = (μ_earth / (initial_orbit + r_earth))**0.5

    a_tranfer = 0.5 * (2 * r_earth + initial_orbit + final_orbit)

    v_burn1 = ( ( 2 / (r_earth + initial_orbit) - 1 / a_tranfer) * μ_earth) ** 0.5

    delta_v1 = abs(v_burn1 - v_initial)

    #phase 1 complete

    v_transfer_apogee = ( ( 2 / (r_earth + final_orbit) - 1 / a_tranfer) * μ_earth) ** 0.5

    v_burn2 = (μ_earth / (final_orbit + r_earth))**0.5

    delta_v2 = abs( v_burn2 - v_transfer_apogee)

    #phase 2 complete

    total_delta_v = delta_v1 + delta_v2

    return total_delta_v

delta_v = []
transfer_orbit = []

for i in range(final_orbit, 300000000, 1000000):   # 1000 km steps
    delta_v.append(bielliptic_solver(i))
    transfer_orbit.append(i)

plt.plot(transfer_orbit, delta_v)
plt.axhline(Hohmann(), linestyle="--", color="gray", label="Hohmann")
plt.title(rf"Hohmann $\Delta v$: {Hohmann():.1f} m/s")
plt.legend()
plt.xlabel("Transfer orbit apoapsis altitude (m)")
plt.ylabel(r"Total $\Delta v$ (m/s)")
plt.show()

