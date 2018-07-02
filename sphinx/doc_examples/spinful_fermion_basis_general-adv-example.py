from __future__ import print_function, division
#
import sys,os
quspin_path = os.path.join(os.getcwd(),"../../")
sys.path.insert(0,quspin_path)
#
from quspin.operators import hamiltonian # operators
from quspin.basis import spinful_fermion_basis_general # spin basis constructor
import numpy as np # general math functions
#
###### define model parameters ######
Lx, Ly = 4, 4 # linear dimension of spin 1 2d lattice
N_2d = Lx*Ly # number of sites for spin 1
#
J=1.0 # hopping matrix element
U=2.0 # onsite interaction
mu=0.5 # chemical potential
#
###### setting up user-defined BASIC symmetry transformations for 2d lattice ######
# we build the advanced symmetry operations operations by concatenating operations for a single spin species
x = np.arange(N_2d)%Lx # x positions for sites for one spin species
y = np.arange(N_2d)//Lx # y positions for sites for one spin species
t_x = (x+1)%Lx + Lx*y # translation along x-direction for one spin species
t_y = x + Lx*((y+1)%Ly) # translation along y-direction for one spin species
# create the spin-up spin-down combined transformations
s = np.arange(2*N_2d) # sites [0,1,2,...,N_2d-1,...,2*N_2d-1] in advanced notation
T_x = np.hstack((t_x,t_x+N_2d)) # translation along x-direction for both spin species
T_y = np.hstack((t_y,t_y+N_2d)) # translation along y-direction for both spin species
S = np.roll(s,N_2d) # fermion spin inversion in the advanced case
#
###### setting up bases ###### (note optional argument simple_symm=False)
basis_2d=spinful_fermion_basis_general(N_2d,simple_symm=False,Nf=(2,2),kxblock=(T_x,0),kyblock=(T_y,0),sblock=(S,0)) 
#
###### setting up hamiltonian ######
# setting up site-coupling lists for advanced case
hopping_left =[[-J,i,T_x[i]] for i in range(2*N_2d)] + [[-J,i,T_y[i]] for i in range(2*N_2d)]
hopping_right=[[+J,i,T_x[i]] for i in range(2*N_2d)] + [[+J,i,T_y[i]] for i in range(2*N_2d)]
potential=[[-mu,i] for i in range(2*N_2d)]
interaction=[[U,i,i+N_2d] for i in range(N_2d)]
#
static=[["+-",hopping_left], # spin-up and spin-down hop to left
		["-+",hopping_right], # spin-up and spin-down hop to right
		["n",potential], # onsite potential for spin-up and spin-down
		["nn",interaction]] # spin-up spin-down interaction
# build hamiltonian
H=hamiltonian(static,[],basis=basis_2d,dtype=np.float64)
# diagonalise H
E=H.eigvalsh()