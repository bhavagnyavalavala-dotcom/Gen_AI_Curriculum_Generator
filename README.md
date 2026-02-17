🚀 AI Curriculum Generator — Hackathon Project
📌 Problem Statement:
Designing a structured, industry-aligned academic curriculum is time-consuming and requires domain expertise. Most institutions and learners struggle to quickly generate semester-wise learning paths that match evolving industry needs.

Manual curriculum planning often leads to:
• Outdated course structures
• Poor industry alignment
• Lack of personalization
• High planning effort

Solution:
AI Curriculum Generator is a smart web application that automatically creates a professional, semester-wise curriculum based on:

• Skill domain
• Experience level
• Course duration
• Industry focus
• Assessment type

The system uses a local AI model to generate structured academic roadmaps instantly and exports them as downloadable PDF reports.

Hackathon Value Proposition:
This project demonstrates:
 Practical Generative AI integration
 Real-world education technology use case
 Full-stack AI application design
 Offline-capable AI inference using local models
 Production-style API architecture
 Exportable structured outputs

Core Features:
• AI-generated curriculum overview
• Semester-wise structured breakdown
• Tools & technologies mapping
• Career opportunities section
• Learning outcomes summary
• Professional formatted output UI
• PDF export support
• Works fully offline using local AI model

System Architecture:
User Input Form
      ↓
Flask Backend API
      ↓
Prompt Builder Service
      ↓
Local AI Model (Ollama)
      ↓
Structured Output Parser
      ↓
Formatted Web Interface
      ↓
PDF Export Generator

Tech Stack:
Backend
• Python
• Flask

AI Engine
• Local LLM via Ollama
• Granite / Phi models

Frontend
• HTML
• CSS
• Jinja Templates

Document Export
• ReportLab (PDF generation)

How It Works:
1. User enters curriculum parameters
2. Backend builds structured AI prompt
3. Local AI model generates curriculum
4. Output is parsed into readable format
5. Semester sections rendered with styled blocks
6. User can download PDF report

Installation & Setup:
Step 1 — Clone Repository
git clone <https://github.com/bhavagnyavalavala-dotcom/Gen_AI_Curriculum_Generator>
cd ai-curriculum-generator

Step 2 — Create Virtual Environment
python -m venv venv
venv\Scripts\activate

Step 3 — Install Dependencies
pip install flask requests reportlab

Step 4 — Install Ollama
Install Ollama locally and pull model:
ollama pull granite3.3:2b

Step 5 — Run Ollama
ollama run granite3.3:2b

Step 6 — Run Application
python app.py

Open browser:
http://127.0.0.1:5000

