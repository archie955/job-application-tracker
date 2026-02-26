# install node
FROM node:20-alpine as builder

# working directory
WORKDIR /app

ARG VITE_BASEURL
ENV VITE_BASEURL=${VITE_BASEURL}

# copy package.json deps and install deps
COPY package*.json ./
RUN npm install

# install app code
COPY . .
RUN npm run build

# serve the frontend
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# COPY wait-for-it.sh /usr/local/bin/wait-for-it
# RUN chmod +x /usr/local/bin/wait-for-it

# this is the networking issue resolution
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# RUN echo "Starting wait-for-it script..."

CMD ["nginx", "-g", "daemon off;"]

