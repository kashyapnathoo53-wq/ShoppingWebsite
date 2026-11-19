import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1376
HEIGHT = 545

# 1. Background plate with clean travertine floor and realistic mid-air water arc
# "And don't change the background." - Keep the exact approved background plate!
plate_path = r'C:\Users\ADMIN\.gemini\antigravity\brain\c228a748-d79c-4230-b18c-69a39bc2446e\purifier_background_plate_flat_floor_1795120218808.jpg'
bg_raw = Image.open(plate_path).convert('RGB')
bg = bg_raw.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert('RGBA')

# 2. Both RO Machines from the user's second image (100% WHOLESOME, UNTRUNCATED)
# Machine 1: Pearl IoT (white)
# Machine 2: Grand IoT (black)
# Both machines match the user's reference image exactly, with complete rounded bases, feet, and nozzles.
pair_path = os.path.join('images', 'both_ro_pair.png')
pair = Image.open(pair_path).convert('RGBA')

# Scale pair to prominent hero size
TARGET_H = 355
aspect = pair.width / float(pair.height)
pair_w = int(TARGET_H * aspect)
scaled_pair = pair.resize((pair_w, TARGET_H), Image.Resampling.LANCZOS)

# Position pair on the right side, framed by the sweeping liquid water arc
start_x = 720
base_y = 445
py = base_y - TARGET_H  # headroom above machines = 90px

# 3. Soft Realistic Contact Shadow Layer on Travertine Floor
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

# In scaled pair: Pearl center is at ~0.26 * pair_w, Grand center is at ~0.74 * pair_w
cx_pearl = start_x + int(pair_w * 0.26)
cx_grand = start_x + int(pair_w * 0.74)
add_contact_shadow(cx_pearl, base_y - 4, int(pair_w * 0.22), 14, opacity=120)
add_contact_shadow(cx_grand, base_y - 4, int(pair_w * 0.20), 14, opacity=120)

shadow_layer.paste(scaled_pair, (start_x, py), scaled_pair)
print(f"Both RO machines placed at x=({start_x}, {start_x+pair_w}), y=({py}, {py+TARGET_H})")

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

# Save final banner
output_path = os.path.join('images', 'kent-purifiers-banner.webp')
banner.save(output_path, 'WEBP', quality=95)
print(f"Successfully generated {output_path}! File size: {os.path.getsize(output_path)} bytes")
