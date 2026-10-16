# Customer Feedback Analyzer

A Python-based customer feedback analysis application that transforms customer feedback data into a structured management report.

The application combines rule-based analysis, automated PDF reporting, and OpenAI API integration to identify recurring product issues, customer satisfaction patterns, and opportunities for improvement.

## Features

- **CSV Data Processing:** Imports customer feedback records and validates required columns.
- **Performance Metrics:** Calculates average customer ratings, recommendation rates, contact requests, and feedback category totals.
- **Product Issue Analysis:** Classifies product complaints by category and severity using Python keyword-based rules.
- **Issue Prioritization:** Identifies high-, medium-, and low-severity product issues and suggests corrective actions.
- **Feedback Theme Analysis:** Identifies recurring themes in customer suggestions and compliments.
- **AI Management Analysis:** Uses the OpenAI API to generate a professional executive analysis based on the calculated results.
- **Automated PDF Reporting:** Produces a dated PDF report containing statistics, product issues, customer suggestions, compliments, and AI-generated management recommendations.
- **Error Handling:** Continues generating the statistical PDF report if the AI service is unavailable.

## Technologies

- Python
- OpenAI API (`gpt-4.1-mini`)
- ReportLab — PDF generation
- python-dotenv — Environment variable management
- CSV — Standard Python library for reading feedback datasets

## Project Structure

```text
CustomerFeedbackAnalyzer/
├── main.py
├── ai_summary.py
├── report.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env                  # Local only; excluded from Git
└── data/
    └── customer_feedback_dataset.csv
```

## How It Works

1. **Data Import:** The application reads customer feedback from a CSV file.
2. **Validation:** It verifies that all required columns are present.
3. **Statistical Analysis:** Python calculates customer satisfaction indicators and feedback category totals.
4. **Issue Classification:** Product complaints are categorized by severity, with suggested corrective actions.
5. **Theme Identification:** Customer suggestions and compliments are analyzed using predefined keywords.
6. **AI Analysis:** Aggregated statistics and analysis results are sent to the OpenAI API to generate an executive summary.
7. **PDF Generation:** The application produces a management report containing the statistical results, AI analysis, and detailed customer feedback.

The statistical and rule-based analyses are performed locally in Python. The OpenAI API is used to interpret the aggregated results and produce a management-level narrative.

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/GeniOakwood/CustomerFeedbackAnalyzer.git
cd CustomerFeedbackAnalyzer
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**4. Configure the OpenAI API**

Create a `.env` file in the project directory:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

An OpenAI API key with available billing credits is required for AI-generated analysis.

Never commit the `.env` file or expose the API key publicly.

**5. Run the application**

```bash
python main.py
```

The application reads the CSV dataset and generates a dated PDF report in the project directory.

## Example Analysis

The sample dataset contains 50 customer feedback records.

| Metric | Result |
|---|---|
| Average customer rating | 3.44 / 5 |
| Recommendation rate | 72% |
| Product issues | 16 |
| Customer suggestions | 12 |
| Customer compliments | 14 |
| Other feedback | 8 |
| Contact requests | 10 |

The analysis identified recurring mechanical concerns involving pruning shears and hand trowels, alongside customer suggestions relating to product design, ergonomics, and handle length.

These findings are used to generate management recommendations and prioritize potential improvements.

## API Integration and Reliability

The OpenAI API generates a concise executive analysis from the application's structured results.

The integration includes:

- Secure API key management through environment variables.
- A low-cost language model for management-level interpretation.
- Instructions to avoid unsupported findings and invented statistics.
- Exception handling to preserve PDF generation if the API request fails.

If the API is unavailable, the application produces the statistical report with a message explaining that AI analysis could not be generated.

## Project Purpose

This project was developed as a practical Python portfolio application to demonstrate:

- Data processing and validation
- Statistical analysis
- Rule-based text classification
- API integration
- Automated report generation
- Error handling
- Modular Python application design

It demonstrates how Python and generative AI can work together to transform raw customer feedback into actionable management information.

## Future Improvements

Potential extensions include support for additional datasets, more advanced text classification, and automated analysis of larger volumes of feedback.

## Author

Genevieve Duchesne

GitHub: [GeniOakwood](https://github.com/GeniOakwood)