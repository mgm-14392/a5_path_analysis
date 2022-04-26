# project a dynamic property on the structure using the B-factor (tempfactor) field

import numpy as np
import MDAnalysis.analysis.align

psf = '/Users/marianagonzmed/Desktop/PATH_analysis/a5-old.psf'
trj = '/Users/marianagonzmed/Desktop/PATH_analysis/trj3.dcd'

u = MDAnalysis.Universe(psf, trj)
ref = MDAnalysis.Universe(psf, trj)  # copy of u

CORE_selection = "protein"
pdbtrj = "/Users/marianagonzmed/Desktop/PATH_analysis/closedtrj3_distance_bfac.pdb"

# dynamically add new attributes
# ('tempfactors' is pre-defined and filled with zeros as default values)
u.add_TopologyAttr('tempfactors')


with MDAnalysis.Writer(pdbtrj, multiframe=True, bonds=None, n_atoms=u.atoms.n_atoms) as PDB:
    # reference coordinates: set to first frame
    ref.trajectory[2]
    # iterate through our trajectory
    for ts in u.trajectory:
        # superimpose on the reference CORE (at t=0)
        rmsd = MDAnalysis.analysis.align.alignto(u.atoms, ref.atoms, select=CORE_selection)
        distances = np.sqrt(np.sum((u.atoms.positions - ref.atoms.positions)**2, axis=1))
        # project displacement on structure via bfactor ("tempfactor") field
        u.atoms.tempfactors = distances
        PDB.write(u.atoms)
        print("Frame {0}: CORE RMSD before/after superposition: {1[0]:.1f} / {1[1]:.1f} A. "
              "min-max displacement: {2:.1f}...{3:.1f} A".format(ts.frame, rmsd, distances.min(), distances.max()))

print("Wrote PDB trajectory {0} with distances in bfactor field".format(pdbtrj))