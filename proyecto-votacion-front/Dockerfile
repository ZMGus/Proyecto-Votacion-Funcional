# Etapa 1: Construcción del proyecto Angular
FROM node:18-alpine AS build
WORKDIR /app

# Copiar archivos necesarios para la instalación
COPY package*.json ./
RUN npm ci

# Copiar el resto del proyecto
COPY . .

# Construir la aplicación Angular
RUN npm run build

# Listar el contenido del directorio para verificar la construcción
RUN ls -alt ./dist

# Etapa 2: Servir la aplicación usando Nginx
FROM nginx:alpine

# Copiar archivos compilados desde la carpeta correcta
COPY --from=build /app/dist/sistema-votacion-2/browser /usr/share/nginx/html

# Copiar el archivo de configuración de Nginx a la ubicación principal
COPY config/nginx.conf /etc/nginx/nginx.conf

# Eliminar la configuración predeterminada de Nginx
RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 4200
CMD ["nginx", "-g", "daemon off;"]
