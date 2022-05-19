FROM php:5.6.14-apache

ARG RAW_FLAG

RUN echo ${RAW_FLAG} > /flag.txt
RUN chmod 774 /flag.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
CMD ["/docker-entrypoint.sh"]
