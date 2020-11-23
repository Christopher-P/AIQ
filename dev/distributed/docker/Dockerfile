FROM rabbitmq:management

# Define environment variables.
ENV RABBITMQ_DEFAULT_USER chris
ENV RABBITMQ_DEFAULT_PASS TdS3g8opiqi9DA7gi

ADD init.sh /init.sh

RUN ["chmod", "+x", "/init.sh"]

EXPOSE 15672

# Define default command
CMD ["/init.sh"]
