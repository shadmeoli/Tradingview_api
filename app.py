from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tradingview_ta import TA_Handler, Interval, Exchange
import uvicorn

from App.auth import UserSignIn, UserSignup, created_at, MarketDetails
from App.Model import User

app = FastAPI(
    title="Indi Markets",
    contact={
        "name": "Market analysis made easier",
        "email": "shadcodes@gmail.com",
    }
)
# app.mount("/static", StaticFiles(directory="static"), name="static")


# ----------- User login -------------
@app.post("/sign_up")
def user_action(details: UserSignup):
    new_user = User()

    user_details = {}

    user_details["username"] = details.username
    user_details["email"] = details.email
    user_details["phone"] = details.phone
    user_details["age"] = details.age
    user_details["password"] = details.password

    register = new_user.signup(user_details)
    # return register

    if register:
        print(new_user.signup(user_details))
        return {
            "username": details.username,
            "timestamp": created_at(),
            "created" : register
        }

    else:
        return {
            "Error" : "Not created",
            "status" : register
        }
# ------------------------------------


# -------- User Login ---------------
@app.get("/login")
def user_action():
    return {"Hello": "World"}


@app.post("/login")
def user_action(details: UserSignIn):

    old_user = User()

    user_details = {}

    user_details["username"] = details.username
    user_details["password"] = details.password

    log_user = old_user.login(user_details)

    return {
        "coming_back_user": user_details["username"],
        "logged_in_at": created_at(),
        "status" : log_user
    }
# -----------------------------------

# ----------- Market ----------------


@app.post("/markets/")
def market_action(details: MarketDetails):

    product = TA_Handler(symbol=details.symbol, screener=details.screener,
                         exchange=details.exchange, interval=Interval.INTERVAL_1_HOUR)

    _analysis = product.get_analysis().summary

    return {
        "MarketAnalysis": _analysis,
        "Action": _analysis["RECOMMENDATION"]
    }
# -----------------------------------


# RUNNER
if __name__ == '__main__':
    uvicorn
