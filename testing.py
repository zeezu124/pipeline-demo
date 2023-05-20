import subprocess
import json
import time
from datetime import datetime

def perform_stress_test(api_endpoint, input_texts, num_requests):
    # Generate curl commands for each input text
    curl_commands = []
    for input_text in input_texts:
        data = json.dumps({'input_text': input_text})
        curl_commands.append(f'''curl -X POST -H "Content-Type: application/json" 
                             -d \'{data}\' {api_endpoint}''')

    # Send concurrent curl requests using subprocess
    processes = []
    start_time = time.time()
    for _ in range(num_requests):
        for curl_command in curl_commands:
            process = subprocess.Popen(curl_command, shell=True)
            processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.wait()

    # Calculate metrics
    total_time = time.time() - start_time
    average_time = total_time / (num_requests * len(input_texts))
    status = [process.returncode for process in processes]

    # Generate random file name
    #file_name = ''.join(random.choices(string.ascii_lowercase, k=10)) + "_stress_test" +".txt"

    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{current_time}_stress_test.txt"
    # Write metrics to file
    with open(file_name, 'w') as f:
        f.write(f"Total Time: {total_time} seconds\n")
        f.write(f"Average Time: {average_time} seconds\n")
        f.write(f"Status Codes: {status}\n")

    print(f"Metrics written to file: {file_name}")

# Example usage
api_endpoint = "http://127.0.0.1:5000/results"
input_texts = [
    "I can't believe how amazing this day has been!",
    "I'm feeling so excited about the upcoming event.",
    "I'm devastated by the news of her passing.",
    "What a wonderful surprise!",
    "I'm furious at the way they treated us.",
    "This book made me incredibly happy.",
    "I'm anxious about the interview tomorrow.",
    "I feel so betrayed by his actions.",
    "The breathtaking view left me speechless.",
    "I'm heartbroken over the loss of my pet.",
    "I'm proud of my accomplishments today.",
    "I'm terrified of what might happen next.",
    "This delicious meal made me feel content.",
    "I'm frustrated with the lack of progress.",
    "The beautiful sunset brought tears to my eyes.",
    "I'm overwhelmed with joy and gratitude.",
    "I'm disappointed in the outcome of the game.",
    "I'm filled with anticipation for the trip.",
    "The heartwarming movie made me cry.",
    "I'm worried about the future of our planet.",
    "This unexpected gift made me feel loved.",
    "I'm irritated by their constant interruptions.",
    "I'm touched by their kindness and generosity.",
    "The tragic accident left me in shock.",
    "I'm thrilled to have achieved my goal.",
    "I'm annoyed by their lack of consideration.",
    "I'm moved by the powerful speech.",
    "This challenging puzzle frustrated me.",
    "I'm scared of the dark.",
    "I'm elated by the news of their engagement.",
    "I'm exhausted after a long day of work.",
    "The heartbreaking story brought me to tears."
]
num_requests = 10
perform_stress_test(api_endpoint, input_texts, num_requests)