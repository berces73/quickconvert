# 1️⃣ Base image
FROM node:18-alpine

# 2️⃣ Çalışma dizini
WORKDIR /app

# 3️⃣ Package dosyaları
COPY package*.json ./

# 4️⃣ Dependency yükle
RUN npm install --production

# 5️⃣ Tüm dosyaları kopyala
COPY . .

# 6️⃣ Render port
ENV PORT=10000
EXPOSE 10000

# 7️⃣ Uygulamayı başlat
CMD ["npm", "start"]
]



