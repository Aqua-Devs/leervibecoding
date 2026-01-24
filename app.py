"""
LeerVibeCoding.nl - AI-Powered Vibe Coding Platform
Dynamische opdrachten gegenereerd door OpenAI met progressieve moeilijkheid
"""

from flask import Flask, render_template, request, jsonify, session, send_from_directory, redirect
from datetime import timedelta
import requests
import secrets
import json
import os

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Difficulty progression - van basis naar AI-powered apps
DIFFICULTY_LEVELS = [
    {"level": 1, "name": "Je Eerste Stapjes", "focus": "Tekst en plaatjes op een pagina", "ai_integration": False, "min_xp": 0},
    {"level": 2, "name": "Maak Het Mooi", "focus": "Kleuren, lettertypes en layout", "ai_integration": False, "min_xp": 50},
    {"level": 3, "name": "Knoppen & Actie", "focus": "Dingen die bewegen en reageren", "ai_integration": False, "min_xp": 150},
    {"level": 4, "name": "Formulieren", "focus": "Gegevens verzamelen van bezoekers", "ai_integration": False, "min_xp": 300},
    {"level": 5, "name": "AI Schrijft Mee", "focus": "Laat AI teksten schrijven", "ai_integration": True, "min_xp": 500},
    {"level": 6, "name": "Pratende Robots", "focus": "Bouw een chatbot", "ai_integration": True, "min_xp": 750},
    {"level": 7, "name": "Slimme Tools", "focus": "AI-powered hulpmiddelen", "ai_integration": True, "min_xp": 1000},
    {"level": 8, "name": "AI Meester", "focus": "Complete AI-applicaties", "ai_integration": True, "min_xp": 1500},
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
        elif response.status_code == 401:
            print(f"OpenAI error: Invalid API key")
            return None
        elif response.status_code == 429:
            print(f"OpenAI error: Rate limit or quota exceeded")
            return None
        else:
            print(f"OpenAI error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("OpenAI timeout")
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
        recent = completed_assignments[-3:]
        history_context = f"De gebruiker heeft al {len(completed_assignments)} opdrachten afgerond. Recent: {', '.join(recent)}. Verzin iets COMPLEET ANDERS."
    
    assignment_number = len(completed_assignments) + 1
    
    system_prompt = """Je bent een creatieve verhalenverteller die opdrachten verzint voor mensen die willen leren websites te bouwen met AI.

JOUW STIJL:
- Schrijf alsof je een grappige vriend bent die een verhaal vertelt
- GEEN technische termen gebruiken (geen "HTML", "CSS", "JavaScript", "code", "programmeren")
- Schrijf in simpele, alledaagse Nederlandse taal
- Voeg humor toe: grappige situaties, overdrijvingen, herkenbare frustraties
- Maak het verhaal LEVENDIG met details en emotie
- Spreek de lezer direct aan met "je" en "jij"

SCENARIO LENGTE:
- Schrijf een UITGEBREID verhaal van 4-6 zinnen
- Schets de situatie, de klant, het probleem, en waarom het urgent is
- Maak het persoonlijk en herkenbaar

HUMOR ELEMENTEN (kies er minimaal 2):
- Een gestresste ondernemer met een deadline
- Een excentrieke klant met rare wensen
- Een grappige achtergrondverhaal
- Overdreven urgentie ("morgen komt de koningin op bezoek!")
- Herkenbare drama ("de printer is weer stuk, de kat zit op het toetsenbord")
- Typisch Nederlandse situaties (bitterballencrisis, fietsproblemen, weer-klachten)

OUTPUT ALLEEN VALID JSON:
{
    "title": "Pakkende titel (max 5 woorden)",
    "client_name": "Grappige naam voor de klant",
    "client_emoji": "Passende emoji",
    "scenario": "UITGEBREID verhaal (4-6 zinnen) met humor en details. Geen technische termen!",
    "task": "Wat moet er gemaakt worden in simpele woorden (1-2 zinnen). Geen technische termen!",
    "requirements": ["Wat er op moet staan 1", "Wat er op moet staan 2", "etc - in normale mensentaal"],
    "success_criteria": ["zoekwoord1", "zoekwoord2", "zoekwoord3", "zoekwoord4", "zoekwoord5"],
    "hints": ["Praktische tip 1 in mensentaal", "Tip 2", "Tip 3"]
}

BELANGRIJK VOOR REQUIREMENTS:
- Schrijf ze alsof je tegen je oma uitlegt wat er op de website moet komen
- NIET: "Implementeer een responsive header"
- WEL: "Bovenaan moet de naam van de bakkerij staan"
- NIET: "Gebruik flexbox voor de layout"
- WEL: "De taarten moeten naast elkaar staan, niet onder elkaar"

BELANGRIJK VOOR HINTS:
- Geef tips over WAT ze aan de AI moeten vragen
- NIET: "Gebruik CSS grid"
- WEL: "Vraag de AI om de producten in een mooi rijtje te zetten"
- NIET: "Voeg een event listener toe"
- WEL: "Vraag de AI om een knop die iets doet als je erop klikt\""""

    # Difficulty progression
    if level == 1:
        level_prompt = f"""
NIVEAU: Absolute Beginner (Opdracht #{assignment_number})
{history_context}

Dit is voor iemand die nog NOOIT iets met websites heeft gedaan.

MOEILIJKHEIDSGRAAD: Super simpel
- Alleen tekst en plaatjes
- Geen knoppen of bewegende dingen
- Denk aan een simpele poster of flyer, maar dan digitaal

VOORBEELDEN VAN GOEDE SCENARIOS:
- Een bakker die zijn openingstijden online wil zetten
- Een oppas die zichzelf wil voorstellen aan ouders  
- Een voetbalclub die de teamleden wil tonen
- Een oma die haar breipatronen wil delen

Maak het scenario HERKENBAAR en GRAPPIG. Voeg een humoristisch element toe.
De opdracht moet HEEL SIMPEL zijn - gewoon wat tekst op een pagina."""

    elif level == 2:
        level_prompt = f"""
NIVEAU: Beginner met Stijl (Opdracht #{assignment_number})
{history_context}

De gebruiker snapt nu dat je tekst op een pagina kunt zetten. Nu gaan we het MOOI maken.

MOEILIJKHEIDSGRAAD: Iets uitdagender
- Nu met kleuren en mooie lettertypes
- Dingen moeten er professioneel uitzien
- Nog steeds geen knoppen die iets doen

VOORBEELDEN VAN GOEDE SCENARIOS:
- Een hippe koffietent die een menukaart wil die er "instagrammable" uitziet
- Een wedding planner die haar portfolio wil showen
- Een makelaar die een huis wil presenteren alsof het een paleis is
- Een personal trainer die er "fit en succesvol" uit wil zien

Focus op UITERLIJK: kleuren, lettertypes, hoe dingen geplaatst zijn.
Voeg humor toe over klanten die HEEL SPECIFIEK zijn over hoe iets eruit moet zien."""

    elif level == 3:
        level_prompt = f"""
NIVEAU: Nu Wordt Het Interactief (Opdracht #{assignment_number})
{history_context}

De gebruiker kan nu mooie pagina's maken. Tijd voor ACTIE - dingen die bewegen of reageren!

MOEILIJKHEIDSGRAAD: Gemiddeld
- Knoppen die iets doen (tonen/verbergen, kleuren veranderen)
- Dingen die bewegen of animeren
- Interactie met de bezoeker

VOORBEELDEN VAN GOEDE SCENARIOS:
- Een goochelaar die een "klik om te onthullen" truc wil
- Een restaurant met een menu dat je kunt openklappen per categorie
- Een escape room die hints wil verbergen achter knoppen
- Een verjaardagspagina met confetti als je op een knop drukt

De humor zit in klanten die OVERDREVEN enthousiast zijn over simpele functies.
"Als je op de knop drukt moet er CONFETTI komen! En MUZIEK! En VUURWERK!" """

    elif level == 4:
        level_prompt = f"""
NIVEAU: Formulieren en Gegevens (Opdracht #{assignment_number})
{history_context}

Nu wordt het serieus - we gaan INFORMATIE verzamelen van bezoekers.

MOEILIJKHEIDSGRAAD: Pittig
- Formulieren waar mensen dingen kunnen invullen
- Controleren of mensen wel alles goed invullen
- Gegevens opslaan of verwerken

VOORBEELDEN VAN GOEDE SCENARIOS:
- Een pizzeria die online bestellingen wil ontvangen
- Een huisarts die een intake-formulier nodig heeft
- Een escape room die boekingen wil bijhouden
- Een sportschool die aanmeldingen wil verwerken

De humor zit in de CHAOS van verkeerde invoer: "Mensen vullen hun telefoonnummer in bij email!"
Of klanten die VEEL TE VEEL velden willen: "En ook hun bloedgroep! En hun favoriete kleur!" """

    elif level >= 5:
        ai_type = {
            5: ("AI Tekst Generatie", "tekst laten schrijven door AI", "Een slager die elke dag een nieuwe slogan wil, een blogger die geen inspiratie heeft, een makelaar die huizenbeschrijvingen wil"),
            6: ("AI Chatbot", "een pratende assistent bouwen", "Een klantenservice die 24/7 beschikbaar moet zijn, een museum dat vragen wil beantwoorden, een webshop met een virtuele verkoper"),
            7: ("AI Tools", "slimme tools bouwen", "Een restaurant dat reviews wil analyseren, een vertaalbureau, een school die samenvattingen wil maken"),
            8: ("AI Applicatie", "een complete AI-app bouwen", "Een compleet dashboard, een leerplatform, een content management systeem")
        }.get(level, ("AI Applicatie", "iets geweldigs met AI", "Een ambitieus project"))
        
        level_prompt = f"""
NIVEAU: {ai_type[0]} (Opdracht #{assignment_number})
{history_context}

WOW - de gebruiker is gevorderd! Nu gaan we echte AI-magie toevoegen.

MOEILIJKHEIDSGRAAD: Gevorderd
- De website moet {ai_type[1]}
- Dit is INDRUKWEKKEND spul
- De AI doet echt werk voor de bezoeker

VOORBEELDEN: {ai_type[2]}

De humor zit in klanten die NIET SNAPPEN hoe krachtig AI is:
"Kan die robot ook mijn belastingaangifte doen?"
"Wordt de AI niet moe als er veel bezoekers zijn?"

SUCCESS CRITERIA MOETEN BEVATTEN: "fetch", "openai", "async" (dit zijn technische checks, niet voor de gebruiker)

Maak het scenario EPISCH - dit is het eindbaas-niveau!"""

    else:
        level_prompt = f"""
NIVEAU: {level_info['level']} - {level_info['name']} (Opdracht #{assignment_number})
{history_context}

Genereer een passende opdracht voor dit niveau.
Focus: {level_info['focus']}"""

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

# Oude routes redirecten
@app.route('/bouwen')
def bouwen():
    return redirect('/studio')

@app.route('/oefenruimte')
def oefenruimte():
    return redirect('/studio')

@app.route('/studio')
def studio():
    return render_template('studio.html')

@app.route('/oefeningen')
def oefeningen():
    return redirect('/studio')

# Premium routes - redirect to studio
@app.route('/premium')
def premium():
    return redirect('/studio')

@app.route('/premium/dashboard')
def premium_dashboard():
    return redirect('/studio')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/blueprints')
def blueprints():
    return render_template('blueprints.html')

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

@app.route('/api/check-key', methods=['GET'])
def check_key():
    """Check if API key is set in session"""
    has_key = 'openai_api_key' in session and session['openai_api_key']
    return jsonify({'has_key': bool(has_key)})

@app.route('/api/set-key', methods=['POST'])
def set_key():
    """Set OpenAI API key in session"""
    try:
        data = request.json
        api_key = data.get('api_key', '').strip()
        
        if not api_key:
            return jsonify({'success': False, 'error': 'Geen API key opgegeven'})
        
        # Accept both sk- and sk-proj- keys
        if not (api_key.startswith('sk-') or api_key.startswith('sk-proj-')):
            return jsonify({'success': False, 'error': 'Ongeldige key format (moet beginnen met sk-)'})
        
        # Test the key with a simple call
        test = call_openai(api_key, [{"role": "user", "content": "test"}], max_tokens=5)
        
        if test:
            session.permanent = True
            session['openai_api_key'] = api_key
            return jsonify({'success': True})
        else:
            # Even if test fails, save the key - user may have quota issues
            # But warn them
            session.permanent = True
            session['openai_api_key'] = api_key
            return jsonify({'success': True, 'warning': 'Key opgeslagen maar kon niet getest worden. Mogelijk geen credits.'})
    except Exception as e:
        print(f"Error in set_key: {e}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/api/get-key', methods=['GET'])
def get_key():
    """Get API key from session (for client-side use)"""
    api_key = session.get('openai_api_key', '')
    if api_key:
        # Return masked key for display
        masked = api_key[:7] + '...' + api_key[-4:]
        return jsonify({'has_key': True, 'masked_key': masked, 'key': api_key})
    return jsonify({'has_key': False})

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
    try:
        data = request.json
        api_key = data.get('api_key')
        level = data.get('level', 1)
        completed = data.get('completed', [])
        
        print(f"Generating assignment for level {level}")
        
        if not api_key:
            return jsonify({"success": False, "error": "API key vereist"})
        
        assignment = generate_assignment(api_key, level, completed)
        
        if assignment:
            print(f"Assignment generated: {assignment.get('title', 'Unknown')}")
            return jsonify({"success": True, "assignment": assignment})
        else:
            print("Failed to generate assignment")
            return jsonify({"success": False, "error": "Kon geen opdracht genereren. Controleer je API key en credits."})
    except Exception as e:
        print(f"Error in api_generate_assignment: {e}")
        return jsonify({"success": False, "error": f"Server error: {str(e)}"})

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
