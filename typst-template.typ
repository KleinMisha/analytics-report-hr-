
// content boxes
#let grey_box(content) = {

  rect(
    width: 100%,
    height: 20%,
    fill: rgb("#f8f8f8")
  )[
    #content
  ]
}

#let dashed_box(content) = {
  rect(
    width: 100%,
    height: 20%,
    stroke: (paint: rgb("#009ac9"), thickness: 1pt, dash: "dashed")
  )[
    #content
  ]
}
// horizontal lines between sections 
#let horizontal_line()={ 
  line(
    length:105%,
    stroke: 2pt + rgb("#009ac9"),
  
  )
  }

#let report(
  title: none,
  date: none,
  paper: "a4",
  // main content body
  body,
) = {

  // Configure the page properties
  set page(
    paper: paper,
    background: place(
        top,
        rect(
            width: 2cm,
            height: 100%,
            fill: rgb("#009ac9")
        )
    ), 
    margin: (bottom: 1cm, top: 1cm, left: 2.5cm, right: 2.5cm),
  )

  // Configure text properties for main body 
  set text(
    lang: "en",
    region: "US",
    font: "Arial",
    size: 10pt,
  )

  // Configure text properties for headings 
  show heading: x => {
    let sizes = (
      "1": 24pt, // Heading level 1 
      "2": 16pt, // Heading level 2 
      "3": 12pt, // Heading level 3  
    )
    let level = str(x.level)
    let font_size = sizes.at(level)
    let formatted_heading = if level == "1" {upper(x)} else { x }
    let alignment = if level == "1" { left } else { center}

    set text(
      font: "Bitter",
      fill: rgb("#009ac9"),
      size: font_size,
      weight: "bold",
    )
    align(alignment)[#formatted_heading]



  }

  page(align(left + top)[
    #h(-1cm)
    #box(
        fill: rgb("#00aadeff"),
        width: 0.7fr,
        inset: 10pt,
    )[
        #text(size: 2.0em, fill: white)[*#title*]
    ]
    #body
  ])
}