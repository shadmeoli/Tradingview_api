from datetime import datetime
from dataclasses import dataclass

# account creation timestamp
def created_at():
    current_time = datetime.utcnow() 
    return current_time.strftime('%d-%m-%Y')

# the generator class
@dataclass
class UserSignup:

    username: str
    email: str
    phone: int
    age: int
    password: str

# user sign in
@dataclass
class UserSignIn:

    username: str
    password: str

# getting market details 
@dataclass
class MarketDetails:
    """
    symbol="TSLA", 
    screener="america",
    exchange="NASDAQ"
    INTERVAL_1_DAY
    """
    symbol: str
    screener: str
    exchange: str

# in file manual testing
if __name__ == '__main__':
    person = UserSignup(
        "shadrack",
        "shadcodes@gmal.com",
        254742909056,
        25,
        "safe_password"
    )

    print(person)