import pandas as pd
import statsmodels.api as sm

# Load your data
df = pd.read_csv("resources/questionaire_data_sample.csv")

# Define the alternatives for each choice question
scenarios = {
    'Choice Questions 1': [
        {"name": "Option 1", "RouteSafety": "Well-maintained bike lanes", "BicycleFacilities": "Secure parking and showers", "TimeEfficiency": "30 minutes"},
        {"name": "Option 2", "RouteSafety": "Mixed safety", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "20 minutes"},
        {"name": "Different Mode of Transport", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "N/A"}
    ],
    'Choice Questions 2': [
        {"name": "Option 1", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "15 minutes"},
        {"name": "Option 2", "RouteSafety": "Mixed safety", "BicycleFacilities": "Secure parking and showers", "TimeEfficiency": "20 minutes"},
        {"name": "Different Mode of Transport", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "N/A"}
    ],
    'Choice Questions 3': [
        {"name": "Option 1", "RouteSafety": "Well-maintained bike lanes", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "30 minutes"},
        {"name": "Option 2", "RouteSafety": "Mixed safety", "BicycleFacilities": "Secure parking and showers", "TimeEfficiency": "20 minutes"},
        {"name": "Different Mode of Transport", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "N/A"}
    ],
    'Choice Questions 4': [
        {"name": "Option 1", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "Secure parking and showers", "TimeEfficiency": "15 minutes"},
        {"name": "Option 2", "RouteSafety": "Well-maintained bike lanes", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "30 minutes"},
        {"name": "Different Mode of Transport", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "N/A"}
    ],
    'Choice Questions 5': [
        {"name": "Option 1", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "20 minutes"},
        {"name": "Option 2", "RouteSafety": "Mixed safety", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "15 minutes"},
        {"name": "Different Mode of Transport", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "N/A"}
    ],
    'Choice Questions 6': [
        {"name": "Option 1", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "30 minutes"},
        {"name": "Option 2", "RouteSafety": "Well-maintained bike lanes", "BicycleFacilities": "Basic parking, no showers", "TimeEfficiency": "15 minutes"},
        {"name": "Different Mode of Transport", "RouteSafety": "No dedicated bike lanes", "BicycleFacilities": "No parking or showers", "TimeEfficiency": "N/A"}
    ]
}

# Convert into long format
long_format_data = []

# Iterate over all samples in the dataset
for idx, row in df.iterrows():
    # Iterate over all question for each sample
    for q_num in range(1, 7): 
        question_label = f'Choice Questions {q_num}'
        chosen_alternative = row[question_label]
        
        for alt in scenarios[question_label]:
            long_format_data.append({
                'choice_id': idx,
                'question_id': q_num,
                'alternative': alt['name'],
                'RouteSafety': alt['RouteSafety'],
                'BicycleFacilities': alt['BicycleFacilities'],
                'TimeEfficiency': alt['TimeEfficiency'],
                'chosen': 1 if alt['name'] == chosen_alternative else 0
            })

long_df = pd.DataFrame(long_format_data)

# We will neglect the questions were participants opted out.
filtered_df = long_df[long_df['alternative'] != 'Different Mode of Transport']

route_safety_dummies = pd.get_dummies(filtered_df['RouteSafety'], prefix='RouteSafety')
bicycle_facilities_dummies = pd.get_dummies(filtered_df['BicycleFacilities'], prefix='BicycleFacilities')
time_efficiency_dummies = pd.get_dummies(filtered_df['TimeEfficiency'], prefix='TimeEfficiency')

# Drop the desired baseline categories
route_safety_dummies = route_safety_dummies.drop('RouteSafety_No dedicated bike lanes', axis=1)
bicycle_facilities_dummies = bicycle_facilities_dummies.drop('BicycleFacilities_No parking or showers', axis=1)
time_efficiency_dummies = time_efficiency_dummies.drop('TimeEfficiency_20 minutes', axis=1)

# Build the feature matrix `X`
X = pd.concat([route_safety_dummies, bicycle_facilities_dummies, time_efficiency_dummies], axis=1)
# Add intercept
X['intercept'] = 1.0

# The response variable
y = filtered_df['chosen']

# Fit the multinomial logistic regression model
model = sm.MNLogit(y, X.astype(float))
result = model.fit()
print(result.summary())