FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --silent

COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0"]
