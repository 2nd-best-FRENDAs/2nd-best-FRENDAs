# 2nd-best-FRENDAs

## What is 2nd-best-FRENDAs?

2nd-best-FRENDAs is a package that offers a tool to solve and visualize ODEs of metabolic models using a graphical user interface.

## Who is 2nd-best-FRENDAs for?

2nd-best-FRENDAs is intended for researchers interested in easily visualizing and adjusting their desired metabolic models. This was specifically intended to be compatible with metabolic models in SBML and antimony format.

## What can 2nd-best-FRENDAs do?

2nd-best-FRENDAs can solve metabolic models ODEs for metabolite concentrations over time and produce visualizations. These can be adjusted to view metabolites of interest.

## Creating the environment and starting up 2nd-best-FRENDA

To create the virtual environment to run 2nd-best-FRENDA, execute the following line in the folder containing environment.yml (this only needs to be done once):

    conda env create -f environment.yml

Then, whenever you want to activate the environment, execute the following line:

    conda activate 2nd-best-environment

Finally, 2nd-best-FRENDA can be activated by executing the following line:

    streamlit run best-FRENDAs.py

## Example:

multi_enzyme_model.txt is a small metabolic model in antimony format

This can be uploaded to on the GUI upload model tab.

![load_model_tab](https://github.com/best-FRENDAs/2nd-best-FRENDAs/blob/main/pngs/model_load_tab_screenshot.png)

On the solve model tab, the ODE model can be solved with a tellurium roadrunner function over a specified time interval and steps. This can be exported as a csv.

![solve_model_tab](https://github.com/best-FRENDAs/2nd-best-FRENDAs/blob/main/pngs/model_solve_screenshot.png)

The solved model can be visualized on the plot all tab, which shows all metabolites on the graph. 

![plot_all](https://github.com/best-FRENDAs/2nd-best-FRENDAs/blob/main/pngs/model_visualize_all_screenshot.png)

A subset can also be visualized on the plot selected tab.

![plot_selected](https://github.com/best-FRENDAs/2nd-best-FRENDAs/blob/main/pngs/model_visualize_subset_screenshot.png)

A subset filtered by species that have a user-defined amount of fold change can also be plotted on the fold change tab.

![plot_foldchange](https://github.com/best-FRENDAs/2nd-best-FRENDAs/blob/main/pngs/foldchange_screenshot.png)

Lastly, the model can be rerun through 2nd-best-FRENDAs with input changes. On the titration tab, one species' initial concentration can be modified, and the output plot will be its behavior over time for a range of concentrations.
![plot_titration](https://github.com/best-FRENDAs/2nd-best-FRENDAs/blob/main/pngs/titration_screenshot.png)

## Current known issues:
- Solving the model is set so that the button to solve can only be clicked once, unless a time input is changed. However, when it is rerun with an altered input, the output is incorrect because it runs off of something that is not the original input.

## Future additions:
- 2nd-best-FRENDAs allows for fast, customizable, solving of different models. It could be expanded to allow for changes to multiple species, more specific concentration changes or titrations (such as the range and step value), single value replacements, and more.
    - part of this function has been written, see *modify_sim(filename, species_to_edit, new_concentrations)*, but it is not integrated into the GUI yet.