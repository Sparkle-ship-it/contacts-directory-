from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BATCHES = [
    "Georgia A&R representatives and label executives",
    "Southeast festival coordinators",
    "National A&R representatives",
    "Entertainment lawyers (US-based, music industry)",
    "Global music producers and recording studio contacts",
    "Southeast venue managers and booking coordinators",
    "National festival coordinators",
    "Entertainment lawyers (global music industry)",
    "National venue managers and booking coordinators",
    "Global A&R representatives and label executives"
]

def generate_prompt(batch_focus: str) -> str:
    return f"""... (same long prompt we wrote before, with {batch_focus}) ..."""

def run_batch(batch_focus: str, batch_num: int):
    prompt = generate_prompt(batch_focus)
    response = client.chat.completions.create(
        model="gpt-5",   # you can swap for gpt-5-mini if cost/speed matters
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs strict JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content
    data = json.loads(output)

    # Save as CSV
    import pandas as pd
    df = pd.DataFrame(data["rows"])
    df.to_csv(f"batch_{batch_num}.csv", index=False)
    print(f"Batch {batch_num} saved.")

if __name__ == "__main__":
    for i, batch in enumerate(BATCHES, start=1):
        run_batch(batch, i)

