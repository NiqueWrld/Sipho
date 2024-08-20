import os
import json

def combine_intents(data_directory, output_file, command_file):
    combined_intents = []
    command_intents = []

    # Verify the directory exists
    if not os.path.isdir(data_directory):
        print(f"Directory '{data_directory}' does not exist.")
        return

    # Iterate through all files in the specified directory
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(data_directory, filename)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    # Check if 'intents' key exists in the JSON data
                    if 'intents' in data:
                        for intent in data['intents']:
                            if 'command' in intent:
                                command_intents.append({
                                    'tag': intent['tag'],
                                    'command': intent['command']
                                })
                                intent.pop('command')
                                combined_intents.append(intent)
                            else:
                                combined_intents.append(intent)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {file_path}: {e}")

    # Prepare the final combined data
    combined_data = {"intents": combined_intents}

    # Write the combined data to the output JSON file
    with open(output_file, 'w') as out_file:
        json.dump(combined_data, out_file, indent=4)

    # Write the command-specific data to a separate JSON file
    if command_intents:
        with open(command_file, 'w') as cmd_file:
            json.dump({"commands": command_intents}, cmd_file, indent=4)

# Directory containing the JSON files
data_directory = os.path.join(os.path.dirname(__file__), 'Data')
# Output file paths
combined_output_file = os.path.join(os.path.dirname(__file__), 'content.json')
command_output_file = 'commands.json'

combine_intents(data_directory, combined_output_file, command_output_file)
