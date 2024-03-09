from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import tellurium as te


# Load file and convert to SBML
        # If file is in SBML, function will still load the model
def load_model(file_content, selected_option): 
    """ 
    file_content: .txt, .csv, biomodels website
    selected_option: antimony, sbml
    
    Input the file and its syntax/format.
    Output converts to SBML format for modeling. 
    Declares whether file was successfully loaded or not.
    """
    if selected_option=='antimony':
        try:
            model_sbml = te.antimonyToSBML(file_content)
            model_load = te.loadSBMLModel(model_sbml)
            print(f"Successfully converted file from {selected_option} to SBML and loaded.")
        except Exception as e:
            print("Could not load file.", e)
    else: 
        try:
            model_load = te.loadSBMLModel(file_content)
            print(f"Successfully loaded SBML file.")
        except Exception as e:
            print("Could not load SBML file.", e)
    return model_load

#solve model in tellurium
def simulate_model(model_load, t0, t1, steps):
    """
    model_load: roadrunner file output from the load model function
    t0: starting time
    t1: final time (endpoint)
    steps: how many timepoints between t0 and t1

    Input is roadrunner/tellurium file, and interval over which simulation will run.
    Outputs a dataframe used for plotting concentration vs. time.
    """
    result = model_load.simulate(t0, t1, steps) 
    
    # Extract species names
    species_names = model_load.getFloatingSpeciesIds()
    
    # Convert to DataFrame and output to user
    columns = ['Time'] + [str(i) for i in species_names]
    solved_df = pd.DataFrame(data=result, columns=columns) 
        
    return solved_df

#export csv
def export_csv(model):
    """
    Takes a solved model and exports it as a .csv in the same folder as the code.
    Appends the date and time to the beginning of the file name so repeats are not created.
    """
    # Grab current time and date, make variable to display date
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H.%M.%S")
    
    # Save DataFrame to .csv
    model.to_csv(current_time + ' simulation_data.csv', index=False)
    
    return
