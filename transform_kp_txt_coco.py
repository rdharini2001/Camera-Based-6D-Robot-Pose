import csv
import json
from sorcery import dict_of
annotate=[]
annotate1=[]
kp_list=['Text','Grip','Lidar','Rod A','Rod D','Rod B','Rod C','Estop','Power','USB''Rubber Cap','Red Text','Left Top','Left Bottom','Right Top','Right Bottom','Orange Left Top','Orange Left Bottom','Orange Right Top','Orange Right Bottom','Cap Left Top','Cap Left Bottom','Cap Right Top','Cap Right Bottom','Front Left','Front Right','Left Edge','Right Edge','Rod Center','USB Cap']
id=0
for folder in range(0,200):
    for name in range(0,20):
        if folder is 3:
            folder=folder+1
        bbox=[]
        f={}
        final1=[]
        keypoints=[]
        row=[]
        row1=[]
        b=0
        f_name="solo_60/sequence."+str(folder)+"/step"+str(name)+".frame_data.json"
        f=open(f_name)
        # print(f_name)
        data=json.load(f)
        for i in data['captures']:
            for j in i['annotations']:
                if j['id']=="bounding box":
                    for k in j['values']:
                        for l in k['origin']:
                            #    print(l)
                            bbox.append(l)
                        for l in k['dimension']:
                            bbox.append(l)
                else:
                    for k in j['values']:
                        for l in k['keypoints']:
                            keypoints.append(l['location'])        
            
        
        for x in bbox:
            row.append(x)
        
        row[0]=(row[0]+row[2]/2)/833
        row[1]=(row[1]+row[3]/2)/577
        row[2]=(row[2])/833
        row[3]=row[3]/577
        # img_name="step"+str(id)+".Camera.png"
        # row.append(img_name)
        # row.append(1012)
        # row.append(577)
        print(row)
        
        
        
        c=0
        for x in range(0,30):
            
            row1.append(keypoints[x][0]/833)
            row1.append(keypoints[x][1]/577)
            row1.append(2.0)
    
        
        # print(annotate1)
        ann_name="Annotation/img"+str(id)+".txt"
        with open(ann_name, "w") as f:
            f.write(str(0)+" ")
            for x in row:
                f.writelines(str(x)+" ")
            
            for y in row1:
                f.writelines(str(y)+" ")
            # f.writelines(annotate1)        
        f.close()
        id=id+1
