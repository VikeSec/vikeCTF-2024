FROM node:20

WORKDIR /app
COPY index.js package.json package-lock.json .npmrc /app/
RUN npm install --omit=dev
RUN rm .npmrc

CMD [ "npm", "run", "start" ]