from stem.control import Controller
from flask import Flask, render_template


if __name__ == "__main__":

    app = Flask("example")
    port = 5000
    host = "127.0.0.1"
    hidden_svc_dir = "/var/lib/tor/hidden_service"

    @app.route('/')
    def page1():
        '''

        You'll have to change the name of the template with one you actually have.

        '''
        return render_template("a_template.html")
    @app.route('/about')
    def about():
        '''

        You'll have to change the name of the template with one you actually have.

        '''
        return render_template("about.html")
    print " * Getting Controller.."
    controller = Controller.from_port(address="127.0.0.1", port=9051)
    try:
        controller.authenticate(password="YOU'RE CONTROLLER PASSWORD GOES HERE)
        controller.set_options([
            ("HiddenServiceDir", hidden_svc_dir),
            ("HiddenServicePort", "80 %s:%s" %(host, str(port)))
        ])
        svc_name = open(hidden_svc_dir + "/hostname", 'r').read().strip()


            ''' This part will print out the onion address to the server.'''
        print " * Created host: %s" % svc_name
    except Exception as e:
        print e
    app.run()
