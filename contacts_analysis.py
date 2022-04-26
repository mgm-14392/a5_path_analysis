import numpy as np
import MDAnalysis as mda
from MDAnalysis.analysis import diffusionmap, align
import matplotlib.pyplot as plt

psf = '/Users/marianagonzmed/Desktop/PATH_analysis/a5-old.psf'
trj = '/Users/marianagonzmed/Desktop/PATH_analysis/trj3.dcd'

u = mda.Universe(psf, trj)
print(u)
aligner = align.AlignTraj(u,u, select='name CA',
                          in_memory=True).run()

matrix = diffusionmap.DistanceMatrix(u, select='name CA').run()
print(matrix.dist_matrix.shape)

plt.imshow(matrix.dist_matrix, cmap='viridis')#, vmin=0, vmax=6)
plt.xlabel('Frame', weight='bold', fontsize=20)
plt.ylabel('Frame', weight='bold', fontsize=20)
plt.colorbar(label='RMSD')
plt.show()


# source  /Users/marianagonzmed/Desktop/PATH_analysis/pdbbfactor.tcl
# pdbbfactor /Users/marianagonzmed/Desktop/PATH_analysis/adk_distance_bfac.pdb