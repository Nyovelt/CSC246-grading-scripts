import re

# Input text
text = """
I'm process 1282713. Local count: 1. Sequence found at: 14-35.
I'm process 1282713. Local count: 2. Sequence found at: 14-36.
I'm process 1282713. Local count: 3. Sequence found at: 14-37.
I'm process 1282713. Local count: 4. Sequence found at: 16-33.
I'm process 1282713. Local count: 5. Sequence found at: 18-30.
I'm process 1282713. Local count: 6. Sequence found at: 18-32.
I'm process 1282714. Local count: 1. Sequence found at: 13-30.
I'm process 1282714. Local count: 2. Sequence found at: 13-32.
I'm process 1282714. Local count: 3. Sequence found at: 15-31.
Total count: 9 
"""

# Regular expression pattern to capture process ID, local count, and sequence
pattern = r"I'm process (\d+)\. Local count: (\d+)\. Sequence found at: (\d+-\d+)\."

# Find all matches in the text
matches = re.findall(pattern, text)

# # Display the results
# for match in matches:
#     process_id, local_count, sequence = match
#     print(f"Process ID: {process_id}, Local Count: {local_count}, Sequence: {sequence}")
total_count_pattern = r"Total count: (\d+)"
total_count_match = re.search(total_count_pattern, text)
total_count = int(total_count_match.group(1)) if total_count_match else 0
print(total_count == 9)
