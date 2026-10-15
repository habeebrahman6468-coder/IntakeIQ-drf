from google import genai

import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = genai.Client(api_key=api_key)

def get_diet_plan(response_data):

    total_calorie = response_data.get("total_calorie")

    mealtype_summary = response_data.get("mealtype_summary")

    mealtype_summary_text = ""

    for di in mealtype_summary:

        mealtype_summary_text += f".{di.get("meal_type")} : {di.get("total")}\n"

        prompt = f"""
                Act as an expert dietitian specializing in healthy meal planning for people in Kerala, India.

Here is my monthly food summary of last month:
- Total Calories Consumed: {total_calorie}
- Meal Type Breakdown: {mealtype_summary_text}

Based on this data, provide a practical diet plan covering:

1. **Diet Analysis:** Analyze my calorie intake and eating patterns.
2. **Monthly Diet Plan:** Suggest balanced Kerala-style meals for breakfast, lunch, dinner, and snacks.
3. **Nutrition Tips:** Provide 3 to 4 simple tips for healthier eating.
4. **Affordable Choices:** Recommend nutritious, budget-friendly foods available locally.
5. **Health and Safety:** Consider allergies, dietary restrictions, and medical conditions.
 Avoid medical claims or extreme diets, and recommend professional guidance for health conditions requiring specialized nutrition."""

        # Step 4: Call Gemini 2.5 Flash
    response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        

    return response.text

    print(mealtype_summary_text)    