import numpy as np

moveIncrement = .01 #distance the stages move
start_pos = .01 #starting position should be the increment size
end_pos = 1.01 #distance each stage should move when pulling the fiber

moveBack_start = end_pos-moveIncrement
moveBack_end = start_pos-moveIncrement

for y in np.arange(moveBack_start, moveBack_end, -moveIncrement):
    print("Value of y: ", y)
