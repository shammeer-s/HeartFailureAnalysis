import streamlit as st
import pandas as pd
import os

# Use caching to load data only once
@st.cache_data
def load_data(file_path="input/heart.csv"):
    """Loads the heart failure prediction dataset."""
    # Since Streamlit runs from the app's directory, adjust the path if needed
    # Check if the default path exists, otherwise prompt for upload
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Basic preprocessing: Handle potential missing values if any (example: fill with 0)
            # A better strategy might be needed depending on the actual data
            df.fillna(0, inplace=True)
            # Convert Cholesterol 0 values to NaN potentially, then impute, or handle as is.
            # For this example, we'll keep 0s as they might represent missing data handled this way in the notebook.
            return df
        except Exception as e:
            st.error(f"Error loading data from path: {e}")
            return None
    else:
        st.warning(f"Default data file not found at {file_path}. Please upload the 'heart.csv' file.")
        uploaded_file = st.file_uploader("Upload heart.csv", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                df.fillna(0, inplace=True)
                return df
            except Exception as e:
                st.error(f"Error loading uploaded file: {e}")
                return None
        else:
            return None

def preprocess_data_for_viz(df):
    """Preprocesses data specifically for the visualizations."""
    if df is None:
        return None, None, None, None, None, None, None, None, None, None, None, None, None

    # Common preprocessing
    diseased_data = df.loc[df["HeartDisease"] == 1, :].copy()
    healthy_data = df.loc[df["HeartDisease"] == 0, :].copy()

    # --- BP Visualization Data ---
    abnormal_bp_healthy = healthy_data.loc[(healthy_data["RestingBP"] < 115) | (healthy_data["RestingBP"] > 155), :].copy()
    abnormal_bp_diseased = diseased_data.loc[(diseased_data["RestingBP"] < 115) | (diseased_data["RestingBP"] > 155), :].copy()
    normal_bp_healthy = healthy_data.loc[(healthy_data["RestingBP"] >= 115) & (healthy_data["RestingBP"] <= 155), :].copy()
    normal_bp_diseased = diseased_data.loc[(diseased_data["RestingBP"] >= 115) & (diseased_data["RestingBP"] <= 155), :].copy()

    # --- Cholesterol Visualization Data ---
    abnormal_cls_healthy = healthy_data.loc[healthy_data["Cholesterol"] > 200, :].copy()
    abnormal_cls_diseased = diseased_data.loc[diseased_data["Cholesterol"] > 200, :].copy()
    normal_cls_healthy = healthy_data.loc[healthy_data["Cholesterol"] <= 200, :].copy() # Includes 0 values
    normal_cls_diseased = diseased_data.loc[diseased_data["Cholesterol"] <= 200, :].copy() # Includes 0 values

    male_abnormal_cls_healthy_pct = 0
    female_abnormal_cls_healthy_pct = 0
    if not abnormal_cls_healthy.empty:
        male_abnormal_cls_healthy_pct = (len(abnormal_cls_healthy.loc[abnormal_cls_healthy["Sex"] == "M", :]) / len(abnormal_cls_healthy)) * 100
        female_abnormal_cls_healthy_pct = (len(abnormal_cls_healthy.loc[abnormal_cls_healthy["Sex"] == "F", :]) / len(abnormal_cls_healthy)) * 100

    male_abnormal_cls_diseased_pct = 0
    female_abnormal_cls_diseased_pct = 0
    if not abnormal_cls_diseased.empty:
        male_abnormal_cls_diseased_pct = (len(abnormal_cls_diseased.loc[abnormal_cls_diseased["Sex"] == "M", :]) / len(abnormal_cls_diseased)) * 100
        female_abnormal_cls_diseased_pct = (len(abnormal_cls_diseased.loc[abnormal_cls_diseased["Sex"] == "F", :]) / len(abnormal_cls_diseased)) * 100


    # --- ECG Visualization Data ---
    resting_ecg_normal_bp_dis = diseased_data.loc[diseased_data["RestingECG"]=="Normal", :].copy()
    resting_ecg_st_bp_dis = diseased_data.loc[diseased_data["RestingECG"]=="ST", :].copy()
    resting_ecg_lvh_bp_dis = diseased_data.loc[diseased_data["RestingECG"]=="LVH", :].copy()

    male_normal_ecg_pct = 0
    female_normal_ecg_pct = 0
    if not resting_ecg_normal_bp_dis.empty:
        male_normal_ecg_pct = (len(resting_ecg_normal_bp_dis[resting_ecg_normal_bp_dis['Sex'] == 'M']) / len(resting_ecg_normal_bp_dis)) * 100
        female_normal_ecg_pct = (len(resting_ecg_normal_bp_dis[resting_ecg_normal_bp_dis['Sex'] == 'F']) / len(resting_ecg_normal_bp_dis)) * 100

    male_st_ecg_pct = 0
    female_st_ecg_pct = 0
    if not resting_ecg_st_bp_dis.empty:
        male_st_ecg_pct = (len(resting_ecg_st_bp_dis[resting_ecg_st_bp_dis['Sex'] == 'M']) / len(resting_ecg_st_bp_dis)) * 100
        female_st_ecg_pct = (len(resting_ecg_st_bp_dis[resting_ecg_st_bp_dis['Sex'] == 'F']) / len(resting_ecg_st_bp_dis)) * 100

    male_lvh_ecg_pct = 0
    female_lvh_ecg_pct = 0
    if not resting_ecg_lvh_bp_dis.empty:
        male_lvh_ecg_pct = (len(resting_ecg_lvh_bp_dis[resting_ecg_lvh_bp_dis['Sex'] == 'M']) / len(resting_ecg_lvh_bp_dis)) * 100
        female_lvh_ecg_pct = (len(resting_ecg_lvh_bp_dis[resting_ecg_lvh_bp_dis['Sex'] == 'F']) / len(resting_ecg_lvh_bp_dis)) * 100


    return (df, diseased_data, healthy_data,
            abnormal_bp_healthy, abnormal_bp_diseased,
            normal_bp_healthy, normal_bp_diseased,
            abnormal_cls_healthy, abnormal_cls_diseased,
            normal_cls_healthy, normal_cls_diseased,
            male_abnormal_cls_healthy_pct, female_abnormal_cls_healthy_pct,
            male_abnormal_cls_diseased_pct, female_abnormal_cls_diseased_pct,
            resting_ecg_normal_bp_dis, resting_ecg_st_bp_dis, resting_ecg_lvh_bp_dis,
            male_normal_ecg_pct, female_normal_ecg_pct,
            male_st_ecg_pct, female_st_ecg_pct,
            male_lvh_ecg_pct, female_lvh_ecg_pct
            )

