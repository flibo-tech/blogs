<template>
  <v-app>
    <v-app-bar app flat color="white" height="90" class="top-bar">
      <section class="container">
        <div class="row">
          <div class="col-6">
            <router-link to="/">
              <v-img
                alt="Vuetify Logo"
                class="shrink mr-2"
                contain
                src="https://flibo-images.s3-us-west-2.amazonaws.com/logos/flibo-logo.svg"
                transition="scale-transition"
                width="120"
              />
            </router-link>
          </div>
          <div class="col-6" align="right">
            <v-btn
              href="https://play.google.com/store/apps/details?id=com.pivot.flibo&referrer=utm_source%3Dflibo-blogs"
              target="_blank"
              class="f-primary download-btn"
              large
            >
              <span class="mr-2">Download App</span>
            </v-btn>
          </div>
        </div>
      </section>

      <!-- <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://flibo-images.s3-us-west-2.amazonaws.com/logos/flibo-logo.svg"
          transition="scale-transition"
          width="120"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://play.google.com/store/apps/details?id=com.pivot.flibo&referrer=utm_source%3Dflibo-blogs"
        target="_blank"
      >
        <span class="mr-2">Download App</span>
      </v-btn> -->
    </v-app-bar>

    <v-content>
      <router-view
        :article_raw="article_container"
        :description="article_description"
        :title="article_title"
        :image="article_image"
      />
    </v-content>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "App",

  components: {},

  metaInfo() {
    if (this.update_meta) {
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
            content: this.store.blog_host + this.$route.path,
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
            content: this.store.blog_host + this.$route.path,
          },
          {
            vmid: "twitter:image",
            name: "twitter:image",
            content:
              "https://flibo-images.s3-us-west-2.amazonaws.com/covers/login-cover.jpg",
          },
        ],
      };
    }
  },

  data() {
    return {
      store: this.$store.state,
      update_meta: false,
      article_container: null,
      article_description: null,
      article_title: null,
      article_image: null,
    };
  },
  created() {
    this.article_container = document.getElementById("article_container");
    if (this.article_container) {
      this.article_container = this.article_container.outerHTML;

      this.article_metas = document.getElementsByTagName("meta");
      for (let i = 0; i < this.article_metas.length; i++) {
        if (this.article_metas[i].getAttribute("name") == "description") {
          this.article_description = this.article_metas[i].getAttribute(
            "content"
          );
        }

        if (this.article_metas[i].getAttribute("name") == "twitter:title") {
          this.article_title = this.article_metas[i].getAttribute("content");
        }

        if (this.article_metas[i].getAttribute("name") == "twitter:image") {
          this.article_image = this.article_metas[i].getAttribute("content");
        }
      }
    }

    if (this.article_container == null) {
      this.update_meta = true;
      this.$store.state.guest_country = "United States";
      this.$store.state.guest_id = "blog_prerenderer";
    }
  },
  computed: {
    my_store: function () {
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
//import bootstrap grid
@import "~bootstrap/scss/bootstrap-grid";

a {
  text-decoration: underline !important;
  color: #212121 !important;
}
a:link {
}
a:hover {
  color: #4256f6 !important;
}
h1 {
  font-size: 2.8rem;
  line-height: 120%;
  margin: 1.5rem 0 1rem;
}
h2 {
  margin: 0 0 0.6rem;
}
img {
  border-radius: 8px;
}
.f-primary {
  background: linear-gradient(90deg, #8347da, #4256f6) !important;
  color: #ffffff !important;
  text-decoration: none !important;
  // background: aquamarine !important;
}
a.f-primary {
  color: #ffffff !important;
}
.theme--light.v-breadcrumbs .v-breadcrumbs__divider,
.theme--light.v-breadcrumbs .v-breadcrumbs__item--disabled {
  color: rgba(0, 0, 0, 0.38) !important;
  text-decoration: none !important;
}

.download-btn {
  margin-top: 12px;
}

footer {
  text-align: center;
  color: rgba(0, 0, 0, 0.38);
  margin: 20px 0;
}

@media (min-width: 1904px) {
  .container {
    max-width: 1185px !important;
  }
}
@media (max-width: 720px) {
  .container {
    padding: 24px !important;
  }
}
</style>
