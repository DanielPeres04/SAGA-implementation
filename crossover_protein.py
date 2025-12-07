from myalign import MyAlign

#goal -> generate oddspring from two parents (which are 2 MSA)
#input: MSA1, MSA2, and position to split (ex: 3 wil break between the 3rd and 4th residue)

#auxiliary functions

def count_residues(line):
    #how many residues in a sequence from a MSA line
    count = 0
    for n in line:
        if n in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y", "Z"]:
            count += 1
    return count

def index_at_residue(line, count):
     #how many positions in line are needed for count == count
    for i in range(len(line)):
        window = line[0:i]
        if count_residues(window) == count:
            return i


def split_at(alignement, pos_list):
    #breaks the lines in defined positions of a single MSA, and counts the nucleotides in the first break
    #outputs - left break, right break and nucleotides in lbreak
    r = []
    l = []
    res = []
    for i, pos in enumerate(pos_list):
        #print(pos)
        left_block = alignement[i][:(pos)]
        right_block = alignement[i][(pos):]
        l.append(left_block)
        r.append(right_block)
        res.append(count_residues(left_block))
        #print(res)
    return MyAlign(l, "protein"), MyAlign(r, "protein"), res


def residues_to_indexes(alignement, residues):
    #takes as input an MSA2 and the residues of another alignement, MSA1
    #outputs the positions in MSA2 to break in order to get the same number of residues left break, as in the residues input
    ind = []
    for i, res in enumerate(residues):
        ind.append(index_at_residue(alignement[i], res))
    #print(ind)
    return ind

def pad_alignement(block, direction):
    #pads the left break at the end, and the right break in the beginning
    block_lines = block.get_seqs()
    max_len = max([len(line) for line in block_lines])
    pad_block = []
    if direction == "l":
        for line in block_lines:
            padded_line = line + "-" * (max_len - len(line))
            pad_block.append(padded_line)
    elif direction == "r":
        for line in block_lines:
            padded_line = "-" * (max_len - len(line)) + line
            pad_block.append(padded_line)
    else:
        raise NameError("Unknown direction")
    return MyAlign(pad_block, "protein")

def merge(block1, block2):
    #joins two alignement blooxks together into a single alignement block
    left_lines = block1.get_seqs()
    right_lines = block2.get_seqs()
    merged_alignement = []
    for i in range(len(left_lines)):
        merged_alignement.append(left_lines[i]+right_lines[i])
    #print(merged_alignement)
    return MyAlign(merged_alignement, "protein")

def is_all_gaps(alignement, column):
    column_residues = alignement.column(column)
    return column_residues.count("-") == alignement.num_seqs()

def clean_alignement(alignement):
    lines = alignement.get_seqs()
    cleaned_a = [""]*len(lines)
    #print(alignement)
    for i in range(len(alignement)):
        #print(i)
        if is_all_gaps(alignement, i):
            continue
        else:
            for j, line in enumerate(lines):
                cleaned_a[j] += line[i]
    return  MyAlign(cleaned_a, "protein")

def get_offspring(alignement1, alignement2, break_positions_1):

    #print(alignement1)
    #print(alignement2)
    l1, r1, residues1 = split_at(alignement1, break_positions_1)
    #print(l1,r1)
    break_positions_2 = residues_to_indexes(alignement2, residues1)
    l2, r2, _ = split_at(alignement2, break_positions_2)
    pad_l2 = pad_alignement(l2, "l")
    pad_r2 = pad_alignement(r2, "r")
    l1r2 = merge(l1, pad_r2)
    #print(l1r2)
    l2r1 = merge(pad_l2, r1)
    #print(l2r1)
    clean_l1r2 = clean_alignement(l1r2)
    #print(clean_l1r2)
    clean_l2r1 = clean_alignement(l2r1)
    #print(clean_l2r1)

    return(clean_l1r2, clean_l2r1)







#then do split_at using the positions outputed by residues_indexes

#The first MSA is split into recatangles, since the pre_defined positions for cutting on all lines are all the same
#So after the second MSA is cut using the indexes obtained through the residues_to_indexes, the left and the right blocks probably won't be rectangles
#To fix this, we use a function to 

#then we merge
    #merge - join left padded with right unpadded and left unpadded with right padded
        #l2r1 = merge(l1, r2pad)
    #is_all_gaps - checks if a collumn is just all gaps (True if all gaps)
    #clean_alignement - first records all positions of collumns that aren't all gaps
        #then, outputs the new MSA that has no collumns with just gaps

def main():

    MSA1 = MyAlign(["ATC-G-G-TT","A-CCGC-ATC","A-CCG--ATC"],"dna")
    MSA2 = MyAlign(["ATCGG---TT","AC-CGCA-TC","A---CCGATC"],"dna")
    child1, child2 = get_offspring(MSA1, MSA2, [3,3,3])
    #print(child1)
    #print(child2)



if __name__ == "__main__":
    main()