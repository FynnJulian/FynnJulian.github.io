"""File paths"""
##Open Elementtable with Pandas
# The FE exports and the submission template are not published with this code.
# Point ASE_DATA_DIR at the folder holding them, or put them in ./data next to
# this file. The submission template is named with the student number in the
# original; rename it to match below, or set ASE_TEMPLATE.
import os

DATA_DIR = os.environ.get(
    "ASE_DATA_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"),
)
TEMPLATE = os.environ.get("ASE_TEMPLATE", "ASE_Project_Part1_SubmissionTemplate.csv")

locationPanel          = os.path.join(DATA_DIR, "xxyyxyvonMises.csv")
locationStringer       = os.path.join(DATA_DIR, "xxstringer.csv")
locationGeneral_values = os.path.join(DATA_DIR, TEMPLATE)

"""Stringer Placement"""
Stringer_Placemtent =["T", "T","O", "T","O", "T","O", "O","O"]
PoissonRatio = float(0.34)

"""
Geometrie data for the calculations
"""

longSide = 600  #float(input("Panel lenght long side: "))
shortSide = 200  #float(input("Panel lenght short side: "))
thickness = 4  #float(input("Panel thickness: "))

lenghtSTR = 600 #float(input("T-Stringer Segmentlenght: "))
t2Tstr = 2 #float(input("t2 stringer dimensions (See crippeling stress): "))
t1Tstr = 3 #float(input("t1 stringer dimensions (See crippeling stress): "))
a12Tstr = 40 #float(input("a1.2 stringer dimensions (See crippeling stress): "))
a11Tstr = 35 #float(input("a1.1 stringer dimensions (See crippeling stress): "))
A_T_str = t1Tstr*2*a11Tstr + t2Tstr*(a12Tstr-t1Tstr)
I_T_stringer = 47458.95326 #float(input("Moment of inertia T-Stringer: "))


a11Ostr = 17.5 #float(input("‾|_|‾   a1.1 of ‾ (See crippeling stress): "))
ta11Ostr = 2.5  #float(input("thickness of ‾ from ‾|_|‾: "))
a1vOstr = 29 #float(input("‾|_|‾  a1 of | (See crippeling stress): "))
ta1vOstr = 2.5 #float(input("thickness of | from ‾|_|‾: "))
a2hOstr = 20 #float(input("‾|_|‾   a2 of _ (See crippeling stress): "))
ta2hOstr = 2.5 #float(input("thickness of _ from ‾|_|‾: "))
A_O_str = 257.5 #float(input("Area O-Stringer: "))
I_O_stringer = 71434.45146 #float(input("Moment of inertia O-Stringer: "))