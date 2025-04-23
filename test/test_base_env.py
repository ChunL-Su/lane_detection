import sys
import cv2
import numpy as np
from osgeo import gdal  # 测试GDAL
from PyQt5.QtCore import QT_VERSION_STR


print("Qt 版本:", QT_VERSION_STR)
print(f"Python: {sys.version}")
print(f"OpenCV: {cv2.__version__}\nNumPy: {np.__version__}")
print(f"GDAL: {gdal.__version__}")


# 测试基本车道线检测
image = np.zeros((300, 300, 3), dtype=np.uint8)
cv2.line(image, (0, 0), (300, 300), (0, 255, 0), 2)
# cv2.imwrite("test_output.jpg", image)
cv2.imshow("Test", image)
cv2.waitKey(0)
