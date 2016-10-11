var webpack = require("webpack");

module.exports = {
  entry: ["./index.js"],
  output: {
    path: "./static/js",
    publicPath: "/static/js",
    filename: "[name].js",
  }
};

// vim: sts=2 sw=2 et
