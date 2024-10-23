import matplotlib.pyplot as plt
import numpy as np
import docs.source.filters as filters


file_path = 'docs/gain_LNTA.txt'

frequencies = []
dB_values = []

with open(file_path, 'r') as file:
    for line in file:
        # Skip comment lines
        if line.startswith(';'):
            continue
        # Split the line by comma and convert to float
        try:
            freq, dB = map(float, line.split(','))
            frequencies.append(freq)
            dB_values.append(dB)
        except ValueError:
            # In case of a malformed line, print a message and skip
            print(f"Skipping malformed line: {line.strip()}")
            
# Convert lists to numpy arrays
frequencies_gain = np.array(frequencies, dtype=float)
dB_values_gain = np.array(dB_values, dtype=float)

# Define the frequency range for plotting 
freq_range_min = 2e9
freq_range_max = 3e9 

# Apply the frequency range filter
mask_1 = (frequencies_gain >= freq_range_min) & (frequencies_gain <= freq_range_max)            
            

# Plot magnitude response
plt.figure(1)
plt.subplot(2,2,1)
plt.plot(frequencies_gain[mask_1]/1e9, dB_values_gain[mask_1])
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude (dB)')
plt.title('a)')
plt.grid(True)




file_path = 'docs/s11_LNTA.txt'

frequencies = []
dB_values = []

with open(file_path, 'r') as file:
    for line in file:
        # Skip comment lines
        if line.startswith(';'):
            continue
        # Split the line by comma and convert to float
        try:
            freq, dB = map(float, line.split(','))
            frequencies.append(freq)
            dB_values.append(dB)
        except ValueError:
            # In case of a malformed line, print a message and skip
            print(f"Skipping malformed line: {line.strip()}")
            
# Convert lists to numpy arrays
frequencies_s11 = np.array(frequencies, dtype=float)
dB_values_s11 = np.array(dB_values, dtype=float)


# Plot magnitude response

plt.subplot(2,2,2)
plt.plot(frequencies_s11[mask_1]/1e9, dB_values_s11[mask_1])
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude (dB)')
plt.title('b)')
plt.grid(True)


file_path = 'docs/nf_LNTA.txt'

frequencies = []
dB_values = []

with open(file_path, 'r') as file:
    for line in file:
        # Skip comment lines
        if line.startswith(';'):
            continue
        # Split the line by comma and convert to float
        try:
            freq, dB = map(float, line.split(','))
            frequencies.append(freq)
            dB_values.append(dB)
        except ValueError:
            # In case of a malformed line, print a message and skip
            print(f"Skipping malformed line: {line.strip()}")
            
# Convert lists to numpy arrays
frequencies_nf = np.array(frequencies, dtype=float)
dB_values_nf = np.array(dB_values, dtype=float)


# Plot magnitude response

plt.subplot(2,2,3)
plt.plot(frequencies_nf[mask_1]/1e9, dB_values_nf[mask_1])
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude (dB)')
plt.title('c)')
plt.grid(True)




file_path = 'docs/z11_LNTA.txt'

frequencies = []
res = []

with open(file_path, 'r') as file:
    for line in file:
        # Skip comment lines
        if line.startswith(';'):
            continue
        # Split the line by comma and convert to float
        try:
            freq, re, im = map(float, line.split(','))
            frequencies.append(freq)
            res.append(re)
        except ValueError:
            # In case of a malformed line, print a message and skip
            print(f"Skipping malformed line: {line.strip()}")
            
# Convert lists to numpy arrays
frequencies_z11 = np.array(frequencies, dtype=float)
res = np.array(res, dtype=float)


# Plot magnitude response

plt.subplot(2,2,4)
plt.plot(frequencies_z11[mask_1]/1e9, res[mask_1])
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude (Ohm)')
plt.title('d)')
plt.grid(True)
plt.tight_layout()
plt.show()