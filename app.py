import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyBCUY56nWobfSVoxRWemGkjBtWunrpmBrs")

model = genai.GenerativeModel("gemini-1.5-pro")

@app.route("/", methods=["GET"])
def home():
    return "✅ Travel Planner API is Running!"

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    data = request.get_json()

    # Collect data with defaults
    start = data.get("start", "Salem")
    destination = data.get("destination", "Goa")
    travel_mode = data.get("travel_mode", "Train")
    trip_type = data.get("trip_type", "Solo")
    accommodation = data.get("accommodation", "Hotel")
    language = data.get("language", "English")
    food = data.get("food", [])
    must_include = data.get("must_include", "Beaches")
    must_avoid = data.get("must_avoid", "Crowds")
    accessibility = data.get("accessibility", "None")
    budget = data.get("budget", "₹10,000 - ₹15,000")
    num_days = data.get("num_days", "")

    # Create Gemini Prompt
    prompt = f"""
    Plan a travel itinerary from {start} to {destination}.
    {f"Duration: {num_days} days." if num_days else "You decide the ideal number of days."}

    Preferences:
    - Travel Mode: {travel_mode}
    - Trip Type: {trip_type}
    - Accommodation: {accommodation}
    - Food: {', '.join(food) if food else 'No specific preference'}
    - Must Include: {must_include or 'None'}
    - Must Avoid: {must_avoid or 'None'}
    - Language: {language}
    - Accessibility: {accessibility}
    - Budget: {budget}

    Include:
    - Timeline with activities
    - Cost and time management suggestions
    - Place-to-place navigation
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({
            "plan": response.text,
            "flow": {
                "start": start,
                "travel_mode": travel_mode,
                "destination": destination,
                "accommodation": accommodation,
                "must_include": must_include,
                "budget": budget,
                "num_days": num_days or "Flexible"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Run the Flask App ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)