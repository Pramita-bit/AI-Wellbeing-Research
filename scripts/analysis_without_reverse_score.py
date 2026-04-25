import pandas as pd
import numpy as np

analysis_2= pd.read_csv('cleaned_responses.csv')
analysis_2

# dropping negatively scored inconsistant items
items = analysis_2.drop(columns=['W11','W12'])

#re-calculating summations
scale_4_new= analysis_2[['W1','W2','W3','W4','W5','W6','W7','W8','W9','W10']]
analysis_2['Well-being_new'] = scale_4_new.sum(axis=1)

variables=['Motive','Trust','Vigilance','Well-being_new']
analysis_2[variables]


----------------------
# NORMALITY TESTING #
----------------------

# conducting Shapiro-Wilk test
from scipy import stats
shapiro_1 = stats.shapiro(analysis_2['Motive'])
print (shapiro_1)
shapiro_2 = stats.shapiro(analysis_2['Trust'])
print (shapiro_2)
shapiro_3 = stats.shapiro(analysis_2['Vigilance'])
print (shapiro_3)
shapiro_4 = stats.shapiro(analysis_2['Well-being_new'])
print (shapiro_4)

# Visualizing with Q-Q plot
import statsmodels.api as sm
import matplotlib.pyplot as plt

#plotting Q-Q Plot
for var in variables:
    sm.qqplot(analysis_2[var], line='s')
    plt.title(f"Q-Q Plot for {var}")
    plt.show()


---------------------------
# DESCRIPTIVE STATISTICS #
---------------------------

desc = analysis_2[variables].describe().round(2)
desc


-----------------
# CORRELATION #
-----------------

correlation = analysis_2[variables].corr(method='pearson')
correlation


-------------------
# P-VALUE MATRIX #
-------------------

from scipy.stats import pearsonr
data = analysis_2[variables]

#empty matrix
p_matrix = pd.DataFrame(np.zeros((len(variables),len(variables))), columns=variables, index=variables)

#fill matrix
for i in range(len(variables)):
    for j in range(len(variables)):
        if i==j:
            p_matrix.iloc[i,j]=0.0
        else:
            r, p = pearsonr(data.iloc[:,i], data.iloc[:,j])
            p_matrix.iloc[i, j] = p

p_matrix

# APA stars indicating p-values
def stars(p):
    if p==0:
        return'0'
    elif p<0.001:
        return'***'
    elif p<0.01:
        return'**'
    elif p<0.05:
        return'*'
    else:
        return''

star_matrix=p_matrix.map(stars)
star_matrix


-------------------
# FINAL MATRIX #
-------------------

# combining correlation and p-value matrix
final_matrix = correlation.round(2).astype(str)+star_matrix
final_matrix


-----------------------
# RELIABILITY TESTING #
-----------------------

# computing Cronbach's alpha
import pingouin as pg
Motive_items = analysis_2[['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14','M15','M16','M17','M18','M19','M20']]
pg.cronbach_alpha(Motive_items)
Trust_items = analysis_2[['T1','T2','T3']]
pg.cronbach_alpha(Trust_items)
Vigilance_items = analysis_2[['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12']]
pg.cronbach_alpha(Vigilance_items)
Wellbeing_items = analysis_2[['W1','W2','W3','W4','W5','W6','W7','W8','W9','W10']]
pg.cronbach_alpha(Wellbeing_items)


-------------------
# VISUALIZATION #
-------------------

# correlation heatmap
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 4))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()
