const path = require('path');
const fs = require('fs');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserWebpackPlugin = require('terser-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const isDev = process.env.PROJECT_ENV == 'development';
const isProd = !isDev;

const optimize = () => {
    const conf = {
        splitChunks: {
            chunks: 'all'
        }
    };

    if (isProd) {
        conf.minimizer = [
            new CssMinimizerPlugin(),
            new TerserWebpackPlugin()
        ]
        
    }
    return conf;
}

module.exports = {
    mode: isDev ? 'development' : 'production',
    entry: {
        client: [
            path.resolve(__dirname,'src/scss/style.scss'),
            path.resolve(__dirname,'src/js/common/redirect.js'),
            path.resolve(__dirname,'src/js/client/header_burger.js'),
            path.resolve(__dirname,'src/js/client/login_popup.js'),
            path.resolve(__dirname,'src/js/client/offers_slider.js'),
            path.resolve(__dirname,'src/js/client/profile_burger.js'),
            path.resolve(__dirname,'src/js/client/filter_mobile.js'),
            path.resolve(__dirname,'src/js/client/infinity_catalog.js'),
            path.resolve(__dirname,'src/js/client/picked_time.js'),
            path.resolve(__dirname,'src/js/client/slick-slider/slick_starter.js'),
            path.resolve(__dirname,'src/js/common/evo-calendar/evo-starter.js'),
        ],
        admin: [
            path.resolve(__dirname,'src/scss/admin.scss'),
            path.resolve(__dirname,'src/js/common/redirect.js'),
            path.resolve(__dirname,'src/js/common/evo-calendar/evo-starter.js'),
            path.resolve(__dirname,'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
            path.resolve(__dirname,'src/js/admin/show_img.js'),
            path.resolve(__dirname,'src/js/admin/move_img.js'),
        ]
    },
    output: {
        filename: 'js/[name]-[contenthash].bundle.js',
        path: path.resolve(__dirname, '../apps/core/static'),
        clean: {
            keep: /images\//,
        },
    },
    devtool: isDev ? 'source-map' : false,
    module: {
        rules: [
            {
                test: /\.(scss|css)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            url: true,
                            sourceMap: true,
                        }
                    },
                    {loader: 'resolve-url-loader'},
                    {loader: 'sass-loader', options: {sourceMap: true}},
                ]
            },
            {
                test: /\.(png|jpg|webp)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'images/[name]-[hash][ext]'
                }
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/[name]-[contenthash].bundle.css'
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        new BundleTracker({filename: path.resolve(__dirname, 'webpack-stats.json')}),
    ],
    resolve: {
        alias:{
            '@scss': path.resolve(__dirname, 'src/scss')
        }
    },
    optimization: optimize()
};