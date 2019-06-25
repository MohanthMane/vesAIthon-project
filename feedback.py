import os
import numpy as np

(H,W) = (480,640)
THRESHOLD_CONFIDENCE = 0.4


def get_center_coordinates(ymin,xmin,ymax,xmax):
    centerX = (xmin + xmax) // 2
    centerY = (ymin + ymax) // 2
    return centerX, centerY


def give_feedback(classes,scores,boxes,category_index,feedbacks):
    for i in range(len(classes)):

        if scores[i] > THRESHOLD_CONFIDENCE :
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

            if category_index[classes[i]]['name']:
                object_name = category_index[classes[i]]['name']
                position = H_pos + V_pos
                text = object_name + " at " + position

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

