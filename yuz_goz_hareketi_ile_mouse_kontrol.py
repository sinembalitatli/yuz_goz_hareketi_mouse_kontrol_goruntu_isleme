###iki göz kırpma ayrım işlemleri tanımlandı 

import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance
import pyautogui
import win32api
import numpy as np
from keras.models import load_model
from scipy.spatial import distance as dist
import sys
import csv
import h5py

#göz tespiti için metotlar

def righteyeAspectRatio(eyePoints):
    verticaLine1=distance.euclidean(eyePoints[1], eyePoints[5])
    verticaLine2=distance.euclidean(eyePoints[2], eyePoints[4])
    horizontalLine=distance.euclidean(eyePoints[0], eyePoints[3])
    earright=(verticaLine1+verticaLine2)/(2*horizontalLine)
    return earright
def lefteyeAspectRatio(eyePoints):
    verticaLine1=distance.euclidean(eyePoints[1], eyePoints[5])
    verticaLine2=distance.euclidean(eyePoints[2], eyePoints[4])
    horizontalLine=distance.euclidean(eyePoints[0], eyePoints[3])
    earleft=(verticaLine1+verticaLine2)/(2*horizontalLine)
    return earleft
cap=cv2.VideoCapture(0)
def botheyeAspectRatio(eyePoints):
    verticaLine1=distance.euclidean(eyePoints[1], eyePoints[5])
    verticaLine2=distance.euclidean(eyePoints[2], eyePoints[4])
    horizontalLine=distance.euclidean(eyePoints[0], eyePoints[3])
    earboth=((2*verticaLine1+verticaLine2))/(4*horizontalLine)
    return earboth
#web kamerasından görüntü al
cap=cv2.VideoCapture(0)
arr = np.random.randn(1000)
#cnn modelini import
with h5py.File("blinkModel.hdf5", 'w') as f:
    dset = f.create_dataset("default", data=arr)


print("Bilgilendirme...Dosyalar yükleniyor...")
#göz tespiti için kullanılacak verileri al
path="datasets/shape_predictor_68_face_landmarks.dat"
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor(path)
print("Bilgilendirme...koordinatlar alınıyor...")
(leftStart,leftEnd)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rightStart,rightEnd)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
#değişkenler
color=(0,255,0)
thresholdValueright=0.27
thresholdValueleft=0.27
thresholdValueboth=0.54
counterright=0
realCounterright=0
counterleft=0
realCounterleft=0
counterboth=0
realCounterboth=0
font=cv2.FONT_HERSHEY_SIMPLEX

print("Bilgilendirme...Kameraya bağlanılıyor...")
print(".....")
#yüz tespiti için veriler
face_cascade=cv2.CascadeClassifier("datasets/frontalFace.xml")
while True:
    
      
    ret,frame=cap.read()
    if ret==False:
        break
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #yüz tespiti
    faces_frame=face_cascade.detectMultiScale(gray,1.3,3)
   
    for(x,y,w,h) in faces_frame:
        win32api.SetCursorPos((x,y))
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,148,50),3)
       
       
        a =6*x
        b=7*y
        if int(len(faces_frame)) == 0:
            quit()
         #yüz hareketi ile mouse kontrolü sağla   
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(a,b)
        
       
    faces=detector(gray)
    
     #göz tespiti
    for face in faces:
        landmarkPoints=predictor(gray,face)
        landmarkPoints=face_utils.shape_to_np(landmarkPoints)   
        
        leftEye=landmarkPoints[leftStart:leftEnd]
        rightEye=landmarkPoints[rightStart:rightEnd]
        leftEyeAspectRatio=lefteyeAspectRatio(leftEye)
        rightEyeAspectRatio=righteyeAspectRatio(rightEye)
        earright=leftEyeAspectRatio
        earleft=rightEyeAspectRatio
        earboth=leftEyeAspectRatio+rightEyeAspectRatio
        leftConvexHull=cv2.convexHull(leftEye)
        rightConvexHull=cv2.convexHull(rightEye)
        cv2.drawContours(frame,[leftConvexHull],-1,color,1)
        cv2.drawContours(frame,[rightConvexHull],-1,color,1)
        
        #göz kırpma tespiti
        if earleft<thresholdValueleft:
            counterleft=counterleft+1
        else:
            if counterleft>=3:
                if counterboth<3:
                    #kırpma işlemi ile mouse kontrolü sol tık
                    pyautogui.click(button='left')
                    
                 
                    
                    realCounterleft+=1
                    
                    
                    
                    print("bilgilendirme...{}.sol göz kırpma tespit edildi...".format(realCounterleft))
                counterleft=0  
        
                
                
                
                
            
        if earright<thresholdValueright:
            counterright=counterright+1
        else:
            if counterright>=3:
                
                if counterboth<3:
                    #kırpma işlemi ile mouse kontrolü sağ tık
                    pyautogui.click(button='right')
                 
                    
                    realCounterright+=1
                    
                    
                    
                    print("bilgilendirme...{}.sağ göz kırpma tespit edildi...".format(realCounterright))
                counterright=0  
              
                           
                 
                
                
           
        if earboth<thresholdValueboth:
            counterboth=counterboth+1
        else:
            if counterboth>=3:
                #kırpma işlemi ile mouse kontrolü çift tık
                pyautogui.click(clicks=2)
                 
                
                realCounterboth+=1
                print("bilgilendirme...{}.iki  göz kırpma tespit edildi...".format(realCounterboth))
                
            counterboth=0
        #değerlerin görüntü üzerine yazılması   
        cv2.putText(frame,"LeftEyeBlink:{}".format(realCounterleft),(25,50),font,0.8,color,2)
        cv2.putText(frame,"Left- Eye Aspect Ration:{:.2f}".format(earleft),(250,50),font,0.8,color,2)
        cv2.putText(frame,"RightEyeBlink:{}".format(realCounterright),(25,100),font,0.8,color,2)
        cv2.putText(frame,"Right Eye Aspect Ration:{:.2f}".format(earright),(250,100),font,0.8,color,2)
        cv2.putText(frame,"BothEyeBlink:{}".format(realCounterboth),(25,20),font,0.8,color,2)
        cv2.putText(frame,"both Eye Aspect Ration:{:.2f}".format(earboth),(250,20),font,0.8,color,2)
       
        
      
        
            
                
    
    
    
    
    cv2.imshow("",frame)
    
    
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
cap.release()







    

        
        
    







                
    