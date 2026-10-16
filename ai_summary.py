
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_summary(summary, complaint_summary,
                        suggestion_themes, compliment_themes):

    data = {
        "overall_statistics": summary,
        "complaints_by_product": complaint_summary,
        "suggestion_themes": suggestion_themes,
        "compliment_themes": compliment_themes
    }

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "You are a customer feedback analyst preparing a "
            "professional management report. Analyze the provided "
            "statistics, identify key findings, recurring product issues, "
            "customer satisfaction patterns, and recommended actions. "
            "Write a concise executive analysis in 3 to 4 paragraphs. "
            "Do not include a title or an 'Executive Summary' heading. "
            "Base all findings strictly on the supplied data. "
            "Do not invent statistics, trends, or unsupported conclusions. "
            "Present recommendations as possible improvements, not "
            "guaranteed outcomes. Use clear, objective business language."
        ),
        input=json.dumps(data),
        max_output_tokens=500
    )

    return response.output_text
