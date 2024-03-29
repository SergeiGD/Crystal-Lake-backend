const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
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
            new TerserWebpackPlugin(),
        ]
        
    }
    return conf;
}

module.exports = {
    mode: isDev ? 'development' : 'production',
    entry: {
        index_critical: [
            path.resolve(__dirname,'src/scss/index_critical.scss'),
        ],
        client: [
            path.resolve(__dirname,'src/scss/style.scss'),
            path.resolve(__dirname,'src/js/client/header_burger.js'),
            path.resolve(__dirname,'src/js/client/login_popup.js'),
            path.resolve(__dirname,'src/js/client/offers_slider.js'),
            path.resolve(__dirname,'src/js/client/profile_burger.js'),
            path.resolve(__dirname,'src/js/client/filter_mobile.js'),
            path.resolve(__dirname,'src/js/client/sortby.js'),
            path.resolve(__dirname,'src/js/client/load_map.js'),
            path.resolve(__dirname,'src/js/client/delete_cart_item.js'),
            path.resolve(__dirname,'src/js/client/slick-slider/slick_starter.js'),
            path.resolve(__dirname,'src/js/client/ajax/register.js'),
            path.resolve(__dirname,'src/js/common/ajax/ajax_redirect.js'),
            path.resolve(__dirname,'src/js/client/ajax/reset_password.js'),
            path.resolve(__dirname,'src/js/common/ajax/get_room_dates.js'),
            path.resolve(__dirname,'src/js/common/ajax/get_service_dates.js'),
            path.resolve(__dirname,'src/js/common/redirect.js'),

        ],
        admin: [
            path.resolve(__dirname,'src/scss/admin.scss'),
            path.resolve(__dirname,'src/js/common/redirect.js'),
            path.resolve(__dirname,'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
            path.resolve(__dirname,'src/js/admin/show_img.js'),
            path.resolve(__dirname,'src/js/admin/move_img.js'),
            path.resolve(__dirname,'src/js/admin/upload_img.js'),
            path.resolve(__dirname,'src/js/admin/delete_img.js'),
            path.resolve(__dirname,'src/js/admin/new_offer_main_img.js'),
            path.resolve(__dirname,'src/js/admin/select_client.js'),
            path.resolve(__dirname,'src/js/admin/select_room_purchase.js'),
            path.resolve(__dirname,'src/js/admin/select_service_purchase.js'),
            path.resolve(__dirname,'src/js/admin/find_items.js'),
            path.resolve(__dirname,'src/js/admin/item_select.js'),
            path.resolve(__dirname,'src/js/admin/clean_popup.js'),
            path.resolve(__dirname,'src/js/admin/room_purchase_popup_open.js'),
            path.resolve(__dirname,'src/js/admin/service_purchase_popup_open.js'),
            path.resolve(__dirname,'src/js/admin/timetable_popup_open.js'),
            path.resolve(__dirname,'src/js/admin/add_worker_to_timetable.js'),
            path.resolve(__dirname,'src/js/admin/remove_worker_from_timetable.js'),
            path.resolve(__dirname,'src/js/admin/set_called_by.js'),
            path.resolve(__dirname,'src/js/admin/ajax/offer_ajax.js'),
            path.resolve(__dirname,'src/js/admin/ajax/delete_additional_elem.js'),
            path.resolve(__dirname,'src/js/admin/ajax/edit_additional_elem.js'),
            path.resolve(__dirname,'src/js/admin/ajax/add_additional_elem.js'),
            path.resolve(__dirname,'src/js/admin/ajax/manage_purchase.js'),
            path.resolve(__dirname,'src/js/admin/ajax/default_set_main_info.js'),
            path.resolve(__dirname,'src/js/admin/ajax/manage_timetable.js'),
            path.resolve(__dirname,'src/js/common/ajax/get_room_dates.js'),
            path.resolve(__dirname,'src/js/common/ajax/get_service_dates.js'),
            path.resolve(__dirname,'src/js/admin/ajax/ajax_search.js'),
            path.resolve(__dirname,'src/js/common/ajax/ajax_redirect.js'),

        ]
    },
    output: {
        filename: 'js/[name]-[contenthash].bundle.js',
        path: path.resolve(__dirname, '../static'),
        clean: {
            keep: /(admin|polymorphic|images)\//
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
                            sourceMap: isDev,
                        }
                    },
                    {loader: 'resolve-url-loader', options: {sourceMap: isDev}},
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