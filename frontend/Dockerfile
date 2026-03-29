# Use Node.js 20 (LTS)
FROM node:20-bullseye

# Set working directory
WORKDIR /app

# Copy package.json & package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY . .

# Build frontend
RUN npm run build

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev"]