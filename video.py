import cv2


def make_hz_videos(width, height, hz, file_name):
    black_img_path = "img/black.png"
    frameSize = (width, height)
    out_put = cv2.VideoWriter(
        file_name + "_video.avi", cv2.VideoWriter_fourcc(*"DIVX"), hz * 2, frameSize
    )

    for i in range(hz * 2):
        if i % 2:
            black_img = cv2.imread(black_img_path)
            out_put.write(black_img)
        else:
            img = cv2.imread("img/" + file_name + ".png")
            out_put.write(img)

    out_put.release()
