import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import tldextract
import re
from collections import Counter
from collections import defaultdict

def count_random_values(file_path):
    # Dictionary to store the count of each "random" value
    random_value_count = defaultdict(int)

    # Regular expression to find "random":"<string>" patterns
    pattern = re.compile(r'"random":"(.*?)"')

    # Read the file and count the occurrences of each "random" value
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            matches = pattern.findall(line)
            for match in matches:
                random_value_count[match] += 1



    # Filter and print the "random" values that have been repeated
    duplicates = {value: count for value, count in random_value_count.items() if count > 1}

    if duplicates:
        # Calculate the grand total of duplicated random values
        grand_total = sum(duplicates.values())

        # Identify the "random" value with the highest number of duplicates
        max_duplicated_random = max(duplicates, key=duplicates.get)
        max_duplicates = duplicates[max_duplicated_random]
      # Find the top 2 random values with the highest duplicates
        top2 = sorted(duplicates, key=duplicates.get, reverse=True)[:2]

        print("Here are the 'Two separate server hello randoms both appear 4 distinct times in the dataset.'")

        # Print as bullet points
        print("- " + top2[0])
        print("- " + top2[1])

    else:
        print("No duplicated 'random' values found.")

    return duplicates

# Path to the text file
file_path = 'dataset.txt'

# Execute the function
duplicates = count_random_values(file_path)
print ("Now I am working on the FQDNs, please wait ...")

# Regular expression to match FQDNs starting with 'http', 'https', or 'www'
pattern = re.compile(r'\b(?:https?://|www\.)[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+\b')

# Function to search for FQDNs in the text file
def search_fqdns(file_path):
    domains = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            matches = pattern.findall(line)
            domains.extend(matches)

    return domains

# Execute the function
domains = search_fqdns(file_path)

# Extract registerable domains
registerable_domains = [tldextract.extract(domain).registered_domain for domain in domains]
registerable_domain_counts = Counter(registerable_domains)

# Display total number of domains found
print ("Here is what I found")
print(f"\nTotal number of domains found: {len(domains)}")
print(f"Total number of unique registerable domains found: {len(registerable_domain_counts)}")


print ("Now I am working on creating some simple graphs, this tends to take several minutes, please wait ....")

# Bar graphs
plt.figure(figsize=(12, 6))

# Bar graph for 'random' values that appear exactly 4 times
plt.subplot(1, 2, 1)
random_values_4_times = [value for value, count in duplicates.items() if count == 4]
plt.bar(range(len(random_values_4_times)), [4]*len(random_values_4_times), tick_label=random_values_4_times, color='skyblue')
plt.title('"random" Values Appearing 4 Times')
plt.xlabel('"random" Values')
plt.ylabel('Frequency')
plt.xticks(rotation=90)

# Bar graph for unique registerable domains
plt.subplot(1, 2, 2)
domains = list(registerable_domain_counts.keys())
counts = list(registerable_domain_counts.values())
plt.bar(range(len(domains)), counts, tick_label=domains, color='salmon')
plt.title('Unique Registerable Domains')
plt.xlabel('Domains')
plt.ylabel('Number of Occurrences')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()