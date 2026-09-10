import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---------- Load Data ----------
df = pd.read_excel('WIBRS F copy 2.xlsx')

offense_cols = ['AssaultOffense','VehicleTheft','CriminalDamage','Theft','LockedVehicle',
                 'Burglary','Robbery','SexOffense','Arson','Homicide']

# ---------- Style Data ----------
sns.set_theme(style='darkgrid')

#Shared palette family that will be used everywhere
PALETTE = 'vlag'          
CMAP = sns.color_palette(PALETTE, as_cmap=True)
#Single palette family that will be used everywhere
ACCENT = sns.color_palette(PALETTE, 8)[1]  

def bone_bars(n):
#Sample the palette while skipping its washed-out white middle band
#We do this so that every bar stays visible against the shaded background 
    if n == 1:
        pts = [0.15]
    else:
        pts = []
        for i in range(n):
            t = i / (n - 1)
            pts.append(t * 0.4 if t < 0.5 else 0.6 + (t - 0.5) * 0.8)
    return sns.color_palette([CMAP(x) for x in pts])

# ---------- Prep data ----------
# 1. Yearly trend
yearly = df.groupby('ReportedYear').size().reset_index(name='count')

# 2. Day of week
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow = (df['ReportedDateTime'].dt.day_name()
       .value_counts()
       .reindex(dow_order)
       .rename_axis('day')
       .reset_index(name='count'))
month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# 3. Offense type totals
offense_totals = df[offense_cols].sum().sort_values(ascending=False)

# 4. Top weapons (excluding NaN/NONE clutter, keep top 8 real categories)
weapons = df['WeaponUsed'].value_counts()
weapons = weapons[~weapons.index.isin(['NONE'])].head(8)

# 5. Heatmap: Year x Month counts
heat = df.pivot_table(index='ReportedMonth', columns='ReportedYear',
                       values='IncidentNum', aggfunc='count').reindex(range(1, 13))
heat.index = month_labels

# 6. Top 10 wards
top_wards = df['WARD'].value_counts().head(10).sort_values()

# ---------- Figure ----------
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle('Milwaukee WIBRS Crime Dashboard (2020\u20132025)', fontsize=20,
             fontweight='bold', color='#1a1a1a', y=0.995)

# Panel 1: Yearly trend
ax = axes[0, 0]
sns.lineplot(data=yearly, x='ReportedYear', y='count', ax=ax,
             marker='o', markersize=9, linewidth=2.5, color=ACCENT)
ax.fill_between(yearly['ReportedYear'], yearly['count'], color=ACCENT, alpha=0.15)
ax.set_title('Total Incidents by Year', fontsize=13, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('Incidents')
ax.set_xticks(yearly['ReportedYear'])

# Panel 2: Day of week
ax = axes[0, 1]
sns.barplot(data=dow, x='day', y='count', ax=ax, palette=bone_bars(len(dow)), hue='day',
            legend=False)
ax.set_xticklabels([d[:3] for d in dow_order])
ax.set_title('Total Incidents by Day of Week', fontsize=13, fontweight='bold')
ax.set_xlabel('Day'); ax.set_ylabel('Incidents')

# Panel 3: Offense type totals
ax = axes[1, 0]
sns.barplot(x=offense_totals.values, y=offense_totals.index, ax=ax,
            palette=bone_bars(len(offense_totals)), hue=offense_totals.index, legend=False)
ax.set_title('Incidents by Offense Type', fontsize=13, fontweight='bold')
ax.set_xlabel('Count'); ax.set_ylabel('')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Panel 4: Top weapons used
ax = axes[1, 1]
sns.barplot(x=weapons.values, y=weapons.index, ax=ax,
            palette=bone_bars(len(weapons)), hue=weapons.index, legend=False)
ax.set_title('Top Weapons Used (excl. "NONE")', fontsize=13, fontweight='bold')
ax.set_xlabel('Count'); ax.set_ylabel('')

# Panel 5: Year x Month heatmap
ax = axes[2, 0]
sns.heatmap(heat, ax=ax, cmap=PALETTE,
            cbar_kws={'label': 'Incidents'},
            linewidths=0.5, linecolor='#ffffff')
ax.set_title('Incident Volume Heatmap (Month \u00d7 Year)', fontsize=13, fontweight='bold')
ax.set_xlabel('Year'); ax.set_ylabel('')

# Panel 6: Top wards
ax = axes[2, 1]
sns.barplot(x=top_wards.values, y=[f'Ward {int(w)}' for w in top_wards.index],
            ax=ax, palette=bone_bars(len(top_wards)), hue=top_wards.index, legend=False)
ax.set_title('Top 10 Wards by Incident Count', fontsize=13, fontweight='bold')
ax.set_xlabel('Count'); ax.set_ylabel('')

plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.savefig('/mnt/user-data/outputs/wibrs_crime_dashboard_vlag.png', dpi=150,
            bbox_inches='tight')
print('saved')
