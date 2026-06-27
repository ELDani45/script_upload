""" Main script """
import re
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright
from scripts.load_cred import load_credentials


async def main(name_file:str, file_path):
    """ Abrir Zajuna """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://zajuna.sena.edu.co/")
        # await page.pause() Nos aseguramos que las n veces se cierre
        page = await load_credentials(page)


        try:
            # print("Tercer paso")
            await page.get_by_role("link", name="ANALISIS Y DESARROLLO DE SOFTWARE. (3388993)", exact=True).click()
            section = page.locator("div:has(> h3:text('Fase 1. Análisis'))").locator("#collapssesection17")
            await section.wait_for(state="visible", timeout=3500)
            extendido = await section.get_attribute("aria-expanded")
            if extendido == "true":
                print("Está extnedido")
            else:
                # print("NO está extnedido")
                await section.click()
                # print("extendido")

            # actual => actividad de proyecto 2
            act_pro_2 = page.locator("div:has(> h3:text('Actividad de proyecto 2'))").locator("#collapssesection32")
            await act_pro_2.wait_for(state="visible", timeout=5000)
            extend_act_2 = await act_pro_2.get_attribute("aria-expanded")
            if extend_act_2 == "true":
                print("Está extnedido")
            else:
                # print("NO está extnedido")
                await act_pro_2.click()
                # print("extendido act 2")

        except PlaywrightTimeoutError as e:
            print("Error hallado:", e)

        try:
            # print("Buscando guia de aprendizaje")
            guia_apre_2 = page.locator("div:has(> h3:text('Guía de aprendizaje'))").locator("#collapssesection34")
            await guia_apre_2.wait_for(state="visible", timeout=5000)
            extend_guia_2 = await guia_apre_2.get_attribute("aria-expanded")
            if extend_guia_2 == "true":
                print("Está extnedido")
            else:
                # print("NO está extnedido")
                await guia_apre_2.click()
                # print("extendido guia 2")

        except PlaywrightTimeoutError as e:
            print("Error hallado:", e)

        # await browser.close()
        try:
            print("Buscando section tarea")
            #      contenedor de GA2 con todas la seccions de tareas  / lista secciones
            container_sections = page.locator("#coursecontentcollapse34 > ul.flexsections-level-2")
            await container_sections.wait_for(state="visible", timeout=5000)
            elementos_li = container_sections.locator("> li")
            total = await elementos_li.count()

            print("Como llega el nombre de name_file:\n",name_file)
            list_directions_h = []
            name_to_search = name_file.split("_")[0].strip()

            print("Nombre real del archivo a buscar:\n", name_to_search)

            for i in range(total):
                texto = await elementos_li.nth(i).inner_text()
                list_directions_h.append(texto.split(" ")[-1].strip())

            name_final = str(name_to_search[:-5]).strip()
            for letra in name_final:
                if letra == "_":
                    name_final = str(name_final).split("_")[0]
                    name_final = name_final[:-5].strip()
            print("en secciones",name_final)

            if name_final in list_directions_h:
                tarea_locator = page.get_by_label(f"Actividad de aprendizaje {name_final}", exact=True)
                await tarea_locator.wait_for(state="visible", timeout=5000)

                # id hallado
                id_contenedor_dinamico = await tarea_locator.get_attribute("aria-controls")

                if not id_contenedor_dinamico:
                    id_contenedor_dinamico = await tarea_locator.get_attribute("id")

                print(f"ID del contenedor Moodle detectado dinámicamente: {id_contenedor_dinamico}")

                await tarea_locator.click()

                # div especifico to use
                selector_estricto = f"#{id_contenedor_dinamico} ul[data-for='cmlist'] li.activity"
                print(f"Selector generado: {selector_estricto}")

                actividades = page.locator(selector_estricto)

                await actividades.first.wait_for(state="attached", timeout=5000)
                await page.wait_for_timeout(1500)

                total_actividades = await actividades.count()
                print(f"Tareas encontradas: {total_actividades}")

                tarea_especifica_encontrada = False

                for i in range(total_actividades):
                    actividad = actividades.nth(i)
                    texto_completo = await actividad.locator(".instancename").text_content()

                    if not texto_completo:
                        continue

                    patron_evidencia = r"GA\d+-\d+-AA\d+-EV\d+"
                    coincidencia = re.search(patron_evidencia, texto_completo)

                    if coincidencia:
                        codigo_extraido = coincidencia.group(0)

                        if name_to_search in codigo_extraido:
                            print(f"{codigo_extraido}")
                            tarea_especifica_encontrada = True
                            # pendiente de mirar porque tengo que partir asi una linea
                            #  y no puedo hacer todo junto
                            # await page.locator(".dndupload-arrow").first.
                            # ...wait_for(timeout=5000, state="attached").click()
                            await actividad.locator("a.stretched-link").click(force=True)
                            await page.get_by_text("Agregar entrega").click(force=True)
                            tar_input = page.locator(".dndupload-arrow").first
                            await tar_input.wait_for(timeout=5000, state="attached")
                            await tar_input.click()
                            # subida archivo
                            await page.locator("input[name='repo_upload_file']").set_input_files(file_path)
                            # subida directamente la input
                            print("Archivo cargad")
                            await page.pause()
                if not tarea_especifica_encontrada:
                    print("No se encontró la evidencia .")

            else:
                print("Tarea no encontrada en las secciones principales")


        except PlaywrightTimeoutError as e:
            print("Error hallado:", e)
