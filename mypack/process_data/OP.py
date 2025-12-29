import numpy as np
from scipy.special import sph_harm_y
from ase.io import read

def steinhardt_op(atoms, idx=144, l=4, cutoff=5.0, wrap=False):
    """
    快速计算单个原子 idx 的 Steinhardt q_l（严格 cutoff，PBC 用最小像）。
    - 仅适合“单原子/少数原子”场景；若要全体系每原子，NeighborList/neighbor_list 更合适。
    - wrap=False：不强制 wrap 坐标；通常不影响最小像计算。
    """
    if wrap and np.any(atoms.get_pbc()):
        atoms = atoms.copy()
        atoms.wrap()

    n = len(atoms)
    if idx < 0:
        idx += n
    if idx < 0 or idx >= n:
        raise IndexError("atom index out of range")

    cell = atoms.get_cell().array
    pbc = atoms.get_pbc()

    # ---- 计算 idx 到所有原子的最小像位移向量 vecs (N,3) ----
    if np.any(pbc):
        # 用分数坐标做最小像：ds -= round(ds)（只在 pbc 方向上）
        s = atoms.get_scaled_positions(wrap=False)
        ds = s - s[idx]                       # (N,3)
        ds[:, pbc] -= np.round(ds[:, pbc])    # MIC in fractional
        vecs = ds @ cell                      # fractional -> cartesian
    else:
        pos = atoms.get_positions()
        vecs = pos - pos[idx]

    # 距离筛选（严格 cutoff），并排除自身
    r2 = np.einsum("ij,ij->i", vecs, vecs)
    mask = (r2 > 1e-24) & (r2 <= cutoff * cutoff)
    vecs = vecs[mask]
    if vecs.shape[0] == 0:
        return 0.0

    r = np.sqrt(np.einsum("ij,ij->i", vecs, vecs))
    cos_theta = np.clip(vecs[:, 2] / r, -1.0, 1.0)
    theta = np.arccos(cos_theta)
    phi = np.arctan2(vecs[:, 1], vecs[:, 0])

    # 计算 q_lm 并合成 q_l（l 很小，m 循环开销可忽略）
    qlm = np.empty(2 * l + 1, dtype=complex)
    for mi, m in enumerate(range(-l, l + 1)):
        qlm[mi] = np.mean(sph_harm_y(l, m, theta, phi))

    pref = 4.0 * np.pi / (2 * l + 1)
    ql = np.sqrt(pref * np.sum(np.abs(qlm) ** 2))
    return float(ql)