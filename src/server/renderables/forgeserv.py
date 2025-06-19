import json
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from server.renderables import Renderable


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
    server_health: str
    server_icon: str
    server_motd: str
    server_name: str
    server_type: str
    server_version: str
    players: List[Player]


class ForgeServ(Renderable):
    def __init__(self):
        self.file_path = Path("./templates/forgeserv.star").resolve()
        self.is_dynamic = True
        self.template_keys = [
            "<IMAGE>",
            "<SERVER-NAME>",
            "<ONLINE-PLAYERS>",
            "<MAX-PLAYERS>",
        ]
        self.__server_key = 0

    def __parse_servers(self, json_in: str) -> List[Server]:
        """Parses the raw response JSON from the API into a list of servers

        Args:
            json_in (str): The raw JSON string from the API request

        Returns:
            List[Server]: A list of parsed server objects
        """

        data = json.loads(json_in)
        servers: List[Server] = []

        for idx, serv in enumerate(data):
            try:
                servers.append(
                    Server(
                        max_players=serv["max"],
                        online_players=serv["online"],
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

    def resolve_template_keys(self):
        with urllib.request.urlopen("https://api.forgeserv.net") as response:
            servers: List[Server] = self.__parse_servers(response.read().decode())

        if (self.__server_key + 1) > len(servers) - 1:
            self.__server_key = 0
        else:
            self.__server_key += 1

        server = servers[self.__server_key]

        return {
            "<IMAGE>": server.server_icon,
            "<SERVER-NAME>": server.server_name,
            "<ONLINE-PLAYERS>": server.online_players,
            "<MAX-PLAYERS>": server.max_players,
        }
