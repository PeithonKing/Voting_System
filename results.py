import json
import matplotlib.pyplot as plt
import os

# Load the data from the file
with open('votes.json') as f:
    data = json.load(f)

# Create a directory called results if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

# Loop through each post and create a pie chart
for post, candidates in data.items():
    labels = list(candidates.keys())
    sizes = list(candidates.values())

    # Create the pie chart
    plt.pie(sizes, labels=labels, autopct=lambda p : f"{p:.1f}% ({int(p * sum(sizes) / 100)})")
    plt.title(post.upper())
    plt.axis('equal')

    # Save the pie chart to a file in the results directory
    filename = f"results/{post.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.clf()  # Clear the figure for the next iteration

print("Pie charts saved to the results directory!")
