# progweb_back/seed_db.py
from database import get_db, Base, engine
from sqlalchemy.orm import Session
from security import get_password_hash

# Importe seus modelos
from roles.role_model import Role
from user.user_model import User

def seed_database():
    """
    Popula o banco de dados com os dados iniciais (roles e admin).
    """
    
    # Garante que todas as tabelas foram criadas
    Base.metadata.create_all(bind=engine)
    
    # Pega uma sessão do banco
    db: Session = next(get_db())

    try:
        print("Iniciando o processo de semeadura...")

        # --- 1. Criar Roles (Perfis) ---
        admin_role = db.query(Role).filter(Role.name == 'admin').first()
        if not admin_role:
            admin_role = Role(id=1, name='admin')
            db.add(admin_role)
            print("Role 'admin' criada.")
        
        user_role = db.query(Role).filter(Role.name == 'user').first()
        if not user_role:
            user_role = Role(id=2, name='user')
            db.add(user_role)
            print("Role 'user' criada.")
        
        # Commita as roles primeiro para que possamos usar os IDs
        db.commit()

        # --- 2. Criar Usuário Admin ---
        admin_user = db.query(User).filter(User.email == 'admin@example.com').first()
        if not admin_user:
            # A senha "4dm1n123" só existe aqui, neste script temporário.
            # Ela é hasheada antes de tocar o banco de dados.
            admin_password = "4dm1n123"
            hashed_admin_password = get_password_hash(admin_password)

            admin_user = User(
                email='admin@example.com',
                hashed_password=hashed_admin_password,
                full_name='Administrador do Sistema',
                role_id=admin_role.id  # Associa com a role 'admin'
            )
            db.add(admin_user)
            print("Usuário 'admin@example.com' criado com sucesso.")
        
        # Commita o usuário
        db.commit()
        
        print("\nSemeadura do banco de dados concluída!")

    except Exception as e:
        print(f"Erro durante a semeadura: {e}")
        db.rollback() # Desfaz qualquer mudança se um erro ocorrer
    finally:
        db.close() # Fecha a sessão

if __name__ == "__main__":
    seed_database()