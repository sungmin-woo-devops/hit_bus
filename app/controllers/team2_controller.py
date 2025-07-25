from flask import render_template, request, jsonify
from typing import Dict, Any, List
import json
import pandas as pd
from app.services.data_service import DataService

class Team2Controller:
    """Team2 전용 컨트롤러"""
    
    def __init__(self):
        self.data_service = DataService()
    
    def get_team2_page(self) -> str:
        """Team2 메인 페이지 렌더링"""
        try:
            # 데이터베이스에서 데이터 로드
            df = self.data_service.load_team2_data_from_db()
            
            if df.empty:
                return "데이터베이스에서 데이터를 불러오지 못했습니다."
            
            # 상위 노선 조회
            top_routes = df['노선'].value_counts().head(4).index.tolist()
            selected_route = request.args.get('route') or top_routes[0]
            
            # 선택된 노선 필터링
            filtered_df = df[df['노선'] == selected_route]
            
            # 테이블 HTML 생성
            table_html = filtered_df.head(20).to_html(
                classes='table table-bordered table-sm team2-table', 
                index=False
            )
            
            # 시간대별 평균 이용객수 계산
            grouped = filtered_df.groupby('시작시간')['이용객수'].mean().sort_index()
            
            chart_labels = list(grouped.index)
            chart_values = list(grouped.values)
            
            return render_template(
                'team2_index.html',
                table=table_html,
                routes=top_routes,
                selected_route=selected_route,
                chart_labels=json.dumps(chart_labels),
                chart_values=json.dumps(chart_values)
            )
            
        except Exception as e:
            print(f"Team2 페이지 로드 오류: {e}")
            return "데이터를 불러오는 중 오류가 발생했습니다."
    
    def get_team2_data(self) -> Dict[str, Any]:
        """Team2 데이터 API 엔드포인트"""
        try:
            df = self.data_service.load_team2_data_from_db()
            
            if df.empty:
                return {"error": "데이터를 불러올 수 없습니다."}
            
            # 기본 통계
            stats = {
                "total_records": len(df),
                "total_routes": df['노선'].nunique(),
                "total_passengers": df['이용객수'].sum(),
                "avg_passengers": df['이용객수'].mean(),
                "top_routes": df['노선'].value_counts().head(5).to_dict()
            }
            
            return stats
            
        except Exception as e:
            print(f"Team2 데이터 API 오류: {e}")
            return {"error": str(e)}
    
    def get_route_data(self, route_name: str) -> Dict[str, Any]:
        """특정 노선 데이터 조회"""
        try:
            df = self.data_service.load_team2_data_from_db()
            
            if df.empty:
                return {"error": "데이터를 불러올 수 없습니다."}
            
            # 노선 필터링
            filtered_df = df[df['노선'] == route_name]
            
            if filtered_df.empty:
                return {"error": f"노선 '{route_name}'을 찾을 수 없습니다."}
            
            # 노선별 통계
            stats = {
                "route_name": route_name,
                "total_records": len(filtered_df),
                "total_passengers": filtered_df['이용객수'].sum(),
                "avg_passengers": filtered_df['이용객수'].mean(),
                "hourly_stats": filtered_df.groupby('시작시간')['이용객수'].agg(['mean', 'sum', 'count']).to_dict('index')
            }
            
            return stats
            
        except Exception as e:
            print(f"노선 데이터 조회 오류: {e}")
            return {"error": str(e)}
    
    def get_chart_data(self, route_name: str = None) -> Dict[str, Any]:
        """차트 데이터 조회"""
        try:
            df = self.data_service.load_team2_data_from_db()
            
            if df.empty:
                return {"error": "데이터를 불러올 수 없습니다."}
            
            if route_name:
                df = df[df['노선'] == route_name]
            
            # 시간대별 평균 이용객수
            hourly_stats = df.groupby('시작시간')['이용객수'].mean().sort_index()
            
            chart_data = {
                "labels": list(hourly_stats.index),
                "values": list(hourly_stats.values),
                "route_name": route_name or "전체"
            }
            
            return chart_data
            
        except Exception as e:
            print(f"차트 데이터 조회 오류: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """리소스 정리"""
        self.data_service.close_team2_db() 