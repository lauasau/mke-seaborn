# :book: Introduction

Today, I will be practicing my Python skills! Specifically, I want to create a number of different visualizations by utilizing the 'seaborn' library. 
Seaborn is one of my favorite libraries since it is so easy to learn and because it creates such beautiful plots!

<img width="580" height="180" alt="image" src="https://github.com/user-attachments/assets/18680e3c-f450-44c5-90ed-abfe5316bf6b" />


## :chart_with_downwards_trend:Obtaining and Importing the Data
Once again, I will be working with Milwaukee crime data. The dataset that I will be utilizing is available on the 'City of Milwaukee' open data portal, [here](https://data.milwaukee.gov/group/public-safety)

For this analysis, we will be needing to import the following libraries: pandas, numpy, matplotlib.pyplot, matplotlib.ticker, and seaborn.
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
```
## :file_folder: Loading and Prepping the Data
Using the pandas function ```pd.read_excel()```, we will then load the data from our Excel spreadsheet file into a pandas Dataframe. In this case, our Excel file is named "WIBRS F copy 2.xlsx." We will also define the list of the crime-category column name from our dataset.
```python
df = pd.read_excel('WIBRS F copy 2.xlsx')
offense_cols = ['AssaultOffense','VehicleTheft','CriminalDamage','Theft','LockedVehicle',
                 'Burglary','Robbery','SexOffense','Arson','Homicide']
```
## :paintbrush: Styling the Color Palette
Next, I will be selecting which color palette I want to use for my charts. Seaborn has numerous palettes that you can choose from, and you can even create your own. I will be using the palette 'vlag.' Vlag is a diverging colormap, so I will have to add some extra code to make sure that every bar is visibly blue or red and none of them get stuck in the washed-out white gap. 
```python
# ---------- Style: light shaded theme + one shared palette ----------
sns.set_theme(style='darkgrid')

#Shared palette family used everywhere
PALETTE = 'vlag'                        
CMAP = sns.color_palette(PALETTE, as_cmap=True)
ACCENT = sns.color_palette(PALETTE, 8)[1]  # single accent color for line/trend charts
 
def bone_bars(n):
#Sample the palette while skipping its washed-out white middle band \nso every bar stays visible against the shaded background
    if n == 1:
        pts = [0.15]
    else:
        pts = []
        for i in range(n):
            t = i / (n - 1)
            pts.append(t * 0.4 if t < 0.5 else 0.6 + (t - 0.5) * 0.8)
    return sns.color_palette([CMAP(x) for x in pts])
```






