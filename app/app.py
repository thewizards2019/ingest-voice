from flask import Flask
import speech_recognition as sr
from confluent_kafka import Producer
import json
import uuid

# create_app wraps the other functions to set up the project


def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)

    kafkaProducer = Producer({"bootstrap.servers": "localhost:9092"})

    @app.route("/record")
    def hello():
        # get audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak:")
            audio = r.listen(source)

        try:
            data = r.recognize_google(audio)
            print("You said " + data)
            # TODO: add producer {'content': msg}
            # to kafka topic same as ingest-twitter
            data = json.dumps({"content": data.replace("'", '"')})
            kafkaProducer.produce(
                "content_curator_twitter", key=str(uuid.uuid4()), value=data
            )
            kafkaProducer.flush()
            print("ADDED:", data)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        return "Done"

    return app
