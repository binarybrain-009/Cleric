# Use the official Node.js image
FROM node:23-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies first
COPY package.json package-lock.json /app/

# Copy the rest of the app files to the container
COPY src /app/

# Install dependencies
RUN npm install

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
