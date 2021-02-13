<template>
  <div>
    <section class="container" v-if="title">
      <div class="row">
        <div class="col-12">
          <v-breadcrumbs :items="navigation_links"></v-breadcrumbs>
          <v-img
            class="article-movie-poster"
            :src="poster.replace('/w500/', '/w780/')"
            alt=""
            aspect-ratio="2"
          ></v-img>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="article-similar-container">
            <h1>
              Top {{ similar_contents.length }} awesome
              {{ is_movie ? "movies" : "shows" }} like {{ title }} that you will
              enjoy watching
            </h1>

            <p>
              You just finished watching {{ title }} and you can't get over how
              good this {{ is_movie ? "movie" : "show" }} was. Now you want to
              watch more of such masterpieces. We have curated a list of similar
              {{ is_movie ? "movies" : "shows" }} which are created by the likes
              of
              <span v-if="main_artists.length == 3"
                >{{ main_artists[0] }}, {{ main_artists[1] }} and
                {{ main_artists[2] }}</span
              >
              <span v-if="main_artists.length == 2"
                >{{ main_artists[0] }} and {{ main_artists[1] }}</span
              >
              <span v-if="main_artists.length == 1">{{ main_artists[0] }}</span>
              . Here goes the list -
            </p>

            <ol>
              <div class="row">
                <div class="col-6">
                  <li
                    v-for="(item, index) in similar_contents.slice(0, 5)"
                    :key="index"
                  >
                    {{ item.title }}
                  </li>
                </div>

                <div class="col-6">
                  <li
                    v-for="(item, index) in similar_contents.slice(5)"
                    :key="index"
                  >
                    {{ item.title }}
                  </li>
                </div>
              </div>
            </ol>

            <div class="row" style="justify-content: center">
              <div class="col-md-12" style="text-align: center">
                <img
                  class="animal-review lazy"
                  :data-src="
                    require(`../assets/images/animal-review-${
                      Math.floor(Math.random() * 7) + 1
                    }.jpg`)
                  "
                  alt="animal-review"
                />

                <div align="center">
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
            </div>

            <ol class="movie-list">
              <li v-for="(item, index) in similar_contents" :key="index">
                <div class="row">
                  <div class="col-md-5 movie-poster-small">
                    <img
                      class="article-poster lazy"
                      :data-src="item.poster"
                      :alt="item.title"
                    />
                  </div>

                  <!-- MOVIE CONTENT -->
                  <div class="col-md-7">
                    <div class="movie-content">
                      <h2>
                        <a
                          style="color: #333; text-decoration: none"
                          :href="
                            store.app_host +
                            'content/' +
                            item.content_id +
                            '/' +
                            item.title
                              .replace(/[^a-z0-9]+/gi, '-')
                              .toLowerCase()
                          "
                          target="_blank"
                          >{{ item.title }}</a
                        >
                      </h2>

                      <!--  -->
                      <p>{{ item.summary_text }}</p>
                      <p>
                        This {{ is_movie ? "movie" : "show" }}, created by
                        {{ artistConcat(item.main_artists) }}, scores
                        {{ item.imdb_score }} on IMDb.
                      </p>
                      <p>
                        Genres -
                        {{ item.genres.join(" | ").replace(/[/']+/gi, "") }}
                      </p>
                      <!--  -->
                      <p
                        v-if="
                          Object.keys(where_to_watch).length &&
                          where_to_watch[JSON.stringify(item.content_id)]
                            .streaming_info
                        "
                      >
                        <span style="white-space: pre-wrap"
                          >You can watch this on
                        </span>
                        <span
                          v-for="(
                            streaming_item, streaming_index
                          ) in where_to_watch[JSON.stringify(item.content_id)]
                            .streaming_info"
                          :key="streaming_index"
                        >
                          <span
                            style="white-space: pre-wrap"
                            v-if="
                              Object.keys(
                                where_to_watch[JSON.stringify(item.content_id)]
                                  .streaming_info
                              ).indexOf(streaming_index) ==
                                Object.keys(
                                  where_to_watch[
                                    JSON.stringify(item.content_id)
                                  ].streaming_info
                                ).length -
                                  1 &&
                              Object.keys(
                                where_to_watch[JSON.stringify(item.content_id)]
                                  .streaming_info
                              ).indexOf(streaming_index) != 0
                            "
                          >
                            and
                          </span>

                          <span
                            v-else-if="
                              Object.keys(
                                where_to_watch[JSON.stringify(item.content_id)]
                                  .streaming_info
                              ).indexOf(streaming_index) != 0
                            "
                            >,
                          </span>

                          <a
                            style="
                              font-weight: bold;
                              color: #333;
                              text-decoration: none;
                            "
                            :href="streaming_item"
                            target="_blank"
                            >{{
                              streaming_index
                                .replace(/[_]+/gi, " ")
                                .replace(/(^|\s)\S/g, function (t) {
                                  return t.toUpperCase();
                                })
                            }}</a
                          > </span
                        >.
                      </p>
                      <!-- TRAILER -->
                      <v-btn
                        v-if="item.youtube_trailer_id"
                        style="text-decoration: none"
                        :href="
                          'https://www.youtube.com/watch?v=' +
                          item.youtube_trailer_id
                        "
                        target="_blank"
                      >
                        Watch Trailer
                      </v-btn>
                      <!--  -->
                    </div>
                  </div>
                  <!--  -->
                </div>

                <div
                  v-if="index == 2"
                  class="row"
                  style="justify-content: center"
                >
                  <div class="col-md-12" style="text-align: center">
                    <img
                      class="animal-review lazy"
                      :data-src="
                        require(`../assets/images/swipe-screenshot.webp`)
                      "
                      alt="swipe-card"
                    />

                    <div align="center">
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
                </div>
              </li>
            </ol>
          </div>
          <!--  -->
          <!-- FLIBO AD -->
          <div class="row">
            <div class="col-md-12 flibo-ad">
              <a
                href="https://play.google.com/store/apps/details?id=com.pivot.flibo&referrer=utm_source%3Dflibo-blogs"
                target="_blank"
                ><img
                  :data-src="require(`../assets/images/${fliboAd}`)"
                  alt="Download Flibo app"
                  class="lazy"
              /></a>
            </div>
          </div>
          <!-- FLIBO AD ENDS -->
        </div>
        <!--  -->
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import { mixin as onClickOutside } from "vue-on-click-outside";
export default {
  name: "Article",
  mixins: [onClickOutside],
  metaInfo() {
    if (this.title) {
      return {
        title: this.meta_title,
        meta: [
          {
            vmid: "description",
            name: "description",
            content: this.meta_description,
          },
          {
            vmid: "og:title",
            property: "og:title",
            content: this.meta_title,
          },
          {
            vmid: "og:description",
            property: "og:description",
            content: this.meta_description,
          },
          {
            vmid: "og:image",
            property: "og:image",
            content: this.poster.replace("/w500/", "/w780/"),
          },
          {
            vmid: "twitter:title",
            name: "twitter:title",
            content: this.meta_title,
          },
          {
            vmid: "twitter:description",
            name: "twitter:description",
            content: this.meta_description,
          },
          {
            vmid: "twitter:image",
            name: "twitter:image",
            content: this.poster.replace("/w500/", "/w780/"),
          },
        ],
      };
    }
  },
  data: function () {
    return {
      dialog: false, // for popup
      fliboAd: "flibo-ad.png", // FLIBO AD image
      store: this.$store.state,
      is_mobile: window.screen.height > window.screen.width,
      content_name: null,
      is_movie: false,
      is_show: false,
      content_id: null,
      title: null,
      poster: null,
      main_artists: [],
      release_year: null,
      similar_contents: [],
      where_to_watch: {},
      play_trailer_index: null,
      play_trailer: false,
      lazyloadImages: [],
      lazyloadThrottleTimeout: null,
    };
  },
  created() {
    var self = this;
    this.content_name = this.$route.params.content_name_piece
      .replace("movies-like-", "")
      .replace("shows-like-", "");
    this.is_movie = this.$route.params.content_name_piece.startsWith(
      "movies-like-"
    );
    this.is_show = this.$route.params.content_name_piece.startsWith(
      "shows-like-"
    );
    axios
      .post(self.$store.state.api_host + "similar_contents_for_blog", {
        content_name: self.content_name,
        content_type: self.is_movie ? "movie" : "tv",
        guest_id: self.$store.state.guest_id,
      })
      .then(function (response) {
        if (response.status == 200) {
          self.content_id = response.data.content_id;
          self.title = response.data.title;
          self.poster = response.data.poster;
          self.main_artists = response.data.main_artists;
          self.release_year = response.data.release_year;
          self.similar_contents = response.data.similar_contents;

          var content_ids = [];
          var x;
          for (x in self.similar_contents) {
            content_ids.push(self.similar_contents[x].content_id);
          }
          if (self.$store.state.guest_country != null) {
            axios
              .post(
                self.$store.state.api_host + "where_to_watch_similar_content",
                {
                  content_ids: content_ids,
                  country: self.$store.state.guest_country,
                }
              )
              .then(function (response) {
                if (response.status == 200) {
                  self.where_to_watch = response.data;
                  document.dispatchEvent(new Event("x-app-rendered"));
                } else {
                  document.dispatchEvent(new Event("x-app-rendered"));
                }
              });
          } else {
            setTimeout(
              axios
                .post(
                  self.$store.state.api_host + "where_to_watch_similar_content",
                  {
                    content_ids: content_ids,
                    country: self.$store.state.guest_country || "United States",
                  }
                )
                .then(function (response) {
                  if (response.status == 200) {
                    self.where_to_watch = response.data;
                    document.dispatchEvent(new Event("x-app-rendered"));
                  } else {
                    document.dispatchEvent(new Event("x-app-rendered"));
                  }
                }),
              500
            );
          }
        }
      })
      .catch(function (error) {
        // console.log(error);
      });
  },
  computed: {
    navigation_links: function () {
      var crumbs = [
        {
          text: "Home",
          disabled: false,
          href: "/",
        },
        {
          text: (this.is_movie ? "Movies" : "Shows") + " like " + this.title,
          disabled: true,
          href: this.$route.path,
        },
      ];
      return crumbs;
    },
    meta_title: function () {
      return (
        "Top " +
        this.similar_contents.length +
        " awesome " +
        (this.is_movie ? "movies" : "shows") +
        " like " +
        this.title +
        " that you will enjoy watching"
      );
    },
    meta_description: function () {
      return (
        "Are you looking for " +
        (this.is_movie ? "movies" : "shows") +
        " like " +
        this.title +
        "? We have curated a list for you, a list of " +
        (this.is_movie ? "movies" : "shows") +
        " by the likes of " +
        [
          this.main_artists.slice(0, -1).join(", "),
          this.main_artists.slice(-1)[0],
        ].join(this.main_artists.length < 2 ? "" : " and ") +
        "."
      );
    },
  },
  methods: {
    artistConcat(artists) {
      return [artists.slice(0, -1).join(", "), artists.slice(-1)[0]].join(
        artists.length < 2 ? "" : " and "
      );
    },
    lazyload() {
      var self = this;
      if (self.lazyloadImages.length == 0) {
        self.lazyloadImages = document.querySelectorAll("img.lazy");
      }
      if (self.lazyloadThrottleTimeout) {
        clearTimeout(self.lazyloadThrottleTimeout);
      }

      self.lazyloadThrottleTimeout = setTimeout(function () {
        var scrollTop = window.pageYOffset;
        self.lazyloadImages.forEach(function (img) {
          if (img.y - 200 < window.innerHeight) {
            img.src = img.dataset.src;
            img.classList.remove("lazy");
            self.lazyloadImages = document.querySelectorAll("img.lazy");
          }
        });
        if (self.lazyloadImages.length == 0) {
          document.removeEventListener("scroll", self.lazyload);
        }
      }, 20);
    },
  },
  mounted() {
    document.addEventListener("scroll", this.lazyload);
  },
  beforeDestroy() {
    document.removeEventListener("scroll", this.lazyload);
  },
};
</script>

<style lang="scss" scoped>
ol {
  list-style: none;
  counter-reset: article-counter;
  //   columns: 2;
  //   -webkit-columns: 2;
  //   -moz-columns: 2;
}
ol li {
  position: relative;
  padding-left: 25px;
  counter-increment: article-counter;
  margin: 25px 0;
}
ol li::before {
  display: inline-block;
  content: counter(article-counter);
  position: absolute;
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 1px;
  font-size: 1.6rem;
  font-weight: bold;
  top: -8px;
  left: -25px;
  border-radius: 50%;
  background-color: #e8e8e8;
}

ol.movie-list {
  padding-left: 0;
}
ol.movie-list li {
  padding-left: 0px;
}

ol.movie-list li::before {
  display: inline-block;
  content: counter(article-counter);
  position: absolute;
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 1px;
  font-size: 1.6rem;
  font-weight: bold;
  top: 22px;
  left: 10px;
  border-radius: 50%;
  background-color: #e8e8e8;
  z-index: 2;
}

.blog-black-background {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.75);
  display: table;
  top: 0%;
  left: 0%;
  z-index: 100000;
}
.blog-youtube-player-header {
  position: fixed;
  top: calc(50vh - 28.125vw - 20vh - 25px);
  left: 10px;
  z-index: 100001;
  white-space: initial;
  font-size: 25px;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.05;
  letter-spacing: normal;
  text-align: center;
  color: #ffffff;
}
.blog-youtube-player-loader {
  border: 10px solid #f3f3f3;
  border-top: 10px solid #3498db;
  border-radius: 50%;
  width: 14vw;
  height: 14vw;
  animation: spin 2s linear infinite;
  position: fixed;
  top: calc(50vh - 20vh - 7vw);
  left: calc(50% - 7vw);
  z-index: 100000;
}
.desktop-blog-youtube-player-loader {
  border: 10px solid #f3f3f3;
  border-top: 10px solid #3498db;
  border-radius: 50%;
  width: 75px;
  height: 75px;
  animation: spin 2s linear infinite;
  position: fixed;
  top: 312.5px;
  left: calc(50vw - 37.5px);
  z-index: 100000;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.blog-youtube-player {
  position: fixed;
  width: 100vw;
  height: 56.25vw;
  top: calc(50vh - 28.125vw - 20vh);
  left: 0;
  z-index: 100001;
}
.blog-youtube-player-platforms {
  display: inline-flex;
  overflow: scroll;
  max-width: 100%;
}
.blog-youtube-player-platform-cropper {
  width: 50px;
  height: 50px;
  position: relative;
  overflow: hidden;
  border-radius: 20%;
}
.blog-youtube-player-platform-icon {
  display: inline-block;
  position: absolute;
  width: 100%;
  margin-left: -50%;
}
.blog-youtube-player-platforms-container {
  display: inline-block;
  vertical-align: top;
  text-align: center;
  margin: 20px 10px 0px 10px;
  cursor: pointer;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  -webkit-tap-highlight-color: transparent;
}
.blog-tap-to-watch-text {
  white-space: nowrap;
  font-size: 20px;
  font-weight: bold;
  font-style: normal;
  font-stretch: normal;
  line-height: 1.05;
  letter-spacing: normal;
  text-align: center;
  color: #333333;
}
.blog-youtube-player-streaming-box {
  position: fixed;
  bottom: 150px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100001;
  background-color: #ffffff;
  border-radius: 7px;
  padding: 10px;
  max-width: 95vw;
  text-align: center;
}
::-webkit-scrollbar {
  display: none;
}
.article-poster {
  width: 100%;
  max-width: 500px;
}
.animal-review {
  width: 100%;
  max-width: 500px;
}
.article-similar-container {
  max-width: 800px;
  margin: 0 auto;
}
.videoWrapper {
  position: relative;
  /* padding-bottom: 56.25%; /* 16:9 */
  padding-bottom: 60.25%; /*  */
  padding-top: 25px;
  height: 0;
  background-color: #ddd;
}
.videoWrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.movie-content {
  padding-left: 20px;
}

.article-movie-poster {
  border-radius: 21px;
}

.flibo-ad img {
  width: 100%;
}

@media (max-width: 720px) {
  .movie-content {
    padding-left: 0px;
  }
  .movie-poster-small {
    text-align: left;
    padding-right: 80px !important;
  }

  .flibo-ad img {
    // width: calc(100% + 48px);
    // position: relative;
    // left: -24px;
  }
}
</style>