# Interactive Heart Failure Analysis Dashboard

This project is an interactive web application built in Python for analyzing the "Heart Failure Prediction" dataset. It provides a user-friendly dashboard to visually explore the complex relationships between various clinical features and the presence of heart disease.

The dashboard is built using Streamlit for the web interface and Pandas, Matplotlib, and Seaborn for data manipulation and advanced visualization.

## Key Features:

* **Interactive Dashboard:** Developed using Streamlit to allow users to dynamically select from multiple visualizations.
* **Data Processing:** Utilizes Pandas for efficient loading and preprocessing of the dataset, creating subsets for healthy and diseased patients, and filtering by specific clinical criteria (e.g., blood pressure ranges, cholesterol levels).
* **Advanced Visualization:** Implements custom, multi-panel plots using Matplotlib and Seaborn to analyze key factors, including:
  * Blood Pressure vs. Age (comparing healthy vs. diseased)
  * Cholesterol vs. Age (broken down by sex and health status)
  * Max Heart Rate vs. Age (analyzing the impact of exercise-induced angina)
  * Resting ECG Results vs. Blood Pressure
* **Statistical Insights:** Leverages Kernel Density Estimation (KDE) plots and scatter plots to reveal underlying distributions and trends within the data.

**Technologies Used:** Python, Streamlit, Pandas, Matplotlib, Seaborn

## Installation
**Clone the repository (or download the files):**

```shell
git clone https://github.com/shammeer-s/heartfailureanalysis.git
cd heartfailureanalysis
```

**Install the required libraries:**

```shell
pip install -r requirements.txt
```

**Running the Application**
* Navigate to the project's root directory in your terminal.

* Run the following command:
```shell
streamlit run app.py
```

Streamlit will automatically open the dashboard in your default web browser. From there, you can use the sidebar to select a visualization and adjust its parameters.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
