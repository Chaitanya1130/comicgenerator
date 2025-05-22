# textgen_comic.py
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

def generate_comic_script(
    topic: str,
    grade_level: str,
    comic_tone: str = "funny and educational",
    character_types: str = "students and teachers",
    number_of_panels: int = 6
) -> str:
    
    system_prompt = f"""
You are a creative AI comic writer and educational content designer.
Your job is to generate a full script for a {number_of_panels}-panel educational comic strip about "{topic}" for {grade_level} students.
Tone should be {comic_tone} with characters like {character_types}.

Output format:
1. **Title**
2. **Short Introduction**
3. **Comic Strip Panels**:
   - Panel 1: [Scene description] — [Dialogue]
   - Panel 2: ...
4. **Educational Takeaway** (one-line conclusion or moral)

Make it engaging, conceptually accurate, age-appropriate, and visually imaginative.
Return only the script content.
"""

    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        system=system_prompt,
        messages=[
            {"role": "user", "content": system_prompt}
        ],
        max_tokens=1024,
        temperature=0.8
    )

    return response.content[0].text













