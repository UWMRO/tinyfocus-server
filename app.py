from flask import Flask, request
import argparse
import logging

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def ping():
        return 'Tiny Focus Server is running!'

    @app.route('/api/status')
    async def status():
        return await focus_arduino.status()
    
    @app.route('/api/move')
    async def move():
        num_steps = int(request.args.get('steps', 0))
        return await focus_arduino.move_steps(num_steps)
    
    @app.route('/api/abort')
    async def abort():
        return await focus_arduino.abort()
    
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
    
    @app.route('/api/gohome')
    async def go_home():
        return focus_arduino.go_home()
        
    return app


app = create_app()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Tiny Focus Server')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port number to run the server on')
    parser.add_argument('-d', '--debug', action='store_true', help='Use the mock Arduino for testing')
    args = parser.parse_args()

    port = args.port
    app.debug = args.debug

    if args.debug:
        logging.debug("Debug mode is enabled. Using mock Arduino.")
        from mock_arduino.mock import focus_arduino
    else:
        from tinyfocus.arduino_connection import focus_arduino

    app.run(host='127.0.0.1', port=port, debug=True, processes=1, threaded=True)
