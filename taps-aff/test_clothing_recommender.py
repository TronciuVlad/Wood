import pytest
from unittest.mock import mock_open, patch
from clothing_recommender import ClothingRecommender

# Test for decide_what_to_wear static method
def test_decide_what_to_wear():
    assert ClothingRecommender.decide_what_to_wear(14) == 'jumper'
    assert ClothingRecommender.decide_what_to_wear(15) == 't-shirt'
    assert ClothingRecommender.decide_what_to_wear(16) == 't-shirt'

# Test for read_csv method
@patch("builtins.open", new_callable=mock_open, read_data="location,temperature\nGlasgow,14\nEdinburgh,16")
def test_read_csv(mock_file):
    recommender = ClothingRecommender('input.csv', 'output.csv')
    data = recommender.read_csv()
    assert data == [{'location': 'Glasgow', 'temperature': '14'}, {'location': 'Edinburgh', 'temperature': '16'}]

# Test for write_csv method
@patch("builtins.open", new_callable=mock_open)
def test_write_csv(mock_file):
    recommender = ClothingRecommender('input.csv', 'output.csv')
    test_data = [{'location': 'Glasgow', 'temperature': '14', 'what_to_wear': 'jumper'}]
    recommender.write_csv(test_data)
    assert mock_file().write.call_count == 2


# Test for process_csv method
@patch("clothing_recommender.ClothingRecommender.read_csv")
@patch("clothing_recommender.ClothingRecommender.write_csv")
def test_process_csv(mock_write_csv, mock_read_csv):
    mock_read_csv.return_value = [{'location': 'Glasgow', 'temperature': '14'}, {'location': 'Edinburgh', 'temperature': '16'}]
    
    recommender = ClothingRecommender('input.csv', 'output.csv')
    recommender.process_csv()
    
    mock_write_csv.assert_called_once()
    