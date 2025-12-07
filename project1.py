from Bio import SeqIO
from myalign import MyAlign
from generation import Generation
from copy import deepcopy
from substmatrix import SubstMatrix
from data_export import create_xlsx


def load_seqs(seq_file, format):
    """
    return ids and seqs of the input file
    """
    records = list(SeqIO.parse(seq_file, format))
    ids = []
    seqs = []
    for record in records:
        ids.append(record.id)
        seqs.append(str(record.seq))
    return ids, seqs


POPULATION_SIZE = 100
MAX_PADDING = 5
GAP_PENALTY = -10
UNKNOWN_SCORE = -1
CROSSOVER_PROBABILITY = 0.8
N_GENERATIONS = 100
N_CYCLES = 10
FILENAME = "test_gen_n_100"

#   main 
#first step is to initialize the organisms into a template alignement
input_ids, input_seqs = load_seqs("cytochromes.fa", "fasta")
#create the standard msa for the first generation
standard_msa = MyAlign(lseqs = input_seqs, al_type = "protein")

#create the first generation
submat = SubstMatrix(submat_file = "blosum62.mat", gap_penalty= GAP_PENALTY, unknown_score = UNKNOWN_SCORE)

#store information of all cycles
all_cycles_dict = {}
#repeat for n cycles starting in 1
for i in range(1,N_CYCLES+1):
    #for each cycle the generation must be reset
    gen_1 = Generation(standard_msa, POPULATION_SIZE, MAX_PADDING, submat, CROSSOVER_PROBABILITY)
    gen_1_population = gen_1.get_population()

    #   create the blueprint dictionary for every cycle
    generations_dict = {"gen":[], "max_sp": [], "average_fitness": [],"n_cycles": None,  "runtime": None, "identity_percentage": None}

#   for every cycle do for N_generations
    for _ in range(N_GENERATIONS):
        generations_dict["gen"].append(gen_1.get_current_generation())
        generations_dict["max_sp"].append(gen_1.get_generation_max_SP())
        generations_dict["average_fitness"].append(gen_1.get_generation_average_fitness())

        if gen_1.check_status():
            break
        gen_1.update_generation()
    
    generations_dict["n_cycles"] = gen_1.get_current_generation()
    generations_dict["identity_percentage"] = gen_1.get_fitness_identity_percentage()
    generations_dict["runtime"] = "NA"

    all_cycles_dict[f"cycle{i}"] = generations_dict

create_xlsx(FILENAME, all_cycles_dict)

    








