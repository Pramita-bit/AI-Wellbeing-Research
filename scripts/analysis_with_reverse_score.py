import pandas as pd
analysis = pd.read_csv('cleaned_responses.csv')

# retrieving only the total value columns and assigning it to a single variable 
variables = ['Motive','Trust','Vigilance','Well-being']
analysis[variables]


--------------------------
# DESCRIPTIVE STATISTICS #
--------------------------

#descriptive statistics
desc=analysis[variables].describe().round(2)
desc
# mean of age
mean_age= analysis.groupby('Gender')['Age'].mean().round(2)
mean_age
# sd of age
sd_age = analysis.groupby('Gender')['Age'].std().round(2)
sd_age

----------------
# CORRELATION #
----------------

# creating correlation matrix
corr_matrix = analysis[variables].corr(method='pearson')
corr_matrix


-------------
# P-VALUE #
-------------

#p-value calculation
import numpy as np
from scipy.stats import pearsonr
data = analysis[variables]

# empty matrix
p_matrix = pd.DataFrame(np.zeros((len(variables), len(variables))),
                        columns=variables, index=variables)

# fill matrix
for i in range(len(variables)):
    for j in range(len(variables)):
        if i == j:
            p_matrix.iloc[i, j] = 0.0
        else:
            r, p = pearsonr(data.iloc[:,i], data.iloc[:,j])
            p_matrix.iloc[i, j] = p
print(p_matrix)

# presenting p-values as APA stars
def stars(p):
    if p==0:
        return '0'
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


-----------------
# FINAL MATRIX #
-----------------

# combining correlation and star matrix
corr_matrix = data.corr().round(2)
final_matrix = corr_matrix.astype(str)+star_matrix
final_matrix

# Correlation Heatmap 
plt.figure(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# saving everything
corr_matrix.to_csv('correlation.csv')
p_matrix.to_csv('p-value.csv')
final_matrix.to_csv('final_table.csv')
desc.to_csv('descriptiveStat.csv')


-----------------------
# RELIABILITY TESTING #
-----------------------

pip install pingouin
import pingouin as pg

# calculating Cronbach's alpha
Motive_items = analysis[['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14','M15','M16','M17','M18','M19','M20']]
pg.cronbach_alpha(Motive_items)
Trust_items = analysis[['T1','T2','T3']]
pg.cronbach_alpha(Trust_items)
Vigilance_items = analysis[['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12']]
pg.cronbach_alpha(Vigilance_items)
Wellbeing_items = analysis[['W1','W2','W3','W4','W5','W6','W7','W8','W9','W10','W11','W12']]
pg.cronbach_alpha(Wellbeing_items)


## checking internal correlation of Digital Wellbeing Scale items as the reliability is low.
analysis[['W1','W2','W3','W4','W5','W6','W7','W8','W9','W10','W11','W12']].corr()
#Trouble : The 11th and 12th item are reversed and it's not +vely correlating with other items of the same scale. 

# To see if W11 and W12 are the outliers visually with heatmap
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6))
sns.heatmap(Wellbeing_items.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Well-being Item Correlation Heatmap")
plt.show()
