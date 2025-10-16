from __future__ import annotations

import os
from typing import List, Optional
from uuid import UUID

import mysql.connector
from fastapi import FastAPI, HTTPException, Query

from models.address import AddressCreate, AddressRead, AddressUpdate, AddressDelete

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Database helper
# -----------------------------------------------------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "main-db"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "admin"),
        password=os.getenv("MYSQL_PASSWORD", "admin123"),
        database=os.getenv("MYSQL_DATABASE", "main_db"),
    )

# -----------------------------------------------------------------------------
# FastAPI app
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Address API",
    description="Demo FastAPI app using MySQL for Address storage",
    version="0.2.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------
@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Insert address into MySQL
        cursor.execute(
            """
            INSERT INTO addresses (id, name, street, unit, city, state, postal_code, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(address.id),
                address.name,
                address.street,
                address.unit,
                address.city,
                address.state,
                address.postal_code,
                address.country,
            ),
        )
        conn.commit()
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return AddressRead(**address.model_dump())

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    name: Optional[str] = Query(None),
    street: Optional[str] = Query(None),
    unit: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    postal_code: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM addresses WHERE 1=1"
    params = []

    if name:
        query += " AND name=%s"
        params.append(name)
    if street:
        query += " AND street=%s"
        params.append(street)
    if unit:
        query += " AND unit=%s"
        params.append(unit)
    if city:
        query += " AND city=%s"
        params.append(city)
    if state:
        query += " AND state=%s"
        params.append(state)
    if postal_code:
        query += " AND postal_code=%s"
        params.append(postal_code)
    if country:
        query += " AND country=%s"
        params.append(country)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return [AddressRead(**r) for r in results]

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM addresses WHERE id=%s", (str(address_id),))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Address not found")
    return AddressRead(**result)

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM addresses WHERE id=%s", (str(address_id),))
    stored = cursor.fetchone()
    if not stored:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Address not found")

    # Update fields
    updated_data = {**stored, **update.model_dump(exclude_unset=True)}
    cursor.execute(
        """
        UPDATE addresses
        SET name=%s, street=%s, unit=%s, city=%s, state=%s, postal_code=%s, country=%s
        WHERE id=%s
        """,
        (
            updated_data["name"],
            updated_data["street"],
            updated_data["unit"],
            updated_data["city"],
            updated_data["state"],
            updated_data["postal_code"],
            updated_data["country"],
            str(address_id),
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return AddressRead(**updated_data)

@app.delete("/addresses/{address_id}", response_model=AddressDelete)
def delete_address(address_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM addresses WHERE id=%s", (str(address_id),))
    stored = cursor.fetchone()
    if not stored:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Address not found")

    cursor.execute("DELETE FROM addresses WHERE id=%s", (str(address_id),))
    conn.commit()
    cursor.close()
    conn.close()
    return AddressDelete(**stored)

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)