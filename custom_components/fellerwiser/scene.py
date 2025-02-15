"""Platform for scenes integration."""
from __future__ import annotations
from homeassistant.components.scene import Scene

import logging
import requests

_LOGGER = logging.getLogger(__name__)


def list_scenes(host: str, apikey: str):
    """Retrieve all current Scenes from Feller Wiser Gateway."""
    return requests.get("http://" + host + "/api/jobs", headers={'authorization':'Bearer ' + apikey})


async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    apikey = entry.data["apikey"]

    _LOGGER.info("---------------------------------------------- %s %s", host, apikey)

    response = await hass.async_add_executor_job(list_scenes, host, apikey)

    sceneslist = response.json()

    scenes = []
    for value in sceneslist["data"]:
        scenes.append(FellerScene(value, host, apikey))

    async_add_entities(scenes, True)


class FellerScene(Scene):
    """Representation of an Awesome Scene."""

    def __init__(self, data: object, host: str, apikey: str) -> None:
        """Initialize an AwesomeScene.
        
        Unfortunately there's no scene name declared in the json response, if someone finds an elegant method please let us know.
        At present, the scene name is generated with the scene id (Example: Scene 145). You can then rename every single scene in Home Assistant.
        """

        self._data = data
        self._id = str(data["id"])
        self._name = "Scene " + self._id
        self._host = host
        self._apikey = apikey


    @property
    def name(self) -> str:
        """Return the display name of this scene."""
        return self._name


    @property
    def unique_id(self):
        return "scene-" + self._id


    def activate(self, **kwargs: Any) -> None:
        """Here is where the native scene is triggered."""
        _LOGGER.debug("Activated scene id %s", self._id)
        requests.get("http://" + self._host + "/api/jobs/" + self._id + "/trigger", headers={'authorization':'Bearer ' + self._apikey})
        return None
