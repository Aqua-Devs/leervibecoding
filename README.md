# 🚀 LeerVibeCoding.nl

Leer programmeren met AI - een interactief platform voor beginners om vibecoding te leren.

## 🆕 Nieuw: Premium Features

- **Light/Dark Mode** - Website start in light mode, toggle naar dark
- **Premium Blueprints** - 50+ kant-en-klare templates
- **Oefenruimte** - Nu exclusief voor Premium leden
- **Pro Workflows** - Geavanceerde multi-step workflows
- **BYOK** - Bring Your Own Key (eigen OpenAI API key)

### Premium Toegangscodes (voor testing)
- `PREMIUM2024`
- `VIBE2024`
- `MASTERMIND`
- `LEERVIBE`

## 📦 Lokaal draaien

```bash
# Installeer dependencies
pip install -r requirements.txt

# Start de server
python app.py

# Open http://localhost:5000
```

## 🌐 Deployen naar Render via GitHub

### Stap 1: Push naar GitHub

```bash
git init
git add .
git commit -m "Initial commit - LeerVibeCoding"
git branch -M main
git remote add origin https://github.com/JOUW-USERNAME/leervibecoding.git
git push -u origin main
```

### Stap 2: Verbind met Render

1. Ga naar [render.com](https://render.com) en maak een account
2. Klik op **"New +"** → **"Web Service"**
3. Verbind je GitHub en selecteer `leervibecoding`
4. Render detecteert automatisch de instellingen
5. Klik op **"Create Web Service"**

## 🔍 SEO Features

- ✅ Meta tags per pagina
- ✅ Open Graph & Twitter Cards
- ✅ Structured Data (JSON-LD)
- ✅ Sitemap.xml & Robots.txt
- ✅ Canonical URLs

## 📁 Project structuur

```
leervibecoding/
├── app.py                    # Flask applicatie
├── requirements.txt          # Python dependencies
├── render.yaml               # Render configuratie
├── static/
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── logo.svg
│   └── og-image.svg
└── templates/
    ├── base.html             # Base template (light/dark mode)
    ├── index.html            # Landing page
    ├── premium.html          # Premium promotie pagina
    ├── premium_dashboard.html # Premium dashboard
    ├── studio.html           # Oefenruimte (premium)
    ├── tools.html
    ├── workflow.html
    ├── ehbo.html
    ├── inspiratie.html
    └── live-gaan.html
```

## 💰 Monetisatie Model

1. **Gratis** - Basis content (tools, workflow, ehbo, inspiratie)
2. **Premium (€19-29/maand)** - Blueprints, Oefenruimte, Pro Workflows
3. **BYOK** - Gebruikers betalen eigen OpenAI kosten

## ⚙️ Technologieën

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **AI:** OpenAI API (BYOK model)
- **Hosting:** Render

## 📝 Licentie

MIT License
