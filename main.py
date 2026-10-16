import csv
from ai_summary import generate_ai_summary
from report import generate_pdf_report
# 1. VARIABLE
file_path = "data/customer_feedback_dataset.csv"
# 2. VARIABLE — list containing required field names
required_columns = [
    "Submission date",
    "Order number",
    "Product",
    "Feedback type",
    "Overall rating",
    "Would recommend?",
    "Comment",
    "Improvement suggestion",
    "Contact requested?"
]

# 3. FUNCTION
def prepare_row(row):
    row["Overall rating"] = int(row["Overall rating"])
    row["Would recommend?"] = row["Would recommend?"] == "Yes"
    row["Contact requested?"] = row["Contact requested?"] == "Yes"

    return row

def calculate_average_rating(feedback_data):
    total_rating = 0

    for row in feedback_data:
        total_rating += row["Overall rating"]

    average_rating = total_rating / len(feedback_data)

    return average_rating

def calculate_recommendation_rate(feedback_data):
    recommend_count = 0

    for row in feedback_data:
        if row["Would recommend?"]:
            recommend_count += 1

    recommendation_rate = recommend_count / len(feedback_data) * 100

    return recommendation_rate

def count_contact_requests(feedback_data):
    contact_count = 0

    for row in feedback_data:
        if row["Contact requested?"]:
            contact_count += 1

    return contact_count

def count_records(feedback_data, feedback_type):
    count = 0

    for row in feedback_data:
        if row["Feedback type"] == feedback_type:
            count += 1

    return count

def count_issue_by_product(feedback_data):
    issue_count = {}

    for row in feedback_data:
        if row["Feedback type"] == "Product issue":
            product = row["Product"]
            if product in issue_count:
                issue_count[product] += 1
            else:
                issue_count[product] =1
    return issue_count

def extract_issue_comments(feedback_data):
    issue_comments = []

    for row in feedback_data:
        if row["Feedback type"] == "Product issue":
            product = row["Product"]
            comment = row["Comment"]
            if comment:
                issue_comments.append((product,comment))

    return issue_comments

def analyze_issue_comment(product,comment):
    analysis = {}
    analysis["product"] = product
    analysis["comment"] = comment
    analysis["issue_category"] = ""
    analysis["severity"] = ""
    analysis["summary"] = ""
    analysis["suggested_action"] = ""

    if "lock" in comment.lower():
        analysis["issue_category"] = "Safety/Mechanical"
    elif "loose" in comment.lower() or "wobbl" in comment.lower():
        analysis["issue_category"] = "Mechanical/Assembly"
    elif "moves" in comment.lower():
        analysis["issue_category"] = "Mechanical/Assembly"
    elif "grip" in comment.lower() or "sore" in comment.lower():
        analysis["issue_category"] = "Ergonomics"
    elif "bent" in comment.lower():
        analysis["issue_category"] = "Durability"

    if analysis["issue_category"] == "Safety/Mechanical":
        analysis["severity"] = "High"
    elif analysis["issue_category"] in ["Mechanical/Assembly", "Durability"]:
        analysis["severity"] = "Medium"
    elif analysis["issue_category"] == "Ergonomics":
        analysis["severity"] = "Low"

    if analysis["issue_category"] == "Safety/Mechanical":
        analysis["summary"] = "Locking mechanism failure"
    elif analysis["issue_category"] == "Mechanical/Assembly":
        analysis["summary"] = "Loose or unstable components"
    elif analysis["issue_category"] == "Ergonomics":
        analysis["summary"] = "Discomfort during use"
    elif analysis["issue_category"] == "Durability":
        analysis["summary"] = "Component deformation"

    if analysis["issue_category"] == "Safety/Mechanical":
        analysis["suggested_action"] = "Inspect locking mechanism and review product safety"
    elif analysis["issue_category"] == "Mechanical/Assembly":
        analysis["suggested_action"] = "Inspect assembly and component stability"
    elif analysis["issue_category"] == "Ergonomics":
        analysis["suggested_action"] = "Review handle design and user comfort"
    elif analysis["issue_category"] == "Durability":
        analysis["suggested_action"] = "Review material strength and durability"

    return analysis

def summarize_complaints(feedback_data):
    complaint_summary = {}
    for row in feedback_data:
        if row["Feedback type"] == "Product issue":
            product = row["Product"]
            comment = row["Comment"]
            analysis = analyze_issue_comment(product, comment)
            if product not in complaint_summary:
                complaint_summary[product] = {
                    "total_issues": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
            complaint_summary[product]["total_issues"] += 1
            severity = analysis["severity"].lower()
            complaint_summary[product][severity] += 1
    return complaint_summary

def summarize_feedback_themes(feedback_data, feedback_type):
    themes = {
        "Ergonomics": ["grip", "comfort", "padded", "soft", "sore"],
        "Handle length": ["long-handle", "extended-handle", "longer handle"],
        "Product performance": ["sharp", "cut", "strong", "effective", "solid"],
        "Storage and convenience": ["storage", "hanging", "hole"],
        "Product design": ["color", "markings", "version", "model"]
    }

    theme_counts = {}

    for row in feedback_data:
        if row["Feedback type"] == feedback_type:

            if feedback_type == "Suggestion":
                comment = row["Improvement suggestion"].lower()
            else:
                comment = row["Comment"].lower()

            for theme, keywords in themes.items():
                if any(keyword in comment for keyword in keywords):
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1

    return dict(
        sorted(
            theme_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

def generate_summary(feedback_data):
    average_rating = calculate_average_rating(feedback_data)
    recommendation_rate = calculate_recommendation_rate(feedback_data)
    contact_requests = count_contact_requests(feedback_data)
    product_issues = count_records(feedback_data, "Product issue")
    suggestions = count_records(feedback_data, "Suggestion")
    compliments = count_records(feedback_data, "Compliment")
    other = count_records(feedback_data, "Other")

    summary = {}
    summary["average_rating"] = average_rating
    summary["recommendation_rate"] = recommendation_rate
    summary["contact_requests"] = contact_requests
    summary["product_issues"] = product_issues
    summary["suggestions"] = suggestions
    summary["compliments"] = compliments
    summary["other"] = other
    return summary

# 4. MAIN EXECUTION / PROGRAM LOGIC
def main():
    feedback_data = []


    with open(file_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)



    # Validate that all expected columns exist
        missing_columns = [
            column for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        for row in reader:
            row = prepare_row(row)
            feedback_data.append(row)
    summary = generate_summary(feedback_data)
    print(summary)
    complaint_summary = summarize_complaints(feedback_data)
    print("Complaint summary by product:")
    for product, counts in complaint_summary.items():
        print(product, counts)
    print(len(feedback_data))

    average_rating = calculate_average_rating(feedback_data)
    print("Average rating:", average_rating)

    recommendation_rate = calculate_recommendation_rate(feedback_data)
    print("Would recommend:", recommendation_rate, "%")

    contact_requests = count_contact_requests(feedback_data)
    print("Contact requested:", contact_requests)

    issue_count = count_issue_by_product(feedback_data)
    for product,count in issue_count.items():
        print(product,count)

    issue_comments = extract_issue_comments(feedback_data)
    product,comment = issue_comments[0]
    analysis = analyze_issue_comment (product,comment)
    print(analysis)
    for product, comment in issue_comments:
        analysis = analyze_issue_comment(product, comment)
        print(product, "|", analysis["issue_category"], "|", analysis["severity"], "|", analysis["summary"], "|", analysis["suggested_action"], "|", comment)


    product_issues = count_records(feedback_data, "Product issue")
    suggestions = count_records(feedback_data, "Suggestion")
    compliments = count_records(feedback_data, "Compliment")
    other = count_records(feedback_data, "Other")

    print("Product issues:", product_issues)
    print("Suggestions:", suggestions)
    print("Compliments:", compliments)
    print("Other:", other)

    suggestion_themes = summarize_feedback_themes(feedback_data, "Suggestion")
    compliment_themes = summarize_feedback_themes(feedback_data, "Compliment")

    try:
        ai_summary = generate_ai_summary(
        summary,
        complaint_summary,
        suggestion_themes,
        compliment_themes
        )
    except Exception as error:
        print(f"AI analysis unavailable: {error}")
        ai_summary = (
            "AI analysis was unavailable. "
            "The statistical analysis remains available."
    )

    print("\nAI EXECUTIVE SUMMARY")
    print(ai_summary)

    print("Suggestion themes:", suggestion_themes)
    print("Compliment themes:", compliment_themes)

    generate_pdf_report(summary, feedback_data, complaint_summary, ai_summary)
    print("PDF report generated successfully.")

if __name__ == "__main__":
            main()