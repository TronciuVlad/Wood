The folder structure is as follows:

taps-aff
    clothing_recommender_gui.py     -> data visualiser with Create and Delete operations using a Tinkter GUI
    clothing_recommender.py         -> clothing recommender class + csv manipulator
    fahrenheit_cities.txt           -> dataset of cities which use Fahrenheit rather than Celsius
    input.csv                       -> input csv file
    output.csv                      -> output csv file, what the basic solution spits out
    taps-aff.py                     -> caller script for the basic solution
    test_clothing_recommender.py    -> testing script using PyTest
README.txt

Running instructions

Basic solution : nothing needs to be installed for this, you just need to Running

    python taps-aff.py

And it will produce the output.csv, which has the simple solution. It requires the fahrenheit_cities.txt file to determine which cities should
follow the Fahrenheit standard.


GUI : For this you will require Tinkter, which can be installed through

    sudo apt-get install python3-tk

or

    pip install tk

and you can run the GUI through

    python clothing_recommender_gui.py

And you will be able to visualise the data in real time, create new data and delete old one.

Testing: For this you will need pytest and pytest-mock

    pip install pytest pytest-mock

and run the tests through

    pytest test_clothing_recommender.py

The tests don't require the base files data files to be located in the directory.