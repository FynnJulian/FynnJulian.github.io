import numpy as np
import math

def RFstrenght(ultimateStrenght,Stress):
    RF = abs(ultimateStrenght/(Stress*1.5))
    return RF

#Panel asssume Volumne the same for every component
def sig_avg(StressList, V):
    StressArray = np.array(StressList)
    return ((StressArray*V).sum())/(len(StressArray)*V)

# checks for 10 halfwaves for lowest energy state
def k_shear(longSide, shortSide):
    alpha = longSide/shortSide
    if alpha < 1:
        k_shear = 4 + 5.34/(alpha**2)
    if 1<= alpha:
        k_shear = 5.34 + 4/(alpha**2)
    return k_shear

def k_biax(StressXX, StressYY, longSide, shortSide):
    alpha = longSide/shortSide
    beta = StressYY/StressXX
    kold = abs(((1+alpha**2)**2 /(alpha**2 *(1+beta*alpha**2))))
    for n in range(1,10):
        for m in range(1,10):
            knew = (m**2 + n**2 * alpha**2)**2/(alpha**2 * (m**2 + beta * n**2 * alpha**2))
            if abs(knew) <= abs(kold):
                kold = knew
    return kold

def RF_panelbuckel(avgEmod, PoissonRatio, thickness, shortSide, longSide, StressXX, StressYY, StressXY):
    # Added **2 to the thickness/shortSide ratio
    StressE = (avgEmod*math.pi**2 /(12*(1-PoissonRatio**2))*((thickness/shortSide)**2)) 
    
    # Must call the functions with arguments
    current_k_biax = k_biax(StressXX, StressYY, longSide, shortSide)
    current_k_shear = k_shear(longSide, shortSide)
    
    sig_biax = StressE * current_k_biax
    sig_shear = StressE * current_k_shear
    RF_biax = sig_biax/abs(StressXX*1.5)
    RF_shear = sig_shear/abs(StressXY*1.5)
    inverseRF = 1/RF_biax + (1/RF_shear)**2
    return 1/inverseRF


#Stringer NOT SURE ABOUT THE FORMULA, assume lenght is the same for every part
def sig_axial(StressList,lenghtSTR, A_panel, A, sig_xx):
    sig_comb = []
    for i in range(0, len(StressList)):   
        sig_comb.append((StressList[i]*A + sig_xx[i]*A_panel/2 + sig_xx[i+3]*A_panel/2)/(A+(A_panel)))
    return (sum((sig_comb*lenghtSTR)))/(len(sig_comb)*lenghtSTR)

#T-stringer crippeling
def sig_crip_T(t2Tstr, t1Tstr, a12Tstr, a11Tstr, BbaseEmod, yieldStrengh):
    b11 = a11Tstr - t2Tstr/2 * (0.25*(t2Tstr/t1Tstr))
    print("b11: ", b11)
    b12 = a12Tstr - t1Tstr/2 * (2 - 0.5*(t2Tstr/t1Tstr))
    print("b12: ", b12)

    x11 = b11/t1Tstr *  (yieldStrengh/(0.41*BbaseEmod))**(1/2)
    print("x11: ", x11)
    x12 = b12/t2Tstr *  (yieldStrengh/(0.41*BbaseEmod))**(1/2)
    print("x12: ", x12)

    #if 0.4 <= x11 <= 1.095:
    #    a11 = 1.4 - 0.628*x11
    #if 1.095 < x11 <= 1.633:
    #    a11 = 0.78/x11
    #if 1.633 < x11:
   #     a11 = 0.69/(x11**(3/4))
    #if x11 < 0.4:
    #    a11 = 1.4 - 0.628*x11
    #    print("Warning x11 smaller 0.4. estimating a11")
    
    
    if 0.4 <= x12 <= 1.095:
        a12 = 1.4 - 0.628*x12
    if 1.095 < x12 <= 1.633:
        a12 = 0.78/x12
    if 1.633 < x12:
        a12 = 0.69/(x12**(3/4))
    if x12 < 0.4:
        a12 = 1.4 - 0.628*x12
        print("Warning x12 smaller 0.4. estimating a12")
    a11 = 1  #because the T-stringer is atteched to the skin and a11 can therefor not buckel
    
    sig_crip_T_11 = a11 * yieldStrengh
    print("sig_crip_T_11: ", sig_crip_T_11)
    sig_crip_T_12 = a12 * yieldStrengh
    print("sig_crip_T_12: ", sig_crip_T_12)

    stressavg = (sig_crip_T_11*b11*t1Tstr*2 + sig_crip_T_12*b12*t2Tstr)/(2*b11*t1Tstr + b12*t2Tstr)
    print("stressavg: ", stressavg)

    if stressavg < yieldStrengh:
        Fcrip = (sig_crip_T_11*b11*t1Tstr*2 + sig_crip_T_12*b12*t2Tstr)
    if yieldStrengh <= stressavg:
        Fcrip = yieldStrengh*(b11*t1Tstr*2 + b12*t2Tstr)
    
    sig_crip = Fcrip/(2*a11Tstr*t1Tstr + t2Tstr*(a12Tstr-t1Tstr))

    return sig_crip

#Omega-Stringer crippeling
def sig_crip_O(a1vOstr,ta1vOstr,a2hOstr,ta2hOstr,a11Ostr,ta11Ostr,yieldStrengh,BbaseEmod):
    b2v = a1vOstr - ta1vOstr
    b2h = a2hOstr - ta2hOstr
    b1 = a11Ostr - ta1vOstr/2
    def algorithm(bar_b, bar_t, yieldStrengh, bBaseEmod, Ki):
        x = bar_b/bar_t * (yieldStrengh/(Ki*bBaseEmod))**(1/2)
        if 0.4 <= x <= 1.095:
            a = 1.4 - 0.628*x
        if 1.095 < x <= 1.633:
            a = 0.78/x
        if 1.633 < x:
            a = 0.69/(x**(3/4))
        if x < 0.4:
            a = 1.4 - 0.628*0.4
            print("Warning x smaller 0.4. estimating a")
        sig_crip = a*yieldStrengh
        return sig_crip
    sig_crip_a2v = algorithm(b2v, ta1vOstr, yieldStrengh, BbaseEmod, 3.6)
    sig_crip_a2h = algorithm(b2h, ta2hOstr, yieldStrengh, BbaseEmod, 3.6)
    sig_crip_a11 = algorithm(b1, ta11Ostr, yieldStrengh, BbaseEmod, 0.41)

    Stressavg = (sig_crip_a2v*b2v*ta1vOstr*2 + sig_crip_a2h*b2h*ta2hOstr + sig_crip_a11*ta11Ostr*b1*2)/(b2v*ta1vOstr*2 + b2h*ta2hOstr + ta11Ostr*b1*2)
    if yieldStrengh <= Stressavg:
        Fcrit = yieldStrengh*(b2v*ta1vOstr*2 + b2h*ta2hOstr + ta11Ostr*b1*2)
    if Stressavg < yieldStrengh:
        Fcrit = (sig_crip_a2v*b2v*ta1vOstr*2 + sig_crip_a2h*b2h*ta2hOstr + sig_crip_a11*ta11Ostr*b1*2)
    
    sig_crip = Fcrit/(a2hOstr*ta2hOstr + 2*(a1vOstr-ta2hOstr-ta11Ostr)*ta1vOstr + 2*ta11Ostr*a11Ostr)
    return sig_crip

#Column buckeling
def collum_buckeling_RF(lenghtSTR, I, A, yieldStrengh, sig_crip, BbaseEmod, sig_bar, A_panel):
    L = lenghtSTR
    c = 1
    r = (I/(A+A_panel))**(1/2)
    Lambda = L/r
    if abs(yieldStrengh) < abs(sig_crip):
        sig_cutoff = abs(yieldStrengh)
    else:
        sig_cutoff = abs(sig_crip)
    
    Lambda_crit = ((2*math.pi**2 *BbaseEmod)/sig_cutoff)**(1/2)

    # check slenderness for bucking approch
    if Lambda_crit <= Lambda:
        #Euler
        sig_crit = (math.pi**2 * BbaseEmod / (Lambda**2))
    if Lambda < Lambda_crit:
        #Euler-Johnson
        sig_crit = sig_cutoff - 1/BbaseEmod * (sig_cutoff/(2*math.pi))**2 * Lambda**2
    sig_comb = abs(sig_bar)

    RF = sig_crit/(1.5*sig_comb)
    return RF

#Lambda
def Lambda(lenghtSTR, I, A):
    L = lenghtSTR
    c = 1
    r = (I/A)**(1/2)
    Lambda = L/r
    return Lambda

#Lambda crit
def Lambda_crit(yieldStrengh, sig_crip, BbaseEmod):
    if abs(yieldStrengh) < abs(sig_crip):
        sig_cutoff = abs(yieldStrengh)
    else:
        sig_cutoff = abs(sig_crip)
    
    Lambda_crit = ((2*math.pi**2 *BbaseEmod)/sig_cutoff)**(1/2)
    return Lambda_crit
