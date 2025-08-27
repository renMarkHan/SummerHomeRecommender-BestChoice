# import database  # Removed to avoid circular import

# property.py
class Property:
    def __init__(self, property_id, location, ptype, nightly_price, features, tags, image_url=None, image_alt=None, latitude=None, longitude=None):
        self.property_id = property_id
        self.location = location
        self.ptype = ptype
        self.nightly_price = nightly_price
        self.features = features  # could be a list
        self.tags = tags          # could be a list
        self.image_url = image_url
        self.image_alt = image_alt
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<Property {self.ptype} in {self.location} @ ${self.nightly_price}/night>"

    # Example method: check if matches environment
    def matches_environment(self, preferred_env):
        return preferred_env.lower() in [t.lower() for t in self.tags]
    


# ==============================
# CRUD Operations for Property (CRUD refers to create, read, update and delete)
# ==============================
def create_property(location, ptype, nightly_price, features, tags, image_url=None, image_alt=None):
    import sqlite3
    conn = sqlite3.connect("vacation_rentals.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (location, type, nightly_price, features, tags, image_url, image_alt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (location, ptype, nightly_price, features, tags, image_url, image_alt))
    conn.commit()
    conn.close()

def get_property(property_id):
    import sqlite3
    conn = sqlite3.connect("vacation_rentals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties WHERE property_id = ?", (property_id,))
    prop = cursor.fetchone()
    conn.close()
    return prop

def update_property(property_id, **kwargs):
    import sqlite3
    conn = sqlite3.connect("vacation_rentals.db")
    cursor = conn.cursor()
    fields = ", ".join(f"{key} = ?" for key in kwargs.keys())
    values = list(kwargs.values()) + [property_id]
    cursor.execute(f"UPDATE properties SET {fields} WHERE property_id = ?", values)
    conn.commit()
    conn.close()

def delete_property(property_id):
    import sqlite3
    conn = sqlite3.connect("vacation_rentals.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE property_id = ?", (property_id,))
    conn.commit()
    conn.close()

