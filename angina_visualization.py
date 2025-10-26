import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.gridspec import GridSpec

def plot_angina_visualization(diseased_data, interpolation_kind='cubic'):
    """Generates the Exercise Angina vs Max Heart Rate visualization for diseased patients."""
    if diseased_data is None or diseased_data.empty:
        st.warning("No diseased data available for Angina visualization.")
        return

    # Prepare data
    diseased_hr_induced_nm = diseased_data.loc[diseased_data["ExerciseAngina"]=="Y", ["Age", "MaxHR"]].copy()
    diseased_hr_not_induced_nm = diseased_data.loc[diseased_data["ExerciseAngina"]=="N", ["Age", "MaxHR"]].copy()

    # --- Grouped data for main plot lines ---
    diseased_hr_induced_mean = diseased_hr_induced_nm.groupby(by="Age").mean()
    diseased_hr_not_induced_mean = diseased_hr_not_induced_nm.groupby(by="Age").mean()

    # --- Grouped data for smaller plots (by ChestPainType) ---
    pain_types = ['TA', 'ATA', 'NAP', 'ASY']
    induced_pain_groups = {}
    not_induced_pain_groups = {}

    for pain in pain_types:
        induced_data = diseased_data.loc[(diseased_data["ExerciseAngina"]=="Y") & (diseased_data["ChestPainType"]==pain), ["Age", "MaxHR"]]
        not_induced_data = diseased_data.loc[(diseased_data["ExerciseAngina"]=="N") & (diseased_data["ChestPainType"]==pain), ["Age", "MaxHR"]]

        if not induced_data.empty:
            induced_pain_groups[pain] = induced_data.groupby(by="Age").mean()
        else:
            induced_pain_groups[pain] = None

        if not not_induced_data.empty:
            not_induced_pain_groups[pain] = not_induced_data.groupby(by="Age").mean()
        else:
            not_induced_pain_groups[pain] = None

    # Interpolation function
    def get_interpolated_data(group_data, kind='cubic'):
        if group_data is None or len(group_data) < 2: # Need at least 2 points for interpolation
            return None, None
        try:
            interp_func = interp1d(group_data.index, group_data["MaxHR"], kind=kind, fill_value="extrapolate")
            index_new = np.linspace(group_data.index.min(), group_data.index.max(), 100)
            maxhr_new = interp_func(index_new)
            return index_new, maxhr_new
        except ValueError as e:
            # Handle cases where interpolation might fail (e.g., duplicate index)
            # st.warning(f"Interpolation failed: {e}. Plotting raw mean points.")
            return group_data.index, group_data["MaxHR"] # Fallback to raw mean points


    # Create plot
    fig = plt.figure(constrained_layout=True, figsize=(20, 8))
    gs = GridSpec(2, 3, figure=fig, width_ratios=[2, 1, 1])
    gs.update(wspace = 0.2, hspace = 0.1)
    ax1 = fig.add_subplot(gs[:, 0]) # Main plot
    axes_small = [fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2]),
                  fig.add_subplot(gs[1, 1]), fig.add_subplot(gs[1, 2])] # Small plots

    # --- Main Plot ---
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Plot interpolated lines
    ind_idx, ind_hr = get_interpolated_data(diseased_hr_induced_mean, interpolation_kind)
    nind_idx, nind_hr = get_interpolated_data(diseased_hr_not_induced_mean, interpolation_kind)

    line1, line2 = None, None
    if ind_idx is not None:
        line1, = ax1.plot(ind_idx, ind_hr, color="#FF0000", label="Induced Angina (Y)") # Red for induced
        mean_induced_hr = ind_hr.mean()
        ax1.text(85, mean_induced_hr, f"Avg\n{mean_induced_hr:.1f}", color="#FF0000", alpha=0.7, ha='right', va='bottom', fontsize=12, fontweight=600)
        ax1.axhline(mean_induced_hr, lw=1, ls='--', color="#FF0000", alpha=0.7)

    if nind_idx is not None:
        line2, = ax1.plot(nind_idx, nind_hr, color="#A9A9A9", alpha=0.7, label="Not Induced Angina (N)") # Gray for not induced
        mean_not_induced_hr = nind_hr.mean()
        # Optionally add avg line/text for not induced as well

    # Plot raw data points lightly
    ax1.scatter(diseased_hr_induced_nm['Age'], diseased_hr_induced_nm['MaxHR'], color="#FFA07A", alpha=0.1, s=10) # Light red points
    ax1.scatter(diseased_hr_not_induced_nm['Age'], diseased_hr_not_induced_nm['MaxHR'], color="#D3D3D3", alpha=0.1, s=10) # Light gray points


    ax1.set_xticks([30, 40, 50, 60, 70, 80])
    ax1.set_yticks([90, 120, 150, 180])
    ax1.set_xlim(25, 85)
    ax1.set_ylim(80, 210) # Adjusted ylim based on data range
    ax1.set_xlabel("Age")
    ax1.set_ylabel("Max Heart Rate")
    ax1.set_title("Diseased Patients: Max HR vs Age by Exercise Angina", fontsize=16, fontweight="bold")
    ax1.text(25, 215, "Comparing mean Max HR trend for patients with and without exercise-induced angina.", fontsize=12)

    handles = []
    if line1: handles.append(line1)
    if line2: handles.append(line2)
    if handles: ax1.legend(handles=handles, edgecolor="#FFF")


    # --- Small Plots (By ChestPainType) ---
    pain_titles = {
        'TA': 'Typical Angina', 'ATA': 'Atypical Angina',
        'NAP': 'Non-Anginal Pain', 'ASY': 'Asymptomatic'
    }

    for i, pain in enumerate(pain_types):
        ax = axes_small[i]
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        induced_group = induced_pain_groups[pain]
        not_induced_group = not_induced_pain_groups[pain]

        # Plot raw means if available
        if induced_group is not None:
            ax.plot(induced_group.index, induced_group.MaxHR, color="#FF0000", lw=1, marker='o', markersize=3, linestyle='-')
            mean_hr = induced_group.MaxHR.mean()
            ax.text(85, mean_hr, f"Avg\n{mean_hr:.1f}", color="#FF0000", alpha=0.7, ha='right', va='bottom', fontsize=8, fontweight=600)
            ax.axhline(mean_hr, lw=0.5, ls='--', color="#FF0000", alpha=0.7)

        if not_induced_group is not None:
            ax.plot(not_induced_group.index, not_induced_group.MaxHR, color="#A9A9A9", lw=1, alpha=0.7, marker='x', markersize=3, linestyle=':')

        ax.set_xticks([30, 50, 70])
        ax.set_yticks([90, 120, 150, 180])
        ax.set_xlim(25, 85)
        ax.set_ylim(80, 210) # Consistent Y axis
        ax.set_xlabel("Age", fontsize=9, alpha=0.7)
        ax.set_ylabel("Max HR", fontsize=9, alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_title(f"Pain Type: {pain}\n({pain_titles[pain]})", fontsize=10, fontweight="bold")


    st.pyplot(fig)
