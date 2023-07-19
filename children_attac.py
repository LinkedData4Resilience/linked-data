import pandas as pd
import matplotlib.pyplot as plt

# Read the first CSV file
df1 = pd.read_csv('C:/Users/manar/Desktop/linked-data/all-damage-events-timeseries.csv')

# Step 1: Rename the columns
df1 = df1.rename(columns={"monthyear": "Month", "numevts": "Number of Attacks"})

# Step 2: Convert the "Month" column to datetime
df1['Month'] = pd.to_datetime(df1['Month'])

# Read the second CSV file
df2 = pd.read_csv('datasets/childeren-attack-records.csv')

# Step 1: Rename the columns
df2 = df2.rename(columns={"monthyear": "Month", "numevts": "Number of Childeren Died"})

# Step 2: Convert the "Month" column to datetime
df2['Month'] = pd.to_datetime(df2['Month'])

# Calculate the ratio of Subplot 2 to Subplot 1
ratio = df2['Number of Childeren Died'] / df1['Number of Attacks']

# Set the figure size
plt.figure(figsize=(10, 18))

# Convert x-values to string format
x1 = df1['Month'].dt.strftime('%Y-%m')
x2 = df2['Month'].dt.strftime('%Y-%m')

# Plot the first bar plot
plt.subplot(3, 1, 1)  # Set subplot configuration: 3 rows, 1 column, plot 1
plt.bar(x1, df1['Number of Attacks'], width=0.8, color='blue')
plt.ylabel('Number of Attacks')
plt.title('Monthly Number of Attacks', y=-0.2)


# Plot the second bar plot
plt.subplot(3, 1, 2)  # Set subplot configuration: 3 rows, 1 column, plot 2
plt.bar(x2, df2['Number of Childeren Died'], width=0.8, color='red')
plt.ylabel('Number of Childeren Died')
plt.title('Monthly Number of Children Death', y=-0.2)


# Plot the ratio subplot
plt.subplot(3, 1, 3)  # Set subplot configuration: 3 rows, 1 column, plot 3
plt.plot(x2, ratio, color='green', marker='o')
plt.ylabel('Ratio (Attacks / Childeren death)')
plt.title('Ratio of Children Death to Attacks', y=-0.2)


# Adjust the spacing between subplots
plt.tight_layout()

# Display the plot
plt.show()
