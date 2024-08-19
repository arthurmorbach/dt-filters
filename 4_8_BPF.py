import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig


#Variables
Ch = 6.65e-12 
Cr = 500e-15 
k = 1 / (Ch + Cr)
alpha = Ch / (Ch + Cr)

# Coefficients of the transfer function
b = [k]  # Numerator coefficients
a = [1, -2*alpha, (alpha**2) + 2*alpha*1j - 1j - (alpha**2) * 1j]  # Denominator coefficients

# Sampling frequency
fs = 600e6 # Hz

# Frequencies from -pi to pi (normalized to -Nyquist to Nyquist)
omega = np.linspace(-np.pi, np.pi, 1024)

# Convert normalized frequencies (omega) to Hz
frequencies = omega * fs / (2 * np.pi)

#Theoretical input impedance
Zo = 1 / (Cr * fs)
print('Zo = ', Zo)
#Theoretical cut frequency
fc = (fs / (2 * np.pi)) * np.arctan(((1 - alpha) * np.sin(np.pi / 4)) / (alpha + (1 - alpha) * np.cos(np.pi / 4)))
print('Fc = ', fc/1e6, ' MHz')
print('arctan(Cr / Ch) = ', np.arctan(Cr / Ch))
print('fs / (2 * np.pi) = ', fs / (2 * np.pi))

# Evaluate the transfer function H(z) on the unit circle, where z = exp(j*omega)
z = np.exp(1j * omega)
H = np.polyval(b, z) / np.polyval(a, z)

# Normalize 
H = H / np.max(np.abs(H))

# Define the frequency range for plotting 
freq_range_min = -50e6
freq_range_max = 50e6  

# Apply the frequency range filter
mask = (frequencies >= freq_range_min) & (frequencies <= freq_range_max)

# Unit circle in the complex plane
unit_circle = np.exp(1j * omega)

# Plot the unit circle
plt.figure(1)
plt.plot(np.real(unit_circle), np.imag(unit_circle), 'r--', label='Unit Circle')
# Plot H(z) on the complex plane
plt.plot(np.real(H), np.imag(H), 'b', label='H(z) on Unit Circle')
plt.title('H(z) on the Unit Circle (Complex Plane)')
plt.xlabel('Real Part')
plt.ylabel('Imaginary Part')
plt.grid()
plt.axis('equal')  # Equal scaling on both axes
plt.legend()
plt.show()

# Plot magnitude response
plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(frequencies[mask]/1e6, 20 * np.log10(np.abs(H[mask])), 'b')
plt.title('Frequency Response 4/8 BPF')
plt.ylabel('Magnitude [dB]')
plt.grid()

# Plot phase response
plt.subplot(2, 1, 2)
angles = np.unwrap(np.angle(H))
plt.plot(frequencies/1e6, angles, 'b')
plt.ylabel('Phase [radians]')
plt.xlabel('Frequency [MHz]')
plt.grid()
plt.tight_layout()
plt.show()