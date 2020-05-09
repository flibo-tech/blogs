<template>
  <div>
    <v-container class="fill-height">
      <v-row>
        <v-col>
          <v-img
            :src="poster.replace('/w500/', '/w1280/')"
            alt=""
            aspect-ratio="2"
          ></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
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
            <li v-for="(item, index) in similar_contents" :key="index">
              {{ item.title }}
            </li>
          </ol>

          <ol>
            <li v-for="(item, index) in similar_contents" :key="index">
              <v-row>
                <v-col>
                  <img
                    :src="item.poster.replace('/w500/', '/w342/')"
                    :alt="item.title"
                  />
                </v-col>
                <v-col>
                  <v-row>
                    <h2>{{ item.title }}</h2>
                  </v-row>

                  <v-row>
                    {{ item.summary_text }}
                  </v-row>

                  <v-row>
                    You can watch this on
                    <span
                      v-for="(streaming_item,
                      streaming_index) in where_to_watch[
                        JSON.stringify(item.content_id)
                      ].streaming_info"
                      :key="streaming_index"
                    >
                      {{ streaming_index + ", " }}
                    </span>
                  </v-row>
                </v-col>
              </v-row>
            </li>
          </ol>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Article",
  data: function() {
    return {
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
      .then(function(response) {
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
              .then(function(response) {
                if (response.status == 200) {
                  self.where_to_watch = response.data;
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
                .then(function(response) {
                  if (response.status == 200) {
                    self.where_to_watch = response.data;
                  }
                }),
              500
            );
          }
        }
      })
      .catch(function(error) {
        // console.log(error);
      });
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
</style>
