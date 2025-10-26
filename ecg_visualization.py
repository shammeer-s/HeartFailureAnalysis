import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ecg_visualization(diseased_data,
                           resting_ecg_normal_bp_dis, resting_ecg_st_bp_dis, resting_ecg_lvh_bp_dis,
                           male_normal_ecg_pct, female_normal_ecg_pct,
                           male_st_ecg_pct, female_st_ecg_pct,
                           male_lvh_ecg_pct, female_lvh_ecg_pct,
                           kde_bw_adjust=2.0, scatter_alpha=0.5, kde_shade=True):
    """Generates the Resting ECG vs. Blood Pressure visualization for diseased patients."""

    if diseased_data is None or diseased_data.empty:
        st.warning("No diseased data available for ECG visualization.")
        return

    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(20, 9), gridspec_kw={'height_ratios': [0.7, 3]})
    plt.subplots_adjust(hspace=0.1)

    # --- Top KDE Plots (Age Distribution by Sex for each ECG type) ---
    ax_colors = ["#FF0000", "#FFA07A"] # Red for M, Light Red for F

    # Setup common axes properties
    for ax in [ax1, ax2, ax3]:
        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(25, 85)
        ax.set_xlabel("")
        ax.set_ylabel("")
        if not ax.get_legend() is None:
            ax.get_legend().remove()

    # Normal ECG KDE
    if not resting_ecg_normal_bp_dis.empty:
        sns.kdeplot(data=resting_ecg_normal_bp_dis, x="Age", bw_adjust=kde_bw_adjust, ax=ax1, hue="Sex", palette=ax_colors, lw=1, fill=kde_shade)
        ax1.text(43, 0.02, f"Age\nMale-{male_normal_ecg_pct:.1f}%", fontsize=9, ha='right')
        ax1.text(50, 0.005, f"Age\nFemale-{female_normal_ecg_pct:.1f}%", fontsize=9, ha='left')
    ax1.set_title("Age Dist by Sex (ECG Normal)", fontsize=10)


    # ST ECG KDE
    if not resting_ecg_st_bp_dis.empty:
        sns.kdeplot(data=resting_ecg_st_bp_dis, x="Age", bw_adjust=kde_bw_adjust, ax=ax2, hue="Sex", palette=ax_colors, lw=1, fill=kde_shade)
        ax2.text(47, 0.02, f"Age\nMale-{male_st_ecg_pct:.1f}%", fontsize=9, ha='right')
        ax2.text(50, 0.004, f"Age\nFemale-{female_st_ecg_pct:.1f}%", fontsize=9, ha='left')
    ax2.set_title("Age Dist by Sex (ECG ST)", fontsize=10)


    # LVH ECG KDE
    if not resting_ecg_lvh_bp_dis.empty:
        sns.kdeplot(data=resting_ecg_lvh_bp_dis, x="Age", bw_adjust=kde_bw_adjust, ax=ax3, hue="Sex", palette=ax_colors, lw=1, fill=kde_shade)
        ax3.text(48, 0.02, f"Age\nMale-{male_lvh_ecg_pct:.1f}%", fontsize=9, ha='right')
        ax3.text(50, 0.009, f"Age\nFemale-{female_lvh_ecg_pct:.1f}%", fontsize=9, ha='left')
    ax3.set_title("Age Dist by Sex (ECG LVH)", fontsize=10)


    # --- Bottom Scatter/KDE Plots (Age vs RestingBP for each ECG type) ---
    bp_min, bp_max = 115, 155

    # Setup common axes properties
    for ax in [ax4, ax5, ax6]:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylim(80, 210)
        ax.set_xlim(25, 85)
        ax.set_xticks([30, 40, 50, 60, 70, 80])
        ax.set_yticks([])
        ax.set_xlabel("Age")
        ax.set_ylabel("") # Add BP Label if desired
        ax.axhline(y=bp_max + 0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
        ax.axhline(y=bp_min - 0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
        ax.text(24, (bp_min+bp_max)/2, f'Normal BP\n({bp_min}-{bp_max} mmHg)', ha='right', va='center', fontsize=9)

    # Normal ECG Scatter/KDE
    if not resting_ecg_normal_bp_dis.empty:
        sns.kdeplot(data=resting_ecg_normal_bp_dis, x="Age", y="RestingBP", cmap="Reds", bw_adjust=0.5, shade=kde_shade, ax=ax4)
        ax4.scatter(resting_ecg_normal_bp_dis["Age"], resting_ecg_normal_bp_dis["RestingBP"], color="#FF0000", marker=".", alpha=scatter_alpha) # Red points
    ax4.set_title("ECG Normal: Age vs Resting BP", fontsize=10, fontweight="bold")


    # ST ECG Scatter/KDE
    if not resting_ecg_st_bp_dis.empty:
        sns.kdeplot(data=resting_ecg_st_bp_dis, x="Age", y="RestingBP", cmap="Reds", bw_adjust=0.5, ax=ax5, shade=kde_shade)
        ax5.scatter(resting_ecg_st_bp_dis["Age"], resting_ecg_st_bp_dis["RestingBP"], color="#FF0000", marker=".", alpha=scatter_alpha)
    ax5.set_title("ECG ST: Age vs Resting BP", fontsize=10, fontweight="bold")
    ax5.text(27, 188, "ST-T wave abnormality", fontsize=9, ha='left')

    # LVH ECG Scatter/KDE
    if not resting_ecg_lvh_bp_dis.empty:
        sns.kdeplot(data=resting_ecg_lvh_bp_dis, x="Age", y="RestingBP", cmap="Reds", shade=kde_shade, bw_adjust=.5, ax=ax6)
        ax6.scatter(resting_ecg_lvh_bp_dis["Age"], resting_ecg_lvh_bp_dis["RestingBP"], color="#FF0000", marker=".", alpha=scatter_alpha)
    ax6.set_title("ECG LVH: Age vs Resting BP", fontsize=10, fontweight="bold")
    ax6.text(27, 188, "Left ventricular hypertrophy", fontsize=9, ha='left')

    st.pyplot(fig)
