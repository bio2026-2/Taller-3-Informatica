# Taller 3 - Informática 1

**Gestión de información en computación y manejo de bases de datos**

Este proyecto genera 50 registros biomédicos ficticios, los valida, ordena por frecuencia cardíaca, guarda archivos TXT/CSV/JSON y permite almacenarlos y consultarlos en MongoDB Atlas.

## 1. Archivos y carpetas

- `main.py`: programa principal y menú.
- `requirements.txt`: dependencia externa.
- `log.txt`: registro de acciones.
- `data/txt/`: archivo de texto generado.
- `data/csv/`: archivo CSV generado.
- `data/json/`: archivos JSON y resultados de MongoDB.

Las carpetas `data` se crean automáticamente al ejecutar `main.py`.

## 2. Requisitos e instalación en Spyder

1. Abrir Anaconda Navigator y ejecutar Spyder.
2. Abrir `main.py` desde la carpeta del proyecto.
3. En la consola IPython de Spyder ejecutar:

```python
%pip install pymongo
```

También se puede instalar solo la dependencia con `%pip install pymongo`.

4. Ejecutar `main.py` con F5.

## 3. Configurar MongoDB Atlas

1. Crear un clúster gratuito en MongoDB Atlas.
2. En **Database Access**, crear un usuario de base de datos.
3. En **Network Access**, permitir la IP desde la que se conecta el equipo.
4. En el clúster, elegir **Connect > Drivers > Python** y copiar la URI.
5. En la consola IPython de Spyder, antes de seleccionar las opciones 7, 8 o 9, ejecutar:

```python
import os
os.environ["MONGODB_URI"] = "PEGAR_AQUI_LA_URI_DE_ATLAS"
```

Reemplazar el texto por la URI real. No subir la URI, contraseña ni credenciales a GitHub. La variable debe configurarse de nuevo si se reinicia la sesión de Spyder.

La base de datos se llama `taller_informatica` y la colección `signos vitales`. MongoDB las crea al insertar el primer documento.

## 4. Uso

Ejecutar `main.py` con F5 y usar el menú:

1. Generar 50 registros.
2. Mostrar registros.
3. Ordenar por frecuencia cardíaca.
4. Validar los formatos.
5. Exportar TXT, CSV y JSON.
6. Importar registros desde JSON.
7. Insertar registros en MongoDB Atlas.
8. Consultar promedio de FC y registros con SpO2 menor a 94; exportar `resultados_mongo.json`.
9. Buscar un registro en MongoDB por ID.
0. Salir.

Se recomienda ejecutar en orden las opciones 1, 4, 5, 7 y 8. La opción 6 importa el archivo `data/json/registros.json`, por lo que primero debe existir mediante la opción 5.

## 5. Formatos validados

- `id`: `ID-001` (tres dígitos).
- `fr`: número seguido de `Años`.
- `fc`: tres dígitos seguidos de `ppm`.
- `spo2`: número seguido de `%`.

## 6. Consideración

Los datos son generados aleatoriamente y son ficticios. No representan pacientes reales ni deben utilizarse para decisiones clínicas.
