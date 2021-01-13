FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir /etc/nginx/certs

COPY certs/fullchain.pem /etc/nginx/certs/
COPY certs/privkey.pem  /etc/nginx/certs/
COPY certs/chain.pem /etc/nginx/certs/
COPY certs/dhparam.pem /etc/nginx/certs/
