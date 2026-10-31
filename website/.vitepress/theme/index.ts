import DefaultTheme from "vitepress/theme";
import type { Theme } from "vitepress";

import BilibiliBadge from "./components/BilibiliBadge.vue";
import HardwareCard from "./components/HardwareCard.vue";
import ProjectCard from "./components/ProjectCard.vue";
import VersionTable from "./components/VersionTable.vue";
import "./custom.css";

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component("BilibiliBadge", BilibiliBadge);
    app.component("HardwareCard", HardwareCard);
    app.component("ProjectCard", ProjectCard);
    app.component("VersionTable", VersionTable);
  },
} satisfies Theme;
