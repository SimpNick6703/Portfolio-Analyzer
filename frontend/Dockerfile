# frontend/Dockerfile

# --- Stage 1: Build the React application ---
FROM node:18-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
# This is the step that replaces you running it locally
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application for production
RUN npm run build

# --- Stage 2: Serve the application with Nginx ---
FROM nginx:1.25-alpine

# Copy the built files from the 'build' stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the outside world
EXPOSE 80

# The command to start Nginx
CMD ["nginx", "-g", "daemon off;"]