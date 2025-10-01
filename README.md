# Vimshottari-Dasha-Chart


Generate the full 120-year Vimshottari Dasha timeline and export it to Excel.
Given the Moon’s position at birth (zodiac + degree + minute) and date of birth,
this tool builds the complete Dasha sequence automatically.

👉 Includes both a Streamlit web app and a local Python script.

✨ Features

Input Moon position (Sidereal Zodiac + Degree + Minute) and Date of Birth

Nakshatra & ruler detection

First Dasha duration calculated from pre-computed lookup table (hardcoded → accurate to the minute)

Following Dashas built from the standard Vimshottari Dasha table

Full Lv1, Lv2, Lv3 expansion

Export as Excel with planet symbols + color coding

Web interface with dropdowns and download button

📂 Repository Structure
.
├── main.py                # Main script (local execution)
├── utils.py               # Utility functions
├── ZODIAC_TABLE.py        # Zodiac definitions
├── NAKSHATRA_TABLE.py     # Nakshatra definitions
├── DASHA_TABLE.py         # Standard Vimshottari periods
├── DASHA_REMAINING.py     # Precomputed first Dasha remainders (minute precision)
├── requirements.txt       # Dependencies
└── streamlit_app.py       # Web app entry (Streamlit)

🖥️ Local Usage

Clone the repo

git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME


Install dependencies

pip install -r requirements.txt


Run the calculator

python main.py


Results will be saved as an Excel file:
dasha_output_xxxxxx.xlsx (randomized suffix to avoid overwriting).

🌐 Web App (Streamlit)

Install and run

pip install streamlit
streamlit run streamlit_app.py


Open in your browser (default: http://localhost:8501
)

Select zodiac / degree / birth date from dropdowns → preview the timeline table → download Excel.

📊 Example Output

Excel columns:

Date – Start date of each period

Age – Age (rounded down)

Lv1, Lv2, Lv3 – Planet (with symbol + color)

(Example: Moon → Mars → Rahu sequence)

⚡ Requirements

Python 3.9+

pandas

openpyxl

streamlit

🧭 Roadmap

 Add Lv1–Lv3 timeline visualization in web UI

 Add PDF export option

 Auto-generate textual Dasha interpretations
