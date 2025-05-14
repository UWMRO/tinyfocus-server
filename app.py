from flask import Flask, request
import argparse

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def ping():
        return 'Tiny Focus Server is running!'

    @app.route('/api/status')
    def status():
        resp = focus_arduino.status()
        return resp
    
    @app.route('/api/move')
    async def move():
        num_steps = int(request.args.get('steps', 0))
        resp = await focus_arduino.move_steps(num_steps)
        return resp
    
    @app.route('/api/abort')
    def abort():
        resp = focus_arduino.abort()
        return resp
    
    @app.route('/api/absvoltage')
    async def move_absolute():
        new_voltage = int(request.args.get('absvoltage', 0))
        resp = focus_arduino.move_absolute(new_voltage)
        return resp
    #possibly have it move slowly
    
    @app.route('/api/adjvoltage')
    async def move_relative():
        new_voltage = int(request.args.get('adjvoltage', 0))
        resp = focus_arduino.move_relative(new_voltage)
        return resp
    
    return app


app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tiny Focus Server')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port number to run the server on')
    parser.add_argument('-d', '--debug', action='store_true', help='Use the mock Arduino for testing')
    args = parser.parse_args()

    port = args.port
    app.debug = args.debug

    if args.debug:
        print("Debug mode is enabled. Using mock Arduino.")
        from mock_arduino.mock import focus_arduino
    else:
        # we need to figure out how to actually communicate with the arduino
        pass
    app.run(host='127.0.0.1', port=port, debug=True, processes=1, threaded=True)
