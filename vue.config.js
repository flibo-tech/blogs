module.exports = {
  transpileDependencies: ["vuetify"],

  pluginOptions: {
    prerenderSpa: {
      registry: undefined,
      renderRoutes: [
        "/",
        "/movies-like-the-shawshank-redemption",
        "/movies-like-fight-club",
        "/movies-like-her",
        "/shows-like-game-of-thrones",
      ],
      useRenderEvent: true,
      headless: true,
      onlyProduction: true,
    },
  },
};
