import cv2


def detect_laptop_screen(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # Detect edges
    edges = cv2.Canny(
        blur,
        50,
        150
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    best_rectangle = None
    best_area = 0

    for contour in contours:

        perimeter = cv2.arcLength(
            contour,
            True
        )

        approx = cv2.approxPolyDP(
            contour,
            0.02 * perimeter,
            True
        )

        # Laptop screen should look like rectangle
        if len(approx) == 4:

            area = cv2.contourArea(approx)

            if area < 50000:
                continue

            if area > best_area:

                x, y, w, h = cv2.boundingRect(
                    approx
                )

                # Reasonable screen proportions
                ratio = w / float(h)

                if 1.3 < ratio < 2.5:

                    best_area = area

                    best_rectangle = (
                        x,
                        y,
                        w,
                        h
                    )

    return best_rectangle