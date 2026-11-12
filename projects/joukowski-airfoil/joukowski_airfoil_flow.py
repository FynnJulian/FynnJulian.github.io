"""
Joukowski airfoil potential flow with angle of attack.

Pipeline (all per your rotation-based method):
    horizontal-flow cylinder  ->  rotate by -AoA  ->  translate by (a,b)  ->  Joukowski
Streamlines are drawn as contours of the stream function evaluated on a polar
grid in the cylinder plane, then forward-mapped.  No root-finding, no gaps.
"""

import numpy as np
import matplotlib.pyplot as plt

# Only incompressible solver
# ------------------------------------------------------------------ configure
c        = 1            # Joukowski constant (NOT the cylinder radius)
Origen   = [-0.1, 0.1]    # circle-center offset mu = a + i b (camber/thickness)
Velocity = 20.0            # free-stream speed [m/s]
density  = 1.225          # [kg/m^3]
AoA_config      = 1.0    # angle of attack [degree]
Viscosity_config = 1.5 #10^5 m^2/S


n_levels = 600            # number of streamlines
grid_r   = 600           # radial grid resolution
grid_phi = 800           # angular grid resolution
r_outer  = 14.0          # outer radius of the cylinder-plane grid (large enough
                         # that the mapped grid covers the plot window)
xlim, ylim = (-4, 4), (-2, 2)

# --------------------------------------------------------------- derived setup
a, b = Origen
mu   = a + 1j * b
Viscosity = Viscosity_config/(10**5)

AoA = - (AoA_config / 360 *2 * np.pi)      #stupid sign mistake

def calc_radius(c, Origen):
    """Cylinder radius: the circle must pass through the critical point +c."""
    a, b = Origen
    return np.sqrt(b**2 + (c - a)**2)

def find_circulation(Origen, Radius, Velocity, c, AoA):
    """
    Kutta condition for the rotate-by-(-AoA) pipeline.
    y2_te is the trailing-edge critical point traced back into the horizontal-
    flow plane; its height sets gamma.  (Rotation sign and this formula must
    stay coupled: rotate by -AoA  <->  +(c-a)sin - b cos.)
    """
    a, b = Origen
    y2_te = (c - a) * np.sin(AoA) - b * np.cos(AoA)
    gamma = y2_te / Radius
    return 4 * np.pi * Velocity * Radius * gamma

Radius      = calc_radius(c, Origen)
Circulation = find_circulation(Origen, Radius, Velocity, c, AoA)
Lift        = -density * Velocity * Circulation      # Kutta-Joukowski, per unit span

# --------------------------------- stream function on a polar grid (exterior)
r   = np.linspace(Radius, r_outer, grid_r)
phi = np.linspace(0.0, 2 * np.pi, grid_phi)
Rr, Ph = np.meshgrid(r, phi)

# same expression as the old stream_funktion_phy, just evaluated (not solved):
#   psi = U*sin(phi)*(r - R^2/r)  -  Gamma/(2 pi) * ln r
psi = Velocity * np.sin(Ph) * (Rr - Radius**2 / Rr) - Circulation / (2 * np.pi) * np.log(Rr)
psi_stag = -Circulation / ((2 * np.pi) * np.log(Radius))

# ---------------------------- forward map: rotate -> translate -> Joukowski
z_flow  = Rr * np.exp(1j * Ph)          # point in the horizontal-flow plane
z_rot   = z_flow * np.exp(-1j * AoA)    # rotate by -AoA
z_prime = z_rot + mu                    # translate to the offset circle
Z       = z_prime + c**2 / z_prime      # Joukowski map to the airfoil plane
X, Y    = Z.real, Z.imag

# --------------------------------------------------------------------- plot
# ---------------------------- EXTRACT GEOMETRY ----------------------------
# The airfoil boundary corresponds to the inner radius (r = Radius -> column 0 of Meshgrid)
# num_py array matrix matrix[row][collum] -> Matrix[phi][r] r[o]=Radius so Z[:,0] selects all points with r = Radius
# 1. Isolate boundary points (column 0 of your Z matrix)
z_boundary = Z[:, 0]
x_b, y_b = z_boundary.real, z_boundary.imag

# 2. Find Chord
c = np.max(x_b) - np.min(x_b)

# 3. Separate upper (y > mean) and lower (y <= mean) surfaces
y_mean = np.mean(y_b)
upper_mask = y_b >= y_mean
lower_mask = y_b < y_mean

# Sort coordinates along x for interpolation
x_up, y_up = x_b[upper_mask], y_b[upper_mask]
x_low, y_low = x_b[lower_mask], y_b[lower_mask]

idx_up = np.argsort(x_up)
idx_low = np.argsort(x_low)

# 4. Interpolate onto a shared x-grid along the chord
x_grid = np.linspace(np.min(x_b), np.max(x_b), 500)
y_up_interp = np.interp(x_grid, x_up[idx_up], y_up[idx_up])
y_low_interp = np.interp(x_grid, x_low[idx_low], y_low[idx_low])

# 5. True Thickness & t/c Ratio
thickness_distribution = y_up_interp - y_low_interp
t_max = np.max(thickness_distribution)
t_over_c = t_max / c
# --------------------------------------------------------------------- plot
#-----------------------------Drag estimation Blasius and Hoerner-----------
REx = Velocity * c / Viscosity
if REx <= 5*10**5:
    Flat_Cd = 2 * 1.328/np.sqrt(REx)
if 5 * 10**5 < REx < 10**7:
    Flat_Cd = 2 * 0.074 / (REx**0.2)
if REx > 10**7:
    Flat_Cd = 0
Cd = Flat_Cd*(1 + 2* t_over_c + 60 * (t_over_c)**4)
Drag = Cd * c * density * Velocity**2 * 0.5
if Flat_Cd == 0:
 Drag = REx

#---------------------------------------------------------------------------
plt.figure(figsize=(9, 6))
plt.contour(X, Y, psi, levels=n_levels, colors='b', linewidths=0.6,
            linestyles='solid')
plt.axis('equal')
plt.xlim(*xlim)
plt.ylim(*ylim)
plt.title(f"Joukowski airfoil  |  AoA = {AoA_config:.1f} deg  |  "
          f"L = {Lift:.2f} N/m  |  "f" D = {Drag:.2f} N/m (>>camber & >> AoA)" )
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
print(c)
plt.show()
