# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:42:55 2024

@author: KOM
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

avocado = pd.read_excel("C:/users/KOM/Desktop/Opgaver/Uge9/Avocado.xlsx")

# add column of Total sold
avocado["Total Sold"]=avocado["Total Volume"]*avocado["AveragePrice"]

#Remove Time from Date
avocado['Date'] = avocado['Date'].dt.strftime('%Y-%m-%d')

# SECONDARY DATASET: make a grouped DataFrame with fewer values for Pie plots/Donut
sum_type_per_year = avocado.groupby(['year', 'type'])['Total Volume'].sum()
sum_type_per_year = pd.DataFrame(sum_type_per_year)

#Counting the amount of values (Unused So Far)
counts = avocado.groupby(['year', 'type']).size().to_frame('Counts')

#Concatenate the two above
grouped = pd.concat([sum_type_per_year, counts], axis=1)

#Total percentage
grouped['Percentage'] = grouped["Total Volume"]/sum(grouped['Total Volume'])*100
# Percentage per year
grouped['Percentage per year'] = (grouped['Total Volume'] / grouped.groupby('year')['Total Volume'].transform('sum')) * 100
grouped = grouped.reset_index()

# concatenate year and type as one label
grouped['Label'] = grouped['type'] + ' - ' + grouped['year'].astype(str)


#THIRD DATASET: with only type and amount sold
type_sum_total_sold=avocado.groupby(['type'])['Total Sold'].sum()
type_sum_total_sold = type_sum_total_sold.reset_index()


# FOURTH DATASET: Group bag sizes with type and year (for Opg. 7, Opg. 8 and Opg. 9)
type_bag_size = avocado.groupby(['type', 'year'])[['Small Bags','Large Bags', 'XLarge Bags']].sum()
type_bag_size = type_bag_size.reset_index()

# Melt the dataframe to convert 'Small Bags', 'Large Bags', 'Xlarge Bags' into rows
type_bag_size = type_bag_size.melt(id_vars=['type', 'year'], value_vars=['Small Bags', 'Large Bags', 'XLarge Bags'], var_name='Bag Size', value_name='Total Bags')
type_bag_size['Label'] = type_bag_size['type'] + ' - ' + type_bag_size['year'].astype(str)
#%% Opg. 1 Total Volume per year
sns.barplot(avocado, x = "year", y = "Total Volume", hue="type" , errorbar=None)

# Change X-Label
plt.xlabel('Year')
plt.legend(loc='upper left')
plt.title('Total Volume by Year and Type')
plt.show()

#%% Opg. 2 Percent plot 

plt.pie(grouped["Total Volume"], labels=grouped['Label'], autopct='%.1f%%')
plt.title('Percentage of Total Volume')
plt.show()

#%% Opg. 3 Money spent on avocadoes

g=sns.lineplot(data=avocado, x="Date", y="Total Sold", ci=None)
g.set_xticks(g.get_xticks()[::40])
plt.title('Total Sold by Date')
plt.show()
#%% Opg 4. money spent on each type of avocado

#Pie plot
plt.pie(type_sum_total_sold['Total Sold'], labels=type_sum_total_sold['type'], autopct='%.1f%%')

#Add a white circle in the middle of the pie plot
my_circle=plt.Circle( (0,0), 0.43, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.title('Total Type sold in Percent')
plt.show()
#%% Opg 5. Relation of average price and Total Volume

#Two plots in one
fig, ax = plt.subplots()
sns.lineplot(avocado, x='Date', y='Total Volume', ax=ax, color='b', ci=None, label='Total Volume')
ax2 = ax.twinx()
sns.lineplot(avocado, x='Date', y='AveragePrice', ax=ax2, color='r', ci=None, label='Average Price')

# Set number of ticks on the X-Axis
ax.set_xticks(ax.get_xticks()[::40])
#Position of the legends
ax.legend(loc='upper left')
ax2.legend(loc='upper center')
# Change Y-Label
plt.ylabel('Average Price')
plt.title('Total Volume and Average Price by Date')
plt.show()
#%% Opg. 6 

f=sns.lineplot(avocado, x = "Date", y = "AveragePrice", hue="type" , ci=None)
# Set number of ticks on the X-Axis
f.set_xticks(f.get_xticks()[::40])
# Change Y-Label
plt.ylabel('Average Price')
plt.title('Average Price Change of the Two Types')
plt.show()

#%% Opg. 7 Relation of amount sold and size of avocado bags
sns.barplot(type_bag_size, x='Bag Size', y='Total Bags', ci=None)
plt.title('Number of Bags Sold by Size')
plt.show()

#%% Opg. 8 relation between type and bag size

sns.barplot(type_bag_size, x='Bag Size', y='Total Bags', hue='type', ci=None)
plt.title('Number of Bags Sold by Size and Type')
plt.show()

#%% Opg. 9 Bag size and year
sns.barplot(type_bag_size, x = "year", y = "Total Bags", hue="Bag Size", ci=None )
# Change X-Label
plt.xlabel('Year')
plt.title('Number of Bags Sold by Size and Type per Year')
plt.show()