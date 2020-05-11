const CompressionPlugin = require("compression-webpack-plugin");

module.exports = {
  configureWebpack: {
    plugins: [
      new CompressionPlugin({
        filename: "[path].gz[query]",
        algorithm: "gzip",
        test: /\.js$|\.css$|\.html$/,
        threshold: 10240,
        minRatio: 0.8,
      }),
    ],
  },
  transpileDependencies: ["vuetify"],

  pluginOptions: {
    prerenderSpa: {
      registry: undefined,
      renderRoutes: [
        "/",
        "/movies-like-the-shawshank-redemption",
        "/movies-like-the-dark-knight",
        "/movies-like-inception",
        "/movies-like-fight-club",
        "/movies-like-pulp-fiction",
        "/shows-like-game-of-thrones",
        "/movies-like-forrest-gump",
        "/movies-like-the-lord-of-the-rings-the-fellowship-of-the-ring",
        "/movies-like-the-matrix",
        "/movies-like-the-lord-of-the-rings-the-return-of-the-king",
        "/movies-like-the-godfather",
        "/movies-like-the-dark-knight-rises",
        "/movies-like-the-lord-of-the-rings-the-two-towers",
        "/shows-like-breaking-bad",
        "/movies-like-se7en",
      ],
      useRenderEvent: true,
      headless: true,
      onlyProduction: true,
    },
  },
};
