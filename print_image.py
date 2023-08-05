import cv2
id=0
for folder in range(0,200):
    for name in range(0,20):
        img_name="solo_60/sequence."+str(folder)+"/step"+str(name)+".Camera.png"
        new_img="Images/img"+str(id)+".png"
        print(img_name)
        im=cv2.imread(img_name)
        cv2.imwrite(new_img,im)
        id=id+1
