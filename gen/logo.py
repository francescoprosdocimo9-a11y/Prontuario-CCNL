import sys
from PIL import Image

src, outdir = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
w, h = im.size
px = im.load()
out = Image.new("RGBA", (w, h))
op = out.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        a = 255 - min(r, g, b)  # distance from white
        if a < 8:
            op[x, y] = (0, 0, 0, 0)
            continue
        af = a / 255.0
        # un-premultiply against white
        ur = max(0, min(255, round((r - 255 * (1 - af)) / af)))
        ug = max(0, min(255, round((g - 255 * (1 - af)) / af)))
        ub = max(0, min(255, round((b - 255 * (1 - af)) / af)))
        op[x, y] = (ur, ug, ub, a)
bbox = out.getbbox()
out = out.crop(bbox)
H = 120
W = round(out.width * H / out.height)
light = out.resize((W, H), Image.LANCZOS)
light.save(outdir + "/logo2-light.png", optimize=True)

dark = light.copy()
dp = dark.load()
for y in range(dark.height):
    for x in range(dark.width):
        r, g, b, a = dp[x, y]
        if a == 0:
            continue
        if r - max(g, b) > 40:  # red part -> brighter red
            dp[x, y] = (min(255, int(r * 1.0 + 90)), min(255, g + 70), min(255, b + 62), a)
        else:  # black/grey part -> light
            dp[x, y] = (236, 236, 236, a)
dark.save(outdir + "/logo2-dark.png", optimize=True)
print(bbox, light.size)
