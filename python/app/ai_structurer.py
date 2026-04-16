import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv("../../.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyser_document(text: str) -> dict:
    prompt = f"""
Tu es un expert académique francophone.
Analyse ce document en profondeur et extrait toutes les informations importantes.
Ignore les numéros de pages, headers, footers.

TEXTE :
{text[:6000]}

Réponds en JSON strict :
{{
    "titre_document": "titre exact du document",
    "auteur": "nom auteur ou null",
    "institution": "université ou école ou null",
    "annee": "année ou null",
    "domaine": "domaine académique",
    "resume_global": "résumé complet en 5 phrases",
    "sections_principales": [
        {{
            "nom": "nom exact de la section",
            "contenu_resume": "résumé du contenu en 3 phrases complètes",
            "points_importants": ["point 1", "point 2", "point 3"]
        }}
    ],
    "problematique": "question centrale complète",
    "objectifs": ["objectif 1", "objectif 2", "objectif 3"],
    "methodologie": "description complète de la méthode",
    "resultats_cles": "résultats principaux détaillés",
    "conclusion_principale": "conclusion complète"
}}

Réponds UNIQUEMENT avec le JSON.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=3000
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])


def generer_slides(analyse: dict) -> list:
    sections = analyse.get("sections_principales", [])
    
    prompt = f"""
Tu es un expert PowerPoint académique francophone.
Crée une présentation complète et professionnelle.

ANALYSE DU DOCUMENT :
- Titre : {analyse.get('titre_document')}
- Auteur : {analyse.get('auteur')}
- Institution : {analyse.get('institution')}
- Année : {analyse.get('annee')}
- Domaine : {analyse.get('domaine')}
- Résumé : {analyse.get('resume_global')}
- Problématique : {analyse.get('problematique')}
- Objectifs : {analyse.get('objectifs')}
- Méthodologie : {analyse.get('methodologie')}
- Résultats : {analyse.get('resultats_cles')}
- Conclusion : {analyse.get('conclusion_principale')}
- Sections : {json.dumps(sections, ensure_ascii=False)}

STRUCTURE OBLIGATOIRE :
1. Slide titre — titre + auteur + institution + année
2. Slide sommaire — liste toutes les grandes parties
3. Slide introduction — contexte et problématique
4. Slide objectifs — liste des objectifs
5. Slides sections — UNE slide par section principale avec vrai contenu
6. Slide méthodologie — approche utilisée
7. Slide résultats — résultats clés
8. Slide discussion — analyse des résultats
9. Slide conclusion — synthèse et perspectives
10. Slide remerciements — slide finale

RÈGLES STRICTES :
- Titres courts max 5 mots
- Contenu : phrase d'intro complète
- Points : phrases complètes et informatives
- AUCUN numéro de page
- Contenu basé sur le VRAI document

Génère en JSON :
[
    {{
        "titre": "Titre court",
        "contenu": "Phrase d'introduction complète de la slide",
        "points": ["Point complet 1", "Point complet 2", "Point complet 3"],
        "type": "titre"
    }}
]

Types possibles : titre, sommaire, contenu, methodologie, resultats, discussion, conclusion, remerciements

Réponds UNIQUEMENT avec le JSON.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=4000
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    start = raw.find("[")
    end = raw.rfind("]") + 1
    return json.loads(raw[start:end])


def structure_content(text: str) -> list:
    print("🔍 Étape 1 : Analyse du document...")
    analyse = analyser_document(text)
    print(f"✅ Document : {analyse.get('titre_document')}")
    print(f"👤 Auteur : {analyse.get('auteur')}")
    print(f"🏫 Institution : {analyse.get('institution')}")
    print(f"📝 Sections : {len(analyse.get('sections_principales', []))}")

    print("🎨 Étape 2 : Génération des slides...")
    slides = generer_slides(analyse)
    print(f"✅ {len(slides)} slides générées !")
    return slides