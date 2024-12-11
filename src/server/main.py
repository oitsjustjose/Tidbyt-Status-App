"""
Architecture:

Python App that loops infinitely, pushing the correct Pixlet state to the TidByt
Changes come in via WebAPI so we can make a lightweight desktop client and leave the work to the RasPi
Also allows the TidByt to still have forgeserv.net data without needing to be stood up
"""

from state import AppState, StateManager
from fastapi import FastAPI

app = FastAPI()
state_mgr = StateManager(timeout=10)


@app.post("/")
def change_state(new_state: int):
    state_mgr.update(AppState(new_state))
    return {"msg": "👍"}
