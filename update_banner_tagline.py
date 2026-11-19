import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1376
HEIGHT = 545

# 1. Base Architectural Surface: Warm alabaster wall to grounded travertine floor
banner = Image.new('RGB', (WIDTH, HEIGHT), (248, 247, 243))
draw = ImageDraw.Draw(banner)

FLOOR_Y = 413

# Draw Wall gradient (soft alabaster #F9F8F5 -> #ECE8E1)
for y in range(FLOOR_Y):
    t = y / float(FLOOR_Y)
    r = int(249 - 13 * (t ** 1.2))
    g = int(248 - 16 * (t ** 1.2))
    b = int(245 - 20 * (t ** 1.2))
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Draw Floor gradient (grounded travertine/limestone plane #E7E2DA -> #DAD4C7)
for y in range(FLOOR_Y, HEIGHT):
    t = (y - FLOOR_Y) / float(HEIGHT - FLOOR_Y)
    r = int(231 - 13 * t)
    g = int(226 - 14 * t)
    b = int(218 - 19 * t)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Floor horizon line with soft ambient contact occlusion
draw.line([(0, FLOOR_Y), (WIDTH, FLOOR_Y)], fill=(215, 208, 196))
draw.line([(0, FLOOR_Y + 1), (WIDTH, FLOOR_Y + 1)], fill=(245, 242, 236))

# 2. Water Caustics Layer (10-12% soft sun-refracted light web across upper/mid wall)
caustic_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
caustic_draw = ImageDraw.Draw(caustic_layer)

import random
random.seed(42)

for _ in range(35):
    cx = random.randint(300, WIDTH - 50)
    cy = random.randint(30, FLOOR_Y - 40)
    rx = random.randint(45, 110)
    ry = random.randint(25, 65)
    
    points = []
    num_pts = random.randint(5, 8)
    for i in range(num_pts):
        angle = (i / float(num_pts)) * 2 * math.pi
        rad = rx if i % 2 == 0 else ry
        rad += random.randint(-8, 8)
        px = cx + int(rad * math.cos(angle))
        py = cy + int(rad * 0.65 * math.sin(angle))
        points.append((px, py))
    
    caustic_draw.polygon(points, fill=(255, 255, 255, random.randint(8, 18)))
    caustic_draw.line(points + [points[0]], fill=(225, 245, 255, random.randint(18, 38)), width=random.randint(2, 4))

caustic_layer = caustic_layer.filter(ImageFilter.GaussianBlur(16))
banner = Image.alpha_composite(banner.convert('RGBA'), caustic_layer).convert('RGB')

# 3. Sculptural Water Arc Ribbon (Positioned in the background layer BEHIND the RO machines)
water_arc_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
arc_draw = ImageDraw.Draw(water_arc_layer)

arc_draw.ellipse([580, 80, 1320, 420], fill=(56, 189, 248, 16))
arc_draw.ellipse([700, 100, 1260, 380], fill=(186, 230, 253, 24))

def bezier_curve(p0, p1, p2, p3, steps=120):
    pts = []
    for i in range(steps + 1):
        t = i / float(steps)
        u = 1 - t
        x = (u**3)*p0[0] + 3*(u**2)*t*p1[0] + 3*u*(t**2)*p2[0] + (t**3)*p3[0]
        y = (u**3)*p0[1] + 3*(u**2)*t*p1[1] + 3*u*(t**2)*p2[1] + (t**3)*p3[1]
        pts.append((int(x), int(y)))
    return pts

lower_pts = bezier_curve((420, 420), (620, 280), (840, 110), (1330, 260))
upper_pts = bezier_curve((460, 410), (640, 220), (860, 80), (1345, 240))

ribbon_poly = lower_pts + upper_pts[::-1]
arc_draw.polygon(ribbon_poly, fill=(186, 230, 253, 75))

lower_core = bezier_curve((440, 415), (630, 255), (850, 100), (1335, 252))
upper_core = bezier_curve((455, 412), (638, 235), (858, 90), (1340, 246))
arc_draw.polygon(lower_core + upper_core[::-1], fill=(240, 249, 255, 110))

for i in range(len(upper_pts) - 1):
    t = i / float(len(upper_pts))
    alpha = int(220 * math.sin(t * math.pi))
    arc_draw.line([upper_pts[i], upper_pts[i+1]], fill=(255, 255, 255, alpha), width=3)

for i in range(len(lower_pts) - 1):
    t = i / float(len(lower_pts))
    alpha = int(140 * math.sin(t * math.pi))
    arc_draw.line([lower_pts[i], lower_pts[i+1]], fill=(125, 211, 252, alpha), width=2)

drops = [
    (790, 85, 4), (825, 78, 5.5), (870, 72, 6), (915, 76, 5), (960, 90, 4.5),
    (1010, 112, 5), (1060, 140, 4), (1110, 172, 5.5), (1165, 205, 4.5),
    (740, 115, 3.5), (710, 135, 3), (850, 60, 3.5), (940, 68, 3)
]

for dx, dy, dr in drops:
    arc_draw.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=(186, 230, 253, 140))
    arc_draw.ellipse([dx - dr*0.5, dy - dr*0.5, dx, dy], fill=(255, 255, 255, 230))

water_arc_blurred = water_arc_layer.filter(ImageFilter.GaussianBlur(3))
water_arc_composite = Image.alpha_composite(water_arc_blurred, water_arc_layer)
banner = Image.alpha_composite(banner.convert('RGBA'), water_arc_composite).convert('RGB')

# 4. Extract & Place the 4 UNTOUCHED KENT RO Purifier Machines
p_pearl = Image.open('images/kent-pearl-left.webp').convert('RGBA')
p1_clean = p_pearl.crop((170, 61, 829, 932))

p_grand = Image.open('p_grand.png').convert('RGBA')
p_grand_no_phone = p_grand.crop((111, 0, p_grand.width, p_grand.height))
p2_clean = p_grand_no_phone.crop((0, 9, 259, 387))

p_star = Image.open('p_grandstar.webp').convert('RGBA')
p3_clean = p_star.crop((315, 70, 923, 938))

p_sup = Image.open('p_supreme.webp').convert('RGBA')
p4_clean = p_sup.crop((311, 60, 916, 933))

# Height 280 with py=135 guarantees 135px headroom above machines (no cropping)
TARGET_H = 280
purifiers = [
    ('Pearl IoT', p1_clean),
    ('Grand IoT', p2_clean),
    ('Grand Star', p3_clean),
    ('Supreme Plus Neo', p4_clean)
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

py = 135
base_y = py + TARGET_H  # 415px

# 5. Soft Contact Shadow Layer on the Travertine Floor
shadow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)

def add_contact_shadow(cx, b_y, rx, ry, opacity=115):
    for i in range(5):
        f = 1.0 - (i / 5.0)
        shadow_draw.ellipse([cx - rx*0.75, b_y - 2 - i, cx + rx*0.75, b_y + 2 + i], fill=(30, 25, 20, int(opacity * 0.45 * f)))
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
    add_contact_shadow(cx, base_y - 4, int(w * 0.44), 14, opacity=115)
    shadow_layer.paste(res_im, (cur_x, py), res_im)
    print(f"{name:18s} placed at x=({cur_x:4d}, {cur_x+w:4d}), y=({py:3d}, {py+TARGET_H:3d})")
    cur_x += w + gap

banner = Image.alpha_composite(banner.convert('RGBA'), shadow_layer).convert('RGB')
draw = ImageDraw.Draw(banner)

# 6. Left Typography Lockup: Brand + Website Burgundy/Gold Color Theme Tagline
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

# 7. TAGLINE IN DM SERIF DISPLAY WITH WEBSITE BURGUNDY & GOLD COLOR THEME
font_dm_path = 'fonts/DMSerifDisplay-Regular.ttf' if os.path.exists('fonts/DMSerifDisplay-Regular.ttf') else 'DMSerifDisplay-Regular.ttf'
f_tagline = ImageFont.truetype(font_dm_path, 42)

text1 = "Mineral Technology."
text2 = "Pure Hydration."

# Line 1: Crisp Dark Charcoal/Black #0A0A0A (matching reference line 1 contrast)
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

# Paste line 2 at y=204
banner.paste(line2_composite, (LEFT_X + b2[0] - 2, 204 + b2[1] - 2), mask)

# Subtitle / Add-on
font_sub = ImageFont.truetype(font_bold, 14)
draw = ImageDraw.Draw(banner)
draw.text((LEFT_X + 2, 292), '100% PURE WATER • MINERAL RO™', font=font_sub, fill=(115, 115, 120))

# Features and vertical divider lines
badges_file = 'delicate_burgundy_badges.png'
if os.path.exists(badges_file):
    b_img = Image.open(badges_file)
    banner.paste(b_img, (LEFT_X, 366), b_img)

# Save final banner
output_path = os.path.join('images', 'kent-purifiers-banner.webp')
banner.save(output_path, 'WEBP', quality=95)
print(f"Successfully generated {output_path}! File size: {os.path.getsize(output_path)} bytes")
