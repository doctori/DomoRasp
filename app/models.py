from app import db
from datetime import datetime
import time
import sys
from RF24 import *

radio = RF24(22,0)
pipes = [ "1Node","2Node"]
millis = lambda: int(round(time.time() * 1000))
payloadSize = 16

class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    status = db.Column(db.Integer)
    description = db.Column(db.Text)
    elements = db.relationship('Element', backref='controller', lazy='dynamic')
    addedAt = db.Column(db.DateTime)
    pipeRead = db.Column(db.String(32))
    pipeWrite = db.Column(db.String(32))

    def __repr__(self):
        return '<Controller %r>' % (self.name)

    def __init__(self, name, status, description,pipeRead,pipeWrite):
        self.name = name
        self.status = status
        self.description = description
        self.addedAt = datetime.now()
        self.pipeRead = pipeRead
        self.pipeWrite = pipeWrite

    def switch(self):
        if self.status != 0:
            self.status = 0
        else:
            self.status = 255
        self.updateController()
        db.session.commit()

    def updateController(self):
        for element in self.elements:
            element.status = self.status
            element.updateElement()


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text())
    status = db.Column(db.Integer)
    lastUpdate = db.Column(db.DateTime)
    addedAt = db.Column(db.DateTime)
    controller_id = db.Column(db.Integer, db.ForeignKey('controller.id'))

    def __init__(self, name, status, description,controller_id):
        self.name = name
        self.status = status
        self.description = description
        self.controller_id = controller_id
        self.addedAt = datetime.now()

    def getPayload(self):
        return "%d|%d" % (self.id, self.status)

    def switch(self):
        if self.status != 0:
            self.status = 0
        else:
            self.status = 255
        self.updateElement()
        db.session.commit()

    def updateElement(self):
        payload = self.getPayload()
        print('Trying To Communicate with the Arduino Nano')

        radio.begin()
        radio.setAutoAck(1);
        radio.enableAckPayload();
        radio.setRetries( 15, 15);

        radio.printDetails()
        print("writing to pipe : "+self.controller.pipeWrite.encode('utf-8'))
        print("Reading to Pipe : "+self.controller.pipeRead.encode('utf-8'))
        radio.openWritingPipe(self.controller.pipeWrite.encode('utf-8'))
        radio.openReadingPipe(1,self.controller.pipeRead.encode('utf-8'))

        while 1:
            radio.stopListening()
            print('Now sending ', str(payload), ' ... ',)
            radio.write(payload)
            radio.startListening()

            # Wait here until we get a response, or timeout
            started_waiting_at = millis()
            timeout = False
            while (not radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 1000:
                    timeout = True

            # Describe the results
            if timeout:
                print('failed, response timed out.')
            else:
                # Grab the response, compare, and send to debugging spew
                len = radio.getDynamicPayloadSize()
                receive_payload = radio.read(len)

                # Spew it
                print('got response size=', len, ' value="', receive_payload, '"')
                break
            time.sleep(1)