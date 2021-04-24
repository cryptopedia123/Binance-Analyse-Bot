
// 	Reminder: In order to restart .js files : press SHIFT + REFRESH in the browser to reload Javascript


// We obtained the code from 
// https://uk.tradingview.com/lightweight-charts/
// https://jsfiddle.net/TradingView/eaod9Lq8/

// This chart is the first one on the top of the page
// The chart uses the data we saved in /history, which are based on the inputs of the user 
// Then we had the live trade data to the historical trade data


var chart = LightweightCharts.createChart(document.getElementById('chart_custom'), {
	width: 600,
    height: 300,
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
//   upColor: 'rgba(255, 144, 0, 1)',
  upColor: '#00ff00',
  downColor: '#ff0000',
  borderDownColor: '#ff0000',
  borderUpColor: '#00ff00',
  wickDownColor: '#ff0000',
  wickUpColor: '#00ff00',
});




// // Below is the code to pull the historical data saved in /history to the chart
// // the data is already formated the right way

fetch('http://127.0.0.1:5000/history')
	.then((r) => r.json())
	.then((response) => {
		console.log(response)

		candleSeries.setData(response);
	})


// // Now we are adding to our historical datas the live trades coming from the Binance websocket
// // we use https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams

var BinanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_15m");
BinanceSocket.onmessage = function(event) {
	// console.log(event.data);
	var message = JSON.parse(event.data);
	var candlestick = message.k;
	candleSeries.update({
		time: candlestick.t / 1000,
		// time: Date.now(),
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}
// ISSUE : We do not want to update the chart with new trade data if the user specified an end_date and/or an end_time
// ISSUE : We only want the live trade data to be added to the chart if the user didn't specify the end_date or the end_time




// below is useless. it is the format of the data for the chart, i keep it just in case, just to try if the chart works

// candleSeries.setData([
// 	{ time: '2018-10-19', open: 180.34, high: 180.99, low: 178.57, close: 9.85 },
// 	{ time: '2018-10-22', open: 180.82, high: 181.40, low: 177.56, close: 178.75 },
// 	{ time: '2018-10-23', open: 175.77, high: 179.49, low: 175.44, close: 178.53 },
// 	{ time: '2018-10-24', open: 178.58, high: 182.37, low: 176.31, close: 176.97 },
// 	{ time: '2018-10-25', open: 177.52, high: 180.50, low: 176.83, close: 179.07 },
// 	{ time: '2018-10-26', open: 176.88, high: 177.34, low: 170.91, close: 172.23 },
// 	{ time: '2018-10-29', open: 173.74, high: 175.99, low: 170.95, close: 173.20 },
// 	{ time: '2018-10-30', open: 173.16, high: 176.43, low: 172.64, close: 176.24 },
// 	{ time: '2018-10-31', open: 177.98, high: 178.85, low: 175.59, close: 175.88 },
// 	{ time: '2018-11-01', open: 176.84, high: 180.86, low: 175.90, close: 180.46 },
// 	{ time: '2018-11-02', open: 182.47, high: 183.01, low: 177.39, close: 179.93 },
// 	{ time: '2018-11-05', open: 181.02, high: 182.41, low: 179.30, close: 182.19 },
// 	{ time: '2018-11-06', open: 181.93, high: 182.65, low: 180.05, close: 182.01 },
// 	{ time: '2018-11-07', open: 183.79, high: 187.68, low: 182.06, close: 187.23 },
// 	{ time: '2018-11-08', open: 187.13, high: 188.69, low: 185.72, close: 188.00 },
// 	{ time: '2018-11-09', open: 8.32, high: 8.48, low: 4.96, close: 5.99 },
// ]);

