# install node
FROM node:20-alpine as builder

# working directory
WORKDIR /app

# copy package.json deps
COPY package*.json .

# install deps
RUN npm run build

# serve the frontend
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]

