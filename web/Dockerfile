# install node
FROM node:20-alpine as builder

# working directory
WORKDIR /app

# copy package.json deps and install deps
COPY package*.json ./
RUN npm install

# install app code
COPY . .
RUN npm run build

# serve the frontend
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

