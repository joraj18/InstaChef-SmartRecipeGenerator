import os
import google.generativeai as genai
import jsonify
import json

with open("API\config\config.json", "r") as file:
    config = json.load(file)

    # Configure API key
    api_key = config["GENAI_API_KEY"]
    genai.configure(api_key=api_key)      

    # Create the model instance
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def llm(user_input):
    prompt = (
        "Using the following ingredients, provide creative recipes: "
        f"{user_input}. Include ingredient quantities, instructions, nutritional information, "
        "serving size, preparation time, and any helpful tips or healthy substitutes. Do not give in markdown format.Also mention recipe1, recipe2 etc,."
    )

    # Generate the response
    response = model.generate_content(prompt)

    return (response.text)


