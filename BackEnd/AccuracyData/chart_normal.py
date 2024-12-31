import pandas as pd
import matplotlib.pyplot as plt

# Read data from text file
df = pd.read_csv('./BackEnd/AccuracyData/algorithm_accuracy_normal.txt', delimiter=' - ', header=None, names=['name', 'accuracy'])

# Split 'name' column to get only algorithm names
df['name'] = df['name'].apply(lambda x: x.split(' ')[0])

# Convert 'accuracy' column to float
df['accuracy'] = df['accuracy'].astype(float)

# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(df['name'], df['accuracy'], color=['blue', 'orange', 'green', 'red'])
plt.xlabel('Algorithm')
plt.ylabel('Accuracy')
plt.title('Comparison of Algorithm Accuracy')
plt.ylim(0.6, 1.0)  
plt.tight_layout()
plt.show()
