"""
Script para testar a conexão com o banco de dados
e verificar qual ambiente está configurado.
"""
import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

print("=" * 60)
print("🔧 CONFIGURAÇÃO DO BANCO DE DADOS")
print("=" * 60)
print(f"\n📍 Ambiente: {ENVIRONMENT}")

if ENVIRONMENT == "production":
    DATABASE_URL = "postgresql://progweb:gGFVRNTkOsLoniiz7EA3ugeScHfNeXx2@dpg-d4p0shmr433s73ebvlbg-a.ohio-postgres.render.com/progweb_bd"
    print("🌐 Modo: PRODUÇÃO (Render)")
    print(f"🔗 Host: dpg-d4p0shmr433s73ebvlbg-a.ohio-postgres.render.com")
    print(f"📦 Database: progweb_bd")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    print("💻 Modo: DESENVOLVIMENTO (Local)")
    if DATABASE_URL:
        # Extrai informações da URL (sem mostrar a senha completa)
        if "@" in DATABASE_URL:
            parts = DATABASE_URL.split("@")
            host_db = parts[1] if len(parts) > 1 else "N/A"
            print(f"🔗 Conexão: ...@{host_db}")
        else:
            print(f"🔗 URL: {DATABASE_URL}")
    else:
        print("❌ DATABASE_URL não configurada no .env!")

print("\n" + "=" * 60)
print("💡 Para mudar o ambiente, edite ENVIRONMENT no arquivo .env")
print("   - development: usa banco local")
print("   - production: usa banco do Render")
print("=" * 60)
