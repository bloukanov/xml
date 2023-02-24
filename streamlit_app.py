import os
import xml.etree.ElementTree as ET

import pandas as pd
import streamlit as st
import boto3


bucket_name = "my-bucket-name"
output_folder = "finished_xml_files"


s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

st.title("Create XML Files")
data = st.file_uploader("Upload additional data file", type="csv")

movie_metadata_to_adjust = [
    "Title", 
    "Summary_Short", 
    "Year", 
    "Ad_Content_ID", 
    "Sling_Category", 
    "Licensing_Window_Start", 
    "Licensing_Window_End", 
    "Rating"
]

movie_metadata_to_adjust = st.multiselect(
    "Select metadata to adjust",
    movie_metadata_to_adjust,
    default=movie_metadata_to_adjust    
)

n_ad_break_cols = st.number_input("Number of ad break cols in additional data file", min_value=1, value=12)

vod_metadata_dir = st.selectbox(
    "Select directory containing vod metadata", 
    # Return only directories
    [file.key for file in bucket.objects.all() if file.key.split("/")[-1]==""]
)

if st.button("Submit"):
    for file in bucket.objects.filter(Prefix=vod_metadata_dir):
        if file.key.endswith(".xml"):
            title_nospace = file.key.split(".")[0]
            data_row = data.loc[data["Title_nospace"] == title_nospace]
            tree = ET.fromstring(file.get()["Body"].read())
            root = tree.getroot()
            # title_metadata = root[1][0]
            title_metadata = root.find(".//AMS[@Asset_Class='title']..")  # The .. selects the parent of the AMS element
            movie_metadata = root.find(".//AMS[@Asset_Class='movie']..")
            parent_asset = root.find("./Asset")
            
            for metadata_item in movie_metadata_to_adjust:
                [item] = [child for child in title_metadata if child.get("Name") == metadata_item]
                item.attrib["Value"] = str(data_row[metadata_item].values[0])

            for i in range(n_ad_break_cols):
                if not pd.isnull(data_row[f"Ad_Break_{i+1}"].values[0]):
                    adb_item = root.find(f".//App_Data[@Name='Ad_Break_{i+1}']")
                    adb_item.attrib["Value"] = str(data_row[f"Ad_Break_{i+1}"].values[0])
                else:
                    # Remove the ad break if it's in the vod_metadata xml but not in the data csv
                    if root.find(f".//App_Data[@Name='Ad_Break_{i+1}']") is not None:
                        movie_metadata.remove(root.find(f".//App_Data[@Name='Ad_Break_{i+1}']"))

            parent_asset.insert(2, ET.Element("Asset"))
            caption_asset = parent_asset[2]
            ET.SubElement(caption_asset, "Metadata")
            caption_metadata = caption_asset[0]
            caption_asset_id = movie_metadata.find("AMS").attrib["Asset_ID"].replace("M", "C")
            title = data_row["Title"].values[0]
            ET.SubElement(caption_metadata, "AMS", {"Asset_Class": "closed caption", 
                                                    "Asset_ID": caption_asset_id,
                                                    "Asset_Name": f"{title}-Caption",
                                                    "Creation_Date": root.find("./Metadata/AMS").attrib["Creation_Date"],
                                                    "Description": f"{title}-Caption",
                                                    "Product": "MOD",
                                                    "Provider": "Swerve",
                                                    "Provider_ID": "swerve.tv",
                                                    "Verb": "",
                                                    "Version_Major": "1",
                                                    "Version_Minor": "0"})
            ET.SubElement(caption_metadata, "App_Data", {"App": "MOD", "Name": "Type", "Value": "closed caption"})
            ET.SubElement(caption_asset, "Content", {"Value": f"{title_nospace}.scc"})

            # ET.SubElement(
            #     title_metadata, "App_Data", {"App": "MOD", "Name": "Actors", "Value": data_row["Actors"].values[0]}
            # )
            
            ET.indent(root, space="    ")
            tree.write(os.path.join("tmp", file.key))
            bucket.upload_file(os.path.join("tmp", file.key), output_folder + "/" + file.key)
        
