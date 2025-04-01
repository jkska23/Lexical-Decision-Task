# Lexical Decision Task: Code-Switching and Bilingual Performance

## Project Overview
This project investigates how code-switching (mixing languages) affects lexical decision task performance in bilingual speakers. The experiment measures reaction time and accuracy when participants identify words and nonwords in both single-language and mixed-language conditions.

## Research Question
How does code-switching impact the performance of bilingual speakers in a lexical decision task?

## Hypothesis
Bilingual speakers will exhibit slower reaction times and/or lower accuracy when presented with mixed-language (code-switched) stimuli compared to single-language stimuli.

## Experimental Design
### Stimuli
- **English Words:** Common and less common real English words.
- **Non-English Words:** Real words from the chosen second language (e.g., Chinese: "苹果").
- **Pseudo-Words:** Non-words that follow the phonological rules of the language (e.g., "abble" for English, "苹桌" for Chinese).

### Participants
- **Target Group:** Bilingual speakers fluent in both English and the second language.
- **Monolinguals Excluded:** The experiment focuses solely on bilingual cognitive processing.

### Procedure
1. Participants complete two blocks of lexical decision tasks:
   - **Single-Language Block:** Words appear in one language (English or Chinese).
   - **Mixed-Language Block:** Words appear in both languages, simulating code-switching.
   - Block order is counterbalanced across participants.
2. On each trial, a word appears on the screen.
3. The participant presses a key to indicate if the word is real or not.
4. Reaction time and accuracy are recorded.
5. Data is stored in a structured format (CSV/Excel) for analysis.

## Implementation Details
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript (Templates folder)
- **Data Storage:** CSV for reaction time and accuracy logging

## Setup and Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/jkska23/Lexical-Decision-Task.git
   cd Lexical-Decision-Task
   ```
2. Install dependencies:
   ```bash
   pip install Flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the experiment in a web browser at `http://localhost:5000`

## Example Data
A sample dataset demonstrating reaction times and accuracy is included in the `data/` folder.

## Contact
For questions or feedback, please reach out via email or GitHub Issues.

note:
- this repo is a vibe coding mess. use it at your own discretion. 
