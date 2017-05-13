FROM node:7.10
RUN apt-get update && apt-get install -y calibre && npm install -g gitbook-cli && gitbook fetch


ADD . /code
WORKDIR /code
RUN npm install && gitbook build && cd _book && gitbook pdf ../ ./Talk_jsdayes2017.pdf && cd ..
EXPOSE 8080
CMD [ "npm", "start" ]
