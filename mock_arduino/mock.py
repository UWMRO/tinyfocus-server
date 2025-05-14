from flask import jsonify
import asyncio

class focus_arduino:
    """
    A mock for the focuser arduino. It simulates what will be returned from the actual arduino so that
    we can test the server without needing to have the actual arduino connected.
    """

    # step position of the motor
    position = 0
    # voltage readout of the potentiometer
    voltage = 0
    # the upper and lower limits of the motor in steps (need to evaluate if this should be voltage instead)
    # also possible that this is just arbitrary, so idk.
    up_limit = 100
    down_limit = -100
    # whether the motor is currently moving
    moving = False

    # Specifications for the below functions can be found here:
    # https://docs.google.com/document/d/18srtLU6njw8gjQcMVPEmYDES0dOmodDcjzHt4GefPW0/edit?tab=t.0

    @classmethod
    def status(cls):
        return jsonify({
            "moving": cls.moving,
            "voltage": cls.voltage,
            "limit": cls.position >= cls.up_limit or cls.position <= cls.down_limit,
            "step": cls.position,
        })
    
    @classmethod
    async def move_steps(cls, num_steps):
        cls.moving = True
        for _ in range(abs(num_steps)):
            if not cls.moving or cls.position > cls.up_limit or cls.position < cls.down_limit:
                if cls.position > cls.up_limit:
                    cls.position = cls.up_limit
                elif cls.position < cls.down_limit:
                    cls.position = cls.down_limit
                break
            if num_steps > 0:
                cls.position += 1
            else:
                cls.position -= 1
            await asyncio.sleep(0.1)
        cls.moving = False
        return jsonify({"code": 200})

    @classmethod
    def abort(cls):
        cls.moving = False
        return jsonify({"code": 200})
    
    @classmethod
    def move_absolute(cls, voltage):
        cls.voltage = voltage
        return jsonify({"code": 200})
        

    @classmethod
    def move_relative(cls, voltage):
        cls.voltage += voltage
        return jsonify({"code": 200})
    

    @classmethod
    def home(cls):
        pass
