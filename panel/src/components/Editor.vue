<template>
  <codemirror
    ref="editor"
    v-model="code"
    :options="cmOptions"
    class="code"
    @ready="onCmReady"
  />
</template>

<script>
import { codemirror } from "vue-codemirror";

// import base style
import "codemirror/lib/codemirror.css";

// language
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/clike/clike.js"; //contain C C++ Java
import "codemirror/mode/python/python.js";

//theme css
import "codemirror/theme/monokai.css";
import "codemirror/theme/neat.css";
import "codemirror/theme/cobalt.css";

//hint
import "codemirror/addon/hint/show-hint.js";
import "codemirror/addon/hint/show-hint.css";
import "codemirror/addon/hint/javascript-hint.js";
import "codemirror/addon/selection/active-line.js";

//other addon
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/comment/comment.js";

// vuex
import { mapState } from "vuex";
import { mapGetters } from "vuex";

export default {
  components: {
    codemirror,
  },
  data() {
    return {
      // code: "",
      cmOptions: {
        tabSize: 2,
        mode: "text/javascript",
        theme: "default",
        lineNumbers: true,
        line: true,
        autoCloseBrackets: true,
        smartIndent: true,
        indentUnit: 2,
        extraKeys: {
          "Ctrl-/": "toggleComment",
        },
      },
    };
  },
  props:["code"],
  mounted() {
    console.log(this.code)
  },
  methods: {
    onCmReady(cm) {
      cm.setSize("100%", "100%");
      cm.on("keypress", () => {
        cm.showHint({ completeSingle: false });
      });
    },
  },
  computed: {
    ...mapState(["theme"]),
    ...mapGetters(["editorLanguage"]),
    codemirror() {
      return this.$refs.editor.codemirror;
    },
    getUserCode() {
      console.log(this.codemirror.getValue());
      return this.codemirror.getValue();
    },
  },
  watch: {
    editorLanguage: function () {
      this.codemirror.setOption("mode", this.editorLanguage);
      this.codemirror.refresh();
    },
    theme: function () {
      this.codemirror.setOption("theme", this.theme);
    },
    code(){
      this.UserCode = this.codemirror.getValue();
      this.codemirror.refresh();
      this.$emit('getCode', this.UserCode)
      // this.$store.commit("submitCode", this.UserCode);
    }
  },
  created() {
    this.$bus.$on("runCode", () => {
      this.$store.commit("submitCode", this.getUserCode);
    });
  },
  beforeDestroy() {
    this.$bus.$off("runCode");
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&display=swap");

.CodeMirror * {
  font-family: "JetBrains Mono", monospace;
}
.vue-codemirror {
  width: 75%;
  height: Calc(100%-64px);
  display: inline-block;
}

.code{
  height: 90vh;
}
</style>
