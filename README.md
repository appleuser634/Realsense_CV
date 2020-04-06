# Realsense_CV

### Ros_CV_test.py 
RealSenseの深度画像から特定色の領域の中心座標と距離を取得し画像表示の際にプロットするコード

### show_center_depth.py 
ROSからRealSenseの深度情報を取得し画角中心の距離を表示するコード

### realsense_color_depth.py 
RealSenseからの深度画像とカラー画像を表示するコード

### realsense_same_position.py 
アーム先端に見立てたオレンジ色のオブジェクトの距離と平面座標を取得し、その近辺の領域をマスク処理して描画するコード

### デモ動画

[ROSからの深度情報を3次元でプロットして表示する](https://drive.google.com/file/d/1-kIBC4Rt8rcKhoX4_j1OfzPzK4eMalPJ/view?usp=sharing)

[特定色の三次元座標を描画する](https://drive.google.com/open?id=1IrP83jeOdUFeGwyY-Vvom26eLdPCLfjl)

[対象オブジェクトと同等距離の領域をマスクして描画する](https://drive.google.com/open?id=19mWSraDM8KJTHDmGOEYvDQE9NOYPnewb)

#### 環境構築参考リンク

[RealSenseをROSで扱うための環境構築](https://github.com/IntelRealSense/realsense-ros.git)

[簡単にビルド済みのOpenCVをインストールする方法](https://qiita.com/fiftystorm36/items/1a285b5fbf99f8ac82eb)
