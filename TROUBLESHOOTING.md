# Troubleshooting

## Poor Mosaic Decensorings/Mosaic Decensoring Does Nothing
The mosaic decensoring is a WIP feature. Poor results should be expected.

## Strange Color Decensors
If your decensor output looks like this, then the censored regions were not colored correctly.

![Bad decensor](/readme_images/mermaid_face_censored_bad_decensor.png)

*Make sure you have antialiasing off.*

Here are some examples of bad and good colorings:

|Image|Zoom|Comment|
|--- | --- | ---|
|![Incomplete coloring](/readme_images/mermaid_face_censored_bad_incomplete.png)|![Incomplete coloring](/readme_images/mermaid_face_censored_bad_incomplete_zoom.png)|Some censored pixels was left uncolored. Expand your selections to fully cover all censored regions.|
|![Bad edges](/readme_images/mermaid_face_censored_bad_edge.png)|![Bad edges](/readme_images/mermaid_face_censored_bad_edge_zoom.png)|Some pixels around the edges of the green regions are not pure green. This will cause the green to bleed into the decensors. Make sure anti-aliasing is off and to use a pencil tool and not a brush tool if possible.|
|![Perfect coloring!](/readme_images/mermaid_face_censored_good.png)|![Perfect coloring! The censored region is uniformly colored correctly.](/readme_images/mermaid_face_censored_good_zoom.png)|Perfect coloring!|