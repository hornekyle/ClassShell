#let formatter(
	title: none,
	doc
) = {
	set page("us-letter",margin:(
			top: 0.5in,
			bottom: 0.5in,
			left: 0.5in,
			right: 0.5in,
		))
	set par(
		justify: true,
		first-line-indent: 1.5em,
		spacing: 1em,
	)
	set text(
		font: "IBM Plex Serif",
		size: 11pt,
	)
	show heading: set block(
		above: 1.5em,
		below: 1em,
	)
	show heading: set text(font: "IBM Plex Sans")
	show heading.where(level: 1): set text(size: 13pt)
	show heading.where(level: 2): set text(
		size: 11pt,
		style: "italic",
	)
	show math.equation: set text(font: "Euler Math", size:10pt, fallback: false)
	show math.equation.where(block: true): set align(left)
	
	text(
		font: "IBM Plex Sans",
		size: 18pt,
		weight: "bold",
	)[#title]
	
	doc
}
