import os
import pandas as pd

#Variables of the second window (from existing)
number_ext = os.environ.get("number_ext")
number_inj = os.environ.get("number_inj")
parambig2 = os.environ.get("parambig2")
paramsmall12 = os.environ.get("paramsmall12")
paramsmall22 = os.environ.get("paramsmall22")
file_path = os.environ.get("file_path")
if file_path:
    df = pd.read_csv(file_path, header=None)
else:
    print("file_path is empty or not set. Unable to load the file.")
