# 🚀 LeerVibeCoding.nl

Leer programmeren met AI - een interactief platform voor beginners om vibecoding te leren.

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
# Maak een nieuwe repository op GitHub.com
# Ga dan naar je project folder en run:

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
3. Klik op **"Connect a repository"** en verbind je GitHub
4. Selecteer je `leervibecoding` repository
5. Render detecteert automatisch de instellingen:
   - **Name:** leervibecoding
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Klik op **"Create Web Service"**

### Stap 3: Wacht op deployment

Render bouwt en deploy je app automatisch. Na een paar minuten krijg je een URL zoals:
`https://leervibecoding.onrender.com`

## 🔍 SEO Features

Deze website is volledig geoptimaliseerd voor zoekmachines:

- ✅ **Meta tags** - Title, description, keywords per pagina
- ✅ **Open Graph** - Facebook/LinkedIn preview afbeeldingen
- ✅ **Twitter Cards** - Twitter preview ondersteuning
- ✅ **Structured Data** - JSON-LD schema voor Course, FAQ, Organization
- ✅ **Sitemap.xml** - Automatische sitemap voor crawlers
- ✅ **Robots.txt** - Crawler instructies
- ✅ **Canonical URLs** - Voorkom duplicate content
- ✅ **Semantic HTML** - Correcte heading hiërarchie
- ✅ **Preconnect** - Snellere font loading

### Na deployment: Google Search Console

1. Ga naar [Google Search Console](https://search.google.com/search-console)
2. Voeg je domein toe
3. Verifieer eigendom via DNS of HTML tag
4. Submit je sitemap: `https://jouw-domein.nl/sitemap.xml`

## 📁 Project structuur

```
leervibecoding/
├── app.py              # Flask applicatie
├── requirements.txt    # Python dependencies
├── render.yaml         # Render configuratie
├── .gitignore          # Git ignore file
├── static/             # Static bestanden
│   ├── robots.txt      # Crawler instructies
│   ├── sitemap.xml     # Sitemap voor SEO
│   ├── logo.svg        # Logo bestand
│   └── og-image.svg    # Social media preview
└── templates/          # HTML templates
    ├── base.html       # Base template met SEO
    ├── index.html      # Landing page
    ├── studio.html     # Oefenruimte
    ├── tools.html      # Gereedschapskist
    ├── workflow.html   # Leren pagina
    ├── ehbo.html       # EHBO pagina
    ├── inspiratie.html # Showcase
    └── live-gaan.html  # Deployment guide
```

## ⚙️ Technologieën

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **AI:** OpenAI API
- **Hosting:** Render
- **SEO:** Schema.org, Open Graph, Twitter Cards

## 📝 Licentie

MIT License - Vrij te gebruiken en aan te passen.
