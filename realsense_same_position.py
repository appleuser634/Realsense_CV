import pyrealsense2 as rs
import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

#ストリーム設定
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

#ストリーム開始
pipeline.start(config)

#画角調整用
align_to = rs.stream.color
align = rs.align(align_to)

#アーム先端と仮定したオブジェクトの距離画像からHSVを取得
#返り値はアーム先端のHSV値と画像中の座標(実質、三次元座標)
def get_arm_hsv(img,depth_colormap):

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    depth_colormap = cv2.cvtColor(depth_colormap,cv2.COLOR_BGR2HSV)

    lo_color = np.array([0,120,120])
    hi_color = np.array([20,255,255])

    mask = cv2.inRange(hsv,lo_color,hi_color)

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(cnt) for cnt in contours]
    
    if len(areas) == 0:
        return None,None,None

    big_index = np.argmax(areas)

    big_area = contours[big_index]

    M = cv2.moments(big_area)

    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])
    
    hsv_color = depth_colormap[y][x]

    return hsv_color,x,y

#カメラからアーム先端の距離と同じ距離の領域に対してマスク処理をかける
def detect_same_depth(depth_colormap,hsv_color):
    
    hsv = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

    lo_parm = [l-5 for l in hsv_color]
    hi_parm = [l+5 for l in hsv_color]

    lo_color = np.array(lo_parm)
    hi_color = np.array(hi_parm)

    mask = cv2.inRange(hsv,lo_color,hi_color)

    return mask


try:
    while True:
        frames = pipeline.wait_for_frames()
        #depth_frame = frames.get_depth_frame()
        #color_frame = frames.get_color_frame()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)

        #images = np.hstack((color_image, depth_colormap))

        hsv_color,x,y = get_arm_hsv(color_image,depth_colormap)
        
        if hsv_color is None:
            continue
        
        cv_image = cv2.circle(color_image,(x,y),5,(0,255,0),-1) 
        
        print("COLOR:",hsv_color)
        
        mask = detect_same_depth(depth_colormap,hsv_color)
        
        only = cv2.bitwise_and(color_image,color_image,mask=mask)

            
        cv2.imshow('RealSense', depth_colormap)
        cv2.imshow('Show depth!',color_image)
        cv2.imshow("show only!",only)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
