FROM orientdb:latest

ENV ORIENTDB_ROOT_PASSWORD=root

EXPOSE 2424 2480

WORKDIR /orientdb

CMD ["sh", "bin/server.sh"]
