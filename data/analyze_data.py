import pandas as pd
import numpy as np

def analyze_experiment_data():
    # Read the CSV file
    df = pd.read_csv('all_experiment_data.csv', encoding='utf-8-sig')
    
    # Print debug information about the data
    print("\nDebug Information:")
    print(f"Total rows: {len(df)}")
    print("\nUnique conditions found:")
    print(df['condition'].unique())
    print("\nUnique languages found:")
    print(df['language'].unique())
    
    # Convert reaction_time to numeric, handling any non-numeric values
    df['reaction_time'] = pd.to_numeric(df['reaction_time'], errors='coerce')
    
    # Group by participant and condition
    grouped = df.groupby(['participant_id', 'condition', 'language'])
    
    # Initialize results dictionary
    results = {
        'english_single': {'rt': [], 'accuracy': []},
        'chinese_single': {'rt': [], 'accuracy': []},
        'mixed_english': {'rt': [], 'accuracy': []},
        'mixed_chinese': {'rt': [], 'accuracy': []}
    }
    
    # Process each group
    for (participant, condition, language), group in grouped:
        # Skip the first trial for each condition
        group = group.iloc[1:]
        
        # Calculate average reaction time for correct responses
        correct_rt = group[group['accuracy'] == 1]['reaction_time'].mean()
        
        # Calculate accuracy
        accuracy = group['accuracy'].mean() * 100
        
        # Store results
        if condition == 'single' and language == 'english':
            results['english_single']['rt'].append(correct_rt)
            results['english_single']['accuracy'].append(accuracy)
        elif condition == 'single' and language == 'chinese':
            results['chinese_single']['rt'].append(correct_rt)
            results['chinese_single']['accuracy'].append(accuracy)
        elif condition == 'mixed' and language == 'english':
            results['mixed_english']['rt'].append(correct_rt)
            results['mixed_english']['accuracy'].append(accuracy)
        elif condition == 'mixed' and language == 'chinese':
            results['mixed_chinese']['rt'].append(correct_rt)
            results['mixed_chinese']['accuracy'].append(accuracy)
    
    # Print results
    print("\nExperiment Results (excluding first trial):")
    print("-" * 50)
    
    for condition, data in results.items():
        if data['rt']:  # Only print if there's data
            avg_rt = np.mean(data['rt'])
            avg_accuracy = np.mean(data['accuracy'])
            print(f"\n{condition.replace('_', ' ').title()}:")
            print(f"Average Reaction Time (correct responses): {avg_rt:.2f} ms")
            print(f"Average Accuracy: {avg_accuracy:.2f}%")
            print(f"Number of participants: {len(data['rt'])}")
        else:
            print(f"\n{condition.replace('_', ' ').title()}: No data available")

if __name__ == "__main__":
    analyze_experiment_data() 