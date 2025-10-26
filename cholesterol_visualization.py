import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cholesterol_visualization(healthy_data, diseased_data,
                                   abnormal_cls_healthy, abnormal_cls_diseased,
                                   normal_cls_healthy, normal_cls_diseased,
                                   male_abnormal_cls_healthy_pct, female_abnormal_cls_healthy_pct,
                                   male_abnormal_cls_diseased_pct, female_abnormal_cls_diseased_pct,
                                   kde_bw_adjust=2.0, scatter_alpha=0.3, kde_shade=True):
    """Generates the Cholesterol vs. Age visualization."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 9), gridspec_kw={'height_ratios': [0.7, 3]})
    plt.subplots_adjust(hspace=0.1)

    # --- Top KDE Plots (Age Distribution by Sex) ---
    ax1_colors = ["#0000FF", "#FFC0CB"] # Blue for M, Pink for F
    ax2_colors = ["#FF0000", "#FFA07A"] # Red for M, Light Red for F

    for ax in [ax1, ax2]:
        for i in ["top", "right", "left", "bottom"]:
            ax.spines[i].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(25, 85)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.get_legend().remove() # Remove default legend

    # Healthy KDE by Sex
    sns.kdeplot(data=healthy_data, x="Age", bw_adjust=kde_bw_adjust, ax=ax1, hue="Sex", palette=ax1_colors, lw=1, fill=kde_shade)
    ax1.text(33, 0.01, f"Age\nMale-{male_abnormal_cls_healthy_pct:.1f}%", fontsize=9, fontweight="normal", horizontalalignment="right")
    ax1.text(45, 0.005, f"Age\nFemale-{female_abnormal_cls_healthy_pct:.1f}%", fontsize=9, fontweight="normal", horizontalalignment="left")
    ax1.set_title("Age Distribution by Sex (Healthy)", fontsize=12)


    # Diseased KDE by Sex
    sns.kdeplot(data=diseased_data, x="Age", bw_adjust=kde_bw_adjust, ax=ax2, hue="Sex", palette=ax2_colors, lw=1, fill=kde_shade)
    ax2.text(45, 0.02, f"Age\nMale-{male_abnormal_cls_diseased_pct:.1f}%", fontsize=9, fontweight="normal", horizontalalignment="right")
    ax2.text(50, 0.006, f"Age\nFemale-{female_abnormal_cls_diseased_pct:.1f}%", fontsize=9, fontweight="normal", horizontalalignment="left")
    ax2.set_title("Age Distribution by Sex (Diseased)", fontsize=12)


    # --- Bottom Scatter/KDE Plots (Age vs Cholesterol) ---
    cholesterol_threshold = 200

    # Healthy Scatter/KDE
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    # Filter out Cholesterol == 0 for KDE plot if desired, as it skews the density
    kde_data_healthy = abnormal_cls_healthy[abnormal_cls_healthy['Cholesterol'] > 0]
    if not kde_data_healthy.empty:
        sns.kdeplot(data=kde_data_healthy, x="Age", y="Cholesterol", cmap="Blues", shade=kde_shade, ax=ax3, bw_adjust=.5)
    ax3.scatter(abnormal_cls_healthy["Age"], abnormal_cls_healthy["Cholesterol"], color="#0000FF", marker=".") # Blue for abnormal healthy
    ax3.scatter(normal_cls_healthy["Age"], normal_cls_healthy["Cholesterol"], color="#ADD8E6", marker=".", alpha=scatter_alpha) # Light Blue for normal healthy
    ax3.set_ylim(-5, 650)
    ax3.set_xlim(25, 85)
    ax3.set_xticks([30, 40, 50, 60, 70, 80])
    ax3.set_yticks([])
    ax3.set_xlabel("Age")
    ax3.set_ylabel("") # Add Label "Cholesterol" if desired
    ax3.axhline(y=cholesterol_threshold, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    ax3.text(24, 350, f'High cholesterol\n> {cholesterol_threshold} mg/dL', horizontalalignment='right', verticalalignment='center')
    ax3.text(24, cholesterol_threshold, f'{cholesterol_threshold}', horizontalalignment='right', verticalalignment='center')
    ax3.set_title("Healthy: Age vs Cholesterol", fontsize=12)

    # Diseased Scatter/KDE
    ax4.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    kde_data_diseased = abnormal_cls_diseased[abnormal_cls_diseased['Cholesterol'] > 0]
    if not kde_data_diseased.empty:
        sns.kdeplot(data=kde_data_diseased, x="Age", y="Cholesterol", cmap="Reds", shade=kde_shade, ax=ax4, bw_adjust=.5)
    ax4.scatter(abnormal_cls_diseased["Age"], abnormal_cls_diseased["Cholesterol"], color="#FF0000", marker=".") # Red for abnormal diseased
    ax4.scatter(normal_cls_diseased["Age"], normal_cls_diseased["Cholesterol"], marker=".", color="#FFA07A", alpha=scatter_alpha) # Light Red for normal diseased
    ax4.set_ylim(-5, 650)
    ax4.set_xlim(25, 85)
    ax4.set_xticks([30, 40, 50, 60, 70, 80])
    ax4.set_yticks([])
    ax4.set_xlabel("Age")
    ax4.set_ylabel("")
    ax4.axhline(y=cholesterol_threshold, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    ax4.text(24, 350, f'High cholesterol\n> {cholesterol_threshold} mg/dL', horizontalalignment='right', verticalalignment='center')
    ax4.text(24, cholesterol_threshold, f'{cholesterol_threshold}', horizontalalignment='right', verticalalignment='center')
    ax4.set_title("Diseased: Age vs Cholesterol", fontsize=12)


    st.pyplot(fig)
