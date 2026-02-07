FROM node:18

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

ENV PORT=10000
EXPOSE 10000

CMD ["node", "index.js"]




