import unittest
from unittest.mock import MagicMock, patch
import pandas as pd


# Import the function you want to test
from best_FRENDAs import *

'''To do - unittests for all functions in best_FRENDAs'''

class TestTab1UploadModel(unittest.TestCase):

    def test_tab1_upload_model_no_file(self):
        # Test when no file is uploaded
        # Mocking st.file_uploader to return None
        with unittest.mock.patch('streamlit.file_uploader', return_value=None):
            # Capture the output of the function
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab1_upload_model()
                # Assert that the expected message is displayed
                mock_write.assert_called_with("Please upload a file")

    def test_tab1_upload_model_invalid_format(self):
        # Test when an invalid format is uploaded
        # Mocking st.file_uploader to return a file with invalid format
        with unittest.mock.patch('streamlit.file_uploader') as mock_file_uploader:
            mock_file_uploader.return_value.type = "invalid_format"
            # Capture the output of the function
            with unittest.mock.patch('streamlit.error') as mock_error:
                tab1_upload_model()
                # Assert that the error message is displayed
                mock_error.assert_called_with("Invalid format, please upload a .txt or .csv file")

    # Add more test cases as needed

class TestTab2SolveModel(unittest.TestCase):

    def test_tab2_solve_model_no_solve_button_clicked(self):
        # Create a MagicMock object to mimic st.session_state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = True  # Assume 'model_load' is present
        session_state_mock.__getitem__.return_value = 'dummy_model'

        # Patch streamlit.session_state with the MagicMock object
        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.button', return_value=False):
                with unittest.mock.patch('streamlit.write') as mock_write:
                    tab2_solve_model()
                    mock_write.assert_not_called() 

class TestTab3PlotAll(unittest.TestCase):

    def test_tab3_plot_all_no_dataframe(self):
        # Test when no dataframe is present in session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab3_plot_all()
                mock_write.assert_called_with("Load model first")


class TestTab4PlotSelected(unittest.TestCase):

    def test_tab4_plot_selected_no_dataframe(self):
        # Test when no dataframe is present in session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab4_plot_selected()
                mock_write.assert_called_with("Load model first")

    def test_tab4_plot_selected_with_dataframe_no_y_columns_selected(self):
        # Test when dataframe is present in session state but no Y columns are selected
        # Mock dataframe with one column
        mock_df = pd.DataFrame({'Time': [0, 1, 2]})
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = True
        session_state_mock.__getitem__.return_value = mock_df

        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab4_plot_selected()
                mock_write.assert_called_with('No Y columns selected.')


class TestTab5PlotFoldChange(unittest.TestCase):

    def test_tab5_plot_foldchange_no_dataframe(self):
        # Test when no dataframe is present in session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab5_plot_foldchange()
                mock_write.assert_called_with("Load model first")

    # Add more test cases as needed

class TestTab6PlotTitration(unittest.TestCase):

    def test_tab6_plot_titration_no_dataframe(self):
        # Test when no dataframe is present in session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.return_value = False

        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab6_plot_titration()
                mock_write.assert_called_with("Load model first")

    def test_tab6_plot_titration_no_uploaded_file(self):
        # Test when no uploaded file is present in session state
        session_state_mock = MagicMock()
        session_state_mock.__contains__.side_effect = lambda key: key == 'df'

        with unittest.mock.patch('streamlit.session_state', session_state_mock):
            with unittest.mock.patch('streamlit.write') as mock_write:
                tab6_plot_titration()
                mock_write.assert_called_with("Load model first")


if __name__ == '__main__':
    unittest.main()