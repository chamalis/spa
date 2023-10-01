# Set nginx base image
FROM nginx:latest

RUN rm /etc/nginx/conf.d/*.conf

# Copy custom configuration file from the current directory
COPY ./sites/*.conf /etc/nginx/conf.d/
