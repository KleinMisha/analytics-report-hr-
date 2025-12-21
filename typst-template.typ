#let text-box(body)={
    block(fill: rgb("#E6E6E6"))[
        #body 
    ]
}

#let article(
  title: "default",
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
            fill: rgb("#58508d")
        )
    ), 
    margin: (bottom: 1cm, top: 1cm, left: 2.5cm, right: 2.5cm),
  )

  page(align(left + top)[
    #h(-1cm)
    #box(
        fill: rgb("#7D72CA"),
        width: 0.7fr,
        inset: 10pt,
    )[
        #text(size: 2.0em, fill: white)[*#title*]
    ]
    #body
  ])
}