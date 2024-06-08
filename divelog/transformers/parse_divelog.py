if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import xml.etree.ElementTree as ET
import pandas as pd

# Function to convert time string to minutes
def time_to_minutes(time_str):
    if ':' in time_str:
        parts = time_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    return float(time_str)

# Extract dive profiles for all dives with refined temperature handling
def extract_all_dive_profiles_refined(dives_element):
    dive_data = []
    
    for dive in dives_element.findall('dive'):
        dive_number = dive.attrib.get('number', 'N/A')
        sac_rate = dive.attrib.get('sac', 'N/A').replace(' l/min', '')
        for sample in dive.findall('.//sample'):
            time = sample.attrib.get('time', 'N/A').replace(' min', '')
            depth = sample.attrib.get('depth', 'N/A').replace(' m', '')
            temperature = sample.attrib.get('temp', 'N/A').replace(' C', '') if 'temp' in sample.attrib else None
            pressure = sample.attrib.get('pressure', 'N/A').replace(' bar', '') if 'pressure' in sample.attrib else None
            rbt = sample.attrib.get('rbt', 'N/A').replace(':00 min', '') if 'rbt' in sample.attrib else None
            ndl = sample.attrib.get('ndl', 'N/A').replace(':00 min', '') if 'ndl' in sample.attrib else None
            
            if time != 'N/A' and depth != 'N/A':
                data_point = {
                    'dive_number': dive_number,
                    'time': time_to_minutes(time),
                    'depth': float(depth),
                    'temperature': float(temperature) if temperature else None,
                    'pressure': float(pressure) if pressure else None,
                    'rbt': float(rbt) if rbt else None,
                    'ndl': float(ndl) if ndl else None,
                    'sac_rate': float(sac_rate) if sac_rate != 'N/A' else None
                }
                dive_data.append(data_point)

    return dive_data


@transformer
def transform(data, *args, **kwargs):

    # Load and parse the XML file
    tree = ET.parse(data['name'])
    root = tree.getroot()

    return extract_all_dive_profiles_refined(root.find('dives'))


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
