print("====================================================================")
print("   This Script is created by Md. Tanvir Ahmed")
print("   TEAMS Lab, Dept. of Physics, PUST")
print("   GW band gap")
print("====================================================================\n")

k_gaps_dict = {}   # use dict to avoid duplicates

# Global (indirect)
vbm_global = -1e10
cbm_global = 1e10
vbm_k_global = None
cbm_k_global = None

# Local
vbm_k_local = -1e10
cbm_k_local = 1e10

current_k = None
read_band = False


def is_valid_k(kx, ky, kz):
    return (0.0 <= kx <= 1.0) and (0.0 <= ky <= 1.0) and (0.0 <= kz <= 1.0)


with open("OUTCAR", "r") as f:
    for line in f:

        # ---- Detect k-point ----
        if "k-point" in line and ":" in line:
            parts = line.split()
            try:
                kx = float(parts[-3])
                ky = float(parts[-2])
                kz = float(parts[-1])

                # Skip fake k-points immediately
                if not is_valid_k(kx, ky, kz):
                    current_k = None
                    read_band = False
                    continue

                # Save previous k-point
                if current_k is not None:
                    if vbm_k_local > -1e9 and cbm_k_local < 1e9:
                        gap_k = cbm_k_local - vbm_k_local
                        k_gaps_dict[current_k] = gap_k   # overwrite duplicates

                # Reset
                current_k = (kx, ky, kz)
                vbm_k_local = -1e10
                cbm_k_local = 1e10
                read_band = False

            except:
                continue

        # ---- Detect band table ----
        if "band No." in line:
            read_band = True
            continue

        # ---- Read data ----
        if read_band and current_k is not None:
            parts = line.split()

            if len(parts) < 8:
                continue
            if not parts[0].isdigit():
                continue

            try:
                qp = float(parts[2])
                occ = float(parts[-2])

                # LOCAL
                if occ > 1.5:
                    if qp > vbm_k_local:
                        vbm_k_local = qp

                elif occ < 0.5:
                    if qp < cbm_k_local:
                        cbm_k_local = qp

                # GLOBAL
                if occ > 1.5:
                    if qp > vbm_global:
                        vbm_global = qp
                        vbm_k_global = current_k

                elif occ < 0.5:
                    if qp < cbm_global:
                        cbm_global = qp
                        cbm_k_global = current_k

            except:
                continue


# Save last k-point
if current_k is not None:
    if vbm_k_local > -1e9 and cbm_k_local < 1e9:
        gap_k = cbm_k_local - vbm_k_local
        k_gaps_dict[current_k] = gap_k


# Convert to list
k_gaps = list(k_gaps_dict.items())

# ===== OUTPUT =====
print("\n===== DIRECT GAPS (clean) =====")
for k, g in k_gaps:
    print(f"k = {k}, Eg_direct = {g:.6f} eV")

# Minimum direct gap
min_gap = min(k_gaps, key=lambda x: x[1])

print("\n===== MINIMUM DIRECT GAP =====")
print(f"k = {min_gap[0]}")
print(f"Eg_direct(min) = {min_gap[1]:.6f} eV")

# Indirect gap
indirect_gap = cbm_global - vbm_global

print("\n===== INDIRECT GW GAP =====")
print(f"VBM = {vbm_global:.6f} eV at k = {vbm_k_global}")
print(f"CBM = {cbm_global:.6f} eV at k = {cbm_k_global}")
print(f"Eg_indirect = {indirect_gap:.6f} eV")

if vbm_k_global == cbm_k_global:
    print("Gap Type: DIRECT")
else:
    print("Gap Type: INDIRECT")
    
    
    # ================= SAVE OUTPUT =================

with open("GW_results.dat", "w") as f:

    f.write("====================================================================\n")
    f.write("   GW BAND GAP ANALYSIS\n")
    f.write("   Created by Md. Tanvir Ahmed\n")
    f.write("   TEAMS Lab, Dept. of Physics, PUST\n")
    f.write("====================================================================\n\n")

    f.write("===== DIRECT GAPS (per k-point) =====\n")
    f.write("# kx   ky   kz   Eg_direct (eV)\n")

    for k, g in k_gaps:
        f.write(f"{k[0]:.4f}  {k[1]:.4f}  {k[2]:.4f}  {g:.6f}\n")

    f.write("\n===== MINIMUM DIRECT GAP =====\n")
    f.write(f"k = {min_gap[0]}\n")
    f.write(f"Eg_direct(min) = {min_gap[1]:.6f} eV\n")

    f.write("\n===== INDIRECT GW GAP =====\n")
    f.write(f"VBM = {vbm_global:.6f} eV at k = {vbm_k_global}\n")
    f.write(f"CBM = {cbm_global:.6f} eV at k = {cbm_k_global}\n")
    f.write(f"Eg_indirect = {indirect_gap:.6f} eV\n")

    if vbm_k_global == cbm_k_global:
        f.write("Gap Type: DIRECT\n")
    else:
        f.write("Gap Type: INDIRECT\n")
