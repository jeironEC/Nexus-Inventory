FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
COPY html/ /usr/share/nginx/html/html/
COPY css/ /usr/share/nginx/html/css/
COPY js/ /usr/share/nginx/html/js/
COPY templates/ /usr/share/nginx/html/templates/
COPY assets/ /usr/share/nginx/html/assets/
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
