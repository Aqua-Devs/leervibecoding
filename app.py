"""
LeerVibeCoding.nl - AI-Powered Vibe Coding Platform
Dynamische opdrachten gegenereerd door OpenAI met progressieve moeilijkheid
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory
import requests
import secrets
import json
import os

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Difficulty progression - van basis HTML naar AI-powered apps
DIFFICULTY_LEVELS = [
    {"level": 1, "name": "HTML Basics", "focus": "Simpele HTML structuur en tekst", "ai_integration": False, "min_xp": 0},
    {"level": 2, "name": "Styling", "focus": "CSS styling, kleuren, layout", "ai_integration": False, "min_xp": 50},
    {"level": 3, "name": "Interactie", "focus": "JavaScript buttons, events", "ai_integration": False, "min_xp": 150},
    {"level": 4, "name": "Formulieren", "focus": "Forms, validatie, data", "ai_integration": False, "min_xp": 300},
    {"level": 5, "name": "AI Tekst", "focus": "AI-gegenereerde content", "ai_integration": True, "min_xp": 500},
    {"level": 6, "name": "AI Chat", "focus": "Chatbot integratie", "ai_integration": True, "min_xp": 750},
    {"level": 7, "name": "AI Tools", "focus": "AI-powered tools en analyse", "ai_integration": True, "min_xp": 1000},
    {"level": 8, "name": "AI Apps", "focus": "Complete AI-applicaties", "ai_integration": True, "min_xp": 1500},
]

def call_openai(api_key, messages, model="gpt-4o-mini", max_tokens=4000):
    """Call OpenAI API"""
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.8
            },
            timeout=90
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print(f"OpenAI error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"OpenAI exception: {e}")
        return None

def generate_assignment(api_key, level, completed_assignments):
    """Generate a new assignment based on current level"""
    level_info = DIFFICULTY_LEVELS[min(level - 1, len(DIFFICULTY_LEVELS) - 1)]
    
    # Build context about what user has already done
    history_context = ""
    if completed_assignments:
        recent = completed_assignments[-3:]  # Last 3 assignments
        history_context = f"De gebruiker heeft al {len(completed_assignments)} opdrachten gedaan. Recent: {', '.join(recent)}. Geef iets NIEUWS."
    
    system_prompt = """Je bent een creatieve opdracht-generator voor LeerVibeCoding, een platform waar mensen leren AI te gebruiken om websites te bouwen.

Je genereert UITDAGENDE, REALISTISCHE opdrachten in het Nederlands.

BELANGRIJK:
- Maak het scenario herkenbaar (lokale bedrijven, studenten, verenigingen, startups)
- De opdracht moet CONCREET zijn met duidelijke, meetbare requirements
- Geef 5 specifieke SUCCESS CRITERIA waaraan het resultaat MOET voldoen
- Criteria moeten CHECKBAAR zijn (zoekwoorden die in de code moeten voorkomen)

OUTPUT ALLEEN VALID JSON:
{
    "title": "Korte pakkende titel",
    "client_name": "Naam van de fictieve klant",
    "client_emoji": "Een emoji voor de klant (bijv: 👩‍🍳, 🏪, 💼)",
    "scenario": "Het verhaal (2-3 zinnen, spreek de gebruiker aan met 'je')",
    "task": "Concrete opdracht (1-2 zinnen)",
    "requirements": ["Vereiste 1", "Vereiste 2", "Vereiste 3", "Vereiste 4", "Vereiste 5"],
    "success_criteria": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "hints": ["Tip 1", "Tip 2", "Tip 3"]
}"""

    if level_info["ai_integration"]:
        level_prompt = f"""
NIVEAU: {level_info['level']} - {level_info['name']}
FOCUS: {level_info['focus']}
OPDRACHT NUMMER: {len(completed_assignments) + 1}

{history_context}

Dit niveau VEREIST AI-INTEGRATIE! De gebruiker moet een website maken die:
- De OpenAI API aanroept vanuit JavaScript in de browser
- AI-gegenereerde content toont aan de gebruiker
- ECHT WERKT en indrukwekkend is

VOORBEELDEN VAN AI-INTEGRATIES:
Level 5 (AI Tekst):
- Blog post generator
- Product beschrijving schrijver
- Email template maker
- Slogan generator voor bedrijven

Level 6 (AI Chat):
- Klantenservice chatbot
- Persoonlijke assistent
- FAQ beantwoorder
- Virtuele verkoper

Level 7 (AI Tools):
- Sentiment analyzer voor reviews
- Tekst samenvatten tool
- Vertaal applicatie
- Code uitleg tool

Level 8 (AI Apps):
- Volledige AI-powered dashboard
- Interactieve leer-applicatie
- AI content management systeem
- Multi-functie AI werkplek

De success_criteria MOETEN bevatten: "fetch", "openai", "async" en relevante UI elementen.
Genereer een INDRUKWEKKENDE opdracht die de gebruiker laat zien wat mogelijk is!"""
    else:
        level_prompt = f"""
NIVEAU: {level_info['level']} - {level_info['name']}
FOCUS: {level_info['focus']}
OPDRACHT NUMMER: {len(completed_assignments) + 1}

{history_context}

Dit niveau focust op: {level_info['focus']}

PROGRESSIE PER NIVEAU:
Level 1 (HTML): Tekst, koppen, lijsten, structuur, semantische HTML
Level 2 (Styling): Kleuren, fonts, layout, flexbox, moderne CSS
Level 3 (Interactie): Buttons, click events, DOM manipulatie, animaties
Level 4 (Formulieren): Input velden, validatie, form handling, data verwerking

Maak de opdracht UITDAGEND maar haalbaar voor dit niveau.
Success criteria moeten relevante HTML/CSS/JS keywords bevatten die in de code voorkomen."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": level_prompt}
    ]
    
    response = call_openai(api_key, messages)
    
    if response:
        try:
            # Extract JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                assignment = json.loads(response[json_start:json_end])
                assignment['level'] = level_info['level']
                assignment['level_name'] = level_info['name']
                assignment['ai_integration'] = level_info['ai_integration']
                assignment['base_xp'] = 20 + (level_info['level'] * 15)  # XP scales with level
                return assignment
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
    
    return None

def generate_code(api_key, user_prompt, assignment):
    """Generate working code from user's prompt"""
    
    ai_code_template = ""
    if assignment.get('ai_integration'):
        ai_code_template = """
VERPLICHT VOOR AI-INTEGRATIE:
De code MOET deze werkende OpenAI API call bevatten:

```javascript
// API Key wordt door het platform geïnjecteerd
const OPENAI_API_KEY = window.OPENAI_API_KEY;

async function callAI(prompt) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + OPENAI_API_KEY,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'gpt-4o-mini',
            messages: [{role: 'user', content: prompt}],
            max_tokens: 1000
        })
    });
    const data = await response.json();
    return data.choices[0].message.content;
}
```

Gebruik deze functie in de code voor AI-functionaliteit!
"""

    system_prompt = f"""Je bent een expert web developer die COMPLETE, WERKENDE HTML/CSS/JS code genereert.

STRIKTE REGELS:
1. Output ALLEEN complete HTML (één bestand, GEEN markdown, GEEN uitleg)
2. CSS MOET in een <style> tag IN de HTML staan
3. JavaScript MOET in een <script> tag IN de HTML staan
4. GEEN externe files, ALLES inline
5. Voor afbeeldingen: https://picsum.photos/[width]/[height]?random=[nummer]
6. Moderne, MOOIE styling (gradients, shadows, border-radius, animations)
7. RESPONSIVE design
8. De code moet DIRECT WERKEN in een iframe

{ai_code_template}

OPDRACHT CONTEXT:
Titel: {assignment.get('title', '')}
Klant: {assignment.get('client_name', '')}
Scenario: {assignment.get('scenario', '')}
Taak: {assignment.get('task', '')}
Requirements: {json.dumps(assignment.get('requirements', []), ensure_ascii=False)}

Begin DIRECT met <!DOCTYPE html> - GEEN uitleg, GEEN markdown!"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Genereer code voor:\n\n{user_prompt}"}
    ]
    
    return call_openai(api_key, messages, max_tokens=4000)

def evaluate_result(api_key, user_prompt, code, assignment):
    """Evaluate the generated code"""
    
    system_prompt = """Je bent een eerlijke beoordelaar van web development opdrachten.
Je taak is om te evalueren of de code voldoet aan de requirements.

SCORING RICHTLIJNEN:
- 100: Alle requirements goed geïmplementeerd, ziet er professioneel uit
- 85-99: Bijna perfect, kleine details kunnen beter
- 70-84: Goed werk, de meeste requirements zijn aanwezig
- 50-69: Basis is aanwezig maar belangrijke dingen missen
- 30-49: Gedeeltelijk gedaan, veel verbeterpunten
- 0-29: Voldoet niet aan de opdracht

WEES EERLIJK MAAR NIET TE STRENG:
- Als de basis goed is en het werkt, geef minimaal 70%
- Kleine styling verschillen zijn geen grote problemen
- Focus op functionaliteit en de kernrequirements

Output ALLEEN valid JSON:
{
    "score": 0-100,
    "criteria_results": {"criterium": true/false, ...},
    "feedback": "Specifieke feedback in het Nederlands",
    "missing": ["Wat er concreet mist"],
    "suggestions": ["Concrete verbetersuggestie voor de prompt"]
}"""

    requirements = assignment.get('requirements', [])
    criteria = assignment.get('success_criteria', [])
    
    evaluation_prompt = f"""
OPDRACHT: {assignment.get('title')}
KLANT: {assignment.get('client_name')}
TAAK: {assignment.get('task')}

REQUIREMENTS:
{chr(10).join(f"- {r}" for r in requirements)}

SUCCESS CRITERIA (keywords/elementen):
{json.dumps(criteria, ensure_ascii=False)}

GEBRUIKER'S PROMPT:
{user_prompt}

GEGENEREERDE CODE:
{code[:4000]}

Beoordeel eerlijk maar rechtvaardig."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": evaluation_prompt}
    ]
    
    response = call_openai(api_key, messages, max_tokens=1000)
    
    if response:
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                return json.loads(response[json_start:json_end])
        except:
            pass
    
    # Fallback: keyword check
    code_lower = code.lower()
    criteria_results = {}
    for c in criteria:
        criteria_results[c] = c.lower() in code_lower
    
    criteria_met = sum(1 for v in criteria_results.values() if v)
    total = len(criteria) if criteria else 1
    pct = criteria_met / total
    
    # Fair scoring based on criteria
    if pct >= 1.0:
        score = 100
    elif pct >= 0.8:
        score = 85
    elif pct >= 0.6:
        score = 70
    elif pct >= 0.4:
        score = 55
    else:
        score = 35
    
    return {
        "score": score,
        "criteria_results": criteria_results,
        "feedback": f"{criteria_met}/{total} criteria gevonden in de code",
        "missing": [c for c, met in criteria_results.items() if not met],
        "suggestions": ["Wees specifieker in je prompt", "Noem alle requirements expliciet"]
    }

# ============ ROUTES ============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bouwen')
def bouwen():
    return render_template('studio.html', levels=DIFFICULTY_LEVELS)

@app.route('/oefenruimte')
def oefenruimte():
    return render_template('studio.html', levels=DIFFICULTY_LEVELS)

@app.route('/studio')
def studio():
    return render_template('studio.html', levels=DIFFICULTY_LEVELS)

@app.route('/oefeningen')
def oefeningen():
    return render_template('studio.html', levels=DIFFICULTY_LEVELS)

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/starten')
def starten():
    return render_template('tools.html')

@app.route('/workflow')
def workflow():
    return render_template('workflow.html')

@app.route('/ehbo')
def ehbo():
    return render_template('ehbo.html')

@app.route('/inspiratie')
def inspiratie():
    return render_template('inspiratie.html')

@app.route('/live-gaan')
def live_gaan():
    return render_template('live-gaan.html')

# SEO Routes
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml', mimetype='application/xml')

@app.route('/og-image.png')
def og_image():
    return send_from_directory(app.static_folder, 'og-image.svg', mimetype='image/svg+xml')

@app.route('/logo.svg')
def logo():
    return send_from_directory(app.static_folder, 'logo.svg', mimetype='image/svg+xml')

@app.route('/api/validate-key', methods=['POST'])
def validate_key():
    """Validate OpenAI API key"""
    data = request.json
    api_key = data.get('api_key', '').strip()
    
    if not api_key or not api_key.startswith('sk-'):
        return jsonify({'valid': False, 'error': 'Ongeldige key format'})
    
    # Test the key
    test = call_openai(api_key, [{"role": "user", "content": "Hi"}], max_tokens=5)
    
    if test:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False, 'error': 'Key werkt niet'})

@app.route('/api/generate-assignment', methods=['POST'])
def api_generate_assignment():
    """Generate a new assignment"""
    data = request.json
    api_key = data.get('api_key')
    level = data.get('level', 1)
    completed = data.get('completed', [])
    
    if not api_key:
        return jsonify({"success": False, "error": "API key vereist"})
    
    assignment = generate_assignment(api_key, level, completed)
    
    if assignment:
        return jsonify({"success": True, "assignment": assignment})
    else:
        return jsonify({"success": False, "error": "Kon geen opdracht genereren"})

@app.route('/api/submit-prompt', methods=['POST'])
def api_submit_prompt():
    """Submit prompt and get code + evaluation"""
    data = request.json
    api_key = data.get('api_key')
    user_prompt = data.get('prompt')
    assignment = data.get('assignment')
    
    if not api_key or not user_prompt or not assignment:
        return jsonify({"success": False, "error": "Missende data"})
    
    # Generate code
    code = generate_code(api_key, user_prompt, assignment)
    
    if not code:
        return jsonify({"success": False, "error": "Kon geen code genereren"})
    
    # Clean code (remove markdown if present)
    if "```html" in code:
        code = code.split("```html")[1].split("```")[0].strip()
    elif "```" in code:
        parts = code.split("```")
        if len(parts) >= 2:
            code = parts[1].strip()
            if code.startswith("html"):
                code = code[4:].strip()
    
    # Ensure it starts with DOCTYPE
    if not code.strip().lower().startswith("<!doctype"):
        if "<html" in code.lower():
            code = "<!DOCTYPE html>\n" + code
    
    # Evaluate
    evaluation = evaluate_result(api_key, user_prompt, code, assignment)
    
    # Calculate XP - meer bij hogere scores
    base_xp = assignment.get('base_xp', 30)
    score = evaluation.get('score', 0)
    
    if score >= 100:
        xp_earned = base_xp  # Volle XP
        is_complete = True
    elif score >= 85:
        xp_earned = int(base_xp * 0.8)  # 80% XP
        is_complete = True
    elif score >= 70:
        xp_earned = int(base_xp * 0.6)  # 60% XP
        is_complete = True
    elif score >= 50:
        xp_earned = int(base_xp * 0.3)  # 30% XP
        is_complete = False
    else:
        xp_earned = 0
        is_complete = False
    
    return jsonify({
        "success": True,
        "code": code,
        "evaluation": evaluation,
        "xp_earned": xp_earned,
        "is_complete": is_complete
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
