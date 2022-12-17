# pull official base image
FROM postgres:14-alpine

# add backup directory
RUN mkdir backup

# add backup file
COPY huntydb_dump.sql /backup/.

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
