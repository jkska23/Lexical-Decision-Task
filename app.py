# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
import json
import os
import time
import csv
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

# Stimuli
english_words = [
    {"word": "apple", "type": "real"},
    {"word": "table", "type": "real"},
    {"word": "chair", "type": "real"}, 
    {"word": "happy", "type": "real"},
    {"word": "running", "type": "real"},
    {"word": "book", "type": "real"},
    {"word": "window", "type": "real"},
    {"word": "orange", "type": "real"},
    {"word": "house", "type": "real"},
    {"word": "flower", "type": "real"}
]

chinese_words = [
    {"word": "苹果", "type": "real", "meaning": "apple"},
    {"word": "桌子", "type": "real", "meaning": "table"},
    {"word": "椅子", "type": "real", "meaning": "chair"},
    {"word": "快乐", "type": "real", "meaning": "happy"},
    {"word": "跑步", "type": "real", "meaning": "running"},
    {"word": "书", "type": "real", "meaning": "book"},
    {"word": "窗户", "type": "real", "meaning": "window"},
    {"word": "橙子", "type": "real", "meaning": "orange"},
    {"word": "房子", "type": "real", "meaning": "house"},
    {"word": "花", "type": "real", "meaning": "flower"}
]

english_pseudo = [
    {"word": "abble", "type": "pseudo"},
    {"word": "tablen", "type": "pseudo"},
    {"word": "chaur", "type": "pseudo"},
    {"word": "happit", "type": "pseudo"},
    {"word": "runing", "type": "pseudo"},
    {"word": "booc", "type": "pseudo"},
    {"word": "windon", "type": "pseudo"},
    {"word": "orenge", "type": "pseudo"},
    {"word": "hause", "type": "pseudo"},
    {"word": "flowel", "type": "pseudo"}
]

chinese_pseudo = [
    {"word": "苹桌", "type": "pseudo"},
    {"word": "子子", "type": "pseudo"},
    {"word": "椅书", "type": "pseudo"},
    {"word": "快窗", "type": "pseudo"},
    {"word": "跑花", "type": "pseudo"},
    {"word": "书房", "type": "pseudo"},
    {"word": "窗橙", "type": "pseudo"},
    {"word": "橙苹", "type": "pseudo"},
    {"word": "房椅", "type": "pseudo"},
    {"word": "花书", "type": "pseudo"}
]

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demographics', methods=['GET', 'POST'])
def demographics():
    if request.method == 'POST':
        # Generate a unique participant ID
        participant_id = str(uuid.uuid4())[:8]
        
        # Process demographics form data
        demo_data = {
            'participant_id': participant_id,
            'name': request.form.get('name', ''),  # Add name field
            'age': request.form.get('age', ''),
            'gender': request.form.get('gender', ''),
            'education': request.form.get('education', ''),
            'english_proficiency': request.form.get('english_proficiency', ''),
            'chinese_proficiency': request.form.get('chinese_proficiency', ''),
            'bilingual_history': request.form.get('bilingual_history', ''),
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'data_type': 'demographics',
            'block_order': request.form.get('block_order', '')
        }
        
        # Save demographics data to CSV
        save_to_csv(demo_data, participant_id)
        
        # Set up session for experiment
        session['participant_id'] = participant_id
        session['participant_name'] = demo_data['name']  # Store name in session
        session['block_order'] = demo_data['block_order']
        session['completed_blocks'] = []
        session['demographics_completed'] = True
        
        # Redirect to instructions
        return redirect(url_for('instructions'))
    
    return render_template('demographics.html')

@app.route('/instructions')
def instructions():
    # Check if demographics have been completed
    if 'demographics_completed' not in session:
        return redirect(url_for('demographics'))
        
    condition = request.args.get('condition', 'single')
    return render_template('instructions.html', condition=condition)

@app.route('/experiment')
def experiment():
    # Check if demographics have been completed
    if 'demographics_completed' not in session:
        return redirect(url_for('demographics'))
    
    participant_id = session.get('participant_id')
    condition = request.args.get('condition', 'single')
    block_number = int(request.args.get('block', 1))
    
    # Create stimuli list based on the condition
    stimuli = []
    
    if condition == 'single':
        # Single language block (English only)
        if block_number == 1:
            # Ensure equal number of real and pseudo words
            stimuli = english_words[:5] + english_pseudo[:5]  # 5 real + 5 pseudo
        # Single language block (Chinese only)
        else:
            stimuli = chinese_words[:5] + chinese_pseudo[:5]  # 5 real + 5 pseudo
    else:
        # Mixed language block
        # Ensure equal number of real and pseudo words for each language
        stimuli = (english_words[:5] + chinese_words[:5] +  # 5 real English + 5 real Chinese
                  english_pseudo[:5] + chinese_pseudo[:5])  # 5 pseudo English + 5 pseudo Chinese
    
    # Randomize stimuli
    random.shuffle(stimuli)
    
    # Add trial numbers and block information
    for i, stimulus in enumerate(stimuli):
        stimulus['trial_number'] = i + 1
        stimulus['block_number'] = block_number
        stimulus['condition'] = condition
    
    print(f"Debug - Stimuli for {condition} block {block_number}: {json.dumps(stimuli)}")  # Debug print
    
    return render_template('experiment.html', 
                          stimuli_json=json.dumps(stimuli),  # Pass as JSON string
                          participant_id=participant_id,
                          condition=condition,
                          block_number=block_number,
                          block_order=session.get('block_order', 'single_first'))

def save_to_csv(data, participant_id):
    """Save data to a CSV file"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Determine file type based on data_type
    data_type = data.get('data_type', '')
    if data_type == 'demographics':
        filename = "data/all_demographics.csv"
        # Define the order of columns for demographics data
        fieldnames = ['participant_id', 'name'] + [k for k in data.keys() if k not in ['participant_id', 'name']]
    else:
        filename = "data/all_experiment_data.csv"
        # Define the order of columns for experiment data
        fieldnames = ['participant_id', 'participant_name'] + [k for k in data.keys() if k not in ['participant_id', 'participant_name']]
    
    file_exists = os.path.exists(filename)
    
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.get_json()
    participant_id = data.get('participant_id', 'anonymous')
    
    # Add timestamp and data type to the data
    data['timestamp'] = datetime.now().strftime("%Y%m%d_%H%M%S")
    data['data_type'] = 'experiment'
    
    # Add participant name from session
    data['participant_name'] = session.get('participant_name', '')
    
    # Add additional experiment-specific fields
    data['reaction_time'] = data.get('reaction_time', '')
    data['accuracy'] = data.get('accuracy', '')
    data['stimulus'] = data.get('stimulus', '')
    data['response'] = data.get('response', '')
    data['trial_number'] = data.get('trial_number', '')
    data['block_number'] = data.get('block_number', '')
    data['condition'] = data.get('condition', '')
    
    # Save to CSV
    save_to_csv(data, participant_id)
    
    return jsonify({"status": "success", "message": "Data saved successfully"})

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/download-data')
def download_data():
    # For a real experiment, you'd want to secure this with a password
    # This is just for demonstration/testing purposes
    data_files = []
    
    # Check if the data files exist
    experiment_file = 'data/all_experiment_data.csv'
    demographics_file = 'data/all_demographics.csv'
    
    if os.path.exists(experiment_file) or os.path.exists(demographics_file):
        data_files = [
            ('all_experiment_data.csv', 'Experiment Data'),
            ('all_demographics.csv', 'Demographics Data')
        ]
    
    return render_template('download_data.html', data_files=data_files)

@app.route('/get-data-file/<filename>')
def get_data_file(filename):
    if os.path.exists(f'data/{filename}'):
        data = []
        with open(f'data/{filename}', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return jsonify(data)
    return jsonify({"error": "File not found"})

if __name__ == '__main__':
    app.run(debug=True)