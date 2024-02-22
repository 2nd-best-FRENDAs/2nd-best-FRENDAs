
## User Stories
#### User Story 1 (Stakeholders)
Maggie runs TX-TL experiments to learn more about metabolic pathways. She wants to perform metabolic modeling of varying enzyme concentrations to optimize bioproduction pathways while running fewer wet-lab experiments. Maggie wants to model her pathway using enzyme parameters from databases like BRENDA and KEGG. Maggie currently collects enzyme parameters and reactions using FRENDA-BRENDA, then inputs this into ODBM to create ODEs and parameters in a synthetic biology markdown language (SBML). These programs are in development in her lab. She analyzes the output in tellurium which can create plots from SBML. Maggie wants to use BEST-FRENDA to automate modulation of her parameters and increase data visualization ability with tools like escher maps.

#### User Story 2 (Outside users)
Timothy runs TX-TL experiments and wants to model his pathways. Timothy found a metabolic model already published with the reactions, species, and kinetic parameters defined. He wants to use BEST-FRENDA to easily visualize this model and make adjustments to enzyme concentrations with a UI.

## Components
### Basic Info

### Name: BEST-FRENDA
  - What it does: A piece of software to use in tandem with other Carothers Lab programs (FRENDA-BRENDA and ODBM). Currently, the entire pipeline allows for inputting a list of enzymes that directly or indirectly affect the metabolic pathway of interest and obtaining kinetic models to visualize changes in flux, depending on concentration of metabolites, enzymes and activity, against time. BEST-FRENDA will increase functionality of the ODBM output by including a UI for data visualization for parameters such as starting concentration and included enzymes, as well as an increase of visualization options.
  - The objective is to take, as an input, any kinetic model, regardless if it is from FRENDA-BRENDA, and output visualization of metabolic flux through a chosen pathway.
-  This overall 
#### Inputs (with type information): 
- metabolic model in SBML format (txt file) with metabolites, enzymes, reactions and reaction parameters. This is the output of ODBM
- Excel sheet that specifies the following:
- Time and step interval for initial simulations

#### Outputs (with type information):
- Data table (excel file) with ODEs solved, providing metabolite concentrations over time.
- Plot/curve of changing metabolite concentration against time.
- Translate changes into Escher map and visualize perturbations through multiple pathways
- Easily exclude enzymes
- How does changing one enzyme concentration affect metabolite flux through desired pathway vs a side pathway?
- Taking that output, be able to re-input concentrations to optimize flux through the desired pathway.
#### Sub- Components (defined further below)
1. ODE Solver: Tellurium/Roadrunner script for solving ODEs and exporting into dataframe.
2. Plotting: Python script for plotting ODEs
3. Escher: script for plotting metabolic models with pathway of interest highlighted and indication of fluxes
4. Graphical User Interface: GUI for re-inputting concentrations, removal of enzymes from the modeled pathway (e.g., iterative)
  - Dropdown for inputting concentrations
  - Biomodels for other kinetic models
#### Side Effects
- Changing Escher map with respect to removing enzymes, changing concentrations, and adding an enzyme (done outside of tellurium).
- What changes can be made “close” to our software? What changes need to be made outside of our software?
- How do other piece outputs changing affect OUR software?

### Name: ODE Solver

#### Inputs
- metabolic model in SBML format
- time interval and steps for solving ODEs of the model
  - This may originate from GUI output OR excel file, TBD
- List of metabolites of interest to plot from excel file

#### Outputs
- Pandas Dataframe with ODE's solved containing all metabolite concentrations over time and indicates specific metabolites to be plotted.

#### Side Effects
- Need to consider how inputs may have variety of formatting. ODBM format may be adjusted in future or have underlying issues currently.

### Name: ODE Plotting

#### Inputs
- Pandas dataframe from ODE solver with metabolite concentrations over time with metadata indicating metabolites to be plotted

#### Outputs
- Graphs of the specified metabolites plotted over time.

#### Side Effects
- May take alternate inputs from GUI
 
### Name: Escher Plotting

#### Inputs
- metabolic model in SBML format

#### Outputs 
- Escher plot with metabolic pathway indicating flux of intended pathway overlaid on TXTL endogenous e coli metabolism.

