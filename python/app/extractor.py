import fitz
from docx import Document
import re

def nettoyer_texte(text: str) -> str:
    lignes = text.split("\n")
    lignes_propres = []
    
    for ligne in lignes:
        ligne = ligne.strip()
        
        # Ignorer lignes vides
        if not ligne:
            continue
        
        # Ignorer numéros de page seuls
        if re.match(r'^[ivxlcdmIVXLCDM]+$', ligne):
            continue
        if re.match(r'^\d+$', ligne):
            continue
            
        # Ignorer lignes trop courtes
        if len(ligne) < 4:
            continue
            
        # Ignorer lignes avec que des points
        if re.match(r'^[.\s]+$', ligne):
            continue
            
        lignes_propres.append(ligne)
    
    return "\n".join(lignes_propres)

def extract_text(filepath: str) -> str:
    text = ""
    
    if filepath.endswith(".pdf"):
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text() + "\n"
    
    elif filepath.endswith(".docx"):
        doc = Document(filepath)
        for p in doc.paragraphs:
            if p.text.strip():
                text += p.text + "\n"
    
    # Nettoyer le texte
    text = nettoyer_texte(text)
    return text