import os
import sys

# tools 폴더에 있는 document_extractor 로드
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from document_extractor import extract_document

# llm_wiki 폴더 기준
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Top 10 + 후보 20개 매핑 리스트 정의 (relative to REPO_ROOT)
MAPPING = {
    "fone-c348c1c5d9": "raw/sources/ASIS분석자료(FONE)/보고자료(회의자료)/FONE시스템분석및문제점공유.pptx",
    "20260318-3e3ced425c": "raw/sources/ASIS분석자료(FONE)/보고자료(회의자료)/(20260318)차세대 패션관리시스템 개선 제안.pptx",
    "fa-one-73077b7a31": "raw/sources/ASIS분석자료(FONE)/진행중/참고자료/신성통상 FA-ONE 시스템 분석 및 개선.docx",
    "fa-one-5bc95be344": "raw/sources/ASIS분석자료(FONE)/FA-ONE_프로세스_이슈맵.pdf",
    "20260327-process-86845c5311": "raw/sources/ASIS분석자료(FONE)/산출물/(20260327)패션관리시스템_process구성도.pdf",
    "resource-2537e80af1": "raw/sources/ASIS분석자료(FONE)/진행중/현업인터뷰/영업관리팀/차세대 영업관리시스템 요청사항.xlsx",
    "as-is-to-be-761c70f811": "raw/sources/ASIS분석자료(FONE)/분석참고자료/온라인정산AS-IS_TO_BE 비교.pptx",
    "wms-faone-wms-3326b626da": "raw/sources/ASIS분석자료(FONE)/분석참고자료/WMS_교육자료(FAONE,WMS).pptx",
    "plm-83dc3fd156": "raw/sources/ASIS분석자료(FONE)/진행중/참고자료/PLM연동관련.txt",
    "1-faone-ver1-7-40d88e9b38": "raw/sources/FONE분석자료(장재혁차장님)/1. (전체) 기준정보_FAONE_Ver1.7_최종.xlsx",
    "fa-one-innovation-blueprint-2-e1ec660197": "raw/sources/ASIS분석자료(FONE)/진행중/패션관리시스템_주요이슈/FA-ONE_Innovation_Blueprint_(2).pptx",
    "process-4203c55383": "raw/sources/ASIS분석자료(FONE)/산출물/패션관리시스템_process구성도(물류출고까지).pptx",
    "resource-5cc9c9f664": "raw/sources/ASIS분석자료(FONE)/진행중/패션관리시스템_주요이슈/패션관리시스템_주요이슈_개선안.pptx",
    "fa-one-40b4a2bfe5": "raw/sources/ASIS분석자료(FONE)/진행중/차세대_FA-ONE_현업인터뷰_대상_및_세부질문지.txt",
    "rfp-20260424-06e9cd0154": "raw/sources/영업관리_RFP_요구사항_정의서_최종.html",
    "resource-b2218e9191": "raw/sources/ASIS분석자료(FONE)/분석참고자료/온라인정산프로세스_보충반영분완료.pptx",
    "wms-c970d3195f": "raw/sources/ASIS분석자료(FONE)/분석참고자료/WMS센터별패션창고재고관리_팀장검토진행건.pptx",
    "centric-ebd6abd12a": "raw/sources/ASIS분석자료(FONE)/진행중/참고자료/centric/Centric_솔루션_분석.txt",
    "ss10db-tables-c6cb6d8005": "raw/sources/[정보보안팀]DATA인터페이스현황/SS10DB_TABLES.xls",
    "fone-drawio-ff584e7271": "raw/sources/ASIS분석자료(FONE)/산출물/FONE_아키텍처.drawio.pdf"
}

def main():
    print("==========================================")
    print("  원천 기획문서 텍스트/표 마크다운 덤프 스크립트")
    print("==========================================")
    
    # 덤프를 생성하여 저장할 디렉토리 정의
    dump_dir = os.path.join(REPO_ROOT, "raw", "sources", "extracted")
    os.makedirs(dump_dir, exist_ok=True)
    
    success_count = 0
    fail_count = 0
    
    for alias, rel_path in MAPPING.items():
        src_path = os.path.join(REPO_ROOT, rel_path)
        
        # 파일 존재 유무 체크
        if not os.path.exists(src_path):
            print(f"[경고] 파일을 찾을 수 없습니다: {alias} -> {rel_path}")
            fail_count += 1
            continue
            
        print(f"덤프 진행 중: {alias} ({os.path.basename(src_path)})")
        
        # 텍스트 추출
        try:
            content = extract_document(src_path)
            
            # 덤프 파일명 결정
            filename = f"{alias}_extracted.txt"
            dst_path = os.path.join(dump_dir, filename)
            
            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            print(f"   [성공] 추출 완료 -> raw/sources/extracted/{filename}")
            success_count += 1
        except Exception as e:
            print(f"   [실패] 추출 에러: {e}")
            fail_count += 1
            
    print("\n==========================================")
    print(f"  덤프 완료! 성공: {success_count}건, 실패: {fail_count}건")
    print("==========================================")

if __name__ == "__main__":
    main()
