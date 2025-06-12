#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: arduino_connection.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import aiohttp

from .app import logger


IP_ADDRESS = "72.233.250.86"
PORT = "80"


class FocusArduinoConnection:
    """A connection to the focuser arduino. It connects and calls the real arduino."""

    def __init__(self):
        self.address = f"http://{IP_ADDRESS}:{PORT}"

    async def __postRequestToResponse(self, endpoint):
        """Sends a POST request to the Arduino and return the response.

        :param endpoint: The endpoint to send the request to.
                         Include any query parameters in the URL.
        :return: The JSON response from the Arduino,
                 or {"error": message, "code": code} if the request fails.

        """

        logger.debug(f"Requesting {self.address}/{endpoint}")

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.address}/{endpoint}") as resp:
                if resp.status != 200:
                    message = await resp.text()
                    logger.error(
                        f"Error: HTTP Request failed with code "
                        f"{resp.status} - {message}"
                    )
                    return {"error": "HTTP Request failed", "code": resp.status}
                try:
                    logger.debug(f"Response: {await resp.text()}")
                    return await resp.json(content_type=None)
                except Exception as e:
                    logger.error(f"Error: Failed to parse JSON response - {e}")
                    return {
                        "error": "Failed to parse JSON response",
                        "code": resp.status,
                    }

    async def __getRequestToResponse(self, endpoint):
        """Sends a GET request to the Arduino and return the response.

        :param endpoint: The endpoint to send the request to.
                         Include any query parameters in the URL.
        :return: The JSON response from the Arduino,
                 or {"error": message, "code": code} if the request fails.
        """

        logger.debug(f"Requesting {self.address}/{endpoint}")

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.address}/{endpoint}") as resp:
                if resp.status != 200:
                    message = await resp.text()
                    logger.error(
                        f"Error: HTTP Request failed with code "
                        f"{resp.status} - {message}"
                    )
                    return {"error": "HTTP Request failed", "code": resp.status}
                try:
                    logger.debug(f"Response: {await resp.text()}")
                    return await resp.json(content_type=None)
                except Exception as e:
                    logger.error(f"Error: Failed to parse JSON response - {e}")
                    return {
                        "error": "Failed to parse JSON response",
                        "code": resp.status,
                    }

    async def status(self):
        return await self.__getRequestToResponse("status")

    async def move_steps(self, num_steps: int):
        return await self.__postRequestToResponse(f"move?steps={num_steps}")

    async def abort(self):
        return await self.__postRequestToResponse("abort")

    async def move_absolute(self, voltage):
        return await self.__postRequestToResponse(f"set?voltage={voltage}")

    async def move_relative(self, voltage):
        return await self.__postRequestToResponse(f"move?voltage={voltage}")

    async def home(self):
        return await self.__postRequestToResponse("home")
