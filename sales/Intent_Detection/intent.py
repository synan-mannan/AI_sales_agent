import json
from sales.llm import getllm

llm = getllm() # make sure GROQ_API_KEY is set



def analyze_and_reply(email_text):
    prompt = f"""
You are an AI sales assistant.

Your job:
1. Classify the intent of the email
2. Generate a professional reply

Return ONLY JSON in this format:
{{
  "intent": "...",
  "reply": "..."
}}

Possible intents:
- Product Inquiry
- Pricing Request
- Demo Request
- Not Interested
- Spam
- General Inquiry

Customer Email:
\"\"\"
{email_text}
\"\"\"
"""

    response = llm.invoke(prompt)

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "intent": "Unknown",
            "reply": content  # fallback if JSON parsing fails
        }




emails = [
    "Hi, can you share pricing details?",
    "I would like to schedule a demo this week",
    "Send me more information about your product",
    "Not interested anymore"
]

for email in emails:
    result = analyze_and_reply(email)

    print("Email:", email)
    print("Intent:", result["intent"])
    print("Reply:", result["reply"])
    print("=" * 60)