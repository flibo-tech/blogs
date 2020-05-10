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
import axios from "axios";
import DeviceDetector from "device-detector-js";
export default {
  name: "App",

  components: {},

  metaInfo() {
    return {
      title: "Discover Movies & TV Shows",
      meta: [
        {
          vmid: "description",
          name: "description",
          content:
            "You have so many streaming subscriptions but still cannot decide what to watch? We are here to help you personalize all your streaming apps. Swipe your way through clutter.",
        },
        {
          "http-equiv": "Content-Type",
          content: "text/html; charset=UTF-8",
        },
        {
          vmid: "viewport",
          name: "viewport",
          content: "width=device-width, initial-scale=1",
        },
        {
          vmid: "og:title",
          property: "og:title",
          content: "Discover Movies & TV Shows",
        },
        {
          vmid: "og:description",
          property: "og:description",
          content:
            "You have so many streaming subscriptions but still cannot decide what to watch? We are here to help you personalize all your streaming apps. Swipe your way through clutter.",
        },
        {
          vmid: "og:url",
          property: "og:url",
          content: window.location.href,
        },
        {
          vmid: "og:type",
          property: "og:type",
          content: "website",
        },
        {
          vmid: "og:image",
          property: "og:image",
          content:
            "https://flibo-images.s3-us-west-2.amazonaws.com/covers/login-cover.jpg",
        },
        {
          vmid: "twitter:card",
          name: "twitter:card",
          content: "summary",
        },
        {
          vmid: "twitter:title",
          name: "twitter:title",
          content: "Discover Movies & TV Shows",
        },
        {
          vmid: "twitter:description",
          name: "twitter:description",
          content:
            "You have so many streaming subscriptions but still cannot decide what to watch? We are here to help you personalize all your streaming apps. Swipe your way through clutter.",
        },
        {
          vmid: "twitter:url",
          name: "twitter:url",
          content: window.location.href,
        },
        {
          vmid: "twitter:image",
          name: "twitter:image",
          content:
            "https://flibo-images.s3-us-west-2.amazonaws.com/covers/login-cover.jpg",
        },
      ],
    };
  },

  data() {
    return {
      store: this.$store.state,
      ip_info: {
        ip: null,
        city: null,
        region: null,
        country: null,
        location: null,
        network_org: null,
        postal: null,
        timezone: null,
      },
    };
  },
  created() {
    var self = this;

    if (this.$store.state.guest_id == null) {
      var chars =
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
      var length = 16;
      var result = "";
      for (var i = length; i > 0; --i)
        result += chars[Math.floor(Math.random() * chars.length)];
      this.$store.state.guest_id = "blog_" + Date.now() + result;
    }
    if (this.$store.state.guest_country == null) {
      axios
        .get("https://ipinfo.io/?token=a354c067e1fef5")
        .then(function(response) {
          if ([200].includes(response.status)) {
            self.ip_info.ip = response.data.ip;
            self.ip_info.city = response.data.city;
            self.ip_info.region = response.data.region;
            self.ip_info.country = response.data.country;
            self.ip_info.location = response.data.loc;
            self.ip_info.network_org = response.data.org;
            self.ip_info.postal = response.data.postal;
            self.ip_info.timezone = response.data.timezone;

            if (
              Object.keys(self.$store.state.country_mappings).includes(
                self.ip_info.country
              )
            ) {
              self.$store.state.guest_country =
                self.$store.state.country_mappings[response.data.country];
            } else {
              self.$store.state.guest_country = "United States";
            }

            const deviceDetector = new DeviceDetector();
            const device = deviceDetector.parse(navigator.userAgent);

            axios.post(self.$store.state.api_host + "update_device_info", {
              user_id: null,
              session_id: null,
              guest_id: self.$store.state.guest_id,

              is_app: false,

              ip: self.ip_info.ip,
              city: self.ip_info.city,
              region: self.ip_info.region,
              country: self.ip_info.country,
              location: self.ip_info.location,
              network_org: self.ip_info.network_org,
              postal: self.ip_info.postal,
              timezone: self.ip_info.timezone,

              client_type: device.client.type,
              client_name: device.client.name,
              client_version: device.client.version,
              client_engine: device.client.engine,
              client_engine_version: device.client.engineVersion,

              os_name: device.os.name,
              os_version: device.os.version,
              os_platform: device.os.platform,

              device_type: device.device.type,
              device_brand: device.device.brand,
              device_model: device.device.model,

              bot: device.bot,

              screen_width: window.outerWidth,
              screen_height: window.outerHeight,
            });
          }
        });
    }
  },
  computed: {
    my_store: function() {
      return this.$store.state;
    },
  },
  watch: {
    my_store: {
      handler(val) {
        localStorage.setItem("my_store", JSON.stringify(this.my_store));
      },
      deep: true,
    },
  },
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
