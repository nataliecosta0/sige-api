FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/


RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /etc/nginx/certs

COPY nginx.conf /etc/nginx/conf.d/

COPY certs/fullchain.pem /etc/nginx/certs/
COPY certs/privkey.pem  /etc/nginx/certs/
COPY certs/chain.pem /etc/nginx/certs/
COPY certs/dhparam.pem /etc/nginx/certs/
