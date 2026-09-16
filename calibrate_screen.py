import cv2
import json

points = []

WINDOW_NAME = "Screen Calibration"


def mouse_callback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        if len(points) < 4:

            points.append([x, y])

            print(
                f"Point {len(points)}: ({x}, {y})"
            )


cap = cv2.VideoCapture(0)

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(
    WINDOW_NAME,
    mouse_callback
)


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera open nahi hua!")
        break

    frame = cv2.flip(frame, 1)

    # Draw selected points
    for i, point in enumerate(points):

        x, y = point

        cv2.circle(
            frame,
            (x, y),
            8,
            (0, 255, 255),
            -1
        )

        cv2.putText(
            frame,
            str(i + 1),
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    # Draw calibration rectangle
    if len(points) == 4:

        pts = [
            tuple(p)
            for p in points
        ]

        for i in range(4):

            cv2.line(
                frame,
                pts[i],
                pts[(i + 1) % 4],
                (0, 255, 255),
                2
            )

    cv2.imshow(
        WINDOW_NAME,
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # ENTER = save
    if key == 13:

        if len(points) == 4:

            with open(
                "screen_calibration.json",
                "w"
            ) as f:

                json.dump(
                    {
                        "screen_corners": points
                    },
                    f,
                    indent=4
                )

            print()
            print(
                "Screen calibration saved!"
            )
            print(
                "screen_calibration.json created."
            )

            break

        else:

            print(
                "Pehle 4 corners select karo!"
            )

    # R = reset
    elif key == ord("r"):

        points.clear()

        print(
            "Points reset."
        )

    # Q = quit
    elif key == ord("q"):

        break


cap.release()
cv2.destroyAllWindows()