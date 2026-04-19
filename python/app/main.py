from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from extractor import extract_text
from generator import create_pptx
from ai_structurer import structure_content
import shutil, uuid, os, traceback
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/storage", StaticFiles(directory="../../storage"), name="storage")

UPLOAD_DIR = "../../storage/uploads/"
OUTPUT_DIR = "../../storage/output/"

@app.get("/health")
async def health():
    try:
        from ai_structurer import client
        ai_active = client is not None
    except:
        ai_active = False
    return {
        "status": "ok",
        "ai_active": ai_active
    }

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    try:
        print(f"\n📥 Fichier reçu : {file.filename}")

        # 1. Sauvegarder le fichier
        filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = os.path.join(UPLOAD_DIR, filename)

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print(f"💾 Fichier sauvegardé : {input_path}")

        # 2. Extraire le texte
        print("📖 Extraction du texte...")
        text = extract_text(input_path)

        if not text.strip():
            return {"error": "Impossible d'extraire le texte du fichier"}

        print(f"✅ Texte extrait : {len(text)} caractères")

        # 3. Analyser avec Groq IA
        slides_data = None
        try:
            print("🤖 Analyse IA en cours...")
            slides_data = structure_content(text)
            print(f"✅ {len(slides_data)} slides générées par l'IA")
        except Exception as e:
            print(f"⚠️ Erreur IA :")
            print(traceback.format_exc())
            slides_data = None

        # 4. Générer le PowerPoint
        print("🎨 Génération du PowerPoint...")
        output_filename = filename.rsplit(".", 1)[0] + ".pptx"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        create_pptx(text, output_path, slides_data)
        print(f"✅ PowerPoint créé : {output_path}")

        # 5. Vérifier que le fichier existe
        if not os.path.exists(output_path):
            return {"error": "Fichier PowerPoint non trouvé"}

        print("🎉 Conversion terminée !\n")

        return {
            "success": True,
            "output": output_path,
            "output_filename": output_filename,
            "slides_count": len(slides_data) if slides_data else 0,
            "text_length": len(text)
        }

    except Exception as e:
        print(f"❌ Erreur générale :")
        print(traceback.format_exc())
        return {"error": str(e)}