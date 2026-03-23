from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3

app = FastAPI()

class NewUser(BaseModel):
    name: str
    email: EmailStr
    company: str

def get_db():
    return sqlite3.connect("database.db")

@app.post("/webhook/new-user")
def new_user(payload: NewUser):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT companyId FROM companies WHERE name = ?", (payload.company,))
        result = cursor.fetchone()

        if result:
            companyId = result[0]
        else:
            cursor.execute("INSERT INTO companies (name) VALUES (?)", (payload.company,))
            companyId = cursor.lastrowid

        cursor.execute("""
            INSERT INTO users (name, email, city, companyId)
            VALUES (?, ?, ?, ?)
        """, (payload.name, payload.email, None, companyId))

        db.commit()
        return {"status": "success", "message": "User inserted"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))