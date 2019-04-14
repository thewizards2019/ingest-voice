from flask import Flask
import speech_recognition as sr

# create_app wraps the other functions to set up the project


def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)

    @app.route("/record")
    def hello():
        # get audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak:")
            audio = r.listen(source)

        try:
            print("You said " + r.recognize_google(audio))
            # TODO: add producer {'content': msg}
            # to kafka topic same as ingest-twitter
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        return "Done"

    return app
