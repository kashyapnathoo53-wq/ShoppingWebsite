import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1376
HEIGHT = 545

# 1. Background plate with clean travertine floor and realistic mid-air water arc
plate_path = r'C:\Users\ADMIN\.gemini\antigravity\brain\c228a748-d79c-4230-b18c-69a39bc2446e\purifier_background_plate_flat_floor_1795120218808.jpg'
bg_raw = Image.open(plate_path).convert('RGB')
bg = bg_raw.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert('RGBA')

# 2. Extract 4 100% WHOLESOME, UNTRUNCATED PURIFIER MACHINES
# Model 1: Pearl IoT (complete white rounded base down to y=936)
p1 = Image.open('images/purifier-pearl-wholesome.png').convert('RGBA')

# Model 2: Grand IoT (complete rounded body and full copper tap nozzle, no phone)
p2 = Image.open('images/purifier-grand-wholesome.png').convert('RGBA')

# Model 3: Grand Star (complete body, left curve, and full chrome/blue tap nozzle down to y=954)
p3 = Image.open('images/purifier-star-wholesome.png').convert('RGBA')

# Model 4: Supreme Plus Neo (complete body, water glass, and silver drip tray down to y=938)
p4 = Image.open('images/purifier-supreme-wholesome.png').convert('RGBA')

TARGET_H = 280
purifiers = [
    ('Pearl IoT', p1),
    ('Grand IoT', p2),
    ('Grand Star', p3),
    ('Supreme Plus Neo', p4)
]

scaled_purifiers = []
for name, im in purifiers:
    aspect = im.width / float(im.height)
    w = int(TARGET_H * aspect)
    res = im.resize((w, TARGET_H), Image.Resampling.LANCZOS)
    scaled_purifiers.append((name, res, w))

total_models_w = sum(w for _, _, w in scaled_purifiers)
start_x = 445
available_span = 1335 - start_x
remaining_gap_total = available_span - total_models_w
gap = remaining_gap_total // 3

# Floor horizon in bg is at ~415; purifiers grounded cleanly at base_y = 440
base_y = 440
py = base_y - TARGET_H  # 160px headroom above machines

# 3. Soft Realistic Contact Shadow Layer on Floor
shadow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)

def add_contact_shadow(cx, b_y, rx, ry, opacity=120):
    for i in range(5):
        f = 1.0 - (i / 5.0)
        shadow_draw.ellipse([cx - rx*0.75, b_y - 2 - i, cx + rx*0.75, b_y + 2 + i], fill=(35, 30, 25, int(opacity * 0.45 * f)))
    for i in range(14):
        factor = 1.0 - (i / 14.0)
        cur_rx = int(rx * (1.0 + i * 0.14))
        cur_ry = int(ry * (1.0 + i * 0.14))
        alpha = int(opacity * factor * 0.28)
        shadow_draw.ellipse(
            [cx - cur_rx, b_y - cur_ry, cx + cur_rx, b_y + cur_ry],
            fill=(45, 40, 35, alpha)
        )

cur_x = start_x
for name, res_im, w in scaled_purifiers:
    cx = cur_x + w // 2
    add_contact_shadow(cx, base_y - 4, int(w * 0.44), 14, opacity=120)
    shadow_layer.paste(res_im, (cur_x, py), res_im)
    print(f"{name:18s} placed at x=({cur_x:4d}, {cur_x+w:4d}), y=({py:3d}, {py+TARGET_H:3d})")
    cur_x += w + gap

banner = Image.alpha_composite(bg, shadow_layer).convert('RGB')
draw = ImageDraw.Draw(banner)

# 4. Left Typography Lockup: Brand + Website Burgundy/Gold Color Theme Tagline (NO FULL STOPS)
LEFT_X = 42
font_bold = r'C:\Windows\Fonts\segoeuib.ttf'
font_arial_bold = r'C:\Windows\Fonts\arialbd.ttf'

font_logo_big = ImageFont.truetype(font_arial_bold, 54)
font_logo_reg = ImageFont.truetype(font_arial_bold, 22)
font_tag = ImageFont.truetype(font_bold, 14)

# Logo Lockup: KENT® + HOUSE OF PURITY (matching 0.2cm gap, NO RED DOT)
draw.text((LEFT_X, 48), 'KENT', font=font_logo_big, fill=(15, 45, 95))
draw.text((LEFT_X + 152, 50), '®', font=font_logo_reg, fill=(40, 40, 40))
draw.text((LEFT_X + 2, 94), 'HOUSE OF PURITY', font=font_tag, fill=(130, 130, 135))

# 5. TAGLINE IN DM SERIF DISPLAY (NO FULL STOPS) WITH WEBSITE BURGUNDY & GOLD COLOR THEME
font_dm_path = 'fonts/DMSerifDisplay-Regular.ttf' if os.path.exists('fonts/DMSerifDisplay-Regular.ttf') else 'DMSerifDisplay-Regular.ttf'
f_tagline = ImageFont.truetype(font_dm_path, 42)

text1 = "Mineral Technology"
text2 = "Pure Hydration"

# Line 1: Crisp Dark Charcoal/Black #0A0A0A (NO FULL STOP)
draw.text((LEFT_X, 150), text1, font=f_tagline, fill=(10, 10, 10))

# Line 2: Precision Multi-Stop Gradient matching Website Color Palette:
# Regal Burgundy (#800020) -> Ruby Wine (#A81941) -> Velvet Rose (#C04B64) -> Warm Luxury Gold (#B98C50)
dummy = Image.new('RGBA', (1, 1))
d = ImageDraw.Draw(dummy)
b2 = d.textbbox((0, 0), text2, font=f_tagline)
w2 = b2[2] - b2[0]
h2 = b2[3] - b2[1]

gradient_img = Image.new('RGB', (w2 + 4, h2 + 4))
grad_draw = ImageDraw.Draw(gradient_img)

stops = [
    (0.0, (128, 0, 32)),      # Signature Burgundy (#800020)
    (0.40, (168, 25, 65)),    # Rich Ruby Wine (#A81941)
    (0.72, (192, 75, 100)),   # Velvet Rose (#C04B64)
    (1.0, (185, 140, 80))     # Warm Luxury Gold (#B98C50)
]

for x in range(w2 + 4):
    t = x / float(w2 + 4)
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i+1][0]:
            factor = (t - stops[i][0]) / (stops[i+1][0] - stops[i][0])
            c0, c1 = stops[i][1], stops[i+1][1]
            break
    r = int(c0[0] + factor * (c1[0] - c0[0]))
    g = int(c0[1] + factor * (c1[1] - c0[1]))
    b = int(c0[2] + factor * (c1[2] - c0[2]))
    grad_draw.line([(x, 0), (x, h2 + 4)], fill=(r, g, b))

mask = Image.new('L', (w2 + 4, h2 + 4), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.text((2 - b2[0], 2 - b2[1]), text2, font=f_tagline, fill=255)

line2_composite = Image.new('RGBA', (w2 + 4, h2 + 4), (0, 0, 0, 0))
line2_composite.paste(gradient_img, (0, 0), mask)

# Paste line 2 at y=204 (NO FULL STOP)
banner.paste(line2_composite, (LEFT_X + b2[0] - 2, 204 + b2[1] - 2), mask)

# Subtitle / Add-on
font_sub = ImageFont.truetype(font_bold, 14)
draw = ImageDraw.Draw(banner)
draw.text((LEFT_X + 2, 292), '100% PURE WATER • MINERAL RO™', font=font_sub, fill=(115, 115, 120))

# Features and vertical divider lines (trust badges)
badges_file = 'delicate_burgundy_badges.png'
if os.path.exists(badges_file):
    b_img = Image.open(badges_file)
    banner.paste(b_img, (LEFT_X, 366), b_img)

# 6. Smooth feathering into pure white #FFFFFF at top and bottom
# Top 12px soft blend to pure white (255, 255, 255):
white_target = (255, 255, 255)
for y in range(12):
    alpha = (12 - y) / 14.0
    for x in range(WIDTH):
        cur = banner.getpixel((x, y))
        blended = (
            int(cur[0] * (1 - alpha) + white_target[0] * alpha),
            int(cur[1] * (1 - alpha) + white_target[1] * alpha),
            int(cur[2] * (1 - alpha) + white_target[2] * alpha)
        )
        banner.putpixel((x, y), blended)

# Bottom 40px soft blend into pure white (255, 255, 255):
for y in range(HEIGHT - 40, HEIGHT):
    alpha = (y - (HEIGHT - 40)) / 40.0
    for x in range(WIDTH):
        cur = banner.getpixel((x, y))
        blended = (
            int(cur[0] * (1 - alpha) + white_target[0] * alpha),
            int(cur[1] * (1 - alpha) + white_target[1] * alpha),
            int(cur[2] * (1 - alpha) + white_target[2] * alpha)
        )
        banner.putpixel((x, y), blended)

# Save final banner
output_path = os.path.join('images', 'kent-purifiers-banner.webp')
banner.save(output_path, 'WEBP', quality=95)
print(f"Successfully generated {output_path}! File size: {os.path.getsize(output_path)} bytes")
