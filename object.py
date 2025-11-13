import pygame

#체력 부 얼굴 3개

#책: 학점 0.10 증가
#에너지드링크: 체력 0.5개 증가
#보너스 아이템: b, o, o 획득 시 보너스 상태 진입 가능

#은행, 커피컵: 체력 0.5개 감소
#소주: 학점 -0.05 감소
#계단: 점프

#보너스스테이지: 책 점수 0.5 증가 (2~)
class Item:
    def item(self):
        return 0
    
    def obstacle(self):
        return 0
    
    def book(self):
        return 0
    
    def trash(self):
        return 0