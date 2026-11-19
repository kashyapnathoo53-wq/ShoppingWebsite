import os
from PIL import Image, ImageDraw, ImageFont

W = 2752
H = 1188

# 1. Warm Alabaster Wall with Dancing Water Caustics & Travertine Floor
bg_path = r'C:\Users\ADMIN\.gemini\antigravity\brain\c228a748-d79c-4230-b18c-69a39bc2446e\purifier_background_plate_flat_floor_1795120218808.jpg'
bg = Image.open(bg_path).convert('RGB').resize((W, H), Image.Resampling.LANCZOS).convert('RGBA')

# 2. Four Authentic Uncropped KENT RO Purifiers
lineup_path = os.path.join('images', 'four_ro_lineup.png')
lineup = Image.open(lineup_path).convert('RGBA')

pair_w = 1500
TARGET_H = int(pair_w / (lineup.width / float(lineup.height)))
scaled_lineup = lineup.resize((pair_w, TARGET_H), Image.Resampling.LANCZOS)

start_x = W - pair_w - 70
base_y = 970
py = base_y - TARGET_H

# 3. Soft Realistic Grounding Contact Shadows
shadow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)

def add_contact_shadow(cx, b_y, rx, ry, opacity=120):
    for i in range(7):
        f = 1.0 - (i / 7.0)
        shadow_draw.ellipse([cx - rx*0.75, b_y - 3 - i, cx + rx*0.75, b_y + 3 + i], fill=(30, 25, 20, int(opacity * 0.5 * f)))
    for i in range(16):
        factor = 1.0 - (i / 16.0)
        cur_rx = int(rx * (1.0 + i * 0.12))
        cur_ry = int(ry * (1.0 + i * 0.12))
        alpha = int(opacity * factor * 0.28)
        shadow_draw.ellipse(
            [cx - cur_rx, b_y - cur_ry, cx + cur_rx, b_y + cur_ry],
            fill=(45, 40, 35, alpha)
        )

centers_rel = [0.1347, 0.3945, 0.6434, 0.8796]
rx = int(pair_w * 0.105)

for c_rel in centers_rel:
    cx = start_x + int(pair_w * c_rel)
    add_contact_shadow(cx, base_y - 6, rx, 18, opacity=120)

shadow_layer.paste(scaled_lineup, (start_x, py), scaled_lineup)
banner = Image.alpha_composite(bg, shadow_layer).convert('RGB')
draw = ImageDraw.Draw(banner)

# 4. Typography Layout (Replicating image_1.png Editorial Layout in UHD)
font_dm = 'fonts/DMSerifDisplay-Regular.ttf'
font_pjs_bold = 'fonts/PlusJakartaSans-Bold.ttf'
font_pjs_med = 'fonts/PlusJakartaSans-Medium.ttf'
font_pjs_reg = 'fonts/PlusJakartaSans-Regular.ttf'

f_eyebrow = ImageFont.truetype(font_pjs_bold, 28)
f_h1 = ImageFont.truetype(font_dm, 108)
f_body = ImageFont.truetype(font_pjs_reg, 31)
f_metric_val = ImageFont.truetype(font_pjs_bold, 54)
f_metric_lbl = ImageFont.truetype(font_pjs_med, 25)

LEFT_X = 90

# Eyebrow in brushed champagne gold (#B59E52)
eye_text = '★  THE GOLD STANDARD OF PURITY'
draw.text((LEFT_X, 235), eye_text, font=f_eyebrow, fill=(181, 158, 82))
b_eye = draw.textbbox((LEFT_X, 235), eye_text, font=f_eyebrow)
draw.line([(b_eye[2] + 24, 250), (b_eye[2] + 130, 250)], fill=(181, 158, 82), width=3)

# Headline Line 1: Purified Water.
draw.text((LEFT_X, 290), 'Purified Water.', font=f_h1, fill=(15, 30, 40))

# Headline Line 2: Essential Purity. (Burgundy-to-Gold gradient)
text2 = 'Essential Purity.'
dummy = Image.new('RGBA', (1, 1))
d = ImageDraw.Draw(dummy)
b2 = d.textbbox((0, 0), text2, font=f_h1)
w2 = b2[2] - b2[0]
h2 = b2[3] - b2[1]

gradient_img = Image.new('RGB', (w2 + 8, h2 + 8))
grad_draw = ImageDraw.Draw(gradient_img)

stops = [
    (0.0, (128, 0, 32)),      # Signature Burgundy (#800020)
    (0.38, (168, 25, 65)),    # Ruby Wine (#A81941)
    (0.70, (192, 75, 100)),   # Velvet Rose (#C04B64)
    (1.0, (185, 140, 80))     # Warm Luxury Gold (#B98C50)
]

for x in range(w2 + 8):
    t = x / float(w2 + 8)
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i+1][0]:
            factor = (t - stops[i][0]) / (stops[i+1][0] - stops[i][0])
            c0, c1 = stops[i][1], stops[i+1][1]
            break
    r = int(c0[0] + factor * (c1[0] - c0[0]))
    g = int(c0[1] + factor * (c1[1] - c0[1]))
    b = int(c0[2] + factor * (c1[2] - c0[2]))
    grad_draw.line([(x, 0), (x, h2 + 8)], fill=(r, g, b))

mask = Image.new('L', (w2 + 8, h2 + 8), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.text((4 - b2[0], 4 - b2[1]), text2, font=f_h1, fill=255)

line2_comp = Image.new('RGBA', (w2 + 8, h2 + 8), (0, 0, 0, 0))
line2_comp.paste(gradient_img, (0, 0), mask)
banner.paste(line2_comp, (LEFT_X + b2[0] - 4, 420 + b2[1] - 4), mask)

# Multi-line descriptive body copy
body_lines = [
    "India's most trusted water purification, perfected over 25+ years.",
    "Engineered with patented Mineral RO™ multi-stage science that eliminates",
    "100% of dissolved impurities, bacteria, and viruses while retaining vital",
    "natural calcium and magnesium."
]
draw = ImageDraw.Draw(banner)
body_y = 575
for line in body_lines:
    draw.text((LEFT_X, body_y), line, font=f_body, fill=(75, 75, 80))
    body_y += 48

# Horizontal divider line above metrics
divider_y = 795
draw.line([(LEFT_X, divider_y), (LEFT_X + 960, divider_y)], fill=(215, 210, 200), width=2)

# Three-metric row with vertical dividers
metric_y = 835
draw.text((LEFT_X, metric_y), '1 Crore+', font=f_metric_val, fill=(15, 30, 40))
draw.text((LEFT_X, metric_y + 65), 'Happy Families', font=f_metric_lbl, fill=(110, 110, 115))

draw.line([(LEFT_X + 330, metric_y + 5), (LEFT_X + 330, metric_y + 90)], fill=(215, 210, 200), width=2)

draw.text((LEFT_X + 370, metric_y), '25+ Years', font=f_metric_val, fill=(15, 30, 40))
draw.text((LEFT_X + 370, metric_y + 65), 'Purity & Trust', font=f_metric_lbl, fill=(110, 110, 115))

draw.line([(LEFT_X + 710, metric_y + 5), (LEFT_X + 710, metric_y + 90)], fill=(215, 210, 200), width=2)

draw.text((LEFT_X + 750, metric_y), '100%', font=f_metric_val, fill=(15, 30, 40))
draw.text((LEFT_X + 750, metric_y + 65), 'Retained Minerals', font=f_metric_lbl, fill=(110, 110, 115))

# Save UHD files
out_jpg = os.path.join('images', 'uhd_kent_hero_banner.jpg')
out_png = os.path.join('images', 'uhd_kent_hero_banner.png')
out_webp = os.path.join('images', 'uhd_kent_hero_banner.webp')
banner.save(out_jpg, 'JPEG', quality=98)
banner.save(out_png, 'PNG')
banner.save(out_webp, 'WEBP', quality=95)

# Generate plinth stage variant as well
bg_plinth_path = r'C:\Users\ADMIN\.gemini\antigravity\brain\c228a748-d79c-4230-b18c-69a39bc2446e\purifier_background_plate_1795120196259.jpg'
bg_plinth = Image.open(bg_plinth_path).convert('RGB').resize((W, H), Image.Resampling.LANCZOS).convert('RGBA')
shadow_layer_plinth = Image.new('RGBA', (W, H), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer_plinth)
for c_rel in centers_rel:
    cx = start_x + int(pair_w * c_rel)
    add_contact_shadow(cx, base_y - 6, rx, 18, opacity=120)
shadow_layer_plinth.paste(scaled_lineup, (start_x, py), scaled_lineup)
banner_plinth = Image.alpha_composite(bg_plinth, shadow_layer_plinth).convert('RGB')
draw_plinth = ImageDraw.Draw(banner_plinth)

# Re-apply text onto plinth variant
draw_plinth.text((LEFT_X, 235), eye_text, font=f_eyebrow, fill=(181, 158, 82))
draw_plinth.line([(b_eye[2] + 24, 250), (b_eye[2] + 130, 250)], fill=(181, 158, 82), width=3)
draw_plinth.text((LEFT_X, 290), 'Purified Water.', font=f_h1, fill=(15, 30, 40))
banner_plinth.paste(line2_comp, (LEFT_X + b2[0] - 4, 420 + b2[1] - 4), mask)
body_y = 575
for line in body_lines:
    draw_plinth.text((LEFT_X, body_y), line, font=f_body, fill=(75, 75, 80))
    body_y += 48
draw_plinth.line([(LEFT_X, divider_y), (LEFT_X + 960, divider_y)], fill=(215, 210, 200), width=2)
draw_plinth.text((LEFT_X, metric_y), '1 Crore+', font=f_metric_val, fill=(15, 30, 40))
draw_plinth.text((LEFT_X, metric_y + 65), 'Happy Families', font=f_metric_lbl, fill=(110, 110, 115))
draw_plinth.line([(LEFT_X + 330, metric_y + 5), (LEFT_X + 330, metric_y + 90)], fill=(215, 210, 200), width=2)
draw_plinth.text((LEFT_X + 370, metric_y), '25+ Years', font=f_metric_val, fill=(15, 30, 40))
draw_plinth.text((LEFT_X + 370, metric_y + 65), 'Purity & Trust', font=f_metric_lbl, fill=(110, 110, 115))
draw_plinth.line([(LEFT_X + 710, metric_y + 5), (LEFT_X + 710, metric_y + 90)], fill=(215, 210, 200), width=2)
draw_plinth.text((LEFT_X + 750, metric_y), '100%', font=f_metric_val, fill=(15, 30, 40))
draw_plinth.text((LEFT_X + 750, metric_y + 65), 'Retained Minerals', font=f_metric_lbl, fill=(110, 110, 115))

out_plinth = os.path.join('images', 'uhd_kent_hero_banner_plinth.jpg')
banner_plinth.save(out_plinth, 'JPEG', quality=98)

# Also update images/kent-purifiers-banner.webp so website displays this UHD banner immediately
site_banner = banner.resize((1376, 594), Image.Resampling.LANCZOS)
site_banner.save(os.path.join('images', 'kent-purifiers-banner.webp'), 'WEBP', quality=95)

print('UHD renders successfully generated!')
print('JPG size:', os.path.getsize(out_jpg), 'bytes')
print('PNG size:', os.path.getsize(out_png), 'bytes')
print('WEBP size:', os.path.getsize(out_webp), 'bytes')
print('Plinth JPG size:', os.path.getsize(out_plinth), 'bytes')
