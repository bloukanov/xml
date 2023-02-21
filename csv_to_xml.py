import os
import io
import csv
import xml.etree.ElementTree as ET

# Path to CSV file
csv_file = 'data.csv'

# Base path for XML files
xml_path = 'data'

# Create directory if it doesn't exist
if not os.path.exists(xml_path):
    os.makedirs(xml_path)

# Define custom field names
field_names = ['Title', 'Summary', 'Actors', 'Year']

# Open CSV file and read the data
with open(csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    # Skip header row
    next(csvreader)

    # Loop through rows and create XML files
    for row in csvreader:
        # Create XML tree
        root = ET.Element('data')

        # Create XML elements for current row
        item = ET.SubElement(root, 'item')
        for i in range(len(row)):
            ET.SubElement(item, field_names[i]).text = row[i]

        # Write XML to file
        xml_file = f"{xml_path}/{row[0]}.xml"
        xml_string = ET.tostring(root, encoding='utf-8')
        xml_pretty_string = xml_string.decode('utf-8').replace('><', '>\n<')
        with open(xml_file, 'wb') as f:
            f.write(xml_pretty_string.encode('utf-8'))

        # Print XML filename for debugging
        print(f'Wrote XML file: {xml_file}')













