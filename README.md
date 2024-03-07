# 2nd-best-FRENDAs

## What is 2nd-best-FRENDAs?

2nd-best-FRENDAs is a package that offers a tool to solve and visualize ODEs of metabolic models using a graphical user interface.

## Who is 2nd-best-FRENDAs for?

2nd-best-FRENDAs is intended for researchers interested in easily visualizing and adjusting their desired metabolic models. This was specifically intended to be compatible with metabolic models in SBML and antimony format.

## What can 2nd-best-FRENDAs do?

2nd-best-FRENDAs can solve metabolic models ODEs for metabolite concentrations over time and produce visualizations. These can be adjusted to view metabolites of interest.

## Example:

multi_enzyme_model.txt is a small metabolic model in antimony format


This can be uploaded to on the GUI upload model tab.

<img src="/png/model_load_tab_screenshot.png" align="center" width="600px"/>

On the solve model tab, the ODE model can be solved with a tellurium roadrunner function over a specified time interval and steps. This can be exported as a csv.

<img src="model_solve_screenshot.png" align="center" width="600px"/>


The solved model can be visualized on the plot all tab, which shows all metabolites on the graph. 

<img src="model_visualize_all_screenshot.png" align="center" width="600px"/>

A subset can also be visualized on the plot selected tab.

<img scr="model_visualize_subset_screenshot.png" align="center" width="600px"/>

