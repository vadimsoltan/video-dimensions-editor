import sys
import cv2

# coordinates storing the dimensions of the cropped video.
CROP_COORDS = []

# defines how much to scale down the video for viewing.
SCALE = 40


def main():
    '''
    Main function for starting cropping loop and parsing file location.
    '''

    get_cropping_dimensions(sys.argv[1])


def get_cropping_dimensions(video_location):
    '''
    Cropping loop function. Prompts user to select three points indicating area to be cropped.
    : param video_location: Path to the video that is to be cropped
    '''
    cap = cv2.VideoCapture(video_location)
    # set up mouse event listener
    cv2.namedWindow('resized')
    cv2.setMouseCallback('resized', get_coordinates)
    # get total number of frames from the video being edited. User for looping.
    total_frames = int(cap.get(cv2.CAP_PROP_FPS))
    frame_counter = 0
    cropped_frames = []
    confirm_crop = False
    while (cap.isOpened()):
        _, frame = cap.read()
        frame_counter += 1
        # resize video for easier editing.
        resized_frame = reisze_frame(frame, SCALE, cv2.INTER_AREA)
        # check if we have completed the three points for a crop.
        if(len(CROP_COORDS) == 3 and confirm_crop):
            cropped_frame = crop_frame(resized_frame)
            cropped_frames.append(cropped_frame)
            cv2.destroyWindow('resized')
            cv2.imshow('cropped', cropped_frame)
        else:
            for coord in CROP_COORDS:
                cv2.circle(resized_frame, coord, 2, [255, 255, 255], 2)
            cv2.imshow('resized', resized_frame)

        key = cv2.waitKey(1) & 0xFF
        if(key == ord('q')):
            break

        if(key == ord('s')):
            save_cropped_video(cropped_frames)

        if(key == ord('\n') or key == ord('\r')):
            confirm_crop = True
        # loop video
        if(frame_counter == total_frames):
            frame_counter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    cap.release()
    cv2.destroyAllWindows()


def crop_frame(frame):
    '''
    Crops a specified frame based on the selected coorwriterdinates.
    CROP_COORDS = [(starting_x, starting_y),
                    (height_x, height_y), (width_x, width_y)]
    : param frame : A matrix containing informtion about the frame being cropped.
    : return : A truncated version of the original matrix passed in.
    '''
    starting_x = CROP_COORDS[0][0]
    starting_y = CROP_COORDS[0][1]
    crop_height = abs(starting_y - CROP_COORDS[1][1])
    crop_width = abs(starting_x - CROP_COORDS[2][0])
    print(starting_y, starting_x, crop_height, crop_width)

    # cropping frame
    cropped_frame = frame[starting_y: starting_y +
                          crop_height, starting_x: starting_x+crop_width]

    return cropped_frame


def reisze_frame(frame, resize_scale, interpolation):
    '''
    Resizes a farme based on a scale factor and interpolation method.
    : param frame: Is the matrix storing and image.
    : param resize_scale: Is the factor by which to resized the image.
    : param interpolation: Is the algorith used for scaling the image. See OpenCV Doc
    https://docs.opencv.org/master/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d
    : return : A transformed matrix of the original frame.
    '''
    h, w = frame.shape[:2]
    resize_h = (h * resize_scale / 100)
    resize_w = (w * resize_scale / 100)
    dimensions = (int(resize_w), int(resize_h))
    resized_frame = cv2.resize(frame, dimensions, interpolation)

    return resized_frame


def get_coordinates(event, x, y, flags, params):
    '''
    Callback double click listener tied to the capture object instantiated by OpenCv.
    Adds coordinates to global array, indicating area to crop.
    : param event : Is the event type that OpenCV passes to the callback.
    : param x : Is the x coordinate of the mouse on the image.
    : param y : Is the y coordinate of the mouse of the image.
    '''
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        if(len(CROP_COORDS) < 3):
            CROP_COORDS.append((x, y))


def save_cropped_video(frames):
    '''
    Saves video based on the given array of frames.
    : param frames: Array of matricies representing frames of the video.
    '''
    for frame in frames:
        frame = reisze_frame(frame, 100/SCALE, cv2.INTER_CUBIC)
    writer = cv2.VideoWriter('output.avi', -1, 17.0, frames[0].shape[:2])

    for frame in frames:
        writer.write(frame)


main()
