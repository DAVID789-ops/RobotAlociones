import pdfplumber
import re

# Función para extraer datos del PDF
def extraer_datos_pdf(ruta_pdf):
    datos_totales = []

    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()

                # Imprimir el texto completo del PDF para verificar qué se extrae
                print(f"Texto extraído de {ruta_pdf}:\n{texto}\n")

                # Extracción de campos específicos
                datos = {}
                datos['mensajero'] = "Forza"
                datos['precio_envio'] = "31"

                # Buscar "Contacto:"
                contacto_idx = texto.find("Contacto:")
                if contacto_idx != -1:
                    # Buscar la posición de ".oN " después de "Contacto:"
                    fin_contacto_idx = texto.find(".oN ", contacto_idx)
    
                    if fin_contacto_idx != -1:
                        # Extraer el texto entre "Contacto:" y ".oN "
                        texto_contacto = texto[contacto_idx + len("Contacto:"):fin_contacto_idx].strip()
                        datos['contacto'] = texto_contacto
                    else:
                        # Si no se encuentra ".oN ", solo tomar la primera palabra después de "Contacto:"
                        datos['contacto'] = texto[contacto_idx + len("Contacto:"):].strip().split()[0]
                else:
                    # Si no hay "Contacto:", buscar después de "oiratanitseD"
                    destino_idx = texto.find("oiratanitseD")
                    if destino_idx != -1:
                        # Buscar "Tel.:" después de "oiratanitseD"
                        fin_destino_idx = texto.find("Tel.:", destino_idx)
                        if fin_destino_idx != -1:
                            # Extraer el texto entre "oiratanitseD" y "Tel.:"
                            texto_contacto = texto[destino_idx + len("oiratanitseD"):fin_destino_idx].strip()
                            datos['contacto'] = texto_contacto
                        else:
                            datos['contacto'] = "Desconocido"  # Si no se encuentra "Tel.:", indicar "Desconocido"
                    else:
                        datos['contacto'] = "Desconocido"  # Si no se encuentra ni "Contacto:" ni "oiratanitseD"


                # Encuentra la posición de la palabra "oiratanitseD"
                destinatario_idx = texto.find("oiratanitseD")

                # Si se encuentra "oiratanitseD", buscar el número de teléfono después de esa palabra
                if destinatario_idx != -1:
                    tel_idx = texto.find("Tel.:", destinatario_idx)  # Buscar "Tel.:" después de "oiratanitseD"
                    if tel_idx != -1:
                        # Extraer el número de teléfono que está después de "Tel.:"
                        datos['telefono'] = texto[tel_idx + len("Tel.:"):].split()[0]
                    else:
                        datos['telefono'] = None  # Si no encuentra el "Tel.:", asignar None o un valor predeterminado
                else:
                    datos['telefono'] = None  # Si no encuentra "oiratanitseD", asignar None o un valor predeterminado

                # Extraer "Dirección"
                destinatario_idx = texto.find("oiratanitseD")
                if destinatario_idx != -1:
                    # Buscar "Contacto:" después de "oiratanitseD"
                    contacto_idx = texto.find("Contacto:", destinatario_idx)
    
                    if contacto_idx != -1:
                        # Si se encuentra "Contacto:", extraer el texto entre "oiratanitseD" y "Contacto:"
                        direccion = texto[destinatario_idx + len("oiratanitseD"):contacto_idx].strip()
                        datos['direccion'] = direccion
                    else:
                        # Si no se encuentra "Contacto:", buscar ".oN"
                        fin_direccion_idx = texto.find(".oN", destinatario_idx)
        
                        if fin_direccion_idx != -1:
                            # Extraer el texto entre "oiratanitseD" y ".oN"
                            direccion = texto[destinatario_idx + len("oiratanitseD"):fin_direccion_idx].strip()
                            datos['direccion'] = direccion
                        else:
                            # Si no se encuentra ".oN", asumir que la dirección es desconocida
                            datos['direccion'] = "Desconocido"
                else:
                    datos['direccion'] = "Desconocido"



                # Busca la palabra "DOMICILIO"
                # Busca la palabra "DOMICILIO"
                depto_idx = texto.find("DOMICILIO")

                if depto_idx != -1:
                    # Si encuentra "DOMICILIO", toma el valor después de la palabra
                    partes_domicilio = texto[depto_idx + len("DOMICILIO"):].strip().split()
                    datos['departamento'] = partes_domicilio[0] if len(partes_domicilio) > 0 else "Desconocido"

                    # Extraer el municipio (todas las palabras después del departamento hasta un número de uno o dos dígitos)
                    if len(partes_domicilio) > 1:
                        grupo_palabras = []

                        # Comenzar desde la segunda palabra
                        for palabra in partes_domicilio[1:]:
                            # Verificar si la palabra es un número de uno o dos dígitos
                            if palabra.isdigit() and (len(palabra) == 1 or len(palabra) == 2):
                                break  # Salir del bucle si se encuentra un número de uno o dos dígitos
                            grupo_palabras.append(palabra)

                        # Unir las palabras para formar el municipio
                        if grupo_palabras:
                            datos['municipio'] = ' '.join(grupo_palabras)  # Unir palabras en un string
                        else:
                            datos['municipio'] = "Desconocido"  # No hay suficiente información
                    else:
                        datos['municipio'] = None  # No hay suficiente información
                else:
                    # Si no encuentra "DOMICILIO", busca la palabra "OFICINA"
                    oficina_idx = texto.find("OFICINA")

                    if oficina_idx != -1:
                        # Si encuentra "OFICINA", toma el valor después de la palabra
                        partes_oficina = texto[oficina_idx + len("OFICINA"):].strip().split()
                        datos['departamento'] = partes_oficina[0] if len(partes_oficina) > 0 else "Desconocido"

                        # Extraer el municipio (todas las palabras después del departamento hasta un número de uno o dos dígitos)
                        if len(partes_oficina) > 1:
                            grupo_palabras = []

                            # Comenzar desde la segunda palabra
                            for palabra in partes_oficina[1:]:
                                # Verificar si la palabra es un número de uno o dos dígitos
                                if palabra.isdigit() and (len(palabra) == 1 or len(palabra) == 2):
                                    break  # Salir del bucle si se encuentra un número de uno o dos dígitos
                                grupo_palabras.append(palabra)

                            # Unir las palabras para formar el municipio
                            if grupo_palabras:
                                datos['municipio'] = ' '.join(grupo_palabras)  # Unir palabras en un string
                            else:
                                datos['municipio'] = "Desconocido"  # No hay suficiente información
                        else:
                            datos['municipio'] = None  # No hay suficiente información
                    else:
                        # Si no encuentra "OFICINA", busca la palabra "EXPRESS"
                        express_idx = texto.find("EXPRESS")

                        if express_idx != -1:
                            # Si encuentra "EXPRESS", toma el valor después de la palabra
                            partes_express = texto[express_idx + len("EXPRESS"):].strip().split()
                            datos['departamento'] = partes_express[0] if len(partes_express) > 0 else "Desconocido"

                            # Extraer el municipio (todas las palabras después del departamento hasta un número de uno o dos dígitos)
                            if len(partes_express) > 1:
                                grupo_palabras = []

                                # Comenzar desde la segunda palabra
                                for palabra in partes_express[1:]:
                                    # Verificar si la palabra es un número de uno o dos dígitos
                                    if palabra.isdigit() and (len(palabra) == 1 or len(palabra) == 2):
                                        break  # Salir del bucle si se encuentra un número de uno o dos dígitos
                                    grupo_palabras.append(palabra)

                                # Unir las palabras para formar el municipio
                                if grupo_palabras:
                                    datos['municipio'] = ' '.join(grupo_palabras)  # Unir palabras en un string
                                else:
                                    datos['municipio'] = "Desconocido"  # No hay suficiente información
                            else:
                                datos['municipio'] = None  # No hay suficiente información
                        else:
                            # Si no encuentra ninguna de las tres, asigna un valor predeterminado
                            datos['departamento'] = "Desconocido"
                            datos['municipio'] = None  # Asignar None si no se encuentra "DOMICILIO", "OFICINA", ni "EXPRESS"





                # Extraer "Guía No."
                guia_match = re.search(r'FD\d{8}-\d', texto)
                if guia_match:
                    datos['numero_guia'] = guia_match.group(0)

                # Extraer la fecha
                fecha_match = re.search(r'\d{2}/\d{2}/\d{4}', texto)
                if fecha_match:
                    datos['fecha'] = fecha_match.group(0)

                # Extraer "Monto" (buscando el número más cercano a "No. Ticket")
                monto_match = re.search(r'(\b\d{1,3}\b)(?=\s*No\. Orden)', texto)
                if monto_match:
                    datos['monto'] = monto = int(monto_match.group(0))

                    # Condicional para la cantidad
                    if 95 <= monto <= 159:
                        datos['cantidad'] = 1
                    else:
                        datos['cantidad'] = 2

                    # Condicional para el tamaño
                    if 139 <= monto <= 160:
                        datos['tamaño'] = 100
                    elif 95 <= monto <= 114:
                        datos['tamaño'] = 50
                    else:
                        datos['tamaño'] = 100  # Valor por defecto

                    # Condicional para la descripción según el tamaño
                    if datos['tamaño'] == 100:
                        datos['descripcion'] = "Dior sauvage de 100ml 2 onzas y 2 perfume portátil todo con feromonas"
                    elif datos['tamaño'] == 50:
                        datos['descripcion'] = "Dior sauvage 60ml 1 onza"
                    else:
                        datos['descripcion'] = "Descripción no disponible"

                    # Condicional para la ganancia
                    if monto == 139:
                        datos['ganancia'] = 50
                    elif monto in [158, 159, 160]:
                        datos['ganancia'] = 70
                    elif monto == 95:
                        datos['ganancia'] = 25
                    elif monto == 114:
                        datos['ganancia'] = 44
                    else:
                        datos['ganancia'] = 0  # Valor por defecto si no coincide con ninguna condición

                datos_totales.append(datos)

        return datos_totales

    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return None
