import pyrealsense2 as rs
import numpy as np
import cv2

#RealSenseからのカラー画像・深度情報を取得するためのストリーム設定
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

#ストリーム開始
pipeline.start(config)

try:
    while True:
        #RealSenseからのストリームを取得する
        frames = pipeline.wait_for_frames()
        
        #ストリームから深度画像とカラー画像を取得
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        #もし取得できていなければ再取得のためContinue
        if not depth_frame or not color_frame:
            continue
        
        #CVで整形しやすいようにndarrayに変換
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        #深度画像を視覚化しやすいようにカラーマップを適用
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        #カラー画像と深度画像を表示
        cv2.imshow('Color Image!', color_image)
        cv2.imshow('Depth Image!', depth_colormap) 

        #終了イベントのキー待ちを設定 'q'を入力すると終了
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

finally:
    #ストリームを閉じて、表示ウィンドを消す
    pipeline.stop()
    cv2.destroyAllWindows()
