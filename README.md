# Frameworks_Assignment

# CORD-19 Research Dataset Explorer

An interactive **Streamlit** dashboard for exploring a sample of the
[CORD-19](https://www.semanticscholar.org/cord19) research metadata.
You can filter papers by year and journal, view publication trends,
see the top journals, and generate a word cloud of paper titles.

---

## Features
- 📊 **Publication Trends** – bar chart of papers published per year  
- 🏛 **Top Journals** – horizontal bar chart of the most prolific journals  
- ☁️ **Word Cloud** – highlights frequent terms in paper titles  
- 🔎 **Interactive Filters** – slider for year range, dropdown for journal  
- 💾 **Data Preview** – sample of the filtered metadata in a scrollable table  

---

## Project Structure
├─ app.py # Streamlit application
├─ requirements.txt # Python dependencies
└─ README.md # This file

> **Note**  
> The dataset is **not stored in this repository** to keep the repo small.

---access it here **https://drive.google.com/drive/folders/1wdmB_b3M5sEm1kgLj9a0YGFmhtzMwqLP?usp=drive_link**  extract the files into the project folder---

---

## Setup & Run

1. **Clone the repo**
   ```bash
   git clone (https://github.com/braytone-q/Frameworks_Assignment)
   cd Frameworks_Assignment

   
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows


pip install -r requirements.txt

streamlit run app.py

   
