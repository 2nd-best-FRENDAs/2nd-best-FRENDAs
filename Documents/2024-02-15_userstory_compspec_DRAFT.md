
## User Stories
#### User Story 1 (Stakeholders)
Maggie runs TX-TL experiments to learn more about metabolic pathways. She wants to perform metabolic modeling of varying enzyme concentrations to optimize bioproduction pathways while running fewer wet-lab experiments. Maggie wants to model her pathway using enzyme parameters from databases like BRENDA and KEGG. Maggie currently collects enzyme parameters and reactions using FRENDA-BRENDA, then inputs this into ODBM to create ODEs and parameters in a synthetic biology markdown language (SBML). These programs are in development in her lab. She analyzes the output in tellurium which can create plots from SBML. Maggie wants to use BEST-FRENDA to automate modulation of her parameters and increase data visualization ability with tools. This could include visualizing ODE solvers of metabolite concentrations over time, and adjusting or titrating initial concentrations.

#### User Story 2 (Outside users)
Timothy runs TX-TL experiments and wants to model his pathways. Timothy found a metabolic model already published with the reactions, species, and kinetic parameters defined. He wants to use BEST-FRENDA to easily visualize this model and make adjustments to enzyme concentrations with a UI.

## Components
### Basic Info

### Name: BEST-FRENDA
  - What it does: A piece of software to use in tandem with other Carothers Lab programs (FRENDA-BRENDA and ODBM). Currently, the entire pipeline allows for inputting a list of enzymes that directly or indirectly affect the metabolic pathway of interest and obtaining kinetic models to visualize changes in flux, depending on concentration of metabolites, enzymes and activity, against time. BEST-FRENDA will increase functionality of the ODBM output by including a UI for data visualization for parameters such as starting concentration and included enzymes, as well as an increase of visualization options.
  - The objective is to take, as an input, any kinetic model, regardless if it is from FRENDA-BRENDA, and output visualizations of species concentrations over time.

#### Inputs (with type information): 
- metabolic model in SBML format (txt file) with metabolites, enzymes, reactions and reaction parameters. This is the output of ODBM
- Excel sheet that specifies the following:
- Time and step interval for initial simulations

#### Outputs (with type information):
- Data table (excel file) with ODEs solved, providing metabolite concentrations over time.
- Plot/curve of changing metabolite concentration against time.
- Taking that output, be able to re-input concentrations to optimize flux through the desired pathway.
#### Sub- Components (defined further below)
1. ODE Solver: Tellurium/Roadrunner script for solving ODEs and exporting into dataframe.
2. Plotting: Python script for plotting ODEs
3. Escher: script for plotting metabolic models with pathway of interest highlighted and indication of fluxes
4. Graphical User Interface: GUI for re-inputting concentrations, removal of enzymes from the modeled pathway (e.g., iterative)
  - Dropdown for inputting concentrations

#### Side Effects and considerations
- What changes can be made “close” to our software? What changes need to be made outside of our software?
- How do other piece outputs changing affect our software?
- How varied are the inputs from ODBM? Is this expected to change as this software is improved?
- Does GUI effectively communicate user input errors, or when underlying functions aren't working properly?

### Name: ODE Solver

#### Inputs
- metabolic model in SBML or antimony format.
  - This contains information including species, species initial concentrations, reactions, reaction rate constants.
- Time interval (seconds) and steps for solving ODEs of the model
  - This may originate from input in GUI.

#### Outputs
- csv containing ODE solved over specied time interval and steps, with all metabolite concentrations over time

#### Side Effects
- Need to consider how inputs may have variety of formatting. ODBM format may be adjusted in future or have underlying issues currently.
- Is this stored in a format for subsequent data visualization?

### Name: ODE Plotting

#### Inputs
- csv from ODE solver with metabolite concentrations over time 
- (optional) List of subset of metabolites to be plotted

#### Outputs
- Graphs of the specified metabolites plotted over time.

#### Side Effects
- May take alternate inputs from GUI
 
### Name: GUI

#### Inputs
- Initial model upload inputs:
  - Model file in SBML or antimony format
  - file type (antimony, SBML )
- "Solve model" tab
  - user clicks solve model tab
  - time interval to solve ODE over (initial and final time) 
  - interval steps to solve ODE at
  - user clicks "solve model" button
- plotting all data tab
  - User clicks tab "Plotting All Data"
- "Customizable Plot"
  - user selects metabolite concentrations to view on plot on "Y axis data" field
  - user types title
  - user types X and Y axis labels

#### Outputs
- model upload tab
  - Feedback that model was or was not successfully loaded
- solve model tab
  - csv preview of solved ODE
- plotting all data tab
  - plot of all metabolite concentrations over time
- customizable plot tab
  - plot with selected metabolite concentrations over time


### Name: Escher Plotting **[Not implemented]**

#### Inputs
- metabolic model in antimony or SMBL format

#### Outputs 
- Escher plot with metabolic pathway indicating flux of intended pathway overlaid on TXTL endogenous e coli metabolism.
- **limitation:** escher currently requires predrawn metabolic maps, and isn't easily compatible with novel metabolic pathways unless manually drawn using its webserver. Other packages may need to more explored. 

