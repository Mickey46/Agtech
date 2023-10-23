# Install the OpenAI Python library
!pip install openai

# Import necessary libraries
import numpy as np
import string
import os
import openai
import csv
import requests
from io import StringIO

# Set up the OpenAI API key
openai.api_key = 'your-api-key'

# Define the function to talk to the GPT-4 model
def talk(input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a botanist, please translate to common English names."},
            {"role": "user", "content": input}
        ]
    )
    return response.choices[0].message['content']

# URL for the CSV file containing plant names
url = "https://www.gstatic.com/aihub/tfhub/labelmaps/aiy_plants_V1_labelmap.csv"

# Fetch the CSV data from the URL
response = requests.get(url)
response.raise_for_status()  # Raises an exception in case of an error

# Use StringIO to simulate a file object
csv_file = StringIO(response.text)

# Read the CSV file
reader = csv.reader(csv_file)

# Loop over each row in the CSV file
for row in reader:
    print(row[1], " = ", talk(row[1]))

