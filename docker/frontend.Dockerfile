# --- Build Stage ---
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Production Stage ---
FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# Custom nginx config to support React router SPA if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
