import streamlit as st
import pandas as pd
from missing_handler import analyze_missing_data, fill_missing_data
from outlier_detector import detect_outliers_iqr
from type_corrector import correct_dtypes
from category_normalizer import normalize_categories
from report_generator import generate_pdf_report




st.set_page_config(page_title = "Smart Data Cleaner", layout = "centered")

st.title("Smart Data Cleaner")
st.markdown("This application analyzes and corrects missing information in the data you upload.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Original Data")
    st.dataframe(df)

    st.subheader("Missing Data Analysis")
    missing_info = analyze_missing_data(df)

    st.subheader("Outlier Detection (IQR Method)")
    outliers = detect_outliers_iqr(df)

    if outliers:
        for col, indexes in outliers.items():
            st.warning(f" **{col}** column has {len(indexes)} outlier values detected.")
            st.dataframe(df.loc[indexes, [col]])
    else:
        st.success("No outliers detected")

        st.subheader(" Data Type Correction")
        if st.button("Auto-Correct Data Types"):
            corrected_df = correct_dtypes(df.copy())
            st.success("Data types successfully corrected!")
            st.dataframe(corrected_df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Type'}))

    if not missing_info.empty:
        st.dataframe(missing_info)

        st.subheader("Generate PDF Report")
        if st.button("Create and Download PDF Report"):
            pdf_bytes = generate_pdf_report(missing_info)
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="data_cleaning_report.pdf",
                mime="application/pdf"
            )

        st.subheader("Fill in Missing Data")
        strategy = st.selectbox("Choose a Strategy", ["mean", "median", "mode"])

        if st.button("Fill & Display"):
            cleaned_df = fill_missing_data(df.copy(), strategy)
            cleaned_df = normalize_categories(cleaned_df)

            st.success("Missing data successfully filled and categories normalized!!")
            st.subheader("Cleaned Data")
            st.dataframe(cleaned_df)

            csv = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label = "Download Cleaned CSV",
                data = csv,
                file_name = 'cleaned_data.csv',
                mime = 'text/csv'
            )

    else:
        st.success("There is no missing information in the data")

else:
    st.info("To get started, upload a CSV file.")