from HtmlToImage.html_to_image import tirar_print

nome = "Arthur Rogado Reis"
idade = "20"

with open("./baseCard.html", "r", encoding='utf8') as file:
    string = str(file.read())
    string = string.replace("{{nome}}", nome)
    string = string.replace("{{idade}}", idade)

    html = string

img = tirar_print(html, size=(500, 500))
img.show()