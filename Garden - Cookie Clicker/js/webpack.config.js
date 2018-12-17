/* eslint-disable no-undef */
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const webpack = require("webpack");

module.exports = {
    entry: "./src/index.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "dist")
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: "index.html",
            template: "./src/index.html"
        }),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery"
        })
    ],
    resolve: {
        alias: {
            "handlebars" : "handlebars/dist/handlebars.js"
        }
    },
    module: {
        rules : [
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ]
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    "file-loader"
                ]
            },
            {
                test: /\.hbs$/,
                use: [{
                    loader: "handlebars-loader",
                    options: {
                        extensions: [".hbs"],
                        runtimePath: "handlebars/runtime"
                    }
                }]
            }
        ]
    }
};