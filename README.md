# MediaPipe × OpenCVによる目のマスク描画

このプロジェクトは、**MediaPipe** のPose検出機能を使ってWebカメラ映像から人の骨格を検出し、左右の目の位置をもとに目の上に黒い四角形（マスク）をリアルタイムで描画します。

## 主な機能

- MediaPipeによるリアルタイム骨格検出
- 両目の外側の位置（`LEFT_EYE_OUTER` / `RIGHT_EYE_OUTER`）の取得
- 目の向きと距離からマスク（長方形）の座標を計算
- OpenCVで目の上に黒塗りの四角形を描画
- `resize_scale` による出力解像度の調整
- `q`キーで処理を終了可能

## 実行イメージ

![Image](https://github.com/user-attachments/assets/c9e67260-0a1c-4c7b-be02-40270fb5287f)

## 必要環境

- Python 3.7以降
- OpenCV
- MediaPipe
- NumPy

以下のコマンドで依存ライブラリをインストールできます：

```bash
pip install opencv-python mediapipe numpy
