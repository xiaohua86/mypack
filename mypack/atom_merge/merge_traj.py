from ase.io import read, write
from ase.io import Trajectory

def merge_traj(input_file, output_file='merged.traj',is_print=True):
    
    traj_out = Trajectory(output_file, 'w')
    total = 0
    try:
        for path in input_file:
            with Trajectory(path, 'r') as traj_in:
                for atoms in traj_in:
                    traj_out.write(atoms)
                    total += 1
                    if is_print:
                        if total % 100 == 0:
                            print(f'Written {total} frames...', end='\r')
    finally:
        traj_out.close()
    print(f'Finished writing {total} frames to {output_file}.')
    return total
