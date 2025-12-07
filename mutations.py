from crossover_protein import clean_alignement
from random import choice
from myalign import MyAlign

def pick_random_mutation():
    mutation_pool = {0: add_random_gaps, 1: extend_random_gap, 2: remove_random_gap}
    chosen_mutation = mutation_pool[choice(range(len(mutation_pool)))]
    return chosen_mutation


def add_random_gaps(alignement):
    """
    Adds a random gap to every sequence of the alignement, in different positions

    :param alignement: multiple alignement instance
    """

    aligned_seqs = alignement.get_seqs()
    mutated_seqs =[]
    for seq in aligned_seqs:
        i = choice(range(0,len(seq)+1))
        mutated_seq = seq[:i] + "-" + seq[i:]
        mutated_seqs.append(mutated_seq)

    return clean_alignement(MyAlign(lseqs = mutated_seqs, al_type = "protein"))

def extend_random_gap(alignement):
    """
    Extends a random gap in the sequences of an alignement
    
    :param alignement: multiple alignement instance
    """

    aligned_seqs = alignement.get_seqs()
    mutated_seqs = []
    for seq in aligned_seqs:
#       no need to check for repeated indices
#       thus check pick indice from a pool of only positions with gaps
        gap_indices = [i for i, r in enumerate(seq) if r == "-"]
#       if there are no gaps to extend, add random
        if not gap_indices:
            return add_random_gaps(alignement)
        i = choice(gap_indices)
        mutated_seq = seq[:i] + "-" + seq[i:]
        mutated_seqs.append(mutated_seq)

    return clean_alignement(MyAlign(lseqs = mutated_seqs, al_type = "protein"))
    
def remove_random_gap(alignement):
    """
    Removes a random gap from an alignement
    
    :param alignement: multiple alignement instance
    """
    aligned_seqs = alignement.get_seqs()
    mutated_seqs = []
    for seq in aligned_seqs:
        gap_indices = [i for i, r in enumerate(seq) if r == "-"]
#       only removes a gap if the sequence has gaps
        if not gap_indices:
            return alignement
        i = choice(gap_indices)
#       removes a random gap
        if i == 0:
            mutated_seq = seq[1:]
        elif i == (len(seq) - 1):
            mutated_seq = seq[:i]
        else:
            mutated_seq = seq[:i] + seq[(i+1):]
        mutated_seqs.append(mutated_seq)
    return clean_alignement(MyAlign(lseqs = mutated_seqs, al_type = "protein"))




        
