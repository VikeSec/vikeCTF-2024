#!/usr/bin/env -S bash -c "docker run -p 3000:3000 -it --rm \$(docker build --progress plain -f \$0 . 2>&1 | tee /dev/stderr | grep -m 1 -oP 'Successfully built [0-9a-f]*' | awk '{print \$3}')"
# Credit: Florin Lipan
# https://lipanski.com/posts/smallest-docker-image-static-website

FROM alpine:3.13.2 AS builder

ARG THTTPD_VERSION=2.29

# Install all dependencies required for compiling thttpd
RUN apk add --no-cache gcc musl-dev make

# Download thttpd sources
RUN wget http://www.acme.com/software/thttpd/thttpd-${THTTPD_VERSION}.tar.gz \
  && tar xzf thttpd-${THTTPD_VERSION}.tar.gz \
  && mv /thttpd-${THTTPD_VERSION} /thttpd

# Compile thttpd to a static binary which we can copy around
RUN cd /thttpd \
  && ./configure \
  && make CCOPT='-Os -s -static' thttpd

# Create a non-root user to own the files and run our server
RUN adduser -D static


# Switch to the scratch image
FROM scratch

WORKDIR /home/static
EXPOSE 3000

# Copy over the user
COPY --from=builder /etc/passwd /etc/passwd

# Copy the thttpd static binary
COPY --from=builder /thttpd/thttpd /

# Use our non-root user
USER static

# Copy the static website
COPY src .

# Run thttpd
CMD ["/thttpd", "-D", "-h", "0.0.0.0", "-p", "3000", "-d", "/home/static", "-u", "static", "-l", "-", "-M", "60"]

