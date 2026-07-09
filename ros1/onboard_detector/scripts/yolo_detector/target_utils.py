def build_visual_target(boxes, target_classes, image_width, image_height, lost_time):
    matches = [box for box in boxes if len(box) >= 5 and box[4] in target_classes]
    if not matches:
        return [0.0, 0.0, 0.0, 0.0, 0.0, float(lost_time)]

    selected = max(matches, key=_box_area)
    x1, y1, x2, y2 = [float(value) for value in selected[:4]]
    confidence = float(selected[5]) if len(selected) >= 6 else 1.0

    width = max(0.0, x2 - x1)
    height = max(0.0, y2 - y1)
    cx = x1 + width * 0.5
    cy = y1 + height * 0.5
    image_area = float(image_width * image_height)

    return [
        1.0,
        _normalize_center(cx, image_width),
        _normalize_center(cy, image_height),
        (width * height) / image_area if image_area > 0.0 else 0.0,
        confidence,
        0.0,
    ]


def _box_area(box):
    x1, y1, x2, y2 = [float(value) for value in box[:4]]
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def _normalize_center(value, size):
    if size <= 0:
        return 0.0
    return (float(value) / float(size)) * 2.0 - 1.0
