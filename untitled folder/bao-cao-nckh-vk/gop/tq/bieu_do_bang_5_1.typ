#import "@preview/cetz:0.3.4" as cetz: canvas, draw

#set page(width: 17cm, height: 9.8cm, margin: (x: 0.6cm, y: 0.6cm))
#set text(font: "Times New Roman", size: 10pt)

#align(center)[
  #canvas({
    import draw: *

    // ================= LEFT CHART: Số lượng mẫu (Mẫu thử & Đúng) =================
    let x-start = 0.85
    let w1 = 6.3
    let h1 = 5.2
    let max1 = 600

    let items1 = (
      (label: [Hữu cơ\ (`organic`)], total: 389, correct: 346),
      (label: [Vô cơ\ (`inorganic`)], total: 503, correct: 472),
      (label: [Khác\ (`other`)], total: 308, correct: 239),
    )

    let c-blue = rgb("#2563eb")
    let c-green = rgb("#059669")
    let c-purple = rgb("#7c3aed")
    let c-orange = rgb("#d97706")
    let c-dark = rgb("#1e293b")
    let c-gray = rgb("#64748b")
    let c-grid = rgb("#e2e8f0")

    // Left Title
    content((x-start + w1 / 2, h1 + 1.25), text(weight: "bold", size: 10pt, fill: c-dark)[(a) Số lượng mẫu thử và nhận diện đúng])

    // Left Legend
    rect((x-start + w1/2 - 2.8, h1 + 0.65), (x-start + w1/2 - 2.2, h1 + 0.9), fill: c-blue, radius: 1.5pt)
    content((x-start + w1/2 - 2.0, h1 + 0.77), text(size: 8.5pt, fill: c-dark)[Số lần chụp], anchor: "west")

    rect((x-start + w1/2 + 0.5, h1 + 0.65), (x-start + w1/2 + 1.1, h1 + 0.9), fill: c-green, radius: 1.5pt)
    content((x-start + w1/2 + 1.3, h1 + 0.77), text(size: 8.5pt, fill: c-dark)[Nhận diện đúng], anchor: "west")

    // Left Grid
    for i in range(7) {
      let y = (i / 6) * h1
      let val = int(i * 100)
      line((x-start, y), (x-start + w1, y), stroke: (paint: c-grid, thickness: 0.6pt, dash: if i > 0 { "dashed" } else { "solid" }))
      content((x-start - 0.15, y), align(right)[#text(size: 8pt, fill: c-gray)[#val]], anchor: "east")
    }
    content((x-start - 0.75, h1 / 2), angle: 90deg, text(weight: "bold", size: 8.5pt, fill: c-dark)[Số lượng mẫu (lượt)])

    // Left Bars
    let gw1 = w1 / items1.len()
    let bw1 = 0.78
    let g1 = 0.12

    for (idx, it) in items1.enumerate() {
      let cx = x-start + (idx + 0.5) * gw1
      let x1 = cx - bw1 - g1 / 2
      let x2 = cx + g1 / 2

      let y1 = (it.total / max1) * h1
      let y2 = (it.correct / max1) * h1

      // Total bar
      rect((x1, 0), (x1 + bw1, y1), fill: c-blue, stroke: (paint: c-blue.darken(15%), thickness: 0.4pt), radius: (top: 2.5pt))
      content((x1 + bw1 / 2, y1 + 0.15), text(weight: "bold", size: 8pt, fill: c-blue.darken(25%))[#it.total], anchor: "south")

      // Correct bar
      rect((x2, 0), (x2 + bw1, y2), fill: c-green, stroke: (paint: c-green.darken(15%), thickness: 0.4pt), radius: (top: 2.5pt))
      content((x2 + bw1 / 2, y2 + 0.15), text(weight: "bold", size: 8pt, fill: c-green.darken(25%))[#it.correct], anchor: "south")

      // Category label
      content((cx, -0.3), align(center)[#text(weight: "bold", size: 9pt, fill: c-dark)[#it.label]], anchor: "north")
    }

    // ================= RIGHT CHART: Tỉ lệ chính xác (%) =================
    let ox = 9.2 // Offset X for right chart
    let w2 = 6.2
    let h2 = 5.2

    let items2 = (
      (label: [Hữu cơ], rate: 88.95, text: "88,95%"),
      (label: [Vô cơ], rate: 93.84, text: "93,84%"),
      (label: [Khác], rate: 77.60, text: "77,60%"),
      (label: [Tổng cộng], rate: 88.08, text: "88,08%"),
    )

    // Right Title
    content((ox + w2 / 2, h2 + 1.25), text(weight: "bold", size: 10pt, fill: c-dark)[(b) Tỉ lệ nhận diện chính xác theo nhóm])

    // Right Legend
    rect((ox + w2/2 - 2.8, h2 + 0.65), (ox + w2/2 - 2.2, h2 + 0.9), fill: c-purple, radius: 1.5pt)
    content((ox + w2/2 - 2.0, h2 + 0.77), text(size: 8pt, fill: c-dark)[Từng nhóm], anchor: "west")

    rect((ox + w2/2 - 0.3, h2 + 0.65), (ox + w2/2 + 0.3, h2 + 0.9), fill: c-orange, radius: 1.5pt)
    content((ox + w2/2 + 0.5, h2 + 0.77), text(size: 8pt, fill: c-dark)[Tổng thể], anchor: "west")

    line((ox + w2/2 + 1.9, h2 + 0.77), (ox + w2/2 + 2.5, h2 + 0.77), stroke: (paint: rgb("#dc2626"), thickness: 1pt, dash: "dashed"))
    content((ox + w2/2 + 2.65, h2 + 0.77), text(size: 8pt, fill: rgb("#dc2626"), weight: "bold")[TB (88,08%)], anchor: "west")

    // Right Grid (0% - 100%)
    for i in range(6) {
      let y = (i / 5) * h2
      let val = i * 20
      line((ox, y), (ox + w2, y), stroke: (paint: c-grid, thickness: 0.6pt, dash: if i > 0 { "dashed" } else { "solid" }))
      content((ox - 0.15, y), align(right)[#text(size: 8pt, fill: c-gray)[#val%]], anchor: "east")
    }
    content((ox - 0.8, h2 / 2), angle: 90deg, text(weight: "bold", size: 8.5pt, fill: c-dark)[Tỉ lệ chính xác (%)])

    // Average reference line across right chart
    let avg-y = (88.08 / 100) * h2
    line((ox, avg-y), (ox + w2, avg-y), stroke: (paint: rgb("#dc2626"), thickness: 0.8pt, dash: "dashed"))

    // Right Bars
    let gw2 = w2 / items2.len()
    let bw2 = 0.95

    for (idx, it) in items2.enumerate() {
      let cx = ox + (idx + 0.5) * gw2
      let x1 = cx - bw2 / 2
      let y1 = (it.rate / 100) * h2

      let bar-color = if idx == 3 { c-orange } else { c-purple }

      rect((x1, 0), (x1 + bw2, y1), fill: bar-color, stroke: (paint: bar-color.darken(15%), thickness: 0.4pt), radius: (top: 2.5pt))
      content((cx, y1 + 0.15), text(weight: "bold", size: 8pt, fill: bar-color.darken(25%))[#it.text], anchor: "south")

      // Category label
      content((cx, -0.3), align(center)[#text(weight: if idx == 3 { "bold" } else { "bold" }, size: 9pt, fill: if idx == 3 { c-orange.darken(20%) } else { c-dark })[#it.label]], anchor: "north")
    }

  })
]
