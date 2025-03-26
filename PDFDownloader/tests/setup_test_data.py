import pandas as pd

if __name__ == "__main__":
    test_data_file = "tests/test_data/GRI_sample.xlsx"
    download_data = pd.read_excel(
        io='data/GRI_2017_2020 (1).xlsx',
        sheet_name=0,
        nrows=500,
        index_col="BRnum",
        engine="openpyxl"
    )
    wanted = ["BR50077", "BR50078", "BR50101", "BR50197", "BR50217", "BR50276", "BR50277", "BR50344", "BR50388", "BR50389", "BR50390", "BR50391"]
    filtered_df = download_data[download_data.index.isin(wanted)]
    filtered_df.loc["BR50101", "Pdf_URL"] = None
    filtered_df.loc["BR50391", "Pdf_URL"] = None
    filtered_df.loc["BR50391", "Report Html Address"] = None
    writer = pd.ExcelWriter(test_data_file, engine="openpyxl")
    filtered_df.to_excel(writer, sheet_name="0")
    writer.close()

    test_data_meta_file = "tests/test_data/Metadata_sample.xlsx"
    download_meta_data = pd.read_excel(
        io='data/Metadata2006_2016.xlsx',
        sheet_name="Metadata2006_2016",
        nrows=10,
        index_col="BRnum",
        engine="openpyxl"
    )
    # reset_index2 = download_meta_data.reset_index(drop=True)
    writer2 = pd.ExcelWriter(test_data_meta_file, engine="openpyxl")
    download_meta_data.to_excel(writer2, sheet_name="Metadata2006_2016")
    writer2.close()