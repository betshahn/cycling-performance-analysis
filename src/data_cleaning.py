import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

# What predicts cycling performance?
# We will be using the Kaggle dataset "Strava Cycling Dataset" which contains data on various cycling activities recorded by one Strava user. The dataset includes information such as distance, speed, heart rate, and power output for each activity. We will analyze this data to identify factors that may predict cycling performance, such as average speed.

# Loading in the Kaggle dataset
df = pd.read_csv('/Users/betsyhahn/Downloads/cycling-performance-analysis/kaggle-data/public_strava_dataset.csv')
# print(df.head())

# Only want to keep the rows where the activity type is 'Ride' since we are only interested in analyzing bike rides
df_bike = df[df['type'] == 'Ride']
# print(df_bike.head())
# print(df_bike.shape)

# Drop columns that are not relevant to our analysis
#columns_to_drop = []

# For column in df_bike.columns:
print(df_bike.describe())
print(df_bike["average_speed"].describe())

# Find What Predicts Speed
print(
    df_bike.corr(numeric_only=True)["average_speed"]
    .sort_values(ascending=False)
)

# Visualize the relationship between average_heartrate and average_speed
# Scatter plot of average heart rate vs average speed to see if there is a relationship between the two variables
x = df_bike["average_heartrate"]
y = df_bike["average_speed"]

plt.scatter(x, y)

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)

plt.xlabel("Average Heart Rate")
plt.ylabel("Average Speed")
plt.title("Average Speed vs Average Heart Rate")

plt.show()

# This shows that as heart rate increases, average speed also tends to increase, which makes sense as higher heart rates are often associated with more intense physical activity. However, it's important to note that this is just a correlation and does not necessarily imply causation. Other factors such as fitness level, terrain, and weather conditions could also influence both heart rate and speed.

# Let's now look at: 
# How do effort (heart rate) and terrain (elevation gain) influence cycling speed?
print(
df_bike[
    [
        "average_speed",
        "average_heartrate",
        "total_elevation_gain"
    ]
].corr())

# This shows that average heart rate has a stronger positive correlation with average speed (0.65) compared to total elevation gain (0.30). This suggests that while both effort and terrain can influence cycling speed, effort (as measured by heart rate) may be a more significant predictor of speed than terrain (as measured by elevation gain) in this dataset. 
# However, it's important to consider that other factors not included in this analysis could also play a role in determining cycling performance.
# Here we will focus on heart rate and elevation gain as predictors of speed, but in a more comprehensive analysis, we could include other variables such as distance, weather conditions, and fitness level to get a more complete picture of what influences cycling performance.
# We won't look at other predictors 

# Performance is mainly driven by effort (heart rate) and terrian (elevation gain)
# Everything else is seemingly secondary to these two factors.

# So can we predict speed based on heart rate and elevation gain? (ML)
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

features = df_bike[
    ["average_heartrate", "total_elevation_gain"]
]

target = df_bike["average_speed"]

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

print("R^2:", model.score(X_test, y_test))
