import numpy as np
def Rseriell(Zload):
    Rseriell = np.linspace(0,100,100)

    Z = np.zeros( (len(Rseriell), len(Zload)), dtype=np.complex )
    for i in range(len(Rseriell)):
        Z[i,] = Zload + Rseriell[i]

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('Rseriell.dat', result/50.)

def Lseriell(Zload):
    Lseriell = 1j*np.linspace(0,15,100)

    Z = np.zeros( (len(Lseriell), len(Zload)), dtype=np.complex )
    for i in range(len(Lseriell)):
        Z[i,] = Zload + Lseriell[i]

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('Lseriell.dat', result/50.)

def Cseriell(Zload):
    Cseriell = -1j*np.linspace(0,15,100)

    Z = np.zeros( (len(Cseriell), len(Zload)), dtype=np.complex )
    for i in range(len(Cseriell)):
        Z[i,] = Zload + Cseriell[i]

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('Cseriell.dat', result/50.)

def Rparallel(Zload):
    Rparallel = np.linspace(1000,20,100)

    Z = np.zeros( (len(Rparallel), len(Zload)), dtype=np.complex )
    for i in range(len(Rparallel)):
        Z[i,] = 1/(1/Zload + 1/Rparallel[i])

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('Rparallel.dat', result/50.)

def Lparallel(Zload):
    Lparallel = 1j*np.linspace(5000,150,100)

    Z = np.zeros( (len(Lparallel), len(Zload)), dtype=np.complex )
    for i in range(len(Lparallel)):
        Z[i,] = 1/(1/Zload + 1/Lparallel[i])

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('Lparallel.dat', result/50.)

def Cparallel(Zload):
    Cparallel = -1j*np.linspace(5000,150,100)

    Z = np.zeros( (len(Cparallel), len(Zload)), dtype=np.complex )
    for i in range(len(Cparallel)):
        Z[i,] = 1/(1/Zload + 1/Cparallel[i])

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('Cparallel.dat', result/50.)

def TL(ZL, Z0 = 50):
    length = np.linspace(0,0.4999*np.pi,25)
    Z = np.zeros( (len(length), len(ZL)), dtype=np.complex )
    for i in range(len(length)):
        b = length[i]
        Z[i,] = Z0*(ZL+1j*Z0*np.tan(b))/(Z0+1j*ZL*np.tan(b))

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('TL%s.dat' % Z0, result/50)

def LTL(ZL):
    length = np.linspace(0,5*np.pi,100)
    Z0=50
    Z = np.zeros( (len(length), len(ZL)), dtype=np.complex )
    att = 0.05+0.9j
    for i in range(len(length)):
        b = length[i]
        Z[i,] = Z0*(ZL+Z0*np.tanh(att*b))/(Z0+ZL*np.tanh(att*b))

    result = np.zeros((Z.shape[0], 2*Z.shape[1]))
    result[:,0::2] = np.real(Z)
    result[:,1::2] = np.imag(Z)
    np.savetxt('LTL.dat', result/50)

Rseriell( np.array((50, 10+10j, 10-25j, 50+50j, 50-50j)) )
Lseriell( np.array((50, 10+15j, 10-25j, 50+50j, 50-50j, 100-35j, 100+35j)) )
Cseriell( np.array((50, 10+15j, 10-25j, 50+50j, 50-50j, 100-35j, 100+35j)) )

Rparallel( np.array((50, 10+5j, 10-20j, 50+50j, 50-50j)) )
Lparallel( np.array((50, 20-10j, 10, 50+50j, 50-50j, 250-35j, 20+10j)) )
Cparallel( np.array((50, 20-10j, 10, 50+50j, 50-50j, 250-35j, 20+10j)) )

TL( np.array((200,)), 100 )
TL( np.array((0, 10, 50-50j, 1000+30j, 50+10j)) )
LTL( np.array((10,)))
