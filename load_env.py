from dotenv import load_dotenv
import os

def load_env():
    """Chargement et validation des variables d'environnement"""

    # Charger le fichier .env s'il existe
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ Fichier .env chargé")
    else:
        print("⚠️ Fichier .env non trouvé")

    # Liste des variables obligatoires
    required_vars = [
        "API_ID",
        "API_HASH",
        "TELEGRAM_BOT_TOKEN",
        "DATABASE_URL",
        "ADMIN_ID"
    ]

    # Vérification de leur présence
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"❌ Variables d'environnement manquantes : {', '.join(missing)}")
        exit(1)
    else:
        print("✅ Toutes les variables critiques sont présentes")
