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
            path.resolve(__dirname,'src/js/client/sortby.js'),
            path.resolve(__dirname,'src/js/client/slick-slider/slick_starter.js'),
            path.resolve(__dirname,'src/js/common/evo-calendar/evo-starter.js'),
        ],
        admin: [
            path.resolve(__dirname,'src/scss/admin.scss'),
            path.resolve(__dirname,'src/js/common/redirect.js'),
            path.resolve(__dirname,'src/js/common/evo-calendar/evo-starter.js'),
            path.resolve(__dirname,'src/js/common/evo-calendar/evo-calendar.js'),
            path.resolve(__dirname,'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
            path.resolve(__dirname,'src/js/admin/show_img.js'),
            path.resolve(__dirname,'src/js/admin/move_img.js'),
            path.resolve(__dirname,'src/js/admin/upload_img.js'),
            path.resolve(__dirname,'src/js/admin/delete_img.js'),
            path.resolve(__dirname,'src/js/admin/new_offer_main_img.js'),
            path.resolve(__dirname,'src/js/admin/select_client.js'),
            path.resolve(__dirname,'src/js/admin/select_room_purchase.js'),
            path.resolve(__dirname,'src/js/admin/select_service_purchase.js'),
            path.resolve(__dirname,'src/js/admin/select_timetable.js'),
            path.resolve(__dirname,'src/js/admin/find_items.js'),
            path.resolve(__dirname,'src/js/admin/item_select.js'),
            path.resolve(__dirname,'src/js/admin/clean_popup.js'),
            path.resolve(__dirname,'src/js/admin/room_purchase_popup_open.js'),
            path.resolve(__dirname,'src/js/admin/service_purchase_popup_open.js'),
            path.resolve(__dirname,'src/js/admin/timetable_popup_open.js'),
            path.resolve(__dirname,'src/js/admin/add_worker_to_timetable.js'),
            path.resolve(__dirname,'src/js/admin/remove_worker_from_timetable.js'),
            path.resolve(__dirname,'src/js/admin/set_timetable_called_by.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_rooms.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_services.js'),
            path.resolve(__dirname,'src/js/admin/ajax/offer_ajax.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_tags_for_offer.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_services_for_worker.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_groups_for_worker.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_permissions_for_group.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_clients_for_order.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_workers_for_timetable.js'),
            path.resolve(__dirname,'src/js/admin/ajax/search_timetables_for_service.js'),
            path.resolve(__dirname,'src/js/admin/ajax/delete_additional_elem.js'),
            path.resolve(__dirname,'src/js/admin/ajax/edit_additional_elem.js'),
            path.resolve(__dirname,'src/js/admin/ajax/add_additional_elem.js'),
            // path.resolve(__dirname,'src/js/admin/ajax/add_tag_to_offer.js'),
            // path.resolve(__dirname,'src/js/admin/ajax/add_service_to_worker.js'),
            // path.resolve(__dirname,'src/js/admin/ajax/add_group_to_worker.js'),
            // path.resolve(__dirname,'src/js/admin/ajax/add_permission_to_group.js'),
            path.resolve(__dirname,'src/js/admin/ajax/manage_purchase.js'),
            // path.resolve(__dirname,'src/js/admin/ajax/create_same_room.js'),
            path.resolve(__dirname,'src/js/admin/ajax/default_set_main_info.js'),
            path.resolve(__dirname,'src/js/admin/ajax/manage_timetable.js'),
            path.resolve(__dirname,'src/js/admin/ajax/get_dates_info.js'),
            path.resolve(__dirname,'src/js/admin/ajax/get_service_dates_info.js'),
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