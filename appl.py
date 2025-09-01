from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load local model (small, runs offline)
generator = pipeline("text-generation", model="gpt2-medium")

@app.route("/", methods=["GET", "POST"])
def home():
    plan = ""
    if request.method == "POST":
        name = request.form.get("name")
        household_size = request.form.get("household_size")
        activities = request.form.get("activities")
        city = request.form.get("city")

        prompt = (
            f"Create a personalized daily water usage and conservation plan for {name} "
            f"who lives in {city} with a household of {household_size} people. "
            f"They do activities like {activities}. "
            "Give practical water-saving advice in 3-4 friendly sentences."
        )

        response = generator(prompt, max_length=120, num_return_sequences=1)
        plan = response[0]["generated_text"].split("\n")[0]

    return render_template("index.html", plan=plan)

if __name__ == "__main__":
    app.run(debug=True)
