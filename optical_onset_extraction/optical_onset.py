import numpy as np
import pandas as pd
import re
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

print("====================================================================")
print("   Optical Onset Extraction from BSE Spectrum")
print("   Created by Md. Tanvir Ahmed")
print("====================================================================\n")

# ================= READ FILE =================
text = Path('ABSORPTION.dat').read_text().splitlines()

rows = []

for line in text:

    s = line.strip()

    if not s or s.startswith('#'):
        continue

    nums = re.findall(
        r'[-+]?(?:\d*\.\d+|\d+\.?(?:\d*)?)(?:[Ee][-+]?\d+)?',
        s
    )

    if len(nums) >= 7:
        rows.append([float(x) for x in nums[:7]])

df = pd.DataFrame(
    rows,
    columns=['E', 'XX', 'YY', 'ZZ', 'XY', 'YZ', 'XZ']
)

# ================= IN-PLANE ABSORPTION =================
E = df['E'].to_numpy()

# In-plane averaged absorption
A_raw = ((df['XX'] + df['YY']) / 2).to_numpy()

# Slight smoothing for stable fitting
A = gaussian_filter1d(A_raw, sigma=1)

# ================= PARAMETERS =================
threshold = 0.02      # onset threshold (2%)
window = 6            # fitting window size

# ================= BASIC INFO =================
maxA = A.max()

# ================= FIND FIRST BRIGHT PEAK =================
peaks = []

for i in range(1, len(A)-1):

    if A[i] >= A[i-1] and A[i] > A[i+1]:
        peaks.append(i)

# fallback
peak_i = peaks[0] if peaks else np.argmax(A)

E_peak = E[peak_i]

# ================= FIND ONSET REGION =================
mask = A > threshold * maxA

if not np.any(mask):
    raise ValueError("No absorption onset detected.")

start = np.argmax(mask)

# Restrict fitting BEFORE first peak
end = min(peak_i, len(A) - window)

if end <= start:
    end = start + window

# ================= FIND BEST LINEAR FIT =================
best = None

for i in range(start, end):

    x = E[i:i+window]
    y = A[i:i+window]

    if len(x) < window:
        continue

    # Linear fit
    m, b = np.polyfit(x, y, 1)

    if m <= 0:
        continue

    # Fit quality
    yfit = m * x + b

    ss_res = np.sum((y - yfit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

    score = r2

    if best is None or score > best[0]:
        best = (score, m, b, i, r2)

# ================= FALLBACK =================
if best is None:

    print("WARNING: Using derivative fallback.")

    idx = np.argmax(np.gradient(A, E))

    m = np.gradient(A, E)[idx]
    b = A[idx] - m * E[idx]

    fit_start = idx
    r2 = 0.0

else:

    _, m, b, fit_start, r2 = best

# ================= OPTICAL ONSET =================
E_onset = -b / m

# ================= OUTPUT =================
print(f"Optical onset gap  = {E_onset:.4f} eV")
print(f"First bright peak  = {E_peak:.4f} eV")
print(f"Best fit R^2       = {r2:.6f}")
print(f"Maximum absorption = {maxA:.4f}")

# ================= SAVE RESULTS =================
out = Path("output")
out.mkdir(exist_ok=True)

results = pd.DataFrame([
    ["optical_onset_eV", E_onset],
    ["first_peak_eV", E_peak],
    ["best_fit_R2", r2],
    ["max_absorption", maxA]
])

results.to_csv(
    out / "optical_gap_results.dat",
    index=False,
    header=False
)

# ================= PLOT =================
plt.figure(figsize=(6,4))

# Absorption spectrum
plt.plot(E, A, lw=2, label="BSE absorption")

# Linear fitting region
x_fit = E[fit_start:fit_start+window]
y_fit = m * x_fit + b

plt.plot(
    x_fit,
    y_fit,
    'r--',
    lw=2,
    label="Linear fit"
)

# Optical onset
plt.axvline(
    E_onset,
    color='k',
    linestyle=':',
    label=f"Onset = {E_onset:.2f} eV"
)

# First bright peak
plt.axvline(
    E_peak,
    color='blue',
    linestyle='--',
    label=f"Peak = {E_peak:.2f} eV"
)

plt.xlabel("Energy (eV)")
plt.ylabel("Absorption")

plt.legend()
plt.tight_layout()

# ================= SAVE FIGURE =================
plt.savefig("optical_gap_plot.png", dpi=300)
plt.savefig(out / "optical_gap_plot.png", dpi=300)

plt.show()
