"""
SVG icon library. Icons from Lucide (https://lucide.dev), MIT licensed.
Each function returns an inline SVG string sized and colored to match context.
"""

def _svg(path_d: str, size: int = 24, color: str = "#8B5A3C", stroke_width: float = 2) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}"
        viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}"
        stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle;">
        {path_d}
        </svg>"""

def file_text(size=24, color="#8B5A3C"):
    return _svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/>', size, color)

def message_circle(size=24, color="#8B5A3C"):
    return _svg('<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>', size, color)

def pill(size=24, color="#8B5A3C"):
    return _svg('<path d="M10.5 20.5 20.5 10.5a5.66 5.66 0 0 0-8-8L2.5 12.5a5.66 5.66 0 0 0 8 8Z"/><path d="M8.5 8.5l7 7"/>', size, color)

def heart(size=24, color="#8B5A3C"):
    return _svg('<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>', size, color)

def alert_triangle(size=24, color="#D9705B"):
    return _svg('<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>', size, color)

def phone(size=24, color="#8B5A3C"):
    return _svg('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>', size, color)

def droplet(size=24, color="#8B5A3C"):
    return _svg('<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>', size, color)

def map_pin(size=24, color="#FFFFFF"):
    return _svg('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>', size, color)

def siren(size=48, color="#FFFFFF"):
    return _svg('<path d="M7 12a5 5 0 0 1 5-5v0a5 5 0 0 1 5 5v6H7v-6Z"/><path d="M5 20a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v2H5v-2Z"/><path d="M21 12h1"/><path d="M18.5 4.5 18 5"/><path d="M2 12h1"/><path d="M12 2v1"/><path d="m4.929 4.929.707.707"/><path d="M12 12v6"/>', size, color)

def stethoscope(size=100, color="#8B5A3C"):
    return _svg('<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.3.3 0 1 0 .2.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>', size, color)

def camera(size=24, color="#FFFFFF"):
    return _svg('<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>', size, color)

def image_icon(size=24, color="#8B5A3C"):
    return _svg('<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>', size, color)

def arrow_right(size=20, color="#FFFFFF"):
    return _svg('<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>', size, color)

def check_circle(size=24, color="#5C8B6E"):
    return _svg('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>', size, color)

def mic(size=20, color="#8B5A3C"):
    return _svg('<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>', size, color)

def send(size=20, color="#FFFFFF"):
    return _svg('<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>', size, color)

def flask(size=24, color="#8B5A3C"):
    return _svg('<path d="M9 3h6v4l4 8a4 4 0 0 1-4 5H9a4 4 0 0 1-4-5l4-8V3z"/><line x1="9" y1="3" x2="15" y2="3"/><line x1="9" y1="12" x2="15" y2="12"/>', size, color)

def note(size=24, color="#8B5A3C"):
    return _svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="15" x2="15" y2="15"/>', size, color)

def clock(size=24, color="#8B5A3C"):
    return _svg('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>', size, color)

def check(size=24, color="#5C8B6E"):
    return _svg('<polyline points="20 6 9 17 4 12"/>', size, color)

def circle_dot(size=24, color="#D9705B"):
    return _svg('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3" fill="' + color + '"/>', size, color)

def lock(size=24, color="#8B5A3C"):
    return _svg('<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>', size, color)

def wifi_off(size=24, color="#8B5A3C"):
    return _svg('<path d="M1 1 22 22"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 2.28-1.49"/><path d="M10.71 5.05A16 16 0 0 1 22.58 9"/><path d="M1.42 9a16 16 0 0 1 11.87-3.95"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>', size, color)

