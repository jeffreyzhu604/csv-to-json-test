import xml.etree.ElementTree as ET
import pandas as pd
import os

'''

This function takes the XML file generated by ACTS and converts it
to an CSV file to be read into as options for the command line.

'''
def xml_to_csv(xml, csv):
    xml = ET.parse(xml)
    root = xml.getroot()
    
    test_set = root.find('Testset')
    tests = []

    for test in test_set:
        curr = {
            'output' : list(test)[1].text.strip(),
            'delimiter' : list(test)[2].text.strip(),
            'quote' : list(test)[3].text.strip(),
            'trim' : list(test)[4].text.strip(),
            'checktype' : list(test)[5].text.strip(),
            'ignoreempty' : list(test)[6].text.strip(),
            'noheader' : list(test)[7].text.strip(),
            'header' : list(test)[8].text.strip(),
            'flatkeys' : list(test)[9].text.strip(),
            'maxrowlength' : list(test)[10].text.strip(),
            'checkcolumn' : list(test)[11].text.strip(),
            'eol' : list(test)[12].text.strip(),
            'quiet' : list(test)[13].text.strip(),
            'escape' : list(test)[14].text.strip(),
            'colparser' : list(test)[15].text.strip(),           
            'alwayssplitateol' : list(test)[16].text.strip(),
            'nullobject' : list(test)[17].text.strip(),
            'downstreamformat' : list(test)[18].text.strip()
        }
        tests.append(curr)
    
    df = pd.DataFrame(tests)
    df.to_csv(os.path.join('..', 'resources', csv), index=False)

xml_to_csv(os.path.join('..', 'resources', 'csvtojson.xml'), "command_line_options.csv")