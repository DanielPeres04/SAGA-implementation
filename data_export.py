import xlsxwriter

#script to initialize the xlsx file

#a xlsx file can be created with any name
#it stores for each cycle (generation) the current generation, the current max SP score and the average fitness score
#this data can then be used for experimental testing
#it also stores information of the total number of cycles, run time and percentage of MSA identity after termination

def create_xlsx(filename, exp_dict=None):
    """
    Creates a xlsx file that stores the current generation, the current max SP score and the average fitness score \
    for each cycle (generation)
    Aditionally stores the termination total cycles, run time, and MSA identity percentage 
    
    :param filename: The name of the file to create
    :param dict: a dictionary containing the run data
    """
    file = f"{filename}.xlsx"
    workbook = xlsxwriter.Workbook(file)
    for cycle, cycle_dict in exp_dict.items():
        worksheet = create_worksheet(workbook, cycle)
        gen = cycle_dict["gen"]
        worksheet.write_column(1,0, gen)

        max_sp = cycle_dict["max_sp"]
        worksheet.write_column(1,1, max_sp)
        
        average_fitness = cycle_dict["average_fitness"]
        worksheet.write_column(1,2, average_fitness)

        n_cycles = cycle_dict["n_cycles"]
        worksheet.write("F2", n_cycles)

        runtime = cycle_dict["runtime"]
        worksheet.write("G2", runtime)

        identity_percentage = cycle_dict["identity_percentage"]
        worksheet.write("H2", identity_percentage)
        
    workbook.close()



def create_worksheet(workbook_instance, pagename):
    """
    Creates the blueprint of any worksheet
    
    :param workbook_instance: the workbook instance to add the worksheet to
    :param pagename: the name of the worksheet
    """
    worksheet = workbook_instance.add_worksheet(pagename)
    worksheet.write("A1","GENERATION")
    worksheet.write("B1","MAX_SP")
    worksheet.write("C1","AVERAGE_FITNESS")
    worksheet.write("D1","NA")
    worksheet.write("E1","NA")
    worksheet.write("F1","N_CYCLES")
    worksheet.write("G1","RUN_TIME")
    worksheet.write("H1","MSA_IDENTTITY")

    return worksheet

    
def main():    
    filename = "test"
    dict = {
            "cycle_1":{"gen":[1,2,3], "max_sp": [1000, 3000, 5000], "average_fitness": [2000, 4000, 5000],"n_cycles": 3,  "runtime": 21, "identity_percentage": 0.84},
            "cycle_2":{"gen":[1,2,3], "max_sp": [1000, 3000, 6000], "average_fitness": [2000, 4000, 5500],"n_cycles": 3,  "runtime": 22, "identity_percentage": 0.87},
            "cycle_3":{"gen":[1,2,3], "max_sp": [1000, 4000, 6000], "average_fitness": [2000, 4500, 5500],"n_cycles": 3,  "runtime": 19, "identity_percentage": 0.73}
            }


    create_xlsx(filename, dict)

if __name__ == "__main__":
    main()
