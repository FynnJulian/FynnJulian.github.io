# Project files

The source behind each write-up on <https://fynnjulian.github.io/>. Code is
published as it was written and run; the plots on the site come from these files
executed unchanged.

| Folder | What it is |
|---|---|
| [`nosecone-cfd/`](nosecone-cfd/) | Report on a slender nosecone at Mach 2.75, 6 300 m, 2° angle of attack, solved in Ansys Fluent, with the shock angle measured off the solution and compared against the oblique-shock relation. WARR, March 2026. |
| [`joukowski-airfoil/`](joukowski-airfoil/) | Potential-flow solver by conformal mapping, with circulation set by the Kutta condition and the geometry recovered from the mapped boundary. Python, August 2026. |
| [`mobilenet-eurosat/`](mobilenet-eurosat/) | Report on pruning and int8 quantization of a MobileNetV3 land-cover classifier, 16.17 MB down to 0.11 MB. TUM course project with Leon Blum, July 2026. |
| [`orbital-motion/`](orbital-motion/) | Two-body orbit in Hamiltonian form, integrated with symplectic Euler over 400 000 steps. MATLAB, May 2026. |
| [`bielliptic-transfer/`](bielliptic-transfer/) | Sweeps the intermediate apoapsis of a three-burn bi-elliptic transfer and compares its total Δv against the two-burn Hohmann. Python, November 2026. |
| [`stiffened-panel/`](stiffened-panel/) | Reserve-factor toolchain for a stiffened panel: panel buckling, crippling for T- and Ω-stringers, and column buckling, read from FE stress tables and written back into the submission template. TUM coursework, May 2026. |
| [`aerospace-essays/`](aerospace-essays/) | Four short literature-based essays: hydrogen against kerosene, wing sweep and critical Mach number, an ocean on Europa, and lightsail materials. TUM coursework, February 2025. |

## Running the code

`joukowski-airfoil` and `bielliptic-transfer` need Python with NumPy and
Matplotlib, and run as they are. `orbital-motion` runs in MATLAB or Octave.

`stiffened-panel` reads FE exports and a submission template that are not
published here. Point `ASE_DATA_DIR` at the folder holding them, or place them
in a `data/` folder beside the code; `ASE_TEMPLATE` sets the template's filename.
