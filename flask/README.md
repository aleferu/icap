# Flask

Aquí se encontrará el script que mantenga el servidor HTTP y lo necesario para crear una imagen docker que pueda instalarlo en una instancia de manera sencilla.

## URIs hechas:
El argumento YearMonth es común en todas las URIs y es un valor resultado de Year * 100 + Month.
- Ejemplo para el año 2009 mes 6: <\/URI deseada>?YearMonth=200906
Si la fecha deseada no está en la base de datos, manda un error 404.
- `/maxdiff`
    - Solicita a la base de datos Dynamodb aquellas filas que coincidan con YearMonth y devuelve la diferencia entre la temperatura máxima y mínima del mes.
- `/sd`
    - Solicita a la base de datos Dynamodb aquellas filas que coincidan con YearMonth y devuelve la desviación calculada a partir de las temperaturas del mes.
- `/temp`
    - Solicita a la base de datos Dynamodb aquellas filas que coincidan con YearMonth y devuelve la media calculada a partir de las temperaturas del mes.
- URIs que faltan:
    - `/dato` o como sea que se llame la URI si lo hacemos así. Si esto se hace así hará falta un script que coja un CSV y vaya mandando cada fila del CSV al servidor.
