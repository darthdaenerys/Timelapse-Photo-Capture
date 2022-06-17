# import modules and libraries
import cv2
import numpy as np
import time

# defining parameters
width=1280
height=720
start:bool=False
xstart=0
lapsedFrame=np.zeros([height,width,3],dtype=np.uint8)
initial:bool=False

# create window
cv2.namedWindow('Horizontal Timelapse',cv2.WINDOW_NORMAL)

# define camera parameters
camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
camera.set(cv2.CAP_PROP_FPS,30)
camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cv2.setWindowProperty('Horizontal Timelapse',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# defining function for flipping frame
def flipFrame(frame):
    newframe=cv2.flip(frame,1)
    return newframe

# defining the mouse callback function
def mouseClick(event,x,y,*args):
    global start
    if event==cv2.EVENT_LBUTTONDOWN and x>0 and x<150 and y>height-50 and y<height:
        start=True

# set mouse callback function
cv2.setMouseCallback('Horizontal Timelapse',mouseClick)

# program loop
while True:
    _,frame=camera.read()
    frame=flipFrame(frame)

    # check the start flag
    if start:
        lapsedFrame[:,xstart:]=frame[:,xstart:]
        frame[:,xstart:]=lapsedFrame[:,xstart:]
        cv2.line(lapsedFrame,(xstart+5,0),(xstart+5,height),(0,0,0),2)
        xstart+=1

    # create the start button
    if start==False:
        cv2.rectangle(frame,(0,height-50),(150,height),(11, 14, 217),-1)
        cv2.putText(frame,'START',(5,height-10),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),3)

    # display the rendered frame
    if start:
        cv2.imshow('Horizontal Timelapse',lapsedFrame)
    else:
        cv2.imshow('Horizontal Timelapse',frame)

    if (cv2.waitKey(1) & 0xff==ord('q')) or xstart>width+10:
        curr=''
        for i in range(6):
            curr+=f'{time.localtime()[i]}'
        cv2.imwrite("Captures/Capture-"+curr+".jpeg", lapsedFrame)
        break

cv2.destroyAllWindows()