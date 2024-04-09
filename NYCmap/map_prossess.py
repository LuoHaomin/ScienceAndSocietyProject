import cv2
import imutils
import pandas as pd



def color_map(point,color):
    dx = [-1,1,0,0]
    dy = [0,0,1,-1]

    origin = cv2.imread("../NYCmap/MapBorder.jpg")
    k = origin.shape[0]
    visited = {(point[0]*k+point[1])}
    list = []
    list.append(point)
    while(len(list)>0):
        pt = list.pop(0)
        origin[pt]=color
        print(pt)
        for i in range(0,4):
            dpt = (pt[0]+dx[i],pt[1]+dy[i])
            if(dpt[0]>0 and dpt[0]< origin.shape[0] and dpt[1]>0 and dpt[1]< origin.shape[1]):
                if(((dpt[0]*k+dpt[1]) not in visited)  and (origin[dpt][0])+int(origin[dpt][1])+int(origin[dpt][2])>720):
                    list.append(dpt)
                    visited.add(dpt[0]*k+dpt[1])

    # cv2.imshow("ima",imutils.resize(origin,900))
    # if cv2.waitKey(1000):
    #     cv2.destroyAllWindows()


def Draw_Grid():
    origin = cv2.imread("../NYCmap/MapBorder.jpg")
    #print(origin.shape)
    for i in range(0,3000,50):
        if(i%250==0):
            cv2.line(origin, (i, 0), (i, 2999), (255, 255, 0), 2)
        cv2.line(origin,(i,0),(i,2999),(155,155,0),1)
    for i in range(0,3000,50):
        if(i % 250 == 0):
            cv2.line(origin, (0, i), (2999, i), (255, 0, 255), 2)
        cv2.line(origin,(0,i),(2999,i),(155,0,155),1)

    cv2.imwrite("GridedMapBorder.jpg", origin, params=[cv2.IMWRITE_JPEG_QUALITY, 100])
    # cv2.imshow("ima",imutils.resize(origin,1000))
    # if cv2.waitKey(10000):
    #     cv2.destroyAllWindows()

if __name__ == '__main__':
    """
    # df = pd.read_parquet("../NYCmap/taxi_zones.dbf")
    # print(df.to_string())
    origin = cv2.imread("../NYCmap/maps.png",cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(origin,(3,3),0)
    # canny = cv2.Canny(blur,50,50)
    # cv2.imshow("origin", imutils.resize(canny, 600))

    ret, thous = cv2.threshold(blur, 210, 255, cv2.THRESH_BINARY)

    cv2.imwrite("MapBorder.jpg",thous,params=[cv2.IMWRITE_JPEG_QUALITY,99])
    # if cv2.waitKey(1000):
    #     cv2.destroyAllWindows()
    """
    # origin = cv2.imread("../NYCmap/MapBorder.jpg")
    for i in range(0,3000,100):
        # print(int(origin[(i,i)][1])+int(origin[(i,i)][0]))
        color_map((2100,i),(255,200,0))
    # Draw_Grid()