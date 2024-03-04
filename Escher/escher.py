# Imports
import tellurium as te
import escher
from escher import Builder
import cobra
from cobra.io import save_json_model, read_sbml_model

# Functions

# can remove later or merge these functions to other tellurium python file. Or import from that.

def load_model(filename, filetype): 
    """ 
    filename: .txt, .csv, biomodels website
    filetype: ant, sbml
    
    Input the filename/path of the file, and its syntax.
    Output declares whether file was successfully loaded or not
    """
    model_ant = filename
    with open(model_ant, "r") as file:
        model_content = file.read()
    if filetype=='antimony':
        try:
            model_sbml = te.antimonyToSBML(model_content)
            model_load = te.loadSBMLModel(model_sbml)
            print(f"Successfully converted file '{filename}' from {filetype} to SBML and loaded.")
        except Exception as e:
            print("Could not load file.", e)
    else: 
        try:
            model_load = te.loadSBMLModel(model_content)
            print(f"Successfully loaded SBML file {filename}.")
        except Exception as e:
            print("Could not load SBML file.", e)
    return model_load

def ODBM_to_SBML_JSON(ODBM_filename, input_filetype, export_filename):
    #To do: remove errors from cobrapy.io reading?
    #to do: tests
    #to do: add time stamp?
    
    '''Take ODBM output txt file and convert to SBML(.yml) and .JSON filetypes.
    This allows for wider compatibility with cobra, escher and other systems biology packages
    
    Requires tellurium and cobra.io packages
    
    Inputs: 
            ODBM_filename - File name for the output of ODBM. Should be txt file
            input_filetype - file type for input. antimony or sbml are accepted
            export_filenames - names for files returned with function.

    Output: ODBM_SBML and ODBM_JSON - these will have the names as the original file
            but with _SBML and _JSON suffix added.
    '''
    
    # load file into tellurium using load_model function. Assumes input is antimony type
    ODBM_output_model = load_model(ODBM_filename, input_filetype)
    
    #export to SBML filetype
    SBML_export = export_filename + "_SBML.xml"
    JSON_export = export_filename + "_JSON.json"
    
    try:
        ODBM_output_model.exportToSBML(SBML_export)
        print("Exported ODBM to SBML file: "+ SBML_export)
    except:
        print("Error in exporting ODBM to SBML file")
        
    try:
        #load into cobra.io and convert to json filetype
        model = read_sbml_model(SBML_export)
        save_json_model(model, JSON_export)
        
        print("Exported ODBM to JSON file: " + JSON_export)
    except:
        print("error in exporting ODBM to JSON file")  
    
    return

