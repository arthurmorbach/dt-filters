import numpy as np
import matplotlib.pyplot as plt

# Coefficients of the transfer function with imaginary components
b = [1, -(0.5 + 0.3j)]  # Numerator coefficients
a = [1, -(0.25 - 0.4j), 0.1]  # Denominator coefficients

# Sampling frequency
fs = 1000  # Hz

# Frequencies from -pi to pi (normalized to -Nyquist to Nyquist)
omega = np.linspace(-np.pi, np.pi, 1024)

# Evaluate the transfer function H(z) on the unit circle, where z = exp(j*omega)
H = np.polyval(b, np.exp(-1j * omega)) / np.polyval(a, np.exp(-1j * omega))

# Convert normalized frequencies (omega) to Hz
frequencies = omega * fs / (2 * np.pi)

# Plot magnitude response
plt.subplot(2, 1, 1)
plt.plot(frequencies, 20 * np.log10(np.abs(H)), 'b')
plt.title('Frequency Response of H(z) with Complex Coefficients')
plt.ylabel('Magnitude [dB]')
plt.grid()

# Plot phase response
plt.subplot(2, 1, 2)
angles = np.unwrap(np.angle(H))
plt.plot(frequencies, angles, 'b')
plt.ylabel('Phase [radians]')
plt.xlabel('Frequency [Hz]')
plt.grid()

plt.show()