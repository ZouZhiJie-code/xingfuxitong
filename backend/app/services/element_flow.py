ELEMENTS: list[str] = ["意义", "意志", "经济", "健康", "人际", "美德", "热爱", "擅长"]


def next_element(current_element: str | None) -> str:
    if current_element is None:
        return ELEMENTS[0]
    try:
        idx = ELEMENTS.index(current_element)
    except ValueError:
        return ELEMENTS[0]
    return ELEMENTS[min(idx + 1, len(ELEMENTS) - 1)]
