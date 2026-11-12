import pandas as pd
import time
import ASEfunktions as ASE
import CSVfunktions as CSVf
from configCalculator import *


#finds the Value of propertie from table
TablePanel = pd.read_csv(locationPanel, skiprows=CSVf.find_trigger(locationPanel, "Elements"), nrows=90)
TableStringer = pd.read_csv(locationStringer, skiprows=CSVf.find_trigger(locationStringer, "Elements"), nrows=81)


"""Calculating with 3 loadcases hard coded!:"""
Strings_LC1_str = TableStringer.loc[TableStringer['Loadcase'] == 1, 'Element Stresses (1D):CBAR/CBEAM Axial Stress'].tolist()
Stringers_LC1 = [float(i) for i in Strings_LC1_str]

Strings_LC2_str = TableStringer.loc[TableStringer['Loadcase'] == 2, 'Element Stresses (1D):CBAR/CBEAM Axial Stress'].tolist()
Stringers_LC2 = [float(i) for i in Strings_LC2_str]

Strings_LC3_str = TableStringer.loc[TableStringer['Loadcase'] == 3, 'Element Stresses (1D):CBAR/CBEAM Axial Stress'].tolist()
Stringers_LC3 = [float(i) for i in Strings_LC3_str]

#Panel Data
Panel_LC1_XX_str = TablePanel.loc[TablePanel['Loadcase'] == 1, 'XX'].tolist()
Panel_LC1_XX = [float(i) for i in Panel_LC1_XX_str]

Panel_LC1_XY_str = TablePanel.loc[TablePanel['Loadcase'] == 1, 'XY'].tolist()
Panel_LC1_XY = [float(i) for i in Panel_LC1_XY_str]
Panel_LC1_YY_str = TablePanel.loc[TablePanel['Loadcase'] == 1, 'YY'].tolist()
Panel_LC1_YY = [float(i) for i in Panel_LC1_YY_str]
Panel_LC1_vanMises_str = TablePanel.loc[TablePanel['Loadcase'] == 1, 'vonMises'].tolist()
Panel_LC1_vanMises = [float(i) for i in Panel_LC1_vanMises_str]

Panel_LC2_XX_str = TablePanel.loc[TablePanel['Loadcase'] == 2, 'XX'].tolist()
Panel_LC2_XX = [float(i) for i in Panel_LC2_XX_str]
Panel_LC2_XY_str = TablePanel.loc[TablePanel['Loadcase'] == 2, 'XY'].tolist()
Panel_LC2_XY = [float(i) for i in Panel_LC2_XY_str]
Panel_LC2_YY_str = TablePanel.loc[TablePanel['Loadcase'] == 2, 'YY'].tolist()
Panel_LC2_YY = [float(i) for i in Panel_LC2_YY_str]
Panel_LC2_vanMises_str = TablePanel.loc[TablePanel['Loadcase'] == 2, 'vonMises'].tolist()
Panel_LC2_vanMises = [float(i) for i in Panel_LC2_vanMises_str]

Panel_LC3_XX_str = TablePanel.loc[TablePanel['Loadcase'] == 3, 'XX'].tolist()
Panel_LC3_XX = [float(i) for i in Panel_LC3_XX_str]
Panel_LC3_XY_str = TablePanel.loc[TablePanel['Loadcase'] == 3, 'XY'].tolist()
Panel_LC3_XY = [float(i) for i in Panel_LC3_XY_str]
Panel_LC3_YY_str = TablePanel.loc[TablePanel['Loadcase'] == 3, 'YY'].tolist()
Panel_LC3_YY = [float(i) for i in Panel_LC3_YY_str]
Panel_LC3_vanMises_str = TablePanel.loc[TablePanel['Loadcase'] == 3, 'vonMises'].tolist()
Panel_LC3_vanMises = [float(i) for i in Panel_LC3_vanMises_str]

avgEmod = float(CSVf.get_general_value("E-modulus (average) [MPa]", locationGeneral_values))
ultimateStrengh = float(CSVf.get_general_value("Ultimate strength (t/c) [MPa]", locationGeneral_values))
yieldStrengh = float(CSVf.get_general_value("Yield strength (t/c) [MPa]", locationGeneral_values))
BbaseEmod = float(CSVf.get_general_value("E-modulus (B-basis) [MPa]", locationGeneral_values))







"""
FUNKTION CALL & DATA ENTRY
"""

#crippeling stress T - Stringer
Sigma_crip_T = ASE.sig_crip_T(t2Tstr, t1Tstr, a12Tstr, a11Tstr, BbaseEmod, yieldStrengh)
Sigma_crip_O = ASE.sig_crip_O(a1vOstr,ta1vOstr,a2hOstr,ta2hOstr,a11Ostr,ta11Ostr,yieldStrengh,BbaseEmod)
Sigma_crip = []


for i in range(0,len(Stringer_Placemtent)):
    if Stringer_Placemtent[i] == "T":
        Sigma_crip.append(Sigma_crip_T)
    if Stringer_Placemtent[i] == "O":
        Sigma_crip.append(Sigma_crip_O)

CSVf.data_entry(locationGeneral_values, 'Stability Analysis - Column Buckling', 'LC1', 'sig_crip [MPa]',Sigma_crip)
CSVf.data_entry(locationGeneral_values, 'Stability Analysis - Column Buckling', 'LC3', 'sig_crip [MPa]',Sigma_crip)



#RF_Strengh
elements = Panel_LC1_vanMises[:]
for i in range(0, len(Stringers_LC1)):
    elements.append(Stringers_LC1[i])
RF_elements = []
for i in range(0, len(elements)):
    RF_elements.append(ASE.RFstrenght(ultimateStrengh, elements[i]))

CSVf.data_entry(locationGeneral_values, 'Strength Analysis', 'LC1', 'RFstrength [-]',RF_elements)

elements = Panel_LC3_vanMises[:]
for i in range(0, len(Stringers_LC3)):
    elements.append(Stringers_LC3[i])
RF_elements = []
for i in range(0, len(elements)):
    RF_elements.append(ASE.RFstrenght(ultimateStrengh, elements[i]))

CSVf.data_entry(locationGeneral_values, 'Strength Analysis', 'LC3', 'RFstrength [-]',RF_elements)


#sig_Panel_avg
V = longSide*shortSide*thickness

Sig_XX_LC1 = []

string = Panel_LC1_XX[:]
for i in range(0,10):
    Sig_XX_LC1.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC1','sig_xx (average,midplane) [MPa]', Sig_XX_LC1)

Sig_XX_LC3 = []

string = Panel_LC3_XX[:]
for i in range(0,10):
    Sig_XX_LC3.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC3','sig_xx (average,midplane) [MPa]', Sig_XX_LC3)


Sig_XY_LC1 = []

string = Panel_LC1_XY[:]
for i in range(0,10):
    Sig_XY_LC1.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC1','sig_xy (average,midplane) [MPa]', Sig_XY_LC1)

Sig_XY_LC3 = []

string = Panel_LC3_XY[:]
for i in range(0,10):
    Sig_XY_LC3.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC3','sig_xy (average,midplane) [MPa]', Sig_XY_LC3)


Sig_YY_LC1 = []

string = Panel_LC1_YY[:]
for i in range(0,10):
    Sig_YY_LC1.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC1','sig_yy (average,midplane) [MPa]', Sig_YY_LC1)

Sig_YY_LC3 = []

string = Panel_LC3_YY[:]
for i in range(0,10):
    Sig_YY_LC3.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC3','sig_yy (average,midplane) [MPa]', Sig_YY_LC3)



#k-biax, k-shear
k_shear_list = []
for i in range(0,10):
    k_shear_list.append(ASE.k_shear(longSide, shortSide))
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC1','k_shear [-]', k_shear_list)
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC3','k_shear [-]', k_shear_list)

k_biax_list = []
Sig_XX_LC1 = []
RF_Panel_list = []

string = Panel_LC1_XX[:]
for i in range(0,10):
    Sig_XX_LC1.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

Sig_YY_LC1 = []

string = Panel_LC1_YY[:]
for i in range(0,10):
    Sig_YY_LC1.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

Sig_XY_LC1 = []

string = Panel_LC1_XY[:]
for i in range(0,10):
    Sig_XY_LC1.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

for i in range(0,10):
    k_biax_list.append(ASE.k_biax(Sig_XX_LC1[i], Sig_YY_LC1[i], longSide, shortSide))
    RF_Panel_list.append(ASE.RF_panelbuckel(avgEmod, PoissonRatio, thickness, shortSide, longSide, Sig_XX_LC1[i], Sig_YY_LC1[i], Sig_XY_LC1[i]))
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC1','k_biax [-]', k_biax_list)
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC1','RF_panelbuckl [-]', RF_Panel_list)

k_biax_list = []
RF_Panel_list = []
Sig_XX_LC3 = []

string = Panel_LC3_XX[:]
for i in range(0,10):
    Sig_XX_LC3.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

Sig_YY_LC3 = []

string = Panel_LC3_YY[:]
for i in range(0,10):
    Sig_YY_LC3.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

Sig_XY_LC3 = []

string = Panel_LC3_XY[:]
for i in range(0,10):
    Sig_XY_LC3.append(ASE.sig_avg(string[0:3], V))
    del string[0:3]

for i in range(0,10):
    k_biax_list.append(ASE.k_biax(Sig_XX_LC3[i], Sig_YY_LC3[i], longSide, shortSide))
    RF_Panel_list.append(ASE.RF_panelbuckel(avgEmod, PoissonRatio, thickness, shortSide, longSide, Sig_XX_LC3[i], Sig_YY_LC3[i], Sig_XY_LC3[i]))

CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC3','k_biax [-]', k_biax_list)
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Panel Buckling', 'LC3','RF_panelbuckl [-]', RF_Panel_list)


"""average sig with panel and define A,I """
A = shortSide*thickness
#List of Axial stress Average per stringer
Stringer_sig_avg_LC1 = []
Stringer_sig_avg_LC3 = []

stringP = Panel_LC1_XX[:]
string = Stringers_LC1[:]
for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        Stringer_sig_avg_LC1.append(ASE.sig_axial(string[0:3], lenghtSTR, A, A_T_str, stringP))
    if Stringer_Placemtent[i] == "O":
        Stringer_sig_avg_LC1.append(ASE.sig_axial(string[0:3], lenghtSTR, A, A_O_str, stringP))
    del string[0:3]
    del stringP[0:3]

stringP = Panel_LC3_XX[:]
string = Stringers_LC3[:]
for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        Stringer_sig_avg_LC3.append(ASE.sig_axial(string[0:3], lenghtSTR, A, A_T_str, stringP))
    if Stringer_Placemtent[i] == "O":
        Stringer_sig_avg_LC3.append(ASE.sig_axial(string[0:3], lenghtSTR, A, A_O_str, stringP))
    del string[0:3]
    del stringP[0:3]

CSVf.data_entry(locationGeneral_values, 'Stability Analysis - Column Buckling', 'LC1', 'sig_axial (combined, average) [MPa]',Stringer_sig_avg_LC1)
CSVf.data_entry(locationGeneral_values, 'Stability Analysis - Column Buckling', 'LC3', 'sig_axial (combined, average) [MPa]',Stringer_sig_avg_LC3)

#Sigma_crip list
#Stringer_sig_avg_LC1 list
#Stringer_sig_avg_LC3 list
#Stringer placement list
#Sig_xx_LC1
#sig_xxLc3
RF = []

for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        RF.append(ASE.collum_buckeling_RF(lenghtSTR, I_T_stringer, A_T_str, yieldStrengh, Sigma_crip[i], BbaseEmod, Stringer_sig_avg_LC1[i], A))
    if Stringer_Placemtent[i] == "O":
        RF.append(ASE.collum_buckeling_RF(lenghtSTR, I_O_stringer, A_O_str, yieldStrengh, Sigma_crip[i], BbaseEmod, Stringer_sig_avg_LC1[i], A))
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Column Buckling', 'LC1','RF_columnbuckl_comb [-]', RF)

RF = []
A = shortSide*thickness
for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        RF.append(ASE.collum_buckeling_RF(lenghtSTR, I_T_stringer, A_T_str, yieldStrengh, Sigma_crip[i], BbaseEmod, Stringer_sig_avg_LC3[i], A))
    if Stringer_Placemtent[i] == "O":
        RF.append(ASE.collum_buckeling_RF(lenghtSTR, I_O_stringer, A_O_str, yieldStrengh, Sigma_crip[i], BbaseEmod, Stringer_sig_avg_LC3[i], A))
CSVf.data_entry(locationGeneral_values,'Stability Analysis - Column Buckling', 'LC3','RF_columnbuckl_comb [-]', RF)


#Iyy
Iyy = []
for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        Iyy.append(I_T_stringer)
    if Stringer_Placemtent[i] == "O":
        Iyy.append(I_O_stringer)
CSVf.data_entry_noLC(locationGeneral_values, 'Combined crossection properties for the combined stringer-skin column buckling mode', 'I_comb [mm^4]', Iyy)

#Radius of gyration
r = []
for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        r.append((I_T_stringer/(A_T_str + A))**(1/2))
    if Stringer_Placemtent[i] == "O":
        r.append((I_O_stringer/(A_O_str + A))**(1/2))
CSVf.data_entry_noLC(locationGeneral_values, 'Combined crossection properties for the combined stringer-skin column buckling mode', 'r_gyr [mm]', r)

#lambda
Lambda_list = []
for i in range(0,9):
    if Stringer_Placemtent[i] == "T":
        Lambda_list.append(ASE.Lambda(lenghtSTR, Iyy[i], A + A_T_str))
    if Stringer_Placemtent[i] == "O":
        Lambda_list.append(ASE.Lambda(lenghtSTR, Iyy[i], A + A_O_str))
CSVf.data_entry_noLC(locationGeneral_values, 'Combined crossection properties for the combined stringer-skin column buckling mode', 'lamda [-]', Lambda_list)

#Lambda_crit
Lambda_crit_list = []
for i in range(0,9):
    Lambda_crit_list.append(ASE.Lambda_crit(yieldStrengh, Sigma_crip[i], BbaseEmod))
CSVf.data_entry_noLC(locationGeneral_values, 'Combined crossection properties for the combined stringer-skin column buckling mode', 'lamda_crit [-]', Lambda_crit_list)