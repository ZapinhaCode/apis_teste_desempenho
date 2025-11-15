FROM php:8.2-fpm-alpine
RUN apk update && apk add --no-cache \
    build-base \
    libpq-dev \
    netcat-openbsd \
    libzip-dev \
    zip \
    bash \
    && docker-php-ext-install pdo pdo_pgsql opcache zip
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
WORKDIR /var/www/html
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh
RUN mkdir -p /var/www/html/storage \
    && mkdir -p /var/www/html/bootstrap/cache \
    && chown -R www-data:www-data /var/www/html

ENTRYPOINT ["/usr/local/bin/start.sh"]

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
