"""
Architecture:

Python App that loops infinitely, pushing the correct Pixlet state to the TidByt
Changes come in via WebAPI so we can make a lightweight desktop client and leave the work to the RasPi
Also allows the TidByt to still have forgeserv.net data without needing to be stood up
"""

import logging

from fastapi import FastAPI, Response

from server.state import AppState, StateManager

app: FastAPI = FastAPI()
logger = logging.getLogger("uvicorn.error")
state_mgr: StateManager = StateManager(timeout=10)
state_mgr.start()


@app.post("/")
def change_state(new_state: int):
    try:
        state_mgr.update(AppState(new_state))
    except Exception as e:
        logger.warning(f"/change_state ran into an {type(e).__name__}: {str(e)}")
    return Response(status_code=200)
