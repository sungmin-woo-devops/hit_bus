/**
 * D3.js 한국 지도 시각화
 * 버스 정류장 및 노선 정보 표시
 */

class D3Map {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = d3.select(`#${containerId}`);
        this.options = {
            width: 800,
            height: 600,
            center: [127.5, 36.5], // 한국 중심 좌표
            scale: 4000,
            ...options
        };
        
        this.projection = null;
        this.path = null;
        this.svg = null;
        this.tooltip = null;
        this.legend = null;
        
        this.init();
    }
    
    init() {
        this.createSVG();
        this.createProjection();
        this.createTooltip();
        this.createLegend();
    }
    
    createSVG() {
        // 기존 SVG 제거
        this.container.selectAll("svg").remove();
        
        // 새 SVG 생성
        this.svg = this.container
            .append("svg")
            .attr("width", this.options.width)
            .attr("height", this.options.height)
            .style("background-color", "#f8f9fa");
    }
    
    createProjection() {
        this.projection = d3.geoMercator()
            .center(this.options.center)
            .scale(this.options.scale)
            .translate([this.options.width / 2, this.options.height / 2]);
            
        this.path = d3.geoPath().projection(this.projection);
    }
    
    createTooltip() {
        this.tooltip = d3.select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);
    }
    
    createLegend() {
        this.legend = this.svg
            .append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${this.options.width - 120}, 20)`);
            
        const legendData = [
            { color: "#dc3545", label: "버스정류장" },
            { color: "#28a745", label: "버스노선" },
            { color: "#007bff", label: "선택된 지역" }
        ];
        
        this.legend.selectAll(".legend-item")
            .data(legendData)
            .enter()
            .append("g")
            .attr("class", "legend-item")
            .attr("transform", (d, i) => `translate(0, ${i * 25})`)
            .each(function(d) {
                d3.select(this)
                    .append("rect")
                    .attr("class", "legend-color")
                    .attr("width", 16)
                    .attr("height", 16)
                    .style("fill", d.color);
                    
                d3.select(this)
                    .append("text")
                    .attr("x", 24)
                    .attr("y", 12)
                    .style("font-size", "12px")
                    .text(d.label);
            });
    }
    
    // 한국 지도 데이터 로드 및 표시
    async loadKoreaMap() {
        try {
            // 한국 지도 데이터 (TopoJSON 형식)
            const koreaData = await d3.json("https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-municipalities-2018-geo.json");
            
            const features = topojson.feature(koreaData, koreaData.objects.skorea_municipalities_2018_geo);
            
            this.svg.selectAll(".country")
                .data(features.features)
                .enter()
                .append("path")
                .attr("class", "country")
                .attr("d", this.path)
                .attr("data-name", d => d.properties.CTP_KOR_NM)
                .on("mouseover", (event, d) => {
                    d3.select(event.target).style("fill", "#6c757d");
                    this.tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    this.tooltip.html(d.properties.CTP_KOR_NM)
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", (event, d) => {
                    d3.select(event.target).style("fill", "#e9ecef");
                    this.tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                })
                .on("click", (event, d) => {
                    this.selectRegion(d);
                });
                
        } catch (error) {
            console.error("지도 데이터 로드 실패:", error);
            this.showErrorMessage("지도 데이터를 불러올 수 없습니다.");
        }
    }
    
    // 지역 선택
    selectRegion(region) {
        // 기존 선택 해제
        this.svg.selectAll(".country.selected").classed("selected", false);
        
        // 새 지역 선택
        this.svg.selectAll(".country")
            .filter(d => d === region)
            .classed("selected", true);
            
        // 이벤트 발생
        this.container.dispatch("regionSelected", { detail: region });
    }
    
    // 버스 정류장 추가
    addBusStops(stops) {
        const stopsGroup = this.svg.append("g").attr("class", "bus-stops");
        
        stopsGroup.selectAll(".bus-stop")
            .data(stops)
            .enter()
            .append("circle")
            .attr("class", "bus-stop")
            .attr("cx", d => this.projection([d.lng, d.lat])[0])
            .attr("cy", d => this.projection([d.lng, d.lat])[1])
            .attr("r", 4)
            .on("mouseover", (event, d) => {
                d3.select(event.target).attr("r", 6);
                this.tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                this.tooltip.html(`${d.name}<br/>${d.routes}개 노선`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", (event, d) => {
                d3.select(event.target).attr("r", 4);
                this.tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            })
            .on("click", (event, d) => {
                this.selectBusStop(d);
            });
    }
    
    // 버스 노선 추가
    addBusRoutes(routes) {
        const routesGroup = this.svg.append("g").attr("class", "bus-routes");
        
        routesGroup.selectAll(".bus-route")
            .data(routes)
            .enter()
            .append("path")
            .attr("class", "bus-route")
            .attr("d", d => this.path({
                type: "LineString",
                coordinates: d.coordinates
            }))
            .on("mouseover", (event, d) => {
                d3.select(event.target).style("opacity", 1);
                this.tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                this.tooltip.html(`${d.name}<br/>${d.stops}개 정류장`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", (event, d) => {
                d3.select(event.target).style("opacity", 0.7);
                this.tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
    }
    
    // 버스 정류장 선택
    selectBusStop(stop) {
        this.container.dispatch("busStopSelected", { detail: stop });
    }
    
    // 줌 기능
    enableZoom() {
        const zoom = d3.zoom()
            .scaleExtent([1, 8])
            .on("zoom", (event) => {
                this.svg.selectAll("path, circle")
                    .attr("transform", event.transform);
            });
            
        this.svg.call(zoom);
    }
    
    // 지도 리셋
    reset() {
        this.svg.selectAll("*").remove();
        this.createProjection();
        this.createLegend();
    }
    
    // 에러 메시지 표시
    showErrorMessage(message) {
        this.svg.append("text")
            .attr("x", this.options.width / 2)
            .attr("y", this.options.height / 2)
            .attr("text-anchor", "middle")
            .style("font-size", "16px")
            .style("fill", "#dc3545")
            .text(message);
    }
    
    // 지도 크기 조정
    resize(width, height) {
        this.options.width = width;
        this.options.height = height;
        
        this.svg
            .attr("width", width)
            .attr("height", height);
            
        this.projection
            .translate([width / 2, height / 2]);
            
        this.createLegend();
    }
}

// 전역 함수로 노출
window.D3Map = D3Map; 