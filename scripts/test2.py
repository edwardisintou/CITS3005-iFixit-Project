import json
from collections import defaultdict

# Load the JSON data and calculate frequencies of tools and parts
tool_counts = defaultdict(int)
part_counts = defaultdict(int)

# Open and read the dataset
with open('data/Phone.json') as f:
    for line in f:
        phone_data = json.loads(line.strip())
        
        # Count tools in the toolbox
        for tool_data in phone_data.get("Toolbox", []):
            tool_name = tool_data["Name"]
            tool_counts[tool_name.lower()] += 1  # Convert to lowercase for uniform counting
            
            # Check if the URL indicates it's a part and count it
            url = tool_data.get("Url", "")
            if url and '/Parts/' in url:
                part_counts[tool_name.lower()] += 1

# Sort tools and parts by their frequency
sorted_tools = sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
sorted_parts = sorted(part_counts.items(), key=lambda x: x[1], reverse=True)

# Output the most common tools and parts
print("Most common tools:")
for tool, count in sorted_tools:
    print(f"{tool}: {count} times")

# print("\nMost common parts:")
# for part, count in sorted_parts:
#     print(f"{part}: {count} times")
