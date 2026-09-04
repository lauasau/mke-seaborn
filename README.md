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
## :file_folder: Loading the Data
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
 
def vlag_bars(n):
#Sample the palette while skipping its washed-out white middle band
#This way, every bar stays visible against the shaded background
    if n == 1:
        pts = [0.15]
    else:
        pts = []
        for i in range(n):
            t = i / (n - 1)
            pts.append(t * 0.4 if t < 0.5 else 0.6 + (t - 0.5) * 0.8)
    return sns.color_palette([CMAP(x) for x in pts])
```
# :fork_and_knife: Prepping the Data
Next, we will prep the data for analysis.
```python
# ---------- Prep data ----------
# 1. Yearly trend
yearly = df.groupby('ReportedYear').size().reset_index(name='count')
 ```

 ```df.groupby('ReportedYear')``` - buckets every row (incident) in the dataset by its ```ReportedYear``` value.
 
 ```.size()``` - counts how many rows fall into each year-bucket.
 
 ```.reset_index(name='count')``` - turns that into a clean two-column table: ReportedYear and count.

 So ```yearly``` ends up looking like:
| ReportedYear | count |
| ------------- | ------------- |
| 2020 | 35651 |
| 2021 | 43346 |
| 2022 | 37600 |
| 2023 | 36001 |
| 2024 | 35940 |
| 2025 | 30727 |


Next... 
```python
# 2. Day of week
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow = (df['ReportedDateTime'].dt.day_name()
       .value_counts()
       .reindex(dow_order)
       .rename_axis('day')
       .reset_index(name='count'))
month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
```
```dow``` - a chained set of operations that build the ```dow``` table:

```dow_order``` - a list of the days of the week in the order we want them displayed.

```df['ReportedDateTime'].dt.day_name()``` - takes the timestamp of every incident and converts it to the name of the weekday it fell on.

```.value_counts()``` - tallies up how many incidents happened on each weekday.

```.reindex(dow_order)``` - reorders those tallies to match the Monday→Sunday order.

```.rename_axis('day')``` - labels the index column ```"day"```.

```.reset_index(name='count')``` - turns it into a clean two-column table: ```day``` and ```count```.

So ```dow``` ends up looking like:
| day | Count |
| ------------- | ------------- |
| Monday | 31 ... |
| Tuesday | ... |
| ... | ... |
| Sunday | 33 ... |

Next...
```python
# 3. Offense type totals
offense_totals = df[offense_cols].sum().sort_values(ascending=False)
 ```

```df[offense_cols]``` - selects just the ten offense-type columns from the dataset.

```.sum()``` - adds up each column down its full length, giving a single total count per offense type (e.g. how many rows have ```AssaultOffense == 1```).

```.sort_values(ascending=False)``` - reorders those totals from highest to lowest.

So ```offense_totals``` ends up as a simple ranked list:
| Offense | count |
| ------------- | ------------- |
| AssaultOffense | ~79,000 |
| VehicleTheft | ~41,000 |
| ... | ... |
| Homicide | ~1,000 |

Next...
```python
# 4. Top weapons (excluding NaN/NONE clutter, keep top 8 real categories)
weapons = df['WeaponUsed'].value_counts()
weapons = weapons[~weapons.index.isin(['NONE'])].head(8)
 ```

```df['WeaponUsed'].value_counts()``` - looks at the WeaponUsed column and counts how many times each distinct value appears.

```weapons[~weapons.index.isin(['NONE'])]``` - drops the ```"NONE"``` category.

```.head(8)``` - keeps only the top 8 remaining categories by count.

| Weapon | count |
| ------------- | ------------- |
| Personal Weapon | ~33,800 |
| Firearm | ~12,200 |
| ... | ... |

Next...
```python
# 5. Heatmap: Year x Month counts
heat = df.pivot_table(index='ReportedMonth', columns='ReportedYear',
                       values='IncidentNum', aggfunc='count').reindex(range(1, 13))
heat.index = month_labels
 ```

```index='ReportedMonth'``` - makes each row of the resulting table one of the 12 months.

```columns='ReportedYear'``` - makes each column one of the years (2020–2025).

```values='IncidentNum', aggfunc='count'``` - for every month/year combination, counts how many incident numbers fall in that cell.

```.reindex(range(1, 13))``` - forces the row order to be month numbers 1 through 12 in sequence.

The result is a grid like:
| Month | 2020 | 2021 | 2022 | ... |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| 1 | 2900 | 3200 | ... | ... |
| 2 | 2600 | 2900 | ... | ... |
| ... | ... | ... | ... | ... |

Next...
```python
# 6. Top 10 wards
top_wards = df['WARD'].value_counts().head(10).sort_values()
```

```df['WARD'].value_counts()``` - counts how many incidents occurred in each ward, sorted from most incidents to fewest.
```.head(10)``` - keeps only the top 10 wards by incident count, dropping the rest
```.sort_values()``` - re-sorts those 10 wards, but this time in ascending order

So ```top_wards``` ends up as:
| Ward | count | 
| ------------- | ------------- |
| 177 | ~1,600 (10th highest) | 
| 188 | ~1,700 | 
| ... | ... |
| 186 | ~4,000 (highest) |


# :camera: Visualizing our Data
Now that we are done prepping our data, it is time to create our graphics!
```python
# ---------- Figure ----------
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle('Milwaukee WIBRS Crime Dashboard (2020\u20132025)', fontsize=20,
             fontweight='bold', color='#1a1a1a', y=0.995)
```
```plt.subplots(3, 2, ...)``` - created a 3-row × 2-column grid of empty chart panels, stored in ```axes```.

```python
# Panel 1: Yearly trend
ax = axes[0, 0]
sns.lineplot(data=yearly, x='ReportedYear', y='count', ax=ax,
             marker='o', markersize=9, linewidth=2.5, color=ACCENT)
ax.fill_between(yearly['ReportedYear'], yearly['count'], color=ACCENT, alpha=0.15)
ax.set_title('Total Incidents by Year', fontsize=13, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('Incidents')
ax.set_xticks(yearly['ReportedYear'])
```
```ax = axes[0, 0]``` - grabs the specific panel at row 0, column 0 (top-left) and stores it in the variable ```ax.```

```sns.lineplot(...)``` - draws the line chart itself — the yearly incident counts (from the ```yearly``` table built earlier) as a line with round markers at each year, colored with the shared ```ACCENT``` color, 2.5pt thick line.

```ax.fill_between(...)``` - shades the area underneath the line (from the line down to 0) with the same accent color at 15% opacity — that's the soft filled-in look under the curve you see in the image.

```ax.set_title``` - sets this panel's title text to "Total Incidents by Year," bold, size 13.

```ax.set_xlabel``` - labels the x-axis "Year" and the y-axis "Incidents."

```ax.set_xticks(yearly['ReportedYear'])``` - forces the x-axis to show a tick mark for every actual year in the data (2020, 2021, 2022...2025) rather than letting matplotlib pick its own arbitrary tick spacing.






























































































