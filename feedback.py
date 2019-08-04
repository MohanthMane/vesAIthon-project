import os
import numpy as np
import RPi.GPIO as GPIO
import time
#from servoN import get_distance


(H,W) = (480,640)
#threshold confidence
THRESHOLD_CONFIDENCE = 0.4

X,Y = 40,25


def get_center_coordinates(ymin,xmin,ymax,xmax):
    centerX = (xmin + xmax) // 2
    centerY = (ymin + ymax) // 2
    return centerX, centerY


def give_feedback(classes,scores,boxes,category_index,feedbacks,object_mappings):
    

    pin=[26,19,13,6,5,0,11,9,10,22]
    GPIO.setmode(GPIO.BCM)
    #GPIO.setWarnings(False)
    
    for i in pin:
        GPIO.setup(i, GPIO.OUT)

    selected_scores = []
    scores_clone = list(scores)
    scores_clone.sort()
    if len(scores_clone) >= 2:
        selected_scores.append(scores_clone[-1])
        selected_scores.append(scores_clone[-2])
    elif len(scores_clone) > 0:
        selected_scores.append(scores_clone[-1])
    
    for i in range(len(classes)):

        if scores[i] > THRESHOLD_CONFIDENCE and (scores[i] in selected_scores):
            # deriving bounding box coordinates
            (ymin, xmin, ymax, xmax) = (boxes[i] * np.array([H,W,H,W])).astype('int')
            centerX, centerY = get_center_coordinates(ymin,xmin,ymax,xmax)
            width, height = abs(xmax - xmin), abs(ymax - ymin)

            if centerX <= W / 3:
                V_pos = "left, "

            elif centerX <= (W / 3 * 2):
                V_pos = "center, "

            else:
                V_pos = "right, "

            if centerY <= H / 3:
                H_pos = "top "

            elif centerY <= (H / 3 * 2):
                H_pos = "mid "

            else:
                H_pos = "bottom "


            #distance = get_distance(centerX,centerY)

            if category_index[classes[i]]['name']=='dog':
                category_index[classes[i]]['name'] = 'person'

            if category_index[classes[i]]['name']:
                object_name = category_index[classes[i]]['name']
                position = H_pos + V_pos
                text = object_name + " at " + position 
            
            ver_angle = hor_angle = 90

            if position == 'top left, ':
               ver_angle -= Y
               hor_angle += X
            elif position == 'top center, ':
               ver_angle -= Y
               hor_angle = 90
            elif position == 'top right, ':
               ver_angle -= Y
               hor_angle -= X
            elif position == 'mid left, ':
               ver_angle = 90
               hor_angle += X
            elif position == 'mid center, ':
               ver_angle = 90
               hor_angle = 90
            elif position == 'mid right, ':
               ver_angle = 90
               hor_angle -= X
            elif position == 'bottom left, ':
               ver_angle += Y
               hor_angle += X
            elif position == 'top center, ':
               ver_angle += Y
               hor_angle = 90
            elif position == 'top center, ':
               ver_angle += Y
               hor_angle -= X

            #on vib
            States=object_mappings[category_index[classes[i]]['name']];
            for i in range(len(States)):
                #GPIO.setup(pin[i], GPIO.OUT)
                if States[i] is '1':
                    GPIO.output(pin[i],GPIO.HIGH)

            if text and object_name not in feedbacks.keys():
                print(text)
                os.system('say ' + text)
                text = text.split(' at ')
                feedbacks[text[0]] = text[1]

            elif text and (feedbacks[object_name] != position):
                print(text)
                os.system('say ' + text)
                text = text.split(' at ')
                feedbacks[text[0]] = text[1]
            
            os.system('python3 servoN.py ' + str(hor_angle) + ' ' + str(ver_angle))
            time.sleep(0.5)
            ver_angle = hor_angle = 90
            os.system('python3 servoN.py ' + str(hor_angle) + ' ' + str(ver_angle))
            #off vib
            for i in range(0,10):
                GPIO.output(pin[i],GPIO.LOW)
GPIO.cleanup()
