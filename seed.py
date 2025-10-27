from app.database import Base, SessionLocal, engine
from app.models import User
from auth import hash_password

# Create all tables
Base.metadata.create_all(bind=engine)

# Seeder admin
def seed_admin():
    db = SessionLocal()
    username = "admin"
    password = "admin123"
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        print("Admin user is exist")
        return

    admin_user = User(
        username=username,
        hashed_password=hash_password(password),
        is_admin=True
    )
    db.add(admin_user)
    db.commit()
    print(f"Admin user created -> username: {username}, password: {password}")
    db.close()


if __name__ == "__main__":
    seed_admin()
