class SubstMatrix:

    def __init__(self, submat_file, gap_penalty, unknown_score):
        self.alphabet = ""
        self.sm = {}
        self.read_submat_file(submat_file)
        self.gap_penalty = gap_penalty
        self.unknown_score = unknown_score

    def __getitem__(self, ij):
        i, j = ij
        return self.score_pair(i, j)

    def score_pair(self, c1, c2):
        if c1 == c2 == "-":
            return 0 
        if c1 == "-" or c2 == "-":
            return self.gap_penalty
        if c1 == "X" or c2 == "X":
            return self.unknown_score
        if c1 not in self.alphabet or c2 not in self.alphabet:
            return None
        return self.sm[c1][c2]
    
    #def create_submat(self, match, mismatch, alphabet):
        self.sm = {}
        for c1 in alphabet:
            self.sm[c1] = {}
            for c2 in alphabet:
                if (c1 == c2):
                    self.sm[c1][c2] = match
                else:
                    self.sm[c1][c2] = mismatch
    
    def read_submat_file(self, filename):
        self.sm = {}
        with open(filename, 'r') as f:
            matrixfile = f.readlines()

        header = matrixfile[0].split()
        self.alphabet = header
        for line in matrixfile[1:]:
            values = line.split()
            letter = values[0]
            values = values[1:]
            self.sm[letter] = {}
            for i in range(len(header)):
                self.sm[letter][header[i]] = int(values[i])
