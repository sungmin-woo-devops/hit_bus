import * as d3 from 'd3';

function createKoreaMap() {
    chart = {
        width:975,
        height:620,
        zoom:d3.zoom().scaleExtent([1, 8]).on("zoom", zoomed),
        svg:null,
        path:null,
        projection:null,
        g:null,
        stopsGroup:null,
        routesGroup:null,
    }
}