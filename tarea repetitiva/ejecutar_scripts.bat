
@echo off
 
:: Ejecutar descargar_correos.py para que descarge los excel del correo para luego ser verificado por otro bot
python E:\RobotAlociones\IPA\descargar_guias_pagadas\__pycache__\descargar_correos.py

:: Esperar a que termine el primer script
timeout /t 5 /nobreak

:: Ejecutar procesar_pdfs.py para que meta las guias enteras de forza a la base de datos 
python E:\RobotAlociones\IPA\IPA\procesar_pdfs.py

:: Esperar a que termine el segundo script
timeout /t 5 /nobreak

:: Ejecutar verificacio_guias.py para que verifique cuales son las guias pagadas
python E:\RobotAlociones\IPA\verificacion_guias_pagadas\verificacio_guias.py

:: Esperar a que termine el segundo script
timeout /t 5 /nobreak

:: mover archivos de alociones@gmail.com a otra carpeta despues de haber sido procesados
python E:\RobotAlociones\IPA\MoverArchivosDeUnaRutaAOtra\MoverArchivosAlogionesgmail.py

:: Esperar a que termine el segundo script
timeout /t 5 /nobreak

:: MOVER GUIAS a otra carpeta despues de haber sido procesados
python E:\RobotAlociones\IPA\MoverArchivosDeUnaRutaAOtra\MoverGuiasIntroducidasAdb.py

:: ESTE ESCRIP COLOCA EL NÚMEO DE GUIA AD A TODOS LOS PAQUETES QUE SON MOTOTAXI
timeout /t 5 /nobreak

python E:\RobotAlociones\IPA\generador_codigo_barras\seleccionRegistros.py

:: ESTE CODIGO GENERA UN CODIGO DE BARRAS DEACUERDO AL NUMERO DE GUIA AD Y TAMBIEN GENERA UN PDF PARA QUE PUEDA SER IMPRIMIDA LA GUIA DESDE EL PROPIO SITESMAS, ESTO ES SOLO PARA MOTOTAXO Y FUNCIONA EXPLUSIVAMENTE DESPUES DE SELECIONREGISTROS.PY
timeout /t 5 /nobreak

python E:\RobotAlociones\IPA\generador_codigo_barras\GeneradorCodigoBarras.py


:: ESTE CODIGO MUEVE LAS DEVOLUCIONES A LA TABLA DEVOLUCIONES SEGUN EL NUMERO DE GUIA
timeout /t 5 /nobreak

python E:\RobotAlociones\IPA\devoluciones\devolucion.py


:: ESTE CODIGO MUEVE LAS DEVOLUCIONES A LA TABLA DEVOLUCIONES SEGUN EL NUMERO DE GUIA
timeout /t 5 /nobreak
python E:\RobotAlociones\IPA\colocar_terminado\hecho.py


:: ESTE CODIGO MUEVE LAS DEVOLUCIONES A LA TABLA DEVOLUCIONES SEGUN EL NUMERO DE GUIA
timeout /t 5 /nobreak
python E:\RobotAlociones\IPA\pedidosRetenidos\retenidos.py

:: ESTE CODIGO revisa todos los paquetes que no se reportan en 7 días para catalogarlos como extraviado colocar un informe en la carpeta extraviados con más detalles
timeout /t 5 /nobreak
python E:\RobotAlociones\IPA\extravios\extravios.py

:: ESTE CODIGO imprime todos los extraviados
timeout /t 5 /nobreak
python E:\RobotAlociones\IPA\extravios\imprimir.py

:: Finalizar
PAUSE
