import cv2
import numpy as np
# from pyproj import Proj, transform


def show_edges(img, winname='Edges'):
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.imshow(winname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def dfs_gen_road(start_point):
    pass


def fit_lane_lines(edges, img_height=300, img_width=400):
    # set roi
    mask = np.zeros_like(edges)
    cv2.rectangle(mask, (5, 270), (1061, 571), 255, -1)  # 在ROI内画白色矩形
    masked_edges = cv2.bitwise_and(edges, mask)
    # show_edges(masked_edges)

    # 1. 概率霍夫变换检测直线
    lines = cv2.HoughLinesP(masked_edges, rho=1, theta=np.pi / 90, threshold=50,
                            minLineLength=50, maxLineGap=10)
    # show_edges(edges)
    # 创建一个彩色版本的edges用于显示（如果edges是单通道）
    if len(edges.shape) == 2:
        display_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    else:
        display_img = edges.copy()

    # 绘制检测到的线段
    line_counter = 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # filter error line - angle
            angle = np.degrees(np.arctan2(-y2 + y1, x2 - x1)) # 图像的y轴和数学中的y轴相反，所以计算y方向差值时需要注意
            if abs(angle) >= 15:
                # 线中心在图像左侧
                if ((x1+x2)/2 <= img_width*0.4) and (angle > 0):
                    # cv2.line(display_img, (x1, y1), (x2, y2), (0, 255, 0), 1)  # 绿色线段，线宽1
                    cv2.arrowedLine(display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绿色线段，线宽1
                    line_counter += 1

                # 右侧
                if ((x1 + x2) / 2 >= img_width * 0.6) and (angle < 0):
                    # cv2.line(display_img, (x1, y1), (x2, y2), (0, 255, 0), 1)  # 绿色线段，线宽1
                    cv2.arrowedLine(display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    line_counter += 1

                if (img_width*0.4 < (x1+x2)/2 < img_width*0.6) and abs(angle)>=50:
                    # cv2.line(display_img, (x1, y1), (x2, y2), (0, 255, 0), 1)  # 绿色线段，线宽1
                    cv2.arrowedLine(display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    line_counter += 1

    # 显示结果
    cv2.imwrite('./data/images/hough_road_lines_arrow.png', display_img)
    # cv2.imshow(f'Hough Lines {line_counter}', display_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return




    # 2. 提取所有点
    all_points = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        all_points.extend([(x1, y1), (x2, y2)])

    # 3. 多项式拟合（y为自变量，x为因变量）
    points = np.array(all_points)
    coeffs = np.polyfit(points[:, 1], points[:, 0], deg=2)  # 二次拟合

    # 4. 生成拟合曲线
    plot_y = np.linspace(edges.shape[0] // 2, edges.shape[0] - 1, 100)
    plot_x = coeffs[0] * plot_y ** 2 + coeffs[1] * plot_y + coeffs[2]

    return np.array([plot_x, plot_y]).T.astype(int)


def detect_lanes(image_path):
    # 1. 读取图像
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"图像加载失败: {image_path}")

    img_height, img_width = img.shape[:2]

    # 2. 灰度化 + 高斯模糊
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 4. 显示结果
    # cv2.namedWindow('Edges', cv2.WINDOW_NORMAL)
    # cv2.imshow('Edges', edges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # return

    lane_curve = fit_lane_lines(edges, img_height, img_width)
    # for i in range(len(lane_curve) - 1):
    #     cv2.line(img, tuple(lane_curve[i]), tuple(lane_curve[i + 1]), (0, 0, 255), 3)
    # cv2.imshow('Result', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return lane_curve


def image_to_gps(img_point, img_size=(1280, 720)):
    """ 模拟图像坐标转GPS（需替换为实际标定参数） """
    # 假设参数（需根据相机标定调整）
    focal_length = 1000  # 像素单位
    camera_height = 1.5  # 米

    # 1. 归一化坐标
    u, v = img_point
    x = (u - img_size[0] / 2) / focal_length
    y = (v - img_size[1] / 2) / focal_length

    # 2. 转换为地面坐标（简单投影）
    ground_x = camera_height * x
    ground_y = camera_height * y

    # 3. 转换为WGS84坐标（模拟：假设图像中心点是(116.404, 39.915)）
    lon = 116.404 + ground_x / 111320  # 经度近似换算
    lat = 39.915 + ground_y / 110540  # 纬度近似换算

    return lon, lat


if __name__ == "__main__":
    lane_curve = detect_lanes(r"./data/images/road.png")
    # if lane_curve:
    #     lane_gps = [image_to_gps(p) for p in lane_curve]
    #     print("车道线GPS坐标示例:", lane_gps[:3])
