import os
import xml.etree.ElementTree as ET
import pandas as pd

vod_metadata_dir = "vod_metadata_files"
addl_data_path = "data.csv"
output_dir = "output"

data = pd.read_csv(addl_data_path)

for file in os.listdir(vod_metadata_dir):
    if file.endswith(".xml"):
        data_row = data.loc[data["Title"] == file.split(".")[0]]
        tree = ET.parse(os.path.join(vod_metadata_dir, file))
        root = tree.getroot()
        item = root[1][0]
        
        item[18].attrib["Value"] = data_row["Title"].values[0]
        item[17].attrib["Value"] = data_row["Summary"].values[0]
        item[21].attrib["Value"] = str(data_row["Year"].values[0])
        ET.SubElement(item, f"""App_Data App="MOD" Name="Actors" Value="{data_row["Actors"].values[0]}\"""")
        
        tree.write(os.path.join(output_dir, file))
        