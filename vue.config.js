module.exports = {
  transpileDependencies: ["vuetify"],

  pluginOptions: {
    prerenderSpa: {
      registry: undefined,
      renderRoutes: [
        "/",
        "/movies-like-the-shawshank-redemption",
        "/movies-like-fight-club",
      ],
      useRenderEvent: true,
      headless: true,
      onlyProduction: true,
    },
  },
};
