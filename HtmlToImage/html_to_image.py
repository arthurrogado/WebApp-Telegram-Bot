from html2image import Html2Image
from PIL import Image
from io import BytesIO
import uuid
import os

#hti = Html2Image(size=(500, 200), browser_executable='chromedriver')

def tirar_print(html, css = "", size=(500, 500)):
    try:
        hti = Html2Image(size=size, browser='edge', output_path='temp')
    except:
        hti = Html2Image(size=size, output_path='temp')

    filename = str(uuid.uuid4())

    file = hti.screenshot(html_str=html, css_str=css, save_as=f"{filename}.png")[0]
    # file é o caminho para o arquivo

    try:
        with open(file, "rb") as f:
            img = Image.open(BytesIO(f.read()))

        os.remove(file)
        return img
    except Exception as e:
        # throw error
        print("Error. File not found. Maybe hti does not work")
        return Exception("Error. File not found. Maybe hti does not work")


if __name__ == '__main__':
    html = """<h1> An interesting title </h1> This page will be red"""
    css = "body {background: red;}"
    img = tirar_print(html, css)
    img.show()







# import asyncio
# from pyppeteer import launch
# import uuid
# from PIL import Image
# from io import BytesIO
# import os

# async def tirar_print(html, css = "", size=(500, 500)):
#     browser = await launch(headless=True)  # Inicializa o navegador headless
#     page = await browser.newPage()
#     await page.setViewport({'width': size[0], 'height': size[1]})  # Define o tamanho da página
    
#     await page.setContent(html)  # Define o conteúdo HTML da página
#     await page.addStyleTag({'content': css})  # Adiciona o CSS
    
#     # Captura a captura de tela
#     filename = str(uuid.uuid4())
#     file = await page.screenshot({'path': f'HtmlToImage/temp/{filename}.png'})

#     await browser.close()  # Fecha o navegador

#     with open(file, "rb") as f:
#         print(f)
#         img = Image.open(BytesIO(f.read()))

#     os.remove(file)
#     return img


# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(tirar_print(""" <h1> An interesting title </h1> This page will be red """, css=""" body {background: red;}"""))
