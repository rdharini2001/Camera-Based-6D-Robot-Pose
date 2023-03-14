import numpy as np
pts_src=np.array([[-18.5,18.5,1],[-18.5,-18.5,1],[18.5,-18.5,1],[18.5,18.5,1],[-78.5,-41.5,1],[-78.5,-78.5,1],[-41.5,-78.5,1],[-41.5,-41.5,1],[-18.5,178.5,1],[-18.5,161.5,1],[18.5,161.5,1],[18.5,178.5,1],[-18.5,318.5,1],[-18.5,281.5,1],[18.5,281.5,1],[18.5,318.5,1],[-138.5,138.5,1],[-138.5,101.5,1],[-101.5,101.5,1],[-101.5,138.5,1],[-198.5,258.5,1],[-198.5,221.5,1],[-161.5,221.5,1],[-161.5,258.5,1]])  # planar object points 
pts_dst=np.array([[836,462,1],[834,339,1],[743,396,1],[738,460,1],[657,581,1],[670,502,1],[568,497,1],[548,573,1],[823,224,1],[822,191,1],[756,189,1],[754,222,1],[816,131,1],[814,110,1],[758,109,1],[759,139,1],[573,279,1],[586,241,1],[517,242,1],[500,279,1],[516,173,1],[529,147,1],[475,148,1],[459,173,1]]) # image points
import cv2
h, status = cv2.findHomography(pts_src, pts_dst)
# print(h)


#pts_src=np.array([[-78.5,341.5],[-41.5,341.5],[-41.5,378.5],[-78.5,378.5],[-18.5,-18.5],[18.5,-18.5],[18.5,18.5],[-18.5,18.5]])  # planar object points 

pts_src=np.array([[101.5,198.5],[101.5,161.5],[138.5,161.5],[138.5,198.5],[101.5,378.5],[101.5,341.5],[138.5,341.5],[138.5,378.5],[101.5,78.5],[101.5,41.5],[138.5,41.5],[138.5,78.5]])  # planar object test points 



# print(np.shape(pts_src))
h=np.array([[2.59275014,1.22742257,703.045769],[0.0176127956,-0.801686794,417.718048],[0.000208861672,0.00224224441,1.00000000]])
pts_dst=np.zeros((3,1)) # image points
distortion_matrix = np.array([-0.44779831 , 0.21493212,0.0086979,-0.00269077,0.00281984])
camera_matrix = np.array([[951.66304851,0,643.42125081],
 [0,947.84899404,334.96279408],
 [0,0,1]])
# print(np.shape(camera_matrix))
# print(np.shape(distortion_matrix))
pts_src_1=[]
for pts in pts_src:
    # print(np.shape(pts))
    # print()
    pts=cv2.undistortPoints(pts,camera_matrix,distortion_matrix)
    # print(np.shape(pts))
    # print(pts)
    pts_src_1.append(pts)

dst=[]
pts_src_final=[]
for item in pts_src_1:
    for item1 in item:
        for item2 in item1:
            # print(np.shape(item2))
            pts_src_final.append(item2)

# print(pts_src_final)
import cv2,itertools
# from numpy.linalg import inv
# h=inv(h)

for pts in pts_src_final:
    # np.append(pts,1)
    pts=pts.tolist()
    pts.append(1)
    # print(pts)
    # print(np.shape(pts))
    # print(np.shape(h))
    pts=np.asarray(pts)

    # print("Points")
    # print(pts)
    # print("H")
    # print(h)
    pts_dst=np.matmul(h,pts)
    # print(pts_dst)
    pts_dst[0]=pts_dst[0]/pts_dst[2]
    pts_dst[1]=pts_dst[1]/pts_dst[2]
    pts_dst[2]=1
    print(pts_dst)
    dst.append(pts_dst)

# print("Hello")

# print(dst)
#img_test=np.array([[[523.0],[80.0]],[[576.0],[80.0]],[[574.0],[61.0]],[[525.0],[63.0]],[[663.0],[451.0]],[[755.0],[449.0]],[[740.0],[388.0]],[[655.0],[390.0]]])

img_test=np.array([[[1039.0],[233.0]],[[1024.0],[202.0]],[[964.0],[198.0]],[[976.0],[231.0]],[[978.0],[109.0]],[[969.0],[88.0]],[[923.0],[85.0]],[[928.0],[104.0]],[[1089.0],[368.0]],[[1072.0],[321.0]],[[999.0],[319.0]],[[1013.0],[366.0]]])#image test points

# # print(img_test)
img_test_1=[]

for pts in img_test:
#     # print(pts)
#     # print()
    pts=cv2.undistortPoints(np.array(pts),camera_matrix,distortion_matrix, P=camera_matrix)
    img_test_1.append(pts)

img_src_final=[]
for item in img_test_1:
    for item1 in item:
        for item2 in item1:
            # print(np.shape(item2))
            img_src_final.append(item2)
# print(img_src_final)
# print(np.shape(img_src_final))
dist=0
for pts_test,pts in zip(img_src_final,dst):
    # print(pts_test)
    # print()
    # print(pts)
    pts_test=pts_test.tolist()
    # print(pts)
    pts_test.append([1])
    # print(pts)
    # pts_test=np.array(pts_test)
    
#     for p1,p2 in zip(pts_test,pts):
# #         #   print(p1[0],p2[0])
#           dist+=pow(abs(p1[0]-p2[0]),2)
          
#     print(np.sqrt(dist))
# # # #,[-138.5,-78.5],[-101.5,-78.5],[-101.5,-41.5],[-138.5,-41.5]             ,[-41.5,341.5,0],[-41.5,378.5,0],[-78.5,378.5,0
