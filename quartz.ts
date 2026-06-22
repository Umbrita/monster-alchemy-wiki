import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import LeafletMap from "./quartz/components/LeafletMap"

const config = await loadQuartzConfig()
export default config

export const layout = await loadQuartzLayout({
  defaults: {
    afterBody: [LeafletMap],
  },
})