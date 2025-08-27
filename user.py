from database import get_connection, get_all_properties
from property import Property

class User:
    def __init__(self, user_id, name, group_size, preferred_env, budget_min, budget_max, travel_start_date=None, travel_end_date=None, weighed_location=1, weighed_type=1, weighed_features=1, weighed_price=1):
        self.user_id = user_id
        self.name = name
        self.group_size = group_size
        self.preferred_env = preferred_env
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.travel_start_date = travel_start_date
        self.travel_end_date = travel_end_date
        
        # Initialize weighted attributes with default values
        self.weighed_location = weighed_location
        self.weighed_type = weighed_type
        self.weighed_features = weighed_features
        self.weighed_price = weighed_price

    def __repr__(self):
        return f"<User {self.name}, Group size: {self.group_size}, Pref: {self.preferred_env}>"

    def can_afford(self, nightly_price):
        """Check if a price is within user's budget."""
        return self.budget_min <= nightly_price <= self.budget_max

    def match_properties(self):
        """Return a list of Property objects matching the user's budget and preferred environment."""
        all_props = get_all_properties()
    
        matched = [
            prop for prop in all_props
            if self.can_afford(prop.nightly_price) 
            and prop.matches_environment(self.preferred_env)
        ]
    
        return matched

    # ==============================
    # Weighted Attributes Getter and Setter Methods
    # ==============================

    def get_weighed_location(self):
        """Get the weighted location preference value."""
        return self.weighed_location

    def set_weighed_location(self, value):
        """Set the weighted location preference value (1-10)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Weighed location must be a number")
        if value < 1 or value > 10:
            raise ValueError("Weighed location must be between 1 and 10")
        self.weighed_location = int(value)

    def get_weighed_type(self):
        """Get the weighted property type preference value."""
        return self.weighed_type

    def set_weighed_type(self, value):
        """Set the weighted property type preference value (1-10)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Weighed type must be a number")
        if value < 1 or value > 10:
            raise ValueError("Weighed type must be between 1 and 10")
        self.weighed_type = int(value)

    def get_weighed_features(self):
        """Get the weighted features preference value."""
        return self.weighed_features

    def set_weighed_features(self, value):
        """Set the weighted features preference value (1-10)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Weighed features must be a number")
        if value < 1 or value > 10:
            raise ValueError("Weighed features must be between 1 and 10")
        self.weighed_features = int(value)

    def get_weighed_price(self):
        """Get the weighted price preference value."""
        return self.weighed_price

    def set_weighed_price(self, value):
        """Set the weighted price preference value (1-10)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Weighed price must be a number")
        if value < 1 or value > 10:
            raise ValueError("Weighed price must be between 1 and 10")
        self.weighed_price = int(value)

    def get_all_weights(self):
        """Get all weighted preference values as a dictionary."""
        return {
            'weighed_location': self.weighed_location,
            'weighed_type': self.weighed_type,
            'weighed_features': self.weighed_features,
            'weighed_price': self.weighed_price
        }

    def set_all_weights(self, location=None, type_val=None, features=None, price=None):
        """Set multiple weighted preference values at once."""
        if location is not None:
            self.set_weighed_location(location)
        if type_val is not None:
            self.set_weighed_features(features)
        if price is not None:
            self.set_weighed_price(price)

    def set_budget_min(self, value):
        """Set the minimum budget value."""
        if not isinstance(value, (int, float)):
            raise ValueError("Budget must be a number")
        if value < 0:
            raise ValueError("Budget cannot be negative")
        self.budget_min = float(value)

    def set_budget_max(self, value):
        """Set the maximum budget value."""
        if not isinstance(value, (int, float)):
            raise ValueError("Budget must be a number")
        if value < 0:
            raise ValueError("Budget cannot be negative")
        if self.budget_min is not None and value < self.budget_min:
            raise ValueError("Maximum budget cannot be less than minimum budget")
        self.budget_max = float(value)

    def save_weights_to_db(self):
        """Save current weight values to database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET weighed_location=?, weighed_type=?, weighed_features=?, weighed_price=?
            WHERE user_id=?
        ''', (self.weighed_location, self.weighed_type, self.weighed_features, self.weighed_price, self.user_id))
        conn.commit()
        conn.close()

    def save_budget_to_db(self):
        """Save current budget values to database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET budget_min=?, budget_max=?
            WHERE user_id=?
        ''', (self.budget_min, self.budget_max, self.user_id))
        conn.commit()
        conn.close()

# ==============================
# CRUD Operations for Users (CRUD refers to create, read, update and delete)
# ==============================

def create_user(name, weighed_location=1, weighed_type=1, weighed_features=1, weighed_price=1, group_size=None, preferred_env=None, budget_min=None, budget_max=None, travel_start_date=None, travel_end_date=None):
    """Create a new user with weighted preferences."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, group_size, preferred_env, budget_min, budget_max, travel_start_date, travel_end_date, weighed_location, weighed_type, weighed_features, weighed_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, group_size, preferred_env, budget_min, budget_max, travel_start_date, travel_end_date, weighed_location, weighed_type, weighed_features, weighed_price))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user(user_id):
    """Get a user by ID with all weighted attributes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(
            user_id=row[0],
            name=row[1],
            group_size=row[2],
            preferred_env=row[3],
            budget_min=row[4],
            budget_max=row[5],
            travel_start_date=row[6],
            travel_end_date=row[7],
            weighed_location=row[8] if len(row) > 8 else 1,
            weighed_type=row[9] if len(row) > 9 else 1,
            weighed_features=row[10] if len(row) > 10 else 1,
            weighed_price=row[11] if len(row) > 11 else 1
        )
    return None

def update_user_weights(user_id, weighed_location=None, weighed_type=None, weighed_features=None, weighed_price=None):
    """Update user's weighted preferences."""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    values = []
    
    if weighed_location is not None:
        updates.append("weighed_location = ?")
        values.append(weighed_location)
    if weighed_type is not None:
        updates.append("weighed_type = ?")
        values.append(weighed_type)
    if weighed_features is not None:
        updates.append("weighed_features = ?")
        values.append(weighed_features)
    if weighed_price is not None:
        updates.append("weighed_price = ?")
        values.append(weighed_price)
    
    if updates:
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    conn.close()

def get_all_users():
    """Get all users with their weighted attributes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    users = []
    for row in rows:
        user = User(
            user_id=row[0],
            name=row[1],
            group_size=row[2],
            preferred_env=row[3],
            budget_min=row[4],
            budget_max=row[5],
            travel_start_date=row[6],
            travel_end_date=row[7],
            weighed_location=row[8] if len(row) > 8 else 1,
            weighed_type=row[9] if len(row) > 9 else 1,
            weighed_features=row[10] if len(row) > 10 else 1,
            weighed_price=row[11] if len(row) > 11 else 1
        )
        users.append(user)
    
    return users


