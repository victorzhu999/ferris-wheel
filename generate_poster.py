from PIL import Image, ImageDraw, ImageFont
import qrcode

QR1_DATA = "https://victorzhu999.github.io/ferris-wheel/research.html"
QR2_DATA = "https://victorzhu999.github.io/ferris-wheel/teacher.html"
QR1_LABEL = "摩天轮实验探究"
QR2_LABEL = "答题教师统计"
TITLE = "摩天轮互动课堂"
OUTPUT = "poster.png"

W = 800
H = 1600
QR = 320

def gradient_bg(w, h, c1, c2):
    im = Image.new('RGB', (w, h), c1)
    px = im.load()
    for y in range(h):
        r = int(c1[0] + (c2[0]-c1[0])*y/h)
        g = int(c1[1] + (c2[1]-c1[1])*y/h)
        b = int(c1[2] + (c2[2]-c1[2])*y/h)
        for x in range(w):
            px[x,y] = (r,g,b)
    return im

def make_qr(data):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert('L')

def get_font(sz):
    for p in ["C:/Windows/Fonts/msyh.ttc","C:/Windows/Fonts/simhei.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except:
            pass
    return ImageFont.load_default()

def gen():
    poster = gradient_bg(W, H, (12,25,55), (40,12,58))
    poster = poster.convert('RGBA')
    draw = ImageDraw.Draw(poster)

    # Decorative dots
    import random; random.seed(42)
    for _ in range(60):
        x,y = random.randint(0,W), random.randint(0,H)
        r = random.randint(2,5)
        a = random.randint(50,150)
        c = random.choice([(255,255,200, a),(200,255,255, a),(255,200,255, a)])
        draw.ellipse([x-r,y-r,x+r,y+r], fill=c)

    tf = get_font(55)
    lf = get_font(28)
    hf = get_font(22)
    sf = get_font(26)

    # Title
    t = TITLE
    tb = draw.textbbox((0,0), t, font=tf)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    tx, ty = (W-tw)//2, 60
    for o in [6,3,1]:
        draw.text((tx,ty-o), t, font=tf, fill=(255,180,100, 80-o*20))
    draw.text((tx,ty), t, font=tf, fill=(255,225,120))

    # Sub
    s = "扫码参与互动"
    sb = draw.textbbox((0,0), s, font=sf)
    draw.text(((W-(sb[2]-sb[0]))//2, ty+th+20), s, font=sf, fill=(160,180,210))

    # Divider
    dy = ty+th+70
    draw.line([(W//2-100, dy), (W//2+100, dy)], fill=(255,255,150, 80), width=2)

    # QR items
    items = [(make_qr(QR1_DATA), QR1_LABEL, (80,160,255)), (make_qr(QR2_DATA), QR2_LABEL, (255,130,80))]
    y = dy + 60

    for qr_img, label, fc in items:
        # Card: rounded rect bg
        cw, ch = QR + 30, QR + 130
        card = Image.new('RGBA', (cw, ch), (0,0,0,0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0,0,cw,ch], radius=14, fill=(28,35,60,210))
        cd.rounded_rectangle([2,2,cw-2,ch-2], radius=12, outline=fc+(70,))
        poster.paste(card, ((W-cw)//2, y), card)

        # White frame for QR
        fx, fy = (W-cw)//2 + 15, y + 15
        frame = Image.new('RGBA', (QR, QR), (255,255,255,255))
        fd = ImageDraw.Draw(frame)
        fd.rectangle([0,0,QR,QR], fill=(255,255,255,255))
        poster.paste(frame, (fx, fy), frame)

        # Glowing border
        draw.rectangle([fx-2, fy-2, fx+QR+2, fy+QR+2], outline=fc+(50,))

        # Paste QR code (mode 'L')
        qr_r = qr_img.resize((QR, QR), Image.LANCZOS)
        qr_rgba = Image.new('RGBA', qr_r.size, (255,255,255,255))
        qr_rgba.paste(qr_r, (0,0))
        # Create alpha mask: black=opaque, white=transparent
        alpha = qr_r.point(lambda p: 255 if p < 128 else 0)
        qr_rgba.putalpha(alpha)
        poster.paste(qr_rgba, (fx, fy), qr_rgba)

        # Label
        lb = draw.textbbox((0,0), label, font=lf)
        lw = lb[2]- lb[0]
        draw.text(((W-lw)//2, fy+QR+20), label, font=lf, fill=(255,230,180))
        
        h = "扫码参与"
        hb = draw.textbbox((0,0), h, font=hf)
        draw.text(((W-(hb[2]-hb[0]))//2, fy+QR+52), h, font=hf, fill=(140,160,190))

        y += ch + 70

    # Footer
    ft = "探索科学奥秘  激发学习兴趣"
    fb = draw.textbbox((0,0), ft, font=sf)
    draw.text(((W-(fb[2]-fb[0]))//2, y+30), ft, font=sf, fill=(140,160,190))

    poster.convert('RGB').save(OUTPUT, 'PNG')
    print(f"Saved {OUTPUT}")

if __name__ == "__main__":
    gen()