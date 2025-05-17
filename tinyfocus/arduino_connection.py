import logging
import aiohttp

class focus_arduino:
    """
    A connection to the focuser arduino. It connects and calls the real arduino.
    """

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    IP_ADDRESS = "72.233.250.86"
    PORT = "80"

    address = f"http://{IP_ADDRESS}:{PORT}"

    @classmethod
    async def __postRequestToResponse(cls, endpoint):
        """
        Sends a GET request to the Arduino and return the response.
        
        :param endpoint: The endpoint to send the request to. Include any query parameters in the URL.
        :return: The JSON response from the Arduino, or {"error": message} if the request fails.
        """
        logging.debug(f"Requesting {cls.address}/{endpoint}")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{cls.address}/{endpoint}") as resp:
                if resp.status != 200:
                    logging.error(f"Error: HTTP Request failed with code {resp.status} - {await resp.text()}")
                    return {"error": "HTTP Request failed"}
                try:
                    logging.debug(f"Response: {await resp.text()}")
                    return await resp.json(content_type=None)
                except Exception as e:
                    logging.error(f"Error: Failed to parse JSON response - {e}")
                    return {"error": "Failed to parse JSON response"}
        return {"error": "Unexpected failure"}

    @classmethod
    async def __getRequestToResponse(cls, endpoint):
        """
        Sends a GET request to the Arduino and return the response.
        
        :param endpoint: The endpoint to send the request to. Include any query parameters in the URL.
        :return: The JSON response from the Arduino, or {"error": message} if the request fails.
        """
        logging.debug(f"Requesting {cls.address}/{endpoint}")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{cls.address}/{endpoint}") as resp:
                if resp.status != 200:
                    logging.error(f"Error: HTTP Request failed with code {resp.status} - {await resp.text()}")
                    return {"error": "HTTP Request failed"}
                try:
                    logging.debug(f"Response: {await resp.text()}")
                    return await resp.json(content_type=None)
                except Exception as e:
                    logging.error(f"Error: Failed to parse JSON response - {e}")
                    return {"error": "Failed to parse JSON response"}
        return {"error": "Unexpected failure"}

    @classmethod
    async def status(cls):
        return await cls.__getRequestToResponse("status")
    
    @classmethod
    async def move_steps(cls, num_steps):
        return await cls.__postRequestToResponse(f"move?steps={num_steps}")

    @classmethod
    async def abort(cls):
        return await cls.__postRequestToResponse("abort")
    
    @classmethod
    async def move_absolute(cls, voltage):
        return await cls.__postRequestToResponse(f"set?voltage={voltage}")

    @classmethod
    async def move_relative(cls, voltage):
        return await cls.__postRequestToResponse(f"move?voltage={voltage}")

    @classmethod
    async def home(cls):
        return await cls.__postRequestToResponse("home")
