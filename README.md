# Proyecto-Votacion

# Ejecución del Backend

Para poner en marcha el backend del proyecto, sigue los pasos que se indican a continuación:

### Prerrequisitos
1. Tener **Docker Desktop** instalado y ejecutándose en tu ordenador.
2. Verificar que Docker Compose esté disponible en tu entorno.

### Instrucciones de Ejecución

1. **Abrir la Consola en la Carpeta del Proyecto**  
   Navega a la carpeta donde se encuentra el archivo `docker-compose.dev.yml`.

2. **Iniciar los Servicios con Docker Compose**  
   En la consola, ejecuta el siguiente comando:

   ```bash
   docker-compose -f docker-compose.dev.yml up --build (Primera ejecucion)
   docker-compose -f docker-compose.dev.yml up (Una vez buildeado los dockers)
   docker-compose -f docker-compose.dev.yml down (Si se quieren eliminar los contenedores)

   

