import cv2 as cv
import os


def main():

    # videoFeed = cv.VideoCapture(0)

    # while True:
    #     ret, frame = videoFeed.read()
    #     cv.imshow("Video", frame)

    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         break


    # videoFeed.release()
    # cv.destroyAllWindows()

    img = cv.imread(os.path.join("images", "Corrected",  "1.png" ))

    width = int(img.shape[0])
    height = int(img.shape[1])

    print ("Dimentions of image = (" + str(width) + " " + str(height) + ")\n")
    
    scale_percent = 10  

    scale_width = int(width * (scale_percent/100)), int(height * (scale_percent/100))
    img = cv.resize(img, (150,150))

    cv.imshow("Image", img)
    cv.waitKey()
    pass




if __name__ == '__main__':
    main()