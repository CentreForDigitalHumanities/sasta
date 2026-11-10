FROM node:22

WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH=/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json yarn.lock /app/
RUN yarn install --frozen-lockfile

COPY . /app
