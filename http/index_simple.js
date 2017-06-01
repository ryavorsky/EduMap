var data = {};

(function() {

data.parties = [
  {name: "democrat", speeches: [
    "THE DEMOCRAT: Урок Test test TEST test, test American dream American dream",
    "THE DEMOCRAT: Test test TEST test, test American dream Arithmetic Arithmetic Arithmetic"
  ]},
  {name: "republican", speeches: [
    "REPUB: Урок Урок Test TEST test test TEST American dream American dream American dream American dream American dream American dreamAmerican dream American dream Arithmetic Arithmetic Arithmetic Arithmetic Arithmetic Arithmetic"
  ]}
].map(party);

data.speakers = {
  "THE DEMOCRAT": {name: "The Democrat", title: "U.S. representative, Texas"},
  "REPUB": {name: "Repub", title: "U.S. representative, Texas Arithmetic Arithmetic Arithmetic "}
};

data.topics = [
  {name: "Test", re: /\b(Test)\b/gi, x: 234, y: 432},
  {name: "Образование", re: /\b(Образование)\b/gi, x: 100, y: 100},
  {name: "Урок", re: /\b(Урок)\b/gi, x: 107, y: 106},
  {name: "American dream", re: /\b(American dream)\b/gi, x: 558, y: 181},
  {name: "Arithmetic", re: /\b(Arithmetic)\b/gi, x: 43, y: 203}
].map(topic);

data.topic = function(name) {
  var t = topic({name: name, re: new RegExp("\\b(" + d3.requote(name) + ")\\b", "gi")}, data.topics.length);
  data.topics.push(t);
  return t;
};

function party(party) {
  party.speeches = party.speeches.map(speech);
  party.sections = sections(party.speeches);
  party.wordCount = d3.sum(party.sections, function(d) { return countWords(d.speech.text.substring(d.i, d.j)); });
  return party;
}

function speech(text, i) {
  return {text: text, id: i};
}

function sections(speeches) {
  var speakerRe = /(?:\n|^)([A-Z\.()\- ]+): /g,
      sections = [];

  speeches.forEach(function(speech) {
    var speakerName = "AUDIENCE",
        match,
        i = speakerRe.lastIndex = 0;
    while (match = speakerRe.exec(speech.text)) {
      if (match.index > i) sections.push({speaker: speakerName, speech: speech, i: i, j: match.index});
      speakerName = match[1];
      i = speakerRe.lastIndex;
    }
    sections.push({speaker: speakerName, speech: speech, i: i, j: speech.text.length});
  });

  return sections.filter(function(d) { return !/^AUDIENCE\b/.test(d.speaker); });
}

function topic(topic, i) {
  topic.id = i;
  topic.count = 0;
  topic.cx = topic.x;
  topic.cy = topic.y;

  topic.parties = data.parties.map(function(party) {
    var count = 0,
        mentions = [];

    party.sections.forEach(function(section) {
      var text = section.speech.text.substring(section.i, section.j), match;
      topic.re.lastIndex = 0;
      while (match = topic.re.exec(text)) {
        ++count;
        mentions.push({
          topic: topic,
          section: section,
          i: section.i + match.index,
          j: section.i + topic.re.lastIndex
        });
      }
    });

    topic.count += count = count / party.wordCount * 2000;
    return {count: count, mentions: mentions};
  });

  return topic;
}


// total number of all words in the text
function countWords(text) {
  return text.split(/\s+/g)
      .filter(function(d) { return d !== "—"; })
      .length;
}

})();

(function() {

var width = 970,
    height = 540;

var collisionPadding = 4,
    clipPadding = 4,
    minRadius = 16, // minimum collision radius
    maxRadius = 65, // also determines collision search radius
    activeTopic; // currently-displayed topic

var formatShortCount = d3.format(",.0f"),
    formatLongCount = d3.format(".1f"),
    formatCount = function(d) { return (d < 10 ? formatLongCount : formatShortCount)(d); };

var r = d3.scale.sqrt()
    .domain([0, d3.max(data.topics, function(d) { return d.count; })])
    .range([0, maxRadius]);

var force = d3.layout.force()
    .charge(0)
    .size([width, height - 80])
    .on("tick", tick);

var node = d3.select(".g-nodes").selectAll(".g-node"),
    label = d3.select(".g-labels").selectAll(".g-label"),
    arrow = d3.select(".g-nodes").selectAll(".g-note-arrow");

d3.select(".g-nodes").append("rect")
    .attr("class", "g-overlay")
    .attr("width", width)
    .attr("height", height);

updateTopics(data.topics);

// Update the known topics.
function updateTopics(topics) {
  topics.forEach(function(d) {
    d.r = r(d.count);
    d.cr = Math.max(minRadius, d.r);
    d.k = fraction(d.parties[0].count, d.parties[1].count);
    if (isNaN(d.k)) d.k = .5;
    if (isNaN(d.x)) d.x = (1 - d.k) * width + Math.random();
    d.bias = .5 - Math.max(.1, Math.min(.9, d.k));
  });
  data.topics = topics;
  force.nodes(data.topics).start();
  updateNodes();
  updateLabels();
  updateArrows();
  tick({alpha: 0}); // synchronous update
}

// Update the displayed nodes.
function updateNodes() {
  node = node.data(data.topics, function(d) { return d.name; });

  node.exit().remove();

  var nodeEnter = node.enter().append("a")
      .attr("class", "g-node")
      .attr("xlink:href", function(d) { return "#" + encodeURIComponent(d.name); })
      .call(force.drag)
      .call(linkTopic);

  var democratEnter = nodeEnter.append("g")
      .attr("class", "g-democrat");

  democratEnter.append("clipPath")
      .attr("id", function(d) { return "g-clip-democrat-" + d.id; })
    .append("rect");

  democratEnter.append("circle");

  var republicanEnter = nodeEnter.append("g")
      .attr("class", "g-republican");

  republicanEnter.append("clipPath")
      .attr("id", function(d) { return "g-clip-republican-" + d.id; })
    .append("rect");

  republicanEnter.append("circle");

  nodeEnter.append("line")
      .attr("class", "g-split");

  node.selectAll("rect")
      .attr("y", function(d) { return -d.r - clipPadding; })
      .attr("height", function(d) { return 2 * d.r + 2 * clipPadding; });

  node.select(".g-democrat rect")
      .style("display", function(d) { return d.k > 0 ? null : "none" })
      .attr("x", function(d) { return -d.r - clipPadding; })
      .attr("width", function(d) { return 2 * d.r * d.k + clipPadding; });

  node.select(".g-republican rect")
      .style("display", function(d) { return d.k < 1 ? null : "none" })
      .attr("x", function(d) { return -d.r + 2 * d.r * d.k; })
      .attr("width", function(d) { return 2 * d.r; });

  node.select(".g-democrat circle")
      .attr("clip-path", function(d) { return d.k < 1 ? "url(#g-clip-democrat-" + d.id + ")" : null; });

  node.select(".g-republican circle")
      .attr("clip-path", function(d) { return d.k > 0 ? "url(#g-clip-republican-" + d.id + ")" : null; });

  node.select(".g-split")
      .attr("x1", function(d) { return -d.r + 2 * d.r * d.k; })
      .attr("y1", function(d) { return -Math.sqrt(d.r * d.r - Math.pow(-d.r + 2 * d.r * d.k, 2)); })
      .attr("x2", function(d) { return -d.r + 2 * d.r * d.k; })
      .attr("y2", function(d) { return Math.sqrt(d.r * d.r - Math.pow(-d.r + 2 * d.r * d.k, 2)); });

  node.selectAll("circle")
      .attr("r", function(d) { return r(d.count); });
}

// Update the displayed node labels.
function updateLabels() {
  label = label.data(data.topics, function(d) { return d.name; });

  label.exit().remove();

  var labelEnter = label.enter().append("a")
      .attr("class", "g-label")
      .attr("href", function(d) { return "#" + encodeURIComponent(d.name); })
      .call(force.drag)
      .call(linkTopic);

  labelEnter.append("div")
      .attr("class", "g-name")
      .text(function(d) { return d.name; });

  labelEnter.append("div")
      .attr("class", "g-value");

  label
      .style("font-size", function(d) { return Math.max(8, d.r / 2) + "px"; })
      .style("width", function(d) { return d.r * 2.5 + "px"; });

  // Create a temporary span to compute the true text width.
  label.append("span")
      .text(function(d) { return d.name; })
      .each(function(d) { d.dx = Math.max(d.r * 2.5, this.getBoundingClientRect().width); })
      .remove();

  label
      .style("width", function(d) { return d.dx + "px"; })
    .select(".g-value")
      .text(function(d) { return formatShortCount(d.parties[0].count) + " - " + formatShortCount(d.parties[1].count); });

  // Compute the height of labels when wrapped.
  label.each(function(d) { d.dy = this.getBoundingClientRect().height; });
}


// Bind the arrow path elements with their associated topic.
function updateArrows() {
  arrow = arrow.data(
      data.topics.filter(function(d) { return d.arrow; }),
      function(d) { return this.id ? this.id.substring(8) : d.arrow; });
}


// Assign event handlers to topic links.
function linkTopic(a) {
  a   .on("click", click)
      .on("mouseover", mouseover)
      .on("mouseout", mouseout);
}

// Returns the topic matching the specified name, approximately.
// If no matching topic is found, returns undefined.
function findTopic(name) {
  for (var i = 0, n = data.topics.length, t; i < n; ++i) {
    if ((t = data.topics[i]).name === name || new RegExp("^" + (t = data.topics[i]).re.source + "$", "i").test(name)) {
      return t;
    }
  }
}


// Simulate forces and update node and label positions on tick.
function tick(e) {
  node
      .each(bias(e.alpha * 105))
      .each(collide(.5))
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  label
      .style("left", function(d) { return (d.x - d.dx / 2) + "px"; })
      .style("top", function(d) { return (d.y - d.dy / 2) + "px"; });

  arrow.style("stroke-opacity", function(d) {
    var dx = d.x - d.cx, dy = d.y - d.cy;
    return dx * dx + dy * dy < d.r * d.r ? 1: 0;
  });
}

// A left-right bias causing topics to orient by party preference.
function bias(alpha) {
  return function(d) {
    d.x += d.bias * alpha;
  };
}

// Resolve collisions between nodes.
function collide(alpha) {
  var q = d3.geom.quadtree(data.topics);
  return function(d) {
    var r = d.cr + maxRadius + collisionPadding,
        nx1 = d.x - r,
        nx2 = d.x + r,
        ny1 = d.y - r,
        ny2 = d.y + r;
    q.visit(function(quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== d) && d.other !== quad.point && d !== quad.point.other) {
        var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = d.cr + quad.point.r + collisionPadding;
        if (l < r) {
          l = (l - r) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          quad.point.x += x;
          quad.point.y += y;
        }
      }
      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    });
  };
}

// Fisher–Yates shuffle.
function shuffle(array) {
  var m = array.length, t, i;
  while (m) {
    i = Math.floor(Math.random() * m--);
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }
  return array;
}

// Given two quantities a and b, returns the fraction to split the circle a + b.
function fraction(a, b) {
  var k = a / (a + b);
  if (k > 0 && k < 1) {
    var t0, t1 = Math.pow(12 * k * Math.PI, 1 / 3);
    for (var i = 0; i < 10; ++i) { // Solve for theta numerically.
      t0 = t1;
      t1 = (Math.sin(t0) - t0 * Math.cos(t0) + 2 * k * Math.PI) / (1 - Math.cos(t0));
    }
    k = (1 - Math.cos(t1 / 2)) / 2;
  }
  return k;
}


// Rather than flood the browser history, use location.replace.
function click(d) {
  location.replace("#" + encodeURIComponent(d === activeTopic ? "!" : d.name));
  d3.event.preventDefault();
}

// When hovering the label, highlight the associated node and vice versa.
// When no topic is active, also cross-highlight with any mentions in excerpts.
function mouseover(d) {
  node.classed("g-hover", function(p) { return p === d; });
  if (!activeTopic) d3.selectAll(".g-mention p").classed("g-hover", function(p) { return p.topic === d; });
}

// When hovering the label, highlight the associated node and vice versa.
// When no topic is active, also cross-highlight with any mentions in excerpts.
function mouseout(d) {
  node.classed("g-hover", false);
  if (!activeTopic) d3.selectAll(".g-mention p").classed("g-hover", false);
}

})();
