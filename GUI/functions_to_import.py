import io
import os

import pandas as pd
import tellurium as te

# Load file and convert to SBML format, if file is in SBML, function will still load the model
def load_model(file_content, selected_option): 
    """ 
    file_name: .txt, .csv, biomodels website
    selected_option: ant, sbml
    
    Input the file_name/path of the file, and its syntax.
    Output declares whether file was successfully loaded or not
    """
    if selected_option=='antimony':
        #tellurium converstion functions
        model_sbml = te.antimonyToSBML(file_content)
        model_load = te.loadSBMLModel(model_sbml)
    else: 
        model_load = te.loadSBMLModel(file_content)
    return model_load

# solve model in tellurium
def simulate_model(model_load, t0, tf, steps):
    #simulate based on time interval and time steps
    result = model_load.simulate(t0, tf, steps) 
    #convert to dataframe
    species_names = model_load.getFloatingSpeciesIds()
    columns = ['Time'] + [str(i) for i in species_names]
    solved_df = pd.DataFrame(data=result, columns=columns)
    return solved_df

# titration plot
def titration_plot(uploaded_file, species, init_titration_conc, titration_conc, t0, tf, steps, selected_option):
    """ 
    file_name: .txt, .csv, biomodels website
    species: name of species to be titrated in str format (must match the name of a species in the input file)
    titration_conc: list of strings prescribing the various initial concentrations to simulate and plot
    
    Input the uploaded_file/path of the file, species of interest to be titrated, and the concentrations to simulate and plot.
    Output is a single concentration vs time plot containing the profiles of the titrated species at each of the prescribed initial concentrations. 
    
    """
    # Append '=' to confine search to the initial concentration section
    species_edit = species + '='
    # Create empty dataframe to be populated with concentrations
    titration_df = pd.DataFrame()
    #adding one so that the range is inclusive
    titration_conc_shift = titration_conc + 1
    titration_conc_list = list(range(titration_conc_shift))
    
    # for each titration value
    for i in range(init_titration_conc, titration_conc_shift):
        counter = 0
        # Create temp model file with specified change to concentrations
        # Open input file in readlines compatible text form
        file_object = io.BytesIO(uploaded_file.getvalue())
        with io.TextIOWrapper(file_object, encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            # Create empty list that will contain all lines in the .txt
            modified_lines = []
            # for each line in the input .txt file
            for line in lines:
                #identify the index of the prescribed species
                index = line.find(species_edit)
                # An index of -1 means that it is not found, any other number indicates the position the string begins
                if index != -1:
                    # Rewrite the concentration to the one prescribed in new_concentrations
                    modified_line = line[:index + len(species_edit)] + str(titration_conc_list[i]) + '; \n'
                    #print(modified_line)
                    # Add the newly modified line to the list of modified text
                    modified_lines.append(modified_line)
                # If the a modified line was not added to modified_lines (as in, a change to a species was not changed), copy the line exactly
                if len(modified_lines) == counter:
                    modified_lines.append(line)  
                counter += 1
            # Create a new file temp_model.txt in "write mode" and write out the modified lines
            with open('temp_model.txt', 'w') as temp_file:
                temp_file.writelines(modified_lines)
            temp_model_sbml = te.antimonyToSBML('temp_model.txt')
            temp_model = te.loadSBMLModel(temp_model_sbml)
            # Simulate and assign variables to temp model
            df_temp = simulate_model(temp_model, t0, tf, steps)
            # Copy the 'Time' column in the first iteration
            if i == init_titration_conc:
                titration_df['Time'] = df_temp['Time']
            # Add the concentrations of the specified species into the dataframe as a new column
            titration_df[species + ' = ' + str(titration_conc_list[i])]  = df_temp[species]
    os.remove('temp_model.txt')
    return titration_df