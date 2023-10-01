FROM postgres:16.0

# this script shouldn't be actually needed. Its here for convenience
# when creating multiple databases or other actions needed that the
# default postgres docker images doesn't automatically do.
COPY pg-scripts/createdb.sh /docker-entrypoint-initdb.d/
RUN chmod a+x /docker-entrypoint-initdb.d/createdb.sh