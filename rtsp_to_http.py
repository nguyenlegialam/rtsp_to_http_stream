# type uvicorn test_fastAPI_github:app --reload to run
from imutils.video import VideoStream
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
import threading
import imutils
import time
import cv2
import uvicorn
from multiprocessing import Process, Queue

HTTP_PORT = 6064
lock = threading.Lock()
app = FastAPI()

# khai bao so manager (camera su dung)
manager1 = None
manager2 = None
manager3 = None
manager4 = None
manager5 = None
manager6 = None
count_keep_alive = 0

width = 1280
height = 720


# =============== Nhap dia chi ip cua cac camera su dung =================
cam_cong_rtsp = "rtsp://admin:@172.16.0.3:554/axis-media/media.amp"
cam_tret_rtsp = "rtsp://admin:@172.16.0.4:554/axis-media/media.amp"
cam_tang1_rtsp = "rtsp://admin:@172.16.0.8:554/axis-media/media.amp"
cam_tang2_rtsp = "rtsp://admin:@172.16.0.5:554/axis-media/media.amp"
cam_tang3_rtsp = "rtsp://admin:@172.16.0.7:554/axis-media/media.amp"
cam_tang4_rtsp = "rtsp://admin:@172.16.0.6:554/axis-media/media.amp"


# ================ function bat dau ghi lai stream ===================
def start_stream(url_rtsp, manager):
    global width
    global height
    vs = VideoStream(url_rtsp).start()
    while True:
        time.sleep(0.25)

        frame = vs.read()
        frame = imutils.resize(frame, width=680)
        output_frame = frame.copy()

        if output_frame is None:
            continue
        (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
        if not flag:
            continue
        manager.put(encodedImage)


# ================== tao function cho tung camera ===========================
def streamer1():
    try:
        while manager1:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager1.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def streamer2():
    try:
        while manager2:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager2.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def streamer3():
    try:
        while manager3:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager3.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def streamer4():
    try:
        while manager4:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager4.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def streamer5():
    try:
        while manager5:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager5.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


def streamer6():
    try:
        while manager6:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(manager6.get()) + b'\r\n')
    except GeneratorExit:
        print("cancelled")


# ========= function de stream lien tuc cac hinh anh duoc cat tu start_stream() =============
def manager_keep_alive(p):
    global count_keep_alive
    global manager1
    global manager2
    global manager3
    global manager4
    global manager5
    global manager6
    while count_keep_alive:
        time.sleep(1)
        count_keep_alive = count_keep_alive
    p.kill()
    time.sleep(.5)
    p.close()
    manager1.close()
    manager1 = None
    manager2.close()
    manager2 = None
    manager3.close()
    manager3 = None
    manager4.close()
    manager4 = None
    manager5.close()
    manager5 = None
    manager6.close()
    manager6 = None


# ================= dinh nghia cac url ===================
@app.get("/cam-nha", response_class=FileResponse)
async def video_feed_cam_nha():
    return FileResponse('cam_nha.html')


@app.get("/cam-cong")
async def video_feed_cam_cong():
    return StreamingResponse(streamer1(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/cam-tret")
async def video_feed_cam_tret():
    return StreamingResponse(streamer2(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/cam-tang1")
async def video_feed_cam_tang1():
    return StreamingResponse(streamer3(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/cam-tang2")
async def video_feed_cam_tang2():
    return StreamingResponse(streamer4(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/cam-tang3")
async def video_feed_cam_tang2():
    return StreamingResponse(streamer5(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/cam-tang4")
async def video_feed_cam_tang2():
    return StreamingResponse(streamer6(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.get("/")
def keep_alive():
    global manager1
    global manager2
    global manager3
    global manager4
    global manager5
    global manager6
    global count_keep_alive
    count_keep_alive = 10000
    # ============ thuc hien stream da luong (threading) =====================
    if not manager1:
        # ======= Cam cong ========
        manager1 = Queue()
        p1 = Process(target=start_stream, args=(cam_cong_rtsp, manager1,))
        p1.start()
        threading.Thread(target=manager_keep_alive, args=(p1,)).start()
    if not manager2:
        # ======= Cam tret ========
        manager2 = Queue()
        p2 = Process(target=start_stream, args=(cam_tret_rtsp, manager2,))
        p2.start()
        threading.Thread(target=manager_keep_alive, args=(p2,)).start()
    if not manager3:
        # ======= Cam tang 1 ========
        manager3 = Queue()
        p3 = Process(target=start_stream, args=(cam_tang1_rtsp, manager3,))
        p3.start()
        threading.Thread(target=manager_keep_alive, args=(p3,)).start()
    if not manager4:
        # ======= Cam tang 2 ========
        manager4 = Queue()
        p4 = Process(target=start_stream, args=(cam_tang2_rtsp, manager4,))
        p4.start()
        threading.Thread(target=manager_keep_alive, args=(p4,)).start()
    if not manager5:
        # ======= Cam tang 3 ========
        manager5 = Queue()
        p5 = Process(target=start_stream, args=(cam_tang3_rtsp, manager5,))
        p5.start()
        threading.Thread(target=manager_keep_alive, args=(p5,)).start()
    if not manager6:
        # ======= Cam tang 4 ========
        manager6 = Queue()
        p6 = Process(target=start_stream, args=(cam_tang4_rtsp, manager6,))
        p6.start()
        threading.Thread(target=manager_keep_alive, args=(p6,)).start()
    return "welcome"


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # start the flask app
    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT, access_log=False)
