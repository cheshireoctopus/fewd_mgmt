var path = require('path')

module.exports = {
	devtool: 'eval', // map console errors to file/line number; explore eval-source-map and source-map
	entry: {
		js: path.join(__dirname, 'apps/main.babel.js'),
	},
	output: {
		path: path.join(__dirname, 'build'),
		filename: 'bundle.js',
	},
	module: {
		loaders: [
			{
				test: /(\.babel\.js$|\.jsx$)/,
				exclude: /(node_modules|bower_components)/,
				loader: 'babel',
				query: {
					cacheDirectory: true,
					presets: ['es2015', 'react'],
					plugins: ['transform-runtime'],
				}
			},
			{
				test: require.resolve('react'),
				loader: 'expose?React',
			},
			{
				test: require.resolve('underscore'),
				loader: 'expose?_!expose?Underscore',
			},
			{
				test: require.resolve('backbone'),
				loader: 'expose?Backbone',
			},
			{
				test: require.resolve('jquery'),
				loader: 'expose?$!expose?jQuery',
			},
			{
				test: require.resolve('immutable'),
				loader: 'expose?$!expose?Immutable',
			},
			{
				test: /\.css$/,
				loader: 'style-loader!css-loader',
			},
			{ test: /\.(png|woff|woff2|eot|ttf|svg)$/, loader: 'url-loader?limit=100000' }
		],
	},
	resolve: {
		root: path.resolve(path.join(__dirname, 'apps')),
		extensions: ['', '.js', '.jsx', '.json']
	},
}
