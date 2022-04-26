import math
from PIL import Image, ImageDraw, ImageFont

from radar_gen import radar_gen 
from utils import ReduceOpacity

## Load raider assets

class Attr_map():

  def __init__(self, spread, ab_score, ability, ability_desc, description, titan_strain):
    self.spread = spread
    self.ab_score = ab_score
    self.ability = ability
    self.ability_desc = ability_desc
    self.description = description
    self.titan_strain = titan_strain

  def get_overall(self):
    return math.floor(sum(self.spread.values()) / len(self.spread.values()))
    

ATTR_MAP = Attr_map(spread = {
  "A": 5,
  "C": 3,
  "R": 2,
  "P": 4,
  "S": 4,
  "M": 2,
  }, ab_score = 2, ability = "Self-Repair", 
  ability_desc = "This raider can repair minor damage to self over time",
  description = "Julian the Janitor, known as such because of his affinity to clean a place out while robbing it. In all his multiversal forms, his greed is constant. Just to be more irritating, he can fix himself.",
  titan_strain = None)

print(ATTR_MAP.get_overall())
print(ATTR_MAP.spread)

radar_gen()

raider_img = Image.open('raiders/001.png')

## set background 

im = Image.new('RGB', (2000, 3000), (10, 10, 10))
draw =  ImageDraw.Draw(im, 'RGBA')

## draw type based sub-background (brocaded type logo)

logo = Image.open('images/synthetic.png')

logo = logo.resize((round(logo.size[0]*0.5), round(logo.size[1]*0.5)))

logo = ReduceOpacity(logo, 0.2)

img_w, img_h = logo.size
bg_w, bg_h = im.size

for i in range(0,5):
  for j in range(0,6):
    if j%2 == 0:
      offset = ((img_w*i), (img_h*j))
      im.paste(logo, offset, logo)
    else:
      delta = math.floor(img_w/2)
      offset = ((img_w*i - delta), (img_h*j))
      im.paste(logo, offset, logo)

## fit frame if needed

frame = Image.new("RGBA", (2000,3000), (255,215,0))

im = im.resize((round(im.size[0]*0.99), round(im.size[1]*0.995)))

img_w, img_h = im.size
bg_w, bg_h = frame.size

offset = ((bg_w - img_w) // 2, math.floor((bg_h - img_h) // 2))

frame.paste(im, offset)

im = frame

draw =  ImageDraw.Draw(im, 'RGBA')


## paste raider on background and sub-background

img_w, img_h = raider_img.size
bg_w, bg_h = im.size
offset = ((bg_w - img_w) // 2, math.floor((bg_h - img_h) // 2.5))

im.paste(raider_img, offset, raider_img)

## Adding title text

title_font = ImageFont.truetype('fonts/Syncopate-Bold.ttf', 180)
subtitle_font = ImageFont.truetype('fonts/Megrim-Regular.ttf', 120)

draw.text((1050,50), "Julian", font=title_font, fill=(255, 255, 255))
draw.text((1250,220), "The Janitor", font=subtitle_font, full=(255,255,255))

## TEXT UNDERLINE

draw.line([(1000, 380), (img_w, 400)], fill='white', width=5)

## Adding final logo

final_logo = Image.open('images/synthetic.png')

final_logo = final_logo.resize((round(final_logo.size[0]*0.4), round(final_logo.size[1]*0.4)))

img_w, img_h = final_logo.size
bg_w, bg_h = im.size

offset = ((50), (50))
im.paste(final_logo, offset, final_logo)

## Adding stats


### RADAR STATS

radar = Image.open('images/radar_1_1.png')

img_w, img_h = radar.size
offset = (math.floor(bg_w - (2*img_w)), (bg_h - img_h))

im.paste(radar, offset, radar)

im.show()