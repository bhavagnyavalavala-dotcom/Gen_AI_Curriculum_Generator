from flask import Flask, render_template, request, send_file
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

app = Flask(__name__)

generated_text = ""


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/generate', methods=['POST'])
def generate():
    global generated_text

    # -------- SAFE FORM READ --------
    skill = request.form.get('skill', '')
    level = request.form.get('level', '')
    semesters = request.form.get('semesters', '')
    duration = request.form.get('duration', '')
    focus = request.form.get('focus', '')
    assessment = request.form.get('assessment', '')

    prompt = f"""
Create a professional university-level curriculum.

Skill: {skill}
Level: {level}
Total Semesters: {semesters}
Course Duration (Years): {duration}
Industry Focus: {focus}
Assessment Type: {assessment}

FORMAT STRICTLY:

## Curriculum Overview
## Semester-wise Breakdown
For each semester:
Semester X:
Subjects: ...
Projects: ...
Key Outcomes: ...

## Tools & Technologies
## Career Opportunities
## Learning Outcomes
"""

    # -------- SAFE OLLAMA CALL --------
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "granite3.3:2b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        result = response.json()
        generated_text = result.get("response", "Error generating content.")

    except Exception as e:
        generated_text = f"Error connecting to Ollama: {e}"

    # -------- FORMAT OUTPUT --------
    sections = generated_text.split("##")
    formatted_output = ""

    for section in sections:
        if section.strip() == "":
            continue

        lines = section.strip().split("\n")
        title = lines[0]
        content = "\n".join(lines[1:]).strip()

        # Semester block formatting (NO TABLES)
        if "Semester-wise Breakdown" in title:
            formatted_output += f"<h2>{title}</h2>"

            semesters_raw = content.split("Semester ")

            for sem in semesters_raw:
                if sem.strip() == "":
                    continue

                sem_lines = sem.strip().split("\n")
                sem_title = sem_lines[0].replace(":", "")

                formatted_output += f"<div class='semester-box'>"
                formatted_output += f"<h3>Semester {sem_title}</h3>"

                for line in sem_lines[1:]:
                    if ":" in line:
                        key, val = line.split(":", 1)
                        formatted_output += f"<p><b>{key}:</b> {val}</p>"

                formatted_output += "</div>"

        else:
            content_html = content.replace("\n", "<br>")
            formatted_output += f"<h2>{title}</h2><p>{content_html}</p>"

    return f"""
    <html>
    <head>
    <title>Curriculum Report</title>
    <style>

    body {{
        font-family: Georgia, serif;
        background: #f5f7fb;
        padding: 40px;
    }}

    .container {{
        background: white;
        padding: 40px;
        border-radius: 12px;
        max-width: 1000px;
        margin: auto;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }}

    h1 {{
        text-align:center;
        color:#2a5298;
    }}

    h2 {{
        color: #1e3c72;
        border-bottom: 2px solid #1e3c72;
        padding-bottom: 5px;
        margin-top: 30px;
    }}

    h3 {{
        color: #2a5298;
        margin-top: 20px;
    }}

    p {{
        font-size: 16px;
        line-height: 1.7;
        color: #333;
    }}

    .semester-box {{
        background: #f0f4ff;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        border-left: 5px solid #2a5298;
    }}

    button {{
        padding: 10px 15px;
        background: #2a5298;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        margin-right: 10px;
    }}

    button:hover {{
        background: #1e3c72;
    }}

    </style>
    </head>

    <body>
    <div class="container">
    <h1>📘 AI Generated Curriculum</h1>

    {formatted_output}

    <br><br>

    <a href="/download"><button>Download PDF</button></a>
    <a href="/"><button>Go Back</button></a>

    </div>
    </body>
    </html>
    """


@app.route('/download')
def download_pdf():
    global generated_text

    file_path = "Curriculum_Report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter)

    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    elements = []

    for line in generated_text.split("\n"):
        safe_line = line.replace("&", "&amp;")
        elements.append(Paragraph(safe_line, normal))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
