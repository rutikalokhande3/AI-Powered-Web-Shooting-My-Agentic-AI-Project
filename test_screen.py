import cv2
from screen_target import detect_laptop_screen


cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(
        frame,
        1
    )

    screen = detect_laptop_screen(
        frame
    )

    if screen is not None:

        x, y, w, h = screen

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 255),
            3
        )

        # Target point
        target_x = x + w // 2
        target_y = y + h // 2

        cv2.circle(
            frame,
            (target_x, target_y),
            10,
            (0, 255, 255),
            -1
        )

    cv2.imshow(
        "Laptop Target Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()