'''This script contains unittests for best_FRENDAs.py'''

import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

# Import the function you want to test
from best_FRENDAs import *

class TestTab1UploadModel(unittest.TestCase):

    def test_tab1_upload_model_no_file(self):
        '''Test when no file is uploaded that expected statement written'''
        # Creating mock st.file_uploader to return None
        with patch('streamlit.file_uploader', return_value=None), \
            patch('streamlit.write') as mock_write:
            
            tab1_upload_model()
                
            # Assert that the expected message is displayed
            mock_write.assert_called_with("Please upload a file")

    def test_tab1_upload_model_invalid_format(self):
        '''Test invalid format upload, correct statement is written''' 
        # Mocking st.file_uploader to return a file with invalid format, like a pdf
        with patch('streamlit.file_uploader') as mock_file_uploader, \
             patch('streamlit.error') as mock_error:
            mock_file_uploader.return_value.type = "pdf"
            
            tab1_upload_model()
            # Assert that the error message is displayed
            mock_error.assert_called_with("Invalid format, please upload a .txt or .csv file")


class TestTab2SolveModel(unittest.TestCase):

    def test_tab2_solve_model_no_solve_button_clicked(self):
        '''Asserts that nothing written and simulate_model() function is not called if solve button is not clicked'''

        # Create a MagicMock object to mimic st.session_state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = True  # Assume 'model_load' is present
        session_state_mock.__getitem__.return_value = 'dummy_model'

        # Patch streamlit.session_state with the MagicMock object
        with patch('streamlit.session_state', session_state_mock), \
            patch('streamlit.button', return_value=False), \
            patch('streamlit.write') as mock_write, \
            patch('best_FRENDAs.simulate_model') as mock_simulate_model:
            
            tab2_solve_model()

            # Assert nothing written from no solve button clicked
            mock_write.assert_not_called() 

            # Assert simulate model function not run
            mock_simulate_model.assert_not_called()

    def test_tab2_solve_model_solve_button_clicked(self):
        '''Asserts simulate_model() function is called once if solve button is clicked'''

        # Create a MagicMock object to mimic st.session_state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = True  # Assume 'model_load' is present
        session_state_mock.__getitem__.return_value = 'dummy_model'

        # Patch streamlit.session_state with the MagicMock object
        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.button', return_value=True), \
             patch('streamlit.write'), \
             patch('best_FRENDAs.simulate_model') as mock_simulate_model:
            
            tab2_solve_model()

            # Assert simulate model function called once
            mock_simulate_model.assert_called_once()


class TestTab3PlotAll(unittest.TestCase):

    def test_tab3_plot_all_no_dataframe(self):
        '''Test when no dataframe is present in session state that correct statement is written'''
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.write') as mock_write:
            
            tab3_plot_all()
            mock_write.assert_called_with("Load model first")

class TestTab4PlotSelected(unittest.TestCase):

    def test_tab4_plot_selected_no_dataframe(self):
        '''Test when no dataframe is present in session state'''
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.write') as mock_write:
            
            tab4_plot_selected()
            mock_write.assert_called_with("Load model first")

    def test_tab4_plot_selected_with_dataframe_no_y_columns_selected(self):
        '''Test when dataframe is present in session state but no Y columns are selected'''
        # Mock dataframe with one column
        mock_df = pd.DataFrame({'Time': [0, 1, 2]})
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = True
        session_state_mock.__getitem__.return_value = mock_df

        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.write') as mock_write:
            
            tab4_plot_selected()
            mock_write.assert_called_with('No Y columns selected.')


class TestTab5PlotFoldChange(unittest.TestCase):

    def test_tab5_plot_foldchange_no_dataframe(self):
        '''Test when no dataframe is present in session state'''
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.write') as mock_write:
            
            tab5_plot_foldchange()
            mock_write.assert_called_with("Load model first")

    # Need more tests that data processing is correct

class TestTab6PlotTitration(unittest.TestCase):

    def test_tab6_plot_titration_no_dataframe(self):
        # Test when no dataframe is present in session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.write') as mock_write:
            
            tab6_plot_titration()

            mock_write.assert_called_with("Load model first")

    def test_tab6_plot_titration_bad_input(self):
        '''Testing when initial concentration is greater than final titration conc'''
        
        # Prepare mock session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = True  # Assuming all required session state variables are present

        # Mock the titration_plot function

        #number_input designates initial and final titration concs
        with patch('functions_to_import.titration_plot') as mock_titration_plot, \
             patch('streamlit.session_state', session_state_mock), \
             patch('streamlit.button', return_value=True), \
             patch('streamlit.write'), \
             patch('streamlit.selectbox'), \
             patch('streamlit.number_input', side_effect=[6, 5]), \
             patch('streamlit.plotly_chart'), \
             patch('streamlit.error') as mock_error:
                
            tab6_plot_titration()

            # Assert that 'error' function was called with the specified message
            mock_error.assert_called_with("make sure the range end is greater than the range start")

            # Assert that titration_plot was not called
            mock_titration_plot.assert_not_called()


if __name__ == '__main__':
    unittest.main()