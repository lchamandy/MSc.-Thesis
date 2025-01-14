import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from fractions import Fraction
import pickle
import os
import subprocess

current_directory = str(os.getcwd())
print('code works!')
#conversion factors
pc_kpc = 1e3		#number of pc in one kpc
cm_km = 1e5		#number of cm in one km
s_day = 24*3600		#number of seconds in one day
s_min = 60		#number of seconds in one hour
s_hr = 3600		#number of seconds in one hour
cm_Rsun = 6.957e10	#solar radius in cm
g_Msun = 1.989e33	#solar mass in g
cgs_G = 6.674e-8 
cms_c = 2.998e10
g_mH = 1.6736e-24
g_me = 9.10938e-28
cgs_h = 6.626e-27
deg_rad = 180e0/np.pi
arcmin_deg = 60e0
arcsec_deg = 3600e0
kpc_cm = 3.086e+21  #number of ccentimeters in one parsec
Myr_s = 1e+6*(365*24*60*60) #megayears to seconds

#reading the parameter file
with open('parameter_file.txt') as f:
    lines = [line.rstrip() for line in f]

def p(i):
    try:
        return np.float64(lines[i].split('=')[-1])
    except ValueError:
        num, denom = lines[i].split('=')[-1].split('/')
        return np.float64(num) / np.float64(denom)
 

#data extraction for galaxy
os.chdir(current_directory +'\data')

subprocess.run(["python", "data_conv_M31.py", str(int(p(5)))])

with open('data_m31.pickle', 'rb') as f:
     data = pickle.load(f)

kpc_r, dat_sigmatot, dat_sigma, dat_q, dat_omega, dat_sigmasfr, molfrac = data

r = kpc_r.size #common radius of the interpolated data

dat_sigma = p(9)*dat_sigma

T_tb = 0.017*kpc_r*1e+4

if bool(p(6)):
    dat_sigma = dat_sigma*(1/(1-molfrac))

ks_exp = 1.4
ks_const = (dat_sigmasfr/(dat_sigma)**(ks_exp)).mean()

if bool(p(7)):
    if bool(p(8)):
        dat_sigma = (dat_sigmasfr/ks_const)**(1/ks_exp)
    else:
        dat_sigmasfr = ks_const*(dat_sigma)**(ks_exp)

os.chdir(current_directory)


zet = p(0)*np.ones(r)
psi = p(1)*np.ones(r)
b = p(2)*np.ones(r)

T = T_tb#1e+4*np.ones(r)
ca = p(3)*np.ones(r)
rk = p(4)*np.ones(r)
mu = p(9)*np.ones(r)

data_pass = list(zip(dat_sigmatot, dat_sigma, dat_sigmasfr, dat_q, dat_omega, zet, T, psi, b, ca, rk, mu))
os.chdir(current_directory +'\data')

with open('zip_data.pickle', 'wb') as f:
    pickle.dump(data_pass, f)