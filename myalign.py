from random import choice

class MyAlign:
    def __init__(self, lseqs, al_type = "protein"):
        self.listseqs = lseqs
        self.al_type = al_type

    def __len__(self): # number of columns
        return len(self.listseqs[0])

    def __getitem__(self, n):
        # if n is a tuple of two numbers,
        # interpret the first one as the seq index and the second as the column
        if type(n) is tuple and len(n) == 2:
            i, j = n
            return self.listseqs[i][j]
        # otherwise return the sequence of that index
        elif type(n) is int: return self.listseqs[n]
        return None

    def __str__(self):
        res = ""
        for seq in self.listseqs:
            res += "\n" + seq
        return res

    def num_seqs(self):
        return len(self.listseqs)

    def column(self, indice):
        res = []
        for k in range(len(self.listseqs)):
            res.append(self.listseqs[k][indice])
        return res
    
    def get_seqs(self):
        return self.listseqs
    
    def add_variability(self, pad_limit):
        """
        Adds random padding to each of the sequences present in the alignement
        Fixes different lengths by padding the end ofthe sequences so that all have the same length
        """
        max_length = -1
        padded_seqs = []
        
        for seq in self.get_seqs():
            pads = "-" * choice(range(0,pad_limit+1))
            new_seq =  pads + seq
            if len(new_seq) > max_length:
                max_length = len(new_seq)
            padded_seqs.append(new_seq)

        final_seqs = []
        
        for seq in padded_seqs:
            new_seq = seq + ("-" * (max_length - len(seq)))
            final_seqs.append(new_seq)
            
        self.listseqs = final_seqs 

    def get_score(self, submat):
        all_pairs = []
        total_sum = 0
        
        for i in range(len(self.listseqs)):
            for j in range(i + 1, len(self.listseqs)):
                all_pairs.append((i, j))
        for i in range(len(self.listseqs[0])):
            for pair in all_pairs:
                seq_1 = self.get_seqs()[pair[0]] 
                seq_2 = self.get_seqs()[pair[1]]
                total_sum += submat[seq_1[i], seq_2[i]]
        return total_sum




            
        
        
        
