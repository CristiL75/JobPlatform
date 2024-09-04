# Dockerfile for React

# Folosește o imagine oficială Node ca bază
FROM node:16

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele package.json și package-lock.json (dacă există) în directorul de lucru
COPY package*.json /app/

# Instalează dependențele
RUN npm install

# Copiază restul fișierelor aplicației în container
COPY . /app/

# Construiește aplicația React
RUN npm run build

# Expune portul pe care rulează aplicația React (implicit 3000)
EXPOSE 3000

# Rulează aplicația React
CMD ["npm", "start"]
