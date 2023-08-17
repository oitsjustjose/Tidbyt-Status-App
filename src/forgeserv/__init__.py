"""The handler for ForgeServ status updates"""

import datetime
import json
import urllib.request
from dataclasses import dataclass
from time import sleep
from typing import List, Union

import pixlet
from util import Renderable, rel_to_abspath


@dataclass
class Player:
    """Represents a player on the server"""

    name: str
    head: str
    uuid: str


@dataclass
class Server:
    """Represents a single ForgeServ server"""

    max_players: int
    online_players: int
    server_dynmap_url: Union[None, str]
    server_health: str
    server_icon: str
    server_motd: str
    server_name: str
    server_type: str
    server_version: str
    players: List[Player]


def parse_servers(json_in: str) -> List[Server]:
    """Parses the raw response JSON from the API into a list of servers"""
    # https://cravatar.eu/head/fda160e2-e608-4233-b325-558d92a82a0e

    data = json.loads(json_in)

    servers: List[Server] = []

    for idx, serv in enumerate(data):
        try:
            servers.append(
                Server(
                    max_players=serv["max"],
                    online_players=serv["online"],
                    server_dynmap_url=serv["dynmap"],
                    server_health=serv["health"],
                    server_icon=serv["icon"],
                    server_motd=serv["motd"],
                    server_name=serv["name"],
                    server_type=serv["type"],
                    server_version=serv["version"],
                    players=[
                        Player(
                            name=x["name"],
                            uuid=x["uuid"],
                            head=f"https://cravatar.eu/head/{x['uuid']}",
                        )
                        for x in serv["players"]
                    ],
                )
            )
        except ValueError:
            print(f"Skipping server at index {idx}")

    return servers


class ForgeServRenderer(Renderable):
    def __init__(self) -> None:
        self.last_render = datetime.datetime.now()
        self.cached_servers: List[Server] = []
        self.render_file = rel_to_abspath("../templates/rendered.star")
        self.pixlet_out = self.render_file.replace(".star", ".webp")

    def render(self) -> None:
        servers: List[Server] = self.cached_servers

        if not servers or (datetime.datetime.now() - self.last_render).seconds >= 10:
            with urllib.request.urlopen("https://api.forgeserv.net") as response:
                servers = parse_servers(response.read().decode())

        top_server: Server = servers[0]
        for server in servers:
            if server.online_players > top_server.online_players:
                top_server = server

        pixlet.update_template(
            rel_to_abspath("../templates/forgeserv.star"),
            self.render_file,
            {
                "<IMAGE>": top_server.server_icon,
                "<SERVER-NAME>": top_server.server_name,
                "<ONLINE-PLAYERS>": top_server.online_players,
                "<MAX-PLAYERS>": top_server.max_players,
                "<PLAYER-LIST>": ", ".join([x.name for x in top_server.players]),
            },
        )
        pixlet.render(self.render_file)
        pixlet.display(self.pixlet_out, installation_id="status")
        sleep(20)
