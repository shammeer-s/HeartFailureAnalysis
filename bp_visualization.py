import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bp_visualization(healthy_data, diseased_data,
                          abnormal_bp_healthy, abnormal_bp_diseased,
                          normal_bp_healthy, normal_bp_diseased,
                          kde_bw_adjust=2.0, scatter_alpha=0.5, kde_shade=True):
    """Generates the Blood Pressure vs. Age visualization."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 9), gridspec_kw={'height_ratios': [0.7, 3]})
    plt.subplots_adjust(hspace=0.1)

    # --- Top KDE Plots (Age Distribution) ---
    for ax in [ax1, ax2]:
        for i in ["top", "right", "left", "bottom"]:
            ax.spines[i].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(25, 85)
        ax.set_xlabel("")
        ax.set_ylabel("")

    # Healthy KDE
    sns.kdeplot(healthy_data["Age"], bw_adjust=kde_bw_adjust, ax=ax1, color="#0000FF", lw=1, fill=kde_shade) # Blue for healthy
    ax1.axhline(y=0.02, xmin=0.22, xmax=0.62, color='k', linestyle='--', alpha=0.3)
    ax1.text(25, 0.01, "Age", fontsize=9, fontweight="normal", horizontalalignment="left")
    ax1.set_title("Age Distribution (Healthy)", fontsize=12)

    # Diseased KDE
    sns.kdeplot(diseased_data["Age"], bw_adjust=kde_bw_adjust, ax=ax2, color="#FF0000", lw=1, fill=kde_shade) # Red for diseased
    ax2.axhline(y=0.02, xmin=0.35, xmax=0.71, color='k', linestyle='--', alpha=0.3)
    ax2.text(25, 0.01, "Age", fontsize=9, fontweight="normal", horizontalalignment="left")
    ax2.set_title("Age Distribution (Diseased)", fontsize=12)

    # --- Bottom Scatter/KDE Plots (Age vs RestingBP) ---
    bp_min, bp_max = 115, 155 # Define normal BP range

    # Healthy Scatter/KDE
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    sns.kdeplot(data=normal_bp_healthy, x="Age", y="RestingBP", cmap="Blues", ax=ax3, shade=kde_shade, bw_adjust=.5)
    ax3.scatter(abnormal_bp_healthy["Age"], abnormal_bp_healthy["RestingBP"], color="#ADD8E6", marker=".", alpha=scatter_alpha) # Light blue for abnormal healthy
    ax3.scatter(normal_bp_healthy["Age"], normal_bp_healthy["RestingBP"], color="#0000FF", marker=".") # Blue for normal healthy
    ax3.set_ylim(80, 210)
    ax3.set_xlim(25, 85)
    ax3.set_xticks([30, 40, 50, 60, 70, 80])
    ax3.set_yticks([]) # Keep Y axis labels consistent with original if needed, or simplify
    ax3.set_ylabel("") # Add label "Resting BP" if desired
    ax3.set_xlabel("Age")
    ax3.axhline(y=bp_max + 0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    ax3.axhline(y=bp_min - 0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    ax3.text(24, (bp_min+bp_max)/2 , f'Normal BP\n({bp_min}-{bp_max} mmHg)', horizontalalignment='right', verticalalignment='center')
    ax3.set_title("Healthy: Age vs Resting BP", fontsize=12)


    # Diseased Scatter/KDE
    ax4.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    sns.kdeplot(data=normal_bp_diseased, x="Age", y="RestingBP", cmap="Reds", ax=ax4, shade=kde_shade, bw_adjust=.5)
    ax4.scatter(abnormal_bp_diseased["Age"], abnormal_bp_diseased["RestingBP"], color="#FFA07A", marker=".", alpha=scatter_alpha) # Light red for abnormal diseased
    ax4.scatter(normal_bp_diseased["Age"], normal_bp_diseased["RestingBP"], color="#FF0000", marker=".") # Red for normal diseased
    ax4.set_ylabel("")
    ax4.set_xlabel("Age")
    ax4.set_ylim(80, 210)
    ax4.set_xlim(25, 85)
    ax4.set_xticks([30, 40, 50, 60, 70, 80])
    ax4.set_yticks([])
    ax4.axhline(y=bp_max + 0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    ax4.axhline(y=bp_min - 0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    ax4.text(24, (bp_min+bp_max)/2 , f'Normal BP\n({bp_min}-{bp_max} mmHg)', horizontalalignment='right', verticalalignment='center')
    ax4.set_title("Diseased: Age vs Resting BP", fontsize=12)

    st.pyplot(fig)
