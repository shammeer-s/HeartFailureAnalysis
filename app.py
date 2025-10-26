import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.interpolate import interp1d

# Import functions from other modules
from data_loader import load_data, preprocess_data_for_viz
from bp_visualization import plot_bp_visualization
from cholesterol_visualization import plot_cholesterol_visualization
from angina_visualization import plot_angina_visualization
from ecg_visualization import plot_ecg_visualization

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Heart Failure Analysis")
st.title("Heart Failure Analysis Dashboard")

# --- Load and Prepare Data ---
# Attempt to load data using the loader function
# Provide a default path or let the user upload
df_raw = load_data() # You might need to adjust the default path inside load_data

if df_raw is not None:
    # Preprocess data once and reuse
    (df, diseased_data, healthy_data,
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
     ) = preprocess_data_for_viz(df_raw)

    if df is not None:
        # --- Sidebar Controls ---
        st.sidebar.header("Visualization Options")
        viz_choice = st.sidebar.selectbox(
            "Choose Visualization:",
            ["Blood Pressure vs Age", "Cholesterol vs Age", "Angina vs Max HR", "Resting ECG vs BP"]
        )

        st.sidebar.markdown("---")
        st.sidebar.header("Plot Parameters")

        # Common parameters
        kde_shade = st.sidebar.checkbox("Shade KDE Plots", value=True)
        scatter_alpha = st.sidebar.slider("Scatter Point Alpha", 0.1, 1.0, 0.4, 0.05)
        kde_bw = st.sidebar.slider("KDE Bandwidth Adjustment", 0.1, 5.0, 1.0, 0.1) # General KDE BW Adjust

        # Specific parameters if needed (e.g., Angina interpolation)
        interpolation_kind = 'cubic'
        if viz_choice == "Angina vs Max HR":
            interpolation_kind = st.sidebar.selectbox(
                "Interpolation Method (Angina Plot)",
                ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic'],
                index=5 # Default to cubic
            )


        # --- Display Selected Visualization ---
        st.header(viz_choice)

        if viz_choice == "Blood Pressure vs Age":
            st.markdown("Comparing Resting Blood Pressure against Age for Healthy and Diseased individuals. The dashed lines indicate a 'normal' BP range (115-155 mmHg).")
            plot_bp_visualization(healthy_data, diseased_data,
                                  abnormal_bp_healthy, abnormal_bp_diseased,
                                  normal_bp_healthy, normal_bp_diseased,
                                  kde_bw_adjust=kde_bw, scatter_alpha=scatter_alpha, kde_shade=kde_shade)

        elif viz_choice == "Cholesterol vs Age":
            st.markdown("Comparing Cholesterol levels against Age for Healthy and Diseased individuals, broken down by sex in the top plots. The dashed line indicates the threshold for 'high' cholesterol (> 200 mg/dL). Note: Cholesterol values of 0 are plotted but excluded from KDE calculations.")
            plot_cholesterol_visualization(healthy_data, diseased_data,
                                           abnormal_cls_healthy, abnormal_cls_diseased,
                                           normal_cls_healthy, normal_cls_diseased,
                                           male_abnormal_cls_healthy_pct, female_abnormal_cls_healthy_pct,
                                           male_abnormal_cls_diseased_pct, female_abnormal_cls_diseased_pct,
                                           kde_bw_adjust=kde_bw, scatter_alpha=scatter_alpha, kde_shade=kde_shade)

        elif viz_choice == "Angina vs Max HR":
            st.markdown("Analyzing the relationship between Maximum Heart Rate (MaxHR) and Age for Diseased patients, comparing those with and without Exercise-Induced Angina. Smaller plots show trends broken down by Chest Pain Type (TA, ATA, NAP, ASY).")
            plot_angina_visualization(diseased_data, interpolation_kind=interpolation_kind)

        elif viz_choice == "Resting ECG vs BP":
            st.markdown("Comparing Resting Blood Pressure against Age for Diseased individuals, categorized by their Resting ECG results (Normal, ST, LVH). Top plots show age distribution by sex for each ECG category.")
            plot_ecg_visualization(diseased_data,
                                   resting_ecg_normal_bp_dis, resting_ecg_st_bp_dis, resting_ecg_lvh_bp_dis,
                                   male_normal_ecg_pct, female_normal_ecg_pct,
                                   male_st_ecg_pct, female_st_ecg_pct,
                                   male_lvh_ecg_pct, female_lvh_ecg_pct,
                                   kde_bw_adjust=kde_bw, scatter_alpha=scatter_alpha, kde_shade=kde_shade)

        # --- Optional: Display Raw Data ---
        if st.sidebar.checkbox("Show Raw Data Sample"):
            st.subheader("Raw Data Sample")
            st.dataframe(df.head())

    else:
        st.error("Failed to preprocess data. Cannot display visualizations.")

else:
    # This message is shown if load_data returns None (e.g., file not found and not uploaded)
    st.info("Please upload the 'heart.csv' dataset using the file uploader above to view the visualizations.")
