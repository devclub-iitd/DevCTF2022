FROM mattrayner/lamp:latest-1804
WORKDIR /
RUN sed s/'Options Indexes FollowSymLinks'/'Options FollowSymLinks'/g -i /etc/apache2/apache2.conf
COPY . .
RUN chmod +x run.sh
RUN ln -sf /dev/stdout /var/log/apache2/access.log && \
    ln -sf /dev/stderr /var/log/apache2/error.log
CMD ["/run.sh"]