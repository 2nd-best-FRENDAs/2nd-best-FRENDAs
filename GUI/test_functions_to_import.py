''' This script contains test functions for function_to_import.py. These are written as unittests
Make sure multi_enzyme_model.txt is in same directory
'''

from io import BytesIO
import unittest
import antimony
import pandas as pd
from unittest.mock import MagicMock

import tellurium as te

# Import the function you want to test
from functions_to_import import load_model, simulate_model, titration_plot

'''simple model for testing'''

basic_model = """
model test
    compartment C1;
    C1 = 1.0;
    species S1, S2;

    S1 = 10.0;
    S2 = 0.0;
    S1 in C1; S2 in C1;
    J1: S1 -> S2; k1*S1;

    k1 = 1.0;
end
"""

class TestLoadModel(unittest.TestCase):

    def test_modeL_load_upload(self):
        '''checking basic model is loading correctly - comparing file basic_model.txt
        to string stored in variable above as basic_model'''

        with open('basic_model.txt', 'r') as f:
            basic_file = f.read().strip()  # Remove leading and trailing whitespace
        
        # Normalize line endings and remove whitespace from basic_model string
        basic_model_normalized = basic_model.strip().replace('\r\n', '\n')

        self.assertEqual(basic_file, basic_model_normalized)
    
    def test_model_load(self):
        '''One off test with file used in development in antimony format.
        Includes test for correct model type is output when inputs are correct.
        '''
        with open('multi_enzyme_model.txt', 'r') as f:
            file_content = f.read()

        # testing with antimony_load
        ant_model = load_model(file_content, 'antimony')

        ## Assert the output type is RoadRunner
        self.assertIsInstance(ant_model, te.roadrunner.extended_roadrunner.ExtendedRoadRunner)



class TestSimulateModel(unittest.TestCase):

    def test_simulate_model_basic(self):
        '''Test with basic_model. Simulated 3 steps at 3 time points'''
        basic_model_loaded = te.loada(basic_model)
        simulated_model = simulate_model(basic_model_loaded, 0, 2, 3)

        # confirm output type
        self.assertEqual(pd.DataFrame, type(simulated_model))

        # confirm columns 
        expected_columns = ['Time', 'S1', 'S2']
        simulated_model_columns = list(simulated_model.columns)

        self.assertEqual(simulated_model_columns, expected_columns)

        # confirm shape matches expected
        expected_shape = (3,3)
        self.assertEqual(simulated_model.shape, expected_shape)


class TestTitrationPlot(unittest.TestCase):
    
    def test_titration_plot_shape(self):
        '''Test that output shape matches expected for basic_enzyme_model, adjusting titration 3 steps'''
        
        # positional argument needed on streamlit but not here. Inputting none
        selected_option = None

        test_titration_df = titration_plot(basic_model, 'S1', 0, 5, 0, 5, 6, selected_option)

        #print(test_titration_df.shape)


if __name__ == '__main__':
    unittest.main()