<template>
  <v-app>
    <v-app-bar app flat color="white" height="120" class="top-bar">
      <v-container>
        <v-row>
          <v-col>
            <v-img
              alt="Vuetify Logo"
              class="shrink mr-2"
              contain
              src="./assets/flibo-logo.svg"
              transition="scale-transition"
              width="120"
            />
          </v-col>
          <v-col align="right">
            <v-btn
              href="https://play.google.com/store/apps/details?id=com.pivot.flibo"
              target="_blank"
              class="f-primary"
              large
            >
              <span class="mr-2">Download App</span>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

      <!-- <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="./assets/flibo-logo.svg"
          transition="scale-transition"
          width="120"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://play.google.com/store/apps/details?id=com.pivot.flibo"
        target="_blank"
      >
        <span class="mr-2">Download App</span>
      </v-btn> -->
    </v-app-bar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "App",

  components: {},

  data: () => ({
    //
  })
};
</script>

<style lang="scss">
.f-primary {
  background: linear-gradient(90deg, #8347da, #4256f6) !important;
  color: #ffffff !important;
  // background: aquamarine !important;
}

@media (min-width: 1904px) {
  .container {
    max-width: 1185px !important;
  }
}
</style>
