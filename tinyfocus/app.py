#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: app.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from contextlib import asynccontextmanager

from typing import Annotated, AsyncIterator

from fastapi import FastAPI, Path

from tinyfocus.arduino_connection import FocusArduinoConnection


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI app."""

    yield  # Do nothing for now.


app = FastAPI(swagger_ui_parameters={"tagsSorter": "alpha"}, lifespan=lifespan)
focus_arduino = FocusArduinoConnection()


@app.get("/", description="Ping the server to check if it's running.")
def ping():
    """Ping the server to check if it's running."""

    return "Tiny Focus Server is running!"


@app.get("/status", description="Get the current status of the focus motor.")
async def status():
    """Get the current status of the focus motor."""

    return await focus_arduino.status()


@app.get(
    "/move/{steps}",
    description="Move the focus motor by a specified number of steps.",
)
async def move(
    steps: Annotated[
        int,
        Path(description="Number of steps to move the focus motor."),
    ],
):
    """Move the focus motor by a specified number of steps."""

    return await focus_arduino.move_steps(steps)


@app.get("/abort", description="Abort the current movement of the focus motor.")
async def abort():
    """Abort the current movement of the focus motor."""

    return await focus_arduino.abort()
