FROM golang:1.22.0-alpine as builder

RUN apk update && apk add xxd sqlite tar xz

WORKDIR /zig

ADD https://ziglang.org/download/0.11.0/zig-linux-x86_64-0.11.0.tar.xz zig.tar.xz
RUN tar -xf zig.tar.xz
RUN mv zig-linux-x86_64-0.11.0/* . && rmdir zig-linux-x86_64-0.11.0

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY views/ ./views/
COPY main.go ./

# zig cc is for static CGO binaries
RUN CGO_ENABLED=1 GOOS=linux \
    CC="/zig/zig cc -target native-native-musl" \
    CXX="/zig/zig cc -target native-native-musl" \
    go build -v -o vikemerch .

COPY seed.sh ./
RUN ./seed.sh

RUN rm -rf views main.go go.mod go.sum seed.sh


FROM scratch 

COPY --from=alpine:latest /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

WORKDIR /app

COPY assets/ ./assets/

COPY --from=builder /app/ .

EXPOSE 8080

CMD ["./vikemerch"]
