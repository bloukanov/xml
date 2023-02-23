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
        
        [title_item] = [child for child in item if child.get("Name") == "Title"]
        # [title_item] = root.findall("./Asset/Metadata/App_Data[@Name='Title']")
        title_item.attrib["Value"] = data_row["Title"].values[0]
        
        [summary_item] = [child for child in item if child.get("Name") == "Summary_Short"]
        summary_item.attrib["Value"] = data_row["Summary_Short"].values[0]
        
        [year_item] = [child for child in item if child.get("Name") == "Year"]
        year_item.attrib["Value"] = str(data_row["Year"].values[0])

        [ad_content_ID_item] = [child for child in item if child.get("Name") == "Ad_Content_ID"]
        ad_content_ID_item.attrib["Value"] = str(data_row["Ad_Content_ID"].values[0])

        [sling_category_item] = [child for child in item if child.get("Name") == "Sling_Category"]
        sling_category_item.attrib["Value"] = str(data_row["Sling_Category"].values[0])

        [lws_item] = [child for child in item if child.get("Name") == "Licensing_Window_Start"]
        lws_item.attrib["Value"] = str(data_row["Licensing_Window_Start"].values[0])

        [lwe_item] = [child for child in item if child.get("Name") == "Licensing_Window_End"]
        lwe_item.attrib["Value"] = str(data_row["Licensing_Window_End"].values[0])

        [rating_item] = [child for child in item if child.get("Name") == "Rating"]
        rating_item.attrib["Value"] = str(data_row["Rating"].values[0])

        # This part needs to be a loop that ignores empty Ad Break values in CSV

        [adb1_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_1']")
        adb1_item.attrib["Value"] = data_row["Ad_Break_1"].values[0]

        [adb2_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_2']")
        adb2_item.attrib["Value"] = data_row["Ad_Break_2"].values[0]

        [adb3_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_3']")
        adb3_item.attrib["Value"] = data_row["Ad_Break_3"].values[0]

        [adb4_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_4']")
        adb4_item.attrib["Value"] = data_row["Ad_Break_4"].values[0]

        [adb5_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_5']")
        adb5_item.attrib["Value"] = data_row["Ad_Break_5"].values[0]

        [adb6_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_6']")
        adb6_item.attrib["Value"] = data_row["Ad_Break_6"].values[0]

        [adb7_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_7']")
        adb7_item.attrib["Value"] = data_row["Ad_Break_7"].values[0]

        [adb8_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_8']")
        adb8_item.attrib["Value"] = data_row["Ad_Break_8"].values[0]

        [adb9_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_9']")
        adb9_item.attrib["Value"] = data_row["Ad_Break_9"].values[0]

        [adb10_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_10']")
        adb10_item.attrib["Value"] = data_row["Ad_Break_10"].values[0]

        [adb11_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_11']")
        adb11_item.attrib["Value"] = data_row["Ad_Break_11"].values[0]

        [adb12_item] = root.findall("./Asset/Asset/Metadata/App_Data[@Name='Ad_Break_12']")
        adb12_item.attrib["Value"] = data_row["Ad_Break_12"].values[0]

        # Caption Section should go after the 'Movie' asset

        # ET.SubElement(item, "App_Data", {"App": "MOD", "Name": "Actors", "Value": data_row["Actors"].values[0]})
        
        ET.indent(root, space="    ")
        tree.write(os.path.join(output_dir, file))
        
