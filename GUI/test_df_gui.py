import streamlit as st
import unittest
from unittest.mock import patch, MagicMock
import gui_callfunctions as gf
import pandas as pd
import numpy as np
import math 

class TestFileUpload(unittest.TestCase):
    # Create a mock file upload
    @patch("gui_callfunctions.st.file_uploader")
    
    # Test for correct error message when a file is uploaded that is not .csv/.txt
    def test_upload_file_notcsv(self, fake_file_uploader):
        fake_uploaded_file = MagicMock()
        fake_uploaded_file.name = "not_csv.pdf"
        fake_uploaded_file.type = "pdf"
        fake_uploaded_file.read.return_value = b"This is not a CSV file"
        fake_file_uploader.return_value = fake_uploaded_file

        # Load function from script
        gf.upload_model()

        # Assert that the correct error message is being displayed
        self.assertIn("Invalid format, please upload a .txt or .csv file", [call[0] for call in fake_uploaded_file.error.call_args_list])

class TestModeling(unittest.Testcase):
    # Create mock objects from streamlit
    @patch.object(st, "button", return_value=True)  # Fake button click event
    @patch.object(st, "session_state", {"model_load": fake_model_load})  # Fake session state
    def test_solve_model_button(self, fake_button):
        fake_t0 = 0
        fake_tf = 1
        fake_steps = 10
        
        # Call the solve_model function
        with patch('gf.upload_model', fake_simulate_model):
            gf.solve_model()

        # Assert that st.button performs expected duties when clicked
        fake_button.assert_called_once_with("Solve Model")
        
    '''def test_solve_model_dataframe(self):

    def test_visualize_data(self):

    def test_generate_plot(self):

    def test_custom_plot(self):

    def test_main(self):'''

if __name__ == "__main__":
    unittest.main()
