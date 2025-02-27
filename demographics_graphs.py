import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

data = pd.read_csv("resources/questionaire_data_sample.csv")
df = pd.DataFrame(data)

os.makedirs("graphs", exist_ok=True)
sns.set_palette("dark")

def save_plot(x, order, title, file_name):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x=x, order=order)
    plt.title(title)
    plt.xlabel(None)
    plt.savefig(f"graphs/{file_name}.png")
    plt.close()

# Plot Age Distribution
save_plot('ageGroup', ['18-30', '30-40', '40-50', '50-60', '60+'], 'Age Distribution', 'age_distribution')

# Plot Usual Commute Types
save_plot('usualModeOfTransport', None, 'Usual Commute Type', 'usual_commute_type')

# Plot Distance to Commute
save_plot('distanceToCommute', ['<5 km', '<10 km', '<20 km', '30 km +'], 
          'Distance to Commute', 'distance_to_commute')

# Plot Time to Commute
save_plot('timeToCommute', ['<20min', '<30min', '<60min', '60min +'], 
          'Time to Commute', 'time_to_commute')

# Plot Preferred Commute Type
save_plot('idealModeOfTransport', None, 'Preferred Commute Type', 'preferred_commute_type')

# Plot Enjoyment in Current Commute
save_plot('joyInCurrentCommute', ['Definitely yes', 'Sometimes', 'Absolutely not'], 
          'Enjoyment in Current Commute', 'enjoyment_in_current_commute')

print("Graphs saved in the 'graphs' folder.")