import numpy as np

def BPF44(Ch, Cr, fs):
    k = 1 / (Ch + Cr)
    alpha = Ch / (Ch + Cr)

    # Coefficients of the transfer function
    b = [k]  # Numerator coefficients
    a = [1, -1*(alpha + 1j - alpha*1j)]  # Denominator coefficients

    # Frequencies from -pi to pi (normalized to -Nyquist to Nyquist)
    omega = np.linspace(-np.pi, np.pi, 8192)

    z = np.exp(1j * omega)
    H = np.polyval(b, z) / np.polyval(a, z)

    # Normalize 
    H = H / np.max(np.abs(H))
    
    Zo = 1 / (Cr * fs)
    fc = (fs / (2 * np.pi)) * np.arctan(Cr / Ch)
    print('4/4 BPF--------------------------------')
    print('Zo = ', Zo)
    print('Fc = ', fc/1e6, ' MHz')
    print('arctan(Cr / Ch) = ', np.arctan(Cr / Ch))
    print('fs / (2 * np.pi) = ', fs / (2 * np.pi))

    return(H, omega, Zo, fc)


def BPF48(Ch, Cr, fs):
    k = 1 / (Ch + Cr)
    alpha = Ch / (Ch + Cr)

    # Coefficients of the transfer function
    b = [k]  # Numerator coefficients
    a = [1, -2*alpha, (alpha**2) + 2*alpha*1j - 1j - (alpha**2) * 1j]  # Denominator coefficients

    # Frequencies from -pi to pi (normalized to -Nyquist to Nyquist)
    omega = np.linspace(-np.pi, np.pi, 1024)
    z = np.exp(1j * omega)
    H = np.polyval(b, z) / np.polyval(a, z)

    # Normalize 
    H = H / np.max(np.abs(H))

    Zo = 1 / (Cr * fs)
    fc = (fs / (2 * np.pi)) * np.arctan(((1 - alpha) * np.sin(np.pi / 4)) / (alpha + (1 - alpha) * np.cos(np.pi / 4)))
    print('4/8 BPF--------------------------------')
    print('Zo = ', Zo)
    print('Fc = ', fc/1e6, ' MHz')
    print('arctan((1 - alpha)sin(pi/4)) / alpha + (1 - alpha)cos(pi/4) = ', np.arctan(((1 - alpha) * np.sin(np.pi / 4)) / (alpha + (1 - alpha) * np.cos(np.pi / 4))))
    print('fs / (2 * np.pi) = ', fs / (2 * np.pi))
    
    return(H, omega, Zo, fc)


def BPF48CC(Ch, Cr, fs, beta):
    k = 1 / (Ch + Cr)
    alpha = Ch / (Ch + Cr)

    # Coefficients of the transfer function
    b = [0, k*(1-alpha)]  # Numerator coefficients
    a = [1 + beta - alpha*beta, beta*alpha**2 - 2*alpha - alpha*beta, alpha**2 + 2*alpha*1j - 1j - 1j*alpha**2]  # Denominator coefficients

    # Frequencies from -pi to pi (normalized to -Nyquist to Nyquist)
    omega = np.linspace(-np.pi, np.pi, 16384)
    z = np.exp(1j * omega)
    H = np.polyval(b, z) / np.polyval(a, z)
    
    # Normalize 
    H = H / np.max(np.abs(H))
    
    print('4/8 BPF CC--------------------------------')
    print('Zo = Add eq')
    print('Fc = add eq')
    
    return(H, omega)








