import { QuartzComponent, QuartzComponentProps } from "./types"

const LeafletMap: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
  if (fileData.slug !== "map/index") return <></>

  const markers = (fileData.frontmatter?.mapMarkers as any[]) ?? []
  const markersJson = JSON.stringify(markers)

  return (
    <>
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
      <div id="wiki-map" class="leaflet-map-container"></div>
      <script
        type="text/javascript"
        dangerouslySetInnerHTML={{ __html: `window.__MAP_MARKERS__ = ${markersJson};` }}
      />
      <script src="/static/leaflet-map.js" defer />
    </>
  )
}

export default LeafletMap