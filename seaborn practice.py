#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:14:35 2026

@author: lau
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Load & prep ---------------------------------------------------------
df = pd.read_excel('WIBRS F copy 2.xlsx')

# View the first 5 rows of data
print(df.head())

# Exclude the current partial year (2025) from year-over-year comparisons
# so it doesn't look like an artificial decline.
full_years = df[df['ReportedYear'] < 2025]

offense_cols = ['AssaultOffense', 'Burglary', 'CriminalDamage', 'Homicide',
                 'LockedVehicle', 'Robbery', 'SexOffense', 'Theft',
                 'VehicleTheft', 'Arson']

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

sns.set_theme(style = "whitegrid", palette = "viridis")
fig, axes = plt.subplots(2, 3, figsize = (20, 11))
fig.suptitle('Milwaukee-Area Crime Incidents Overview (WIBRS, 2020–2025)',
             fontsize = 18, fontweight = 'bold', y = 0.99)


# 1. Incidents per year -----------------------------------------------------
yearly = df['ReportedYear'].value_counts().sort_index()
sns.barplot(x = yearly.index.astype(str), y = yearly.values, ax = axes[0, 0],
            hue = yearly.index.astype(str), palette = 'crest', legend = False)
axes[0, 0].set_title('Incidents per Year', fontweight = 'bold')
axes[0, 0].set_xlabel('Year')
axes[0, 0].set_ylabel('Number of Incidents')
axes[0, 0].text(len(yearly) - 1, yearly.values[-1], '2025 partial',
                 ha = 'center', va = 'bottom', fontsize = 9, style = 'italic')


# 2. Seasonality: incidents by month (all complete years combined) --------
monthly = full_years['ReportedMonth'].value_counts().sort_index()
sns.lineplot(x = [month_names[m - 1] for m in monthly.index], y = monthly.values,
             marker = 'o', ax=axes[0, 1], color='#2c7fb8', linewidth=2.5)
axes[0, 1].set_title('Seasonality: Incidents by Month (2020–2024)', fontweight='bold')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Total Incidents')
axes[0, 1].tick_params(axis = 'x', rotation = 45)


# 3. Offense type totals -----------------------------------------------------
offense_totals = df[offense_cols].sum().sort_values(ascending=True)
sns.barplot(x = offense_totals.values, y = offense_totals.index, ax = axes[0, 2],
            hue = offense_totals.index, palette = 'mako', legend = False)
axes[0, 2].set_title('Total Incidents by Offense Type', fontweight = 'bold')
axes[0, 2].set_xlabel('Number of Incidents')
axes[0, 2].set_ylabel('')

# 4. Top weapons used (excluding missing/NONE) ------------------------------
weapons = df['WeaponUsed'].dropna()
weapons = weapons[weapons != 'NONE']
top_weapons = weapons.value_counts().head(10).sort_values(ascending = True)
sns.barplot(x = top_weapons.values, y = top_weapons.index, ax = axes[1, 0],
            hue = top_weapons.index, palette = 'flare', legend = False)
axes[1, 0].set_title('Top 10 Weapons Used', fontweight = 'bold')
axes[1, 0].set_xlabel('Number of Incidents')
axes[1, 0].set_ylabel('')

# 5. Year x Month heatmap ----------------------------------------------------
pivot = df.pivot_table(index = 'ReportedYear', columns = 'ReportedMonth',
                        values = 'IncidentNum', aggfunc = 'count')
pivot.columns = [month_names[m - 1] for m in pivot.columns]
sns.heatmap(pivot, annot = True, fmt = '.0f', cmap = 'YlOrRd', ax = axes[1, 1],
            cbar_kws = {'label': 'Incidents'}, linewidths = 0.5)
axes[1, 1].set_title('Incidents Heatmap: Year × Month', fontweight = 'bold')
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Year')

# 6. Top 10 wards by incident count -----------------------------------------
top_wards = df['WARD'].value_counts().head(10).sort_values(ascending = True)
sns.barplot(x = top_wards.values, y = [f'Ward {int(w)}' for w in top_wards.index],
            ax = axes[1, 2], hue=top_wards.index, palette = 'rocket', legend = False)
axes[1, 2].set_title('Top 10 Wards by Incident Count', fontweight = 'bold')
axes[1, 2].set_xlabel('Number of Incidents')
axes[1, 2].set_ylabel('')

plt.tight_layout(rect = [0, 0, 1, 0.97])
plt.savefig('/Users/lau/Desktop/py_scripts/crime_dashboard.png', dpi = 150, bbox_inches = 'tight')
print("Saved dashboard.")