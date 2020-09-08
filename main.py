import sys
import cv2

global crop_coords
crop_coords = []


def main():
    get_cropping_dimensions(sys.argv[1])


def get_cropping_dimensions(video_location):
    cap = cv2.VideoCapture(video_location)
    cv2.namedWindow('resized')
    cv2.setMouseCallback('resized', draw_circle)
    total_frames = int(cap.get(cv2.CAP_PROP_FPS))
    frame_counter = 0
    current_number_coords = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        h, w = frame.shape[:2]
        frame_counter += 1
        # resizing video for easier viewing
        resize_scale = 40
        resize_h = (h * resize_scale / 100)
        resize_w = (w * resize_scale / 100)
        dimensions = (int(resize_w), int(resize_h))
        resized_frame = cv2.resize(frame, dimensions, cv2.INTER_AREA)

        if(current_number_coords < len(crop_coords)):
            cv2.circle(resized_frame, crop_coords[-1], 200, [255, 0, 0], 1)
            current_number_coords = len(crop_coords)
        if(len(crop_coords) == 3):
            starting_y = crop_coords[0][0]
            starting_x = crop_coords[0][1]
            crop_height = abs(starting_x - crop_coords[1][1])
            crop_width = abs(starting_y - crop_coords[2][0])
            print(starting_y, starting_x, crop_height, crop_width)
            # cropping video
            cropped_frame = resized_frame[starting_y: starting_y +
                                          crop_height, starting_x: starting_x+crop_width]
            cv2.destroyWindow('resized')
            cv2.imshow('cropped', cropped_frame)
        else:
            cv2.imshow('resized', resized_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        # loop video
        if(frame_counter == total_frames):
            frame_counter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    print(frame_counter)
    cap.release()
    cv2.destroyAllWindows()


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        crop_coords.append((x, y))


main()
