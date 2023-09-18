import textwrap
from PIL import Image, ImageDraw, ImageFont
from HtmlToImage.html_to_image import tirar_print 

def create_card(name, age):
    # Create a blank image
    img = Image.new('RGB', (500, 500), color=(36, 145, 199))

    # create a draw object based on the image
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font=r"arial.ttf", size=50)
    
    # wraps the text so it doesn't go out of the image, returns a list of strings
    texts = textwrap.wrap(f"Name/Nome: {name}", width=25)

    y_text = -100
    for text in texts:
        _, _, w, h = draw.textbbox((0, 0), text, font = font)
        y_position = (img.height-h)/2 + y_text
        draw.text(( (img.width-w)/2 , y_position ), text, font=font, fill=(255, 255, 0))
        y_text += 30

    y_text += 60
    texts = textwrap.wrap(f"Age/Idade: {age}", width=25)
    for text in texts:
        _, _, w, h = draw.textbbox((0, 0), text, font = font)
        y_position = (img.height-h)/2 + y_text
        draw.text(( (img.width-w)/2 , y_position ), text, font=font)
        y_text += 30

    return img

def create_html_card(name, age):
    with open("./baseCard.html", "r", encoding='utf8') as file:
        string_html = str(file.read())
        string_html = string_html.replace("{{nome}}", name)
        string_html = string_html.replace("{{idade}}", age)
        return tirar_print(string_html)

#create_card("Arthur", "20").show()
