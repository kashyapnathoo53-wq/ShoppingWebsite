import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1376
HEIGHT = 545  # Decreased from lower area by 0.5 cm (~19px from 564)

# 1. Base Studio Lighting Gradient (Smooth luxury studio background matching Frootle 1:1)
banner = Image.new('RGB', (WIDTH, HEIGHT), (247, 246, 243))
draw = ImageDraw.Draw(banner)

# Smooth top-to-bottom studio lighting gradient (seamless floor, NO harsh cut lines)
for y in range(HEIGHT):
    t = y / float(HEIGHT)
    r = int(248 - 8 * t)
    g = int(247 - 9 * t)
    b = int(245 - 9 * t)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# 2. Extract 4 Clean Purifiers (100% Crisp, NO Smartphone)
# Model 1: Pearl IoT (white tabletop model with copper tap)
p_pearl = Image.open('images/kent-pearl-left.webp').convert('RGBA')
p1_clean = p_pearl.crop((170, 61, 829, 932))

# Model 2: Grand IoT (black model with copper tap & IoT display; x >= 111 excludes phone!)
p_grand = Image.open('p_grand.png').convert('RGBA')
p_grand_no_phone = p_grand.crop((111, 0, p_grand.width, p_grand.height))
p2_clean = p_grand_no_phone.crop((0, 9, 259, 387))

# Model 3: Grand Star (white wall-mount model with blue indicators and chrome/blue taps)
p_star = Image.open('p_grandstar.webp').convert('RGBA')
p3_clean = p_star.crop((315, 70, 923, 938))

# Model 4: Supreme Plus Neo (black model with glass dispenser and warranty badge)
p_sup = Image.open('p_supreme.webp').convert('RGBA')
p4_clean = p_sup.crop((311, 60, 916, 933))

# Scale and position all 4 purifiers proportionally with comfortable frame margins
TARGET_H = 295
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
available_span = 1335 - start_x  # generous margin from right border (1376)
remaining_gap_total = available_span - total_models_w
gap = remaining_gap_total // 3

# Exact vertical middle placement for all 4 machines within their line height
py = (HEIGHT - TARGET_H) // 2  # exactly 134px (equal 134px headroom & 135px floor space)
base_y = py + TARGET_H         # exactly 429px

# Soft contact shadow layer
shadow_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)

def add_contact_shadow(cx, b_y, rx, ry, opacity=110):
    for i in range(12):
        factor = 1.0 - (i / 12.0)
        cur_rx = int(rx * (1.0 + i * 0.12))
        cur_ry = int(ry * (1.0 + i * 0.12))
        alpha = int(opacity * factor * 0.28)
        shadow_draw.ellipse(
            [cx - cur_rx, b_y - cur_ry, cx + cur_rx, b_y + cur_ry],
            fill=(25, 25, 28, alpha)
        )

cur_x = start_x
for name, res_im, w in scaled_purifiers:
    cx = cur_x + w // 2
    add_contact_shadow(cx, base_y - 4, int(w * 0.44), 14, opacity=110)
    shadow_layer.paste(res_im, (cur_x, py), res_im)
    print(f"{name:18s} placed at x=({cur_x:4d}, {cur_x+w:4d}), y=({py:3d}, {py+TARGET_H:3d})")
    cur_x += w + gap

# Composite shadow layer onto banner
banner = Image.alpha_composite(banner.convert('RGBA'), shadow_layer).convert('RGB')
draw = ImageDraw.Draw(banner)

# 3. Left Typography Lockup - strictly left-aligned at LEFT_X = 42 like Frootle
LEFT_X = 42
font_bold = r'C:\Windows\Fonts\segoeuib.ttf'
font_arial_bold = r'C:\Windows\Fonts\arialbd.ttf'

font_logo_big = ImageFont.truetype(font_arial_bold, 54)
font_logo_reg = ImageFont.truetype(font_arial_bold, 22)
font_tag = ImageFont.truetype(font_bold, 14)
font_title = ImageFont.truetype(font_bold, 38)
font_accent = ImageFont.truetype(font_bold, 46)
font_sub = ImageFont.truetype(font_bold, 14)

# Logo Lockup: KENT® + HOUSE OF PURITY (NO RED DOT)
draw.text((LEFT_X, 50), 'KENT', font=font_logo_big, fill=(15, 45, 95))
draw.text((LEFT_X + 152, 52), '®', font=font_logo_reg, fill=(40, 40, 40))
draw.text((LEFT_X + 2, 94), 'HOUSE OF PURITY', font=font_tag, fill=(130, 130, 135))

# Taglines: Mineral Technology + Pure Hydration
draw.text((LEFT_X, 162), 'Mineral Technology', font=font_title, fill=(38, 38, 38))
draw.text((LEFT_X, 204), 'Pure Hydration', font=font_accent, fill=(175, 143, 94))

# Subtitle / Add-on
draw.text((LEFT_X + 2, 292), '100% PURE WATER • MINERAL RO™', font=font_sub, fill=(115, 115, 120))

# Features and vertical divider lines (aligned in frame like Frootle)
badges_file = 'delicate_burgundy_badges.png'
if os.path.exists(badges_file):
    b_img = Image.open(badges_file)
    banner.paste(b_img, (LEFT_X, 366), b_img)

# Save final banner
output_path = os.path.join('images', 'kent-purifiers-banner.webp')
banner.save(output_path, 'WEBP', quality=95)
print(f"Successfully generated {output_path}! File size: {os.path.getsize(output_path)} bytes")
